import llvmlite.ir as ir
import llvmlite.binding as llvm
from frontend.visitor import Visitor
from frontend.ast import Declaration, FunctionDefinition, FunctionCall, SubscriptAccess, ArrayDeclaration, Identifier, FunctionCallStatement, ImportStatement
from frontend.types import TypeInfo

class LLVMCodeGenerator(Visitor):
    def __init__(self, symbol_table, imported_modules=None, debug=True):
        self.debug = debug
        self.symbol_table = symbol_table
        self.imported_modules = imported_modules or {}
        self.module = ir.Module(name="main_module")
        self._initialize_llvm()
        self.current_function = None
        self.builder = None
        self.llvm_var_table = {}
        self.global_strings = {}
        self.global_vars = {}
        self.global_dynamic_arrays = []  # (name, element_type_str, initializer_nodes, is_dynamic)
        self.deferred_initializers = []  # (var_name, initializer_node) for function call initializers
        self._define_structs()
        self._declare_runtime_functions()
        self._declare_module_functions()  # Declare functions from imported modules

    def _initialize_llvm(self):
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.module.triple = self.target_machine.triple
        self.module.data_layout = self.target_machine.target_data

    def _define_structs(self):
        # These definitions are ported from the old llvmConverter.py
        d_array_int_struct = self.module.context.get_identified_type("DArrayInt")
        d_array_int_struct.set_body(
            ir.IntType(32).as_pointer(), # data
            ir.IntType(64), # size
            ir.IntType(64)  # capacity
        )
        self.d_array_int_type = d_array_int_struct.as_pointer()

        d_array_string_struct = self.module.context.get_identified_type("DArrayString")
        d_array_string_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(), # data
            ir.IntType(64), # size
            ir.IntType(64)  # capacity
        )
        self.d_array_string_type = d_array_string_struct.as_pointer()

        d_array_float_struct = self.module.context.get_identified_type("DArrayFloat")
        d_array_float_struct.set_body(
            ir.DoubleType().as_pointer(), # data
            ir.IntType(64), # size
            ir.IntType(64)  # capacity
        )
        self.d_array_float_type = d_array_float_struct.as_pointer()

        d_array_char_struct = self.module.context.get_identified_type("DArrayChar")
        d_array_char_struct.set_body(
            ir.IntType(8).as_pointer(), # data
            ir.IntType(64), # size
            ir.IntType(64)  # capacity
        )
        self.d_array_char_type = d_array_char_struct.as_pointer()

        dict_value_struct = self.module.context.get_identified_type("DictValue")
        dict_struct = self.module.context.get_identified_type("Dictionary")
        dict_value_struct.set_body(
            ir.IntType(32), # type
            ir.IntType(64)  # union (simplified)
        )
        self.dict_value_type = dict_value_struct.as_pointer()
        dict_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(), # buckets
            ir.IntType(32), # capacity
            ir.IntType(32)  # size
        )
        self.dict_type = dict_struct.as_pointer()

    def get_llvm_type(self, type_str):
        if type_str.startswith('KEYWORD_'):
            type_str = type_str.split('_')[1].lower()

        if type_str == 'int':
            return ir.IntType(32)
        elif type_str == 'float':
            return ir.DoubleType()
        elif type_str == 'char':
            return ir.IntType(8)
        elif type_str == 'string':
            return ir.IntType(8).as_pointer()
        elif type_str == 'ptr':
            return ir.IntType(8).as_pointer()
        elif type_str == 'boolean' or type_str == 'bool':
            return ir.IntType(1)
        elif type_str == 'void':
            return ir.VoidType()
        elif type_str == 'file':
            return ir.IntType(64)
        elif type_str == 'socket':
            return ir.IntType(32)
        elif type_str == 'd_array_int':
            return self.d_array_int_type
        elif type_str == 'd_array_string':
            return self.d_array_string_type
        elif type_str == 'd_array_float':
            return self.d_array_float_type
        elif type_str == 'd_array_char':
            return self.d_array_char_type
        elif type_str == 'dict':
            return self.dict_type
        elif type_str == 'regex':
            return ir.IntType(8).as_pointer()  # RegexPattern* is a pointer
        elif type_str == 'void*':
            return ir.IntType(8).as_pointer()
        else:
            # Fallback for array types from symbol table like 'array_type(int)'
            # This is a simplification; a real compiler might need more robust type handling.
            if type_str.startswith('array_type'):
                # For now, we handle arrays via pointers, so the base type is what matters.
                # The actual array allocation will handle the size.
                element_type_str = type_str.split('(')[1][:-1]
                return self.get_llvm_type(element_type_str).as_pointer()
            raise ValueError(f"Unknown type: {type_str}")

    def _declare_runtime_functions(self):
        # This is a direct port of the declarations from llvmConverter.py
        # System I/O
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('int').as_pointer()]), name="input_int")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('float').as_pointer()]), name="input_float")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('string').as_pointer()]), name="input_string")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('char').as_pointer()]), name="input_char")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('int')]), name="output_int")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('string')]), name="output_string")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('char')]), name="output_char")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('float'), self.get_llvm_type('int')]), name="output_float")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name="pie_exit")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('int')]), name="pie_sleep")

        # Math Library
        double_type = self.get_llvm_type('float')
        int_type = self.get_llvm_type('int')
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sqrt")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type, double_type]), name="pie_pow")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sin")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_cos")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_tan")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_asin")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_acos")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_atan")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_log")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_log10")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_exp")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_floor")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_ceil")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_round")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_abs")
        ir.Function(self.module, ir.FunctionType(int_type, [int_type]), name="pie_abs_int")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type, double_type]), name="pie_min")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type, double_type]), name="pie_max")
        ir.Function(self.module, ir.FunctionType(int_type, [int_type, int_type]), name="pie_min_int")
        ir.Function(self.module, ir.FunctionType(int_type, [int_type, int_type]), name="pie_max_int")
        ir.Function(self.module, ir.FunctionType(int_type, []), name="pie_rand")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [int_type]), name="pie_srand")
        ir.Function(self.module, ir.FunctionType(int_type, [int_type, int_type]), name="pie_rand_range")
        ir.Function(self.module, ir.FunctionType(double_type, []), name="pie_pi")
        ir.Function(self.module, ir.FunctionType(double_type, []), name="pie_e")
        ir.Function(self.module, ir.FunctionType(int_type, []), name="pie_time")

        # Time Library
        int_type = self.get_llvm_type('int')
        string_type = self.get_llvm_type('string')
        ir.Function(self.module, ir.FunctionType(int_type, []), name="pie_time_now")
        ir.Function(self.module, ir.FunctionType(string_type, [int_type]), name="pie_time_to_local")

        # String Library
        string_type = self.get_llvm_type('string')
        int_type = self.get_llvm_type('int')
        float_type = self.get_llvm_type('float')
        char_type = self.get_llvm_type('char')
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="concat_strings")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type]), name="pie_strlen")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="pie_strcmp")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="pie_strcpy")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="pie_strcat")
        
        # Type-to-string conversion functions
        ir.Function(self.module, ir.FunctionType(string_type, [int_type]), name="int_to_string")
        ir.Function(self.module, ir.FunctionType(string_type, [float_type]), name="float_to_string")
        ir.Function(self.module, ir.FunctionType(string_type, [char_type]), name="char_to_string")
        
        # Type conversion functions (from crypto_lib)
        ir.Function(self.module, ir.FunctionType(int_type, [string_type]), name="string_to_int")
        ir.Function(self.module, ir.FunctionType(float_type, [string_type]), name="string_to_float")
        ir.Function(self.module, ir.FunctionType(char_type, [string_type]), name="string_to_char")
        ir.Function(self.module, ir.FunctionType(int_type, [char_type]), name="char_to_int")
        ir.Function(self.module, ir.FunctionType(char_type, [int_type]), name="int_to_char")
        ir.Function(self.module, ir.FunctionType(float_type, [int_type]), name="int_to_float")
        ir.Function(self.module, ir.FunctionType(int_type, [float_type]), name="float_to_int")
        
        # Cryptography and encoding functions
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, int_type]), name="caesar_cipher")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, int_type]), name="caesar_decipher")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="rot13")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, int_type]), name="char_shift")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="reverse_string")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="xor_cipher")
        
        # Advanced string utilities
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="string_to_upper")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="string_to_lower")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="string_trim")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, int_type, int_type]), name="string_substring")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="string_index_of")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, ir.IntType(8), ir.IntType(8)]), name="string_replace_char")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type]), name="string_reverse")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, ir.IntType(8)]), name="string_count_char")
        ir.Function(self.module, ir.FunctionType(char_type, [string_type, int_type]), name="string_char_at")
        ir.Function(self.module, ir.FunctionType(string_type.as_pointer(), [string_type, string_type, int_type.as_pointer()]), name="string_split")
        
        # String split wrapper that returns DArrayString
        d_array_string_type = self.module.context.get_identified_type("DArrayString")
        ir.Function(self.module, ir.FunctionType(d_array_string_type.as_pointer(), [string_type, string_type]), name="string_split_to_array")

        # File I/O Library
        file_type = self.get_llvm_type('file')
        ir.Function(self.module, ir.FunctionType(file_type, [string_type, string_type]), name="file_open")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type]), name="file_close")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type, string_type]), name="file_write")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type]), name="file_flush")
        ir.Function(self.module, ir.FunctionType(string_type, [file_type]), name="file_read_all")
        ir.Function(self.module, ir.FunctionType(string_type, [file_type]), name="file_read_line")

        # Network Library (if needed)
        # ir.Function(self.module, ir.FunctionType(...), name="...")

        # Dictionary, etc. would be declared here too...
        # (Keeping it concise for this example)
        
        # Dictionary functions
        dict_type = self.dict_type
        dict_value_type = self.dict_value_type
        ir.Function(self.module, ir.FunctionType(dict_type, []), name="dict_create")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [dict_type, string_type, dict_value_type]), name="dict_set")
        ir.Function(self.module, ir.FunctionType(dict_value_type, [dict_type, string_type]), name="dict_get")
        ir.Function(self.module, ir.FunctionType(int_type, [dict_type, string_type]), name="dict_get_int")
        ir.Function(self.module, ir.FunctionType(double_type, [dict_type, string_type]), name="dict_get_float")
        ir.Function(self.module, ir.FunctionType(string_type, [dict_type, string_type]), name="dict_get_string")
        ir.Function(self.module, ir.FunctionType(int_type, [dict_type, string_type]), name="dict_has_key")  # Check if key exists
        ir.Function(self.module, ir.FunctionType(int_type, [dict_type, string_type]), name="dict_key_exists")  # PIE wrapper for key existence
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [dict_type, string_type]), name="dict_delete")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [dict_type]), name="dict_free")
        
        # Dictionary value helper functions
        ir.Function(self.module, ir.FunctionType(dict_value_type, [int_type]), name="dict_value_create_int")
        ir.Function(self.module, ir.FunctionType(dict_value_type, [double_type]), name="dict_value_create_float")
        ir.Function(self.module, ir.FunctionType(dict_value_type, [string_type]), name="dict_value_create_string")
        ir.Function(self.module, ir.FunctionType(dict_value_type, []), name="dict_value_create_null")
        
        # Helper functions for PIE language (matching documentation)
        ir.Function(self.module, ir.FunctionType(dict_value_type, [int_type]), name="new_int")
        ir.Function(self.module, ir.FunctionType(dict_value_type, [double_type]), name="new_float")
        ir.Function(self.module, ir.FunctionType(dict_value_type, [string_type]), name="new_string")

        # Regex functions
        regex_type = ir.IntType(8).as_pointer()  # RegexPattern*

        ir.Function(self.module, ir.FunctionType(regex_type, [string_type]), name="regex_compile")

        ir.Function(self.module, ir.FunctionType(int_type, [regex_type, string_type]), name="regex_match")

        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [regex_type]), name="regex_free")

        # Variable validation functions
        ir.Function(self.module, ir.FunctionType(int_type, [ir.IntType(8).as_pointer()]), name="is_variable_defined")
        ir.Function(self.module, ir.FunctionType(int_type, [ir.IntType(8).as_pointer()]), name="is_variable_null")

        # Dynamic array functions
        int_array_ptr = self.d_array_int_type
        string_array_ptr = self.d_array_string_type
        float_array_ptr = self.d_array_float_type
        bool_type = self.get_llvm_type('boolean')
        
        # Array creation and management functions
        ir.Function(self.module, ir.FunctionType(int_array_ptr, []), name="d_array_int_create")
        ir.Function(self.module, ir.FunctionType(string_array_ptr, []), name="d_array_string_create")
        ir.Function(self.module, ir.FunctionType(float_array_ptr, []), name="d_array_float_create")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [int_array_ptr, int_type]), name="d_array_int_append")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [string_array_ptr, string_type]), name="d_array_string_append")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [float_array_ptr, float_type]), name="d_array_float_append")
        ir.Function(self.module, ir.FunctionType(float_type, [float_array_ptr, int_type]), name="d_array_float_get")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [float_array_ptr, int_type, float_type]), name="d_array_float_set")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [float_array_ptr]), name="d_array_float_free")

        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [int_array_ptr]), name="print_int_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [string_array_ptr]), name="print_string_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [float_array_ptr]), name="print_float_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.d_array_char_type]), name="print_char_array")

        char_array_ptr = self.d_array_char_type
        char_type = self.get_llvm_type('char')
        ir.Function(self.module, ir.FunctionType(char_array_ptr, []), name="d_array_char_create")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [char_array_ptr, char_type]), name="d_array_char_append")
        ir.Function(self.module, ir.FunctionType(char_type, [char_array_ptr, int_type]), name="d_array_char_get")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [char_array_ptr, int_type, char_type]), name="d_array_char_set")
        ir.Function(self.module, ir.FunctionType(int_type, [char_array_ptr]), name="d_array_char_size")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [char_array_ptr]), name="d_array_char_free")
        ir.Function(self.module, ir.FunctionType(char_type, [char_array_ptr]), name="d_array_char_pop")
        ir.Function(self.module, ir.FunctionType(bool_type, [char_array_ptr, char_type]), name="d_array_char_contains")
        ir.Function(self.module, ir.FunctionType(int_type, [char_array_ptr, char_type]), name="d_array_char_indexof")
        ir.Function(self.module, ir.FunctionType(char_array_ptr, [char_array_ptr, char_array_ptr]), name="d_array_char_concat")
        ir.Function(self.module, ir.FunctionType(char_array_ptr, [char_array_ptr]), name="d_array_char_copy")

        # String utility functions 
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="string_contains")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="string_starts_with")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="string_ends_with")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type]), name="string_is_empty")

        # Integer array functions
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [int_array_ptr, int_type]), name="d_array_int_push")
        ir.Function(self.module, ir.FunctionType(int_type, [int_array_ptr]), name="d_array_int_pop")
        ir.Function(self.module, ir.FunctionType(int_type, [int_array_ptr]), name="d_array_int_size")
        ir.Function(self.module, ir.FunctionType(int_type, [int_array_ptr, int_type]), name="d_array_int_contains")
        ir.Function(self.module, ir.FunctionType(int_type, [int_array_ptr, int_type]), name="d_array_int_indexof")
        ir.Function(self.module, ir.FunctionType(int_array_ptr, [int_array_ptr, int_array_ptr]), name="d_array_int_concat")
        ir.Function(self.module, ir.FunctionType(float_type, [int_array_ptr]), name="d_array_int_avg")
        ir.Function(self.module, ir.FunctionType(int_array_ptr, [int_array_ptr]), name="d_array_int_copy")
        ir.Function(self.module, ir.FunctionType(int_type, [int_array_ptr, int_type]), name="d_array_int_get")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [int_array_ptr, int_type, int_type]), name="d_array_int_set")

        # String array functions
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [string_array_ptr, string_type]), name="d_array_string_push")
        ir.Function(self.module, ir.FunctionType(string_type, [string_array_ptr]), name="d_array_string_pop")
        ir.Function(self.module, ir.FunctionType(int_type, [string_array_ptr]), name="d_array_string_size")
        ir.Function(self.module, ir.FunctionType(int_type, [string_array_ptr, string_type]), name="d_array_string_contains")
        ir.Function(self.module, ir.FunctionType(int_type, [string_array_ptr, string_type]), name="d_array_string_indexof")
        ir.Function(self.module, ir.FunctionType(string_array_ptr, [string_array_ptr, string_array_ptr]), name="d_array_string_concat")
        ir.Function(self.module, ir.FunctionType(string_array_ptr, [string_array_ptr]), name="d_array_string_copy")
        ir.Function(self.module, ir.FunctionType(string_type, [string_array_ptr, int_type]), name="d_array_string_get")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [string_array_ptr, int_type, string_type]), name="d_array_string_set")

        # Float array functions  
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [float_array_ptr, float_type]), name="d_array_float_push")
        ir.Function(self.module, ir.FunctionType(float_type, [float_array_ptr]), name="d_array_float_pop")
        ir.Function(self.module, ir.FunctionType(int_type, [float_array_ptr]), name="d_array_float_size")
        ir.Function(self.module, ir.FunctionType(int_type, [float_array_ptr, float_type]), name="d_array_float_contains")
        ir.Function(self.module, ir.FunctionType(int_type, [float_array_ptr, float_type]), name="d_array_float_indexof")
        ir.Function(self.module, ir.FunctionType(float_type, [float_array_ptr]), name="d_array_float_avg")
        ir.Function(self.module, ir.FunctionType(float_array_ptr, [float_array_ptr]), name="d_array_float_copy")
    
    def _declare_module_functions(self):
        """Declare external functions from imported modules."""
        for namespace, module_info in self.imported_modules.items():
            # Handle user-defined modules differently
            if module_info.is_user_module:
                self._generate_user_module_functions(namespace, module_info)
            else:
                # For stdlib modules, just declare external functions
                for func in module_info.get_functions():
                    full_name = f"{namespace}.{func['name']}"
                    c_name = full_name.replace('.', '_')  # http.get -> http_get
                    
                    # Check if already declared
                    try:
                        self.module.get_global(c_name)
                        continue  # Already declared
                    except KeyError:
                        pass  # Not declared yet
                    
                    # Parse signature and create LLVM function type
                    signature = func['signature']
                    if '(' not in signature:
                        continue  # Skip invalid signatures
                    
                    return_type_str, params_str = signature.split('(', 1)
                    return_type_str = return_type_str.strip()
                    params_str = params_str.rstrip(')')
                    
                    # Convert return type
                    llvm_return_type = self._module_type_to_llvm(return_type_str)
                    
                    # Parse parameters
                    llvm_param_types = []
                    if params_str.strip():
                        param_parts = params_str.split(',')
                        for param in param_parts:
                            param = param.strip()
                            if not param:
                                continue
                            # Expected format: "type name" or just "type"
                            parts = param.split()
                            if parts:
                                param_type = ' '.join(parts[:-1]) if len(parts) > 1 else parts[0]
                                llvm_param_types.append(self._module_type_to_llvm(param_type))
                    
                    # Declare the function
                    func_type = ir.FunctionType(llvm_return_type, llvm_param_types)
                    ir.Function(self.module, func_type, name=c_name)
    
    def _generate_user_module_functions(self, namespace, module_info):
        """Generate LLVM code for user-defined module functions."""
        # We need to generate ALL functions from the module (not just exported ones)
        # because exported functions may call private functions
        
        # First, parse the module to get all function definitions
        from frontend.parser import Parser
        
        with open(module_info.pie_file, 'r') as f:
            source_code = f.read()
        
        parser = Parser()
        try:
            module_ast = parser.parse(source_code)
        except Exception as e:
            return  # Skip if can't parse
        
        if not module_ast or not module_ast.statements:
            return
        
        # IMPORTANT: Process transitive dependencies first
        # If this module imports other user modules, we need to generate their functions first
        for stmt in module_ast.statements:
            if isinstance(stmt, ImportStatement):
                import_name = stmt.module_name
                # Check if this is a user-defined module we've imported
                if import_name in self.imported_modules:
                    imported_module = self.imported_modules[import_name]
                    if imported_module.is_user_module:
                        # Recursively generate this module's functions if not already done
                        try:
                            # Check if any function from this module already exists
                            test_funcs = imported_module.metadata.get('exported_functions', {})
                            if test_funcs:
                                first_func = list(test_funcs.keys())[0]
                                c_name = f"{import_name}_{first_func}"
                                self.module.get_global(c_name)
                                # Already generated, skip
                        except KeyError:
                            # Not generated yet, generate it now
                            self._generate_user_module_functions(import_name, imported_module)
        
        # Collect all function definitions
        all_functions = []
        exported_function_names = set(module_info.metadata.get('exported_functions', {}).keys())
        
        for stmt in module_ast.statements:
            if isinstance(stmt, FunctionDefinition):
                all_functions.append((stmt, stmt.name in exported_function_names))
        
        # Generate code for all functions
        for func_ast_node, is_exported in all_functions:
            func_name = func_ast_node.name
            
            # Determine the final name
            if is_exported:
                full_name = f"{namespace}.{func_name}"
                c_name = full_name.replace('.', '_')
            else:
                # Private functions get a prefixed name to avoid conflicts
                full_name = f"_{namespace}_{func_name}"
                c_name = full_name
            
            # Check if already generated
            try:
                self.module.get_global(c_name)
                continue
            except KeyError:
                pass
            
            # Save current state
            saved_builder = getattr(self, 'builder', None)
            saved_function = getattr(self, 'current_function', None)
            saved_variables = getattr(self, 'llvm_var_table', {}).copy()
            saved_generating_module = getattr(self, '_current_generating_module', None)
            
            # Set the current module context
            self._current_generating_module = namespace
            
            # For exported functions, use the namespaced lookup
            # For private functions, look up with the prefixed name
            if is_exported:
                lookup_name = f"{namespace}.{func_name}"
                self._current_module_function_name = lookup_name
                self._current_function_codegen_name = c_name
            else:
                # Add private function to symbol table temporarily
                # Extract type info from AST
                param_types = []
                params = []
                for param in func_ast_node.params:
                    if hasattr(param.param_type, 'type_name'):
                        type_str = param.param_type.type_name
                        if param.param_type.is_array:
                            type_str += '[]'
                    else:
                        type_str = str(param.param_type)
                    param_types.append(type_str)
                    params.append((type_str, param.name))
                
                if hasattr(func_ast_node.return_type, 'type_name'):
                    return_type = func_ast_node.return_type.type_name
                    if func_ast_node.return_type.is_array:
                        return_type += '[]'
                else:
                    return_type = str(func_ast_node.return_type)
                
                # Temporarily add to symbol table with original name
                self.symbol_table.add_symbol(
                    func_name,
                    'function',
                    return_type=return_type,
                    params=params,
                    param_types=param_types
                )
                self._current_module_function_name = None
                self._current_function_codegen_name = c_name
            
            # Generate the function
            self.visit(func_ast_node)
            
            # Clean up
            self._current_module_function_name = None
            self._current_function_codegen_name = None
            self._current_generating_module = saved_generating_module
            
            # Restore state
            if saved_builder is not None:
                self.builder = saved_builder
            if saved_function is not None:
                self.current_function = saved_function
            self.llvm_var_table = saved_variables
    
    def _module_type_to_llvm(self, type_str):
        """Convert a module type string to LLVM type."""
        type_str = type_str.strip()
        
        # Handle module-specific types
        if type_str.startswith('json.'):
            # json.object and json.array are opaque pointers
            return ir.IntType(8).as_pointer()  # void*
        elif type_str.startswith('http.'):
            # http.request and http.response are opaque pointers
            return ir.IntType(8).as_pointer()  # void*
        
        # Handle basic PIE types
        type_mapping = {
            'void': ir.VoidType(),
            'int': ir.IntType(32),
            'float': ir.DoubleType(),
            'string': ir.IntType(8).as_pointer(),
            'char': ir.IntType(8),
            'bool': ir.IntType(1),
            'file': ir.IntType(64),  # FILE* as i64
            'dict': self.dict_type if hasattr(self, 'dict_type') else ir.IntType(8).as_pointer(),
            'function': ir.IntType(8).as_pointer(),  # Function pointer
        }
        
        return type_mapping.get(type_str, ir.IntType(8).as_pointer())

    def _array_runtime_func(self, base_type, operation):
        """Helper to get array runtime function names"""
        func_name = f"d_array_{base_type}_{operation}"
        return self.module.get_global(func_name)

    def generate(self, ast):
        """Generate LLVM IR from the AST."""
        # First pass: process global declarations (variables, arrays, etc.) only
        for stmt in ast.statements:
            if isinstance(stmt, (Declaration, ArrayDeclaration)):
                # Process global declarations
                self.visit(stmt)
        
        # Second pass: declare function definitions
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDefinition):
                self.visit(stmt)
        
        # Create a main function to wrap global statements if needed
        self._create_main_function_if_needed(ast)
        
        return self.finalize()

    def _create_main_function_if_needed(self, ast):
        """Create a main function wrapper for global statements if no main function exists."""
        # Check if there's already a main function
        main_func = None
        try:
            main_func = self.module.get_global("main")
        except KeyError:
            pass
            
        if main_func is None:
            # Create main function
            main_type = ir.FunctionType(ir.IntType(32), [])
            main_func = ir.Function(self.module, main_type, name="main")
            
            # Create entry block
            entry_block = main_func.append_basic_block(name='entry')
            self.builder = ir.IRBuilder(entry_block)
            self.current_function = main_func
            
            # Initialize global dynamic arrays (create + optional initializer append)
            for array_info in self.global_dynamic_arrays:
                # Handle various formats for backward compatibility
                is_multidim = False
                dimensions = 1
                
                if len(array_info) == 4:
                    name, element_type_str, init_nodes, is_dynamic = array_info
                    expr_initializer = None
                elif len(array_info) == 5:
                    name, element_type_str, init_nodes, is_dynamic, expr_initializer = array_info
                elif len(array_info) >= 6:
                    name, element_type_str, init_nodes, is_dynamic, expr_initializer, is_multidim, dimensions = array_info[:7]
                    
                if self.debug:
                    print(f"DEBUG: Processing global array '{name}' with element_type_str='{element_type_str}', multidim={is_multidim}")
                
                if is_dynamic:
                    if is_multidim:
                        # Multi-dimensional array initialization
                        outer_create_func = self.module.get_global("d_array_int_create")
                        outer_array = self.builder.call(outer_create_func, [])
                        self.builder.store(outer_array, self.global_vars[name])
                        
                        if init_nodes:
                            for row_node in init_nodes:
                                if hasattr(row_node, 'values'):
                                    # Create inner array
                                    inner_create_func = self.module.get_global(f"d_array_{element_type_str}_create")
                                    inner_array = self.builder.call(inner_create_func, [])
                                    
                                    # Append elements to inner array
                                    append_func = self.module.get_global(f"d_array_{element_type_str}_append")
                                    expected_elem_type = append_func.function_type.args[1]
                                    for val_node in row_node.values:
                                        raw_val = self.visit(val_node)
                                        val = self._coerce_char_array_element(expected_elem_type, raw_val)
                                        if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                            val = self.builder.sitofp(val, expected_elem_type)
                                        if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                            val = self.builder.load(val)
                                        self.builder.call(append_func, [inner_array, val])
                                    
                                    # Store inner array pointer as two 32-bit integers in outer array
                                    inner_as_int = self.builder.ptrtoint(inner_array, ir.IntType(64))
                                    low_32 = self.builder.trunc(inner_as_int, ir.IntType(32))
                                    high_32 = self.builder.trunc(self.builder.lshr(inner_as_int, ir.Constant(ir.IntType(64), 32)), ir.IntType(32))
                                    outer_append_func = self.module.get_global("d_array_int_append")
                                    self.builder.call(outer_append_func, [outer_array, low_32])
                                    self.builder.call(outer_append_func, [outer_array, high_32])
                    else:
                        # Single-dimensional array
                        create_func = self.module.get_global(f"d_array_{element_type_str}_create")
                        new_array_ptr = self.builder.call(create_func, [])
                        self.builder.store(new_array_ptr, self.global_vars[name])
                        
                        if init_nodes:
                            append_func = self.module.get_global(f"d_array_{element_type_str}_append")
                            array_struct_ptr = new_array_ptr
                            expected_elem_type = append_func.function_type.args[1]
                            if self.debug:
                                print(f"DEBUG: append_func: {append_func.name}, expected_elem_type: {expected_elem_type}")
                            for val_node in init_nodes:
                                raw_val = self.visit(val_node)
                                if self.debug:
                                    print(f"DEBUG: Global dynamic array init - raw_val: {raw_val}, type: {raw_val.type}")
                                val = self._coerce_char_array_element(expected_elem_type, raw_val)
                                if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                    val = self.builder.sitofp(val, expected_elem_type)
                                # Final safety: if still pointer and expected int8, load
                                if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                    val = self.builder.load(val)
                                if self.debug:
                                    print(f"DEBUG: About to call append with val: {val}, type: {val.type}, expected: {expected_elem_type}")
                                self.builder.call(append_func, [array_struct_ptr, val])
                        elif expr_initializer:
                            # Handle expression initializers (like array concatenation, array copy, or subscript access)
                            # Check if this is an identifier (array copy)
                            if isinstance(expr_initializer, Identifier):
                                # Call the copy function to create a new array
                                copy_func = self.module.get_global(f"d_array_{element_type_str}_copy")
                                source_array_ptr = self.global_vars[expr_initializer.name]
                                source_array = self.builder.load(source_array_ptr)
                                new_array_ptr = self.builder.call(copy_func, [source_array])
                                self.builder.store(new_array_ptr, self.global_vars[name])
                            # Check if this is a subscript access (e.g., nested[0])
                            elif isinstance(expr_initializer, SubscriptAccess):
                                # Visit the subscript access to get the inner array pointer
                                source_array = self.visit(expr_initializer)
                                # Call the copy function to create a new array
                                copy_func = self.module.get_global(f"d_array_{element_type_str}_copy")
                                new_array_ptr = self.builder.call(copy_func, [source_array])
                                self.builder.store(new_array_ptr, self.global_vars[name])
                            else:
                                # Handle other expression initializers (like array concatenation)
                                result_array = self.visit(expr_initializer)
                                if result_array is not None:  # Only store if we have a result
                                    self.builder.store(result_array, self.global_vars[name])
            
            # Process all non-function statements in their original order
            # This ensures that statements execute in the order they were written
            for stmt in ast.statements:
                if not isinstance(stmt, FunctionDefinition):
                    # For declarations with deferred initializers, process them now
                    if isinstance(stmt, Declaration):
                        # Check if this declaration has a deferred initializer
                        deferred = None
                        for i, (var_name, initializer_node) in enumerate(self.deferred_initializers):
                            if var_name == stmt.identifier:
                                deferred = (i, var_name, initializer_node)
                                break
                        
                        if deferred:
                            # Process the deferred initializer now
                            i, var_name, initializer_node = deferred
                            init_val = self.visit(initializer_node)
                            # Load the value if it's a pointer to another variable
                            if isinstance(init_val.type, ir.PointerType):
                                global_var_type = self.global_vars[var_name].type.pointee
                                if init_val.type.pointee == global_var_type:
                                    init_val = self.builder.load(init_val)
                            self.builder.store(init_val, self.global_vars[var_name])
                            # Remove from deferred list
                            self.deferred_initializers.pop(i)
                        # Skip other declaration processing since globals were already created
                    elif isinstance(stmt, ArrayDeclaration):
                        # Skip array declarations since they were already processed
                        pass
                    else:
                        # Process other statements (function calls, loops, etc.)
                        self.visit(stmt)
            
            # Return 0 from main
            if not self.builder.block.is_terminated:
                self.builder.ret(ir.Constant(ir.IntType(32), 0))
            
            self.current_function = None
            self.builder = None

    def finalize(self):
        """Finalize the LLVM module and return the parsed module object."""
        llvm_ir = str(self.module)
        if self.debug:
            print("\n--- Generated LLVM IR ---\n")
            print(llvm_ir)

        try:
            llvm_module = llvm.parse_assembly(llvm_ir)
            llvm_module.verify()
            if self.debug:
                print("LLVM Module verification successful!")
            return llvm_module
        except RuntimeError as e:
            print(f"LLVM Module Validation Error: {e}")
            print(f"Failing IR:\n{llvm_ir}")
            raise

    # --- Visitor Methods ---

    def visit_program(self, node):
        # This method is called from the old code path, but we handle program generation differently now
        # Just pass through to avoid issues
        pass
    
    def visit_importstatement(self, node):
        """Import statements are handled during semantic analysis and module declaration."""
        # No code generation needed for imports - functions are already declared
        return None
    
    def visit_exportstatement(self, node):
        """Export statements wrap function/variable definitions."""
        # Just visit the wrapped statement
        return self.visit(node)

    def visit_block(self, node):
        # Each block has its own symbol table scope, managed by the semantic analyzer.
        # Here, we just visit the statements within the block.
        for stmt in node.statements:
            self.visit(stmt)

    def visit_functiondefinition(self, node):
        # 1. Get function type from symbol table (or construct it)
        # Check if this is a user module function being generated
        lookup_name = node.name
        if hasattr(self, '_current_module_function_name') and self._current_module_function_name:
            lookup_name = self._current_module_function_name
        
        func_symbol = self.symbol_table.lookup_function(lookup_name)
        return_type = self.get_llvm_type(func_symbol['return_type'])
        param_types = [self.get_llvm_type(pt) for pt in func_symbol['param_types']]
        func_type = ir.FunctionType(return_type, param_types)

        # 2. Declare the function in the module
        # Use the codegen name if specified (for user module functions)
        func_name = node.name
        if hasattr(self, '_current_function_codegen_name') and self._current_function_codegen_name:
            func_name = self._current_function_codegen_name
        
        self.current_function = ir.Function(self.module, func_type, name=func_name)

        # 3. Create entry block and IR builder
        entry_block = self.current_function.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(entry_block)

        # 4. Allocate space for parameters and store their initial values
        # Save global variables before clearing for new function scope
        saved_globals = {k: v for k, v in self.llvm_var_table.items() if k in self.global_vars}
        self.llvm_var_table.clear()
        # Restore global variables
        self.llvm_var_table.update(saved_globals)
        
        for i, arg in enumerate(self.current_function.args):
            param_name = func_symbol['params'][i][1]
            arg.name = param_name

            # Allocate space for the parameter on the stack
            ptr = self.builder.alloca(param_types[i], name=param_name)
            # Store the argument's value in the allocated space
            self.builder.store(arg, ptr)
            # Add the pointer to our variable table
            self.llvm_var_table[param_name] = ptr

        # 5. Visit the function body
        self.visit(node.body)

        # 6. Add a return statement if one is missing
        if not self.builder.block.is_terminated:
            if return_type == ir.VoidType():
                self.builder.ret_void()
            else:
                # Default return for non-void functions (e.g., return 0 for int main)
                zero = ir.Constant(return_type, 0)
                self.builder.ret(zero)

        # 7. Clean up for the next function
        self.current_function = None
        self.builder = None

    def visit_declaration(self, node):
        var_name = node.identifier
        var_type = self.get_llvm_type(node.var_type.type_name)

        if self.builder is None:
            # Global variable declaration
            if node.initializer and not self._is_function_call_initializer(node.initializer):
                # For global variables with constant initializers, evaluate to get a constant
                init_val = self._evaluate_constant_expression(node.initializer)
                initializer = init_val
            else:
                # Default initialization (used for function call initializers too)
                if isinstance(var_type, ir.IntType):
                    initializer = ir.Constant(var_type, 0)
                elif isinstance(var_type, ir.DoubleType):
                    initializer = ir.Constant(var_type, 0.0)
                elif isinstance(var_type, ir.PointerType):
                    initializer = ir.Constant(var_type, None)
                else:
                    initializer = ir.Constant(var_type, 0)

            # Create global variable
            global_var = ir.GlobalVariable(self.module, var_type, name=var_name)
            global_var.initializer = initializer
            global_var.linkage = 'internal'
            
            # Store reference for later use
            self.global_vars[var_name] = global_var
            self.llvm_var_table[var_name] = global_var
            
            # If this has a function call initializer, defer it for later processing
            if node.initializer and self._is_function_call_initializer(node.initializer):
                self.deferred_initializers.append((node.identifier, node.initializer))
        else:
            # Local variable declaration (inside a function)
            ptr = self.builder.alloca(var_type, name=var_name)
            self.llvm_var_table[var_name] = ptr

            # If there's an initializer, visit it and store its value
            if node.initializer:
                init_val = self.visit(node.initializer)
                
                # Handle variable-to-variable initialization
                # If init_val is a pointer to the same type as var_type, load it to get the value
                if isinstance(init_val.type, ir.PointerType):
                    if init_val.type.pointee == var_type:
                        # init_val is a pointer to a variable of the target type, load it
                        init_val = self.builder.load(init_val)
                
                self.builder.store(init_val, ptr)

    def _evaluate_constant_expression(self, node):
        """Evaluate an expression at compile time to get a constant value."""
        if hasattr(node, 'value'):  # Primary node
            val = node.value
            if isinstance(val, str):
                if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                    return ir.Constant(ir.IntType(32), int(val))
                if val.startswith('"') and val.endswith('"'):
                    # For string literals in global context, create the global string
                    str_val = val[1:-1].replace('\\n', '\n') + '\0'
                    if str_val in self.global_strings:
                        return self.global_strings[str_val]
                    
                    c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                    global_var = ir.GlobalVariable(self.module, c_str.type, name=f".str{len(self.global_strings)}")
                    global_var.initializer = c_str
                    global_var.global_constant = True
                    global_var.linkage = 'internal'
                    # Return the address of the global string
                    ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                    self.global_strings[str_val] = ptr
                    return ptr
                if val == 'true':
                    return ir.Constant(ir.IntType(1), 1)
                if val == 'false':
                    return ir.Constant(ir.IntType(1), 0)
                try:
                    if '.' in val:
                        return ir.Constant(ir.DoubleType(), float(val))
                except ValueError:
                    pass
                # Handle char literals like 'A', 'B', etc.
                if val.startswith("'") and val.endswith("'") and len(val) == 3:
                    ch = val[1]  # Extract the character
                    return ir.Constant(ir.IntType(8), ord(ch))
            elif isinstance(val, (int, float)):
                if isinstance(val, int):
                    return ir.Constant(ir.IntType(32), val)
                else:
                    return ir.Constant(ir.DoubleType(), val)
        
        # Handle binary operations for constant evaluation
        if hasattr(node, 'op') and hasattr(node, 'left') and hasattr(node, 'right'):  # BinaryOp
            left_val = self._evaluate_constant_expression(node.left)
            right_val = self._evaluate_constant_expression(node.right)
            
            # Convert to Python values for computation
            if isinstance(left_val.type, ir.IntType):
                left_py = left_val.constant
            elif isinstance(left_val.type, ir.DoubleType):
                left_py = left_val.constant
            else:
                return ir.Constant(ir.IntType(32), 0)  # Fallback
                
            if isinstance(right_val.type, ir.IntType):
                right_py = right_val.constant
            elif isinstance(right_val.type, ir.DoubleType):
                right_py = right_val.constant
            else:
                return ir.Constant(ir.IntType(32), 0)  # Fallback
            
            # Perform the operation
            if node.op == '+':
                result = left_py + right_py
            elif node.op == '-':
                result = left_py - right_py
            elif node.op == '*':
                result = left_py * right_py
            elif node.op == '/':
                result = left_py / right_py
            elif node.op == '%':
                result = left_py % right_py
            else:
                return ir.Constant(ir.IntType(32), 0)  # Fallback
            
            # Return appropriate type based on operands and result
            if isinstance(result, float) or isinstance(left_py, float) or isinstance(right_py, float):
                return ir.Constant(ir.DoubleType(), float(result))
            else:
                return ir.Constant(ir.IntType(32), int(result))
        
        # For function calls and other expressions, we'll need more sophisticated handling
        # For now, return a default value - use int32 as it's the most common
        return ir.Constant(ir.IntType(32), 0)

    def _is_function_call_initializer(self, node):
        """Check if an initializer node contains a function call or references global variables."""
        # Check if the node's class name indicates it's a function call
        class_name = type(node).__name__
        
        # Check if the node itself is a function call or array subscript access
        if class_name in ['ArrayIndexOf', 'ArrayContains', 'ArrayPush', 'ArrayPop', 'ArraySize', 'ArrayAvg', 'SystemOutput', 'FunctionCall', 'DictionaryLiteral', 'SubscriptAccess']:
            return True
        
        # Check if it's an Identifier referring to another variable (including globals)
        if class_name == 'Identifier':
            return True
        
        # Check if it's a BinaryOp that references global variables
        if class_name == 'BinaryOp':
            return self._contains_global_reference(node)
        
        # For more complex expressions, we might need to check recursively
        # For now, this covers our main use cases
        return False

    def _contains_global_reference(self, node):
        """Check if a node contains references to global variables."""
        class_name = type(node).__name__
        
        if class_name == 'Identifier':
            # Check if this identifier refers to a global variable
            return node.name in self.global_vars
        
        # Recursively check sub-nodes
        if class_name == 'BinaryOp':
            return (self._contains_global_reference(node.left) or 
                    self._contains_global_reference(node.right))
        
        if class_name == 'FunctionCall':
            return True
        
        # For other node types, assume no global reference
        return False

    def visit_arraydeclaration(self, node):
        var_name = node.identifier
        sym = self.symbol_table.lookup_symbol(var_name)
        ti = sym.get('typeinfo') if sym else None
        base = ti.base if ti else node.var_type.type_name.replace('KEYWORD_','').lower()
        is_dyn = ti.is_dynamic if ti else node.is_dynamic
        element_type_ir = self.get_llvm_type(node.var_type.type_name)
        is_global = self.builder is None
        
        # Check if this is a multi-dimensional array
        dimensions = getattr(node, 'dimensions', 1)
        is_multidim = dimensions > 1
        
        if is_dyn:
            # For multi-dimensional arrays, we need arrays of arrays
            if is_multidim:
                # Multi-dimensional dynamic arrays are arrays of DArray pointers
                # For example, int[][] becomes DArrayInt* stored in a DArrayInt
                # But we'll use a pointer-based approach for now
                inner_array_ptr_type = self.get_llvm_type(f'd_array_{base}')
                
                if is_global:
                    # Create a global variable that will hold an array of array pointers
                    outer_array_ptr_type = self.get_llvm_type(f'd_array_int')  # Use int array to store pointers
                    global_var = ir.GlobalVariable(self.module, outer_array_ptr_type, name=var_name)
                    global_var.initializer = ir.Constant(outer_array_ptr_type, None)
                    global_var.linkage = 'internal'
                    self.global_vars[var_name] = global_var
                    self.llvm_var_table[var_name] = global_var
                    
                    # Store info for initialization in main
                    init_nodes = []
                    if node.initializer and hasattr(node.initializer, 'values'):
                        init_nodes = node.initializer.values
                    self.global_dynamic_arrays.append((var_name, base, init_nodes, True, node.initializer, is_multidim, dimensions))
                else:
                    # Allocate a pointer to hold the outer array
                    outer_array_ptr_type = self.get_llvm_type(f'd_array_int')  # Array of pointers
                    ptr = self.builder.alloca(outer_array_ptr_type, name=var_name)
                    self.llvm_var_table[var_name] = ptr
                    
                    if node.initializer and hasattr(node.initializer, 'values'):
                        # Create the outer array
                        outer_create_func = self._array_runtime_func('int', 'create')
                        outer_array = self.builder.call(outer_create_func, [])
                        self.builder.store(outer_array, ptr)
                        
                        # For each row in the initializer
                        for row_node in node.initializer.values:
                            if hasattr(row_node, 'values'):  # Should be an InitializerList
                                # Create inner array for this row
                                inner_create_func = self._array_runtime_func(base, 'create')
                                inner_array = self.builder.call(inner_create_func, [])
                                
                                # Append elements to the inner array
                                append_func = self._array_runtime_func(base, 'append')
                                expected_elem_type = append_func.function_type.args[1]
                                for val_node in row_node.values:
                                    raw_val = self.visit(val_node)
                                    val = self._coerce_char_array_element(expected_elem_type, raw_val)
                                    if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                        val = self.builder.sitofp(val, expected_elem_type)
                                    if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                        val = self.builder.load(val)
                                    self.builder.call(append_func, [inner_array, val])
                                
                                # Store the inner array pointer as an integer in the outer array
                                # Use 64-bit to store pointers on 64-bit systems
                                inner_as_int = self.builder.ptrtoint(inner_array, ir.IntType(64))
                                # Store as 64-bit in an int array (but we'll use a special marker)
                                # Actually, we need to rethink this - we can't store 64-bit values in 32-bit int arrays
                                # Let's split into two 32-bit values
                                low_32 = self.builder.trunc(inner_as_int, ir.IntType(32))
                                high_32 = self.builder.trunc(self.builder.lshr(inner_as_int, ir.Constant(ir.IntType(64), 32)), ir.IntType(32))
                                outer_append_func = self._array_runtime_func('int', 'append')
                                self.builder.call(outer_append_func, [outer_array, low_32])
                                self.builder.call(outer_append_func, [outer_array, high_32])
                    else:
                        # Empty multi-dimensional array
                        outer_create_func = self._array_runtime_func('int', 'create')
                        outer_array = self.builder.call(outer_create_func, [])
                        self.builder.store(outer_array, ptr)
            else:
                # Single-dimensional dynamic array (existing code)
                array_ptr_type = self.get_llvm_type(f'd_array_{base}')
                if is_global:
                    global_var = ir.GlobalVariable(self.module, array_ptr_type, name=var_name)
                    global_var.initializer = ir.Constant(array_ptr_type, None)
                    global_var.linkage = 'internal'
                    self.global_vars[var_name] = global_var
                    self.llvm_var_table[var_name] = global_var
                    
                    # Handle different types of initializers
                    init_nodes = []
                    if node.initializer:
                        if hasattr(node.initializer, 'values'):  # InitializerList
                            init_nodes = node.initializer.values
                        else:  # Expression (like BinaryOp for concatenation)
                            # For global arrays with expression initializers, we'll handle it in main
                            init_nodes = []
                    self.global_dynamic_arrays.append((var_name, base, init_nodes, True, node.initializer, False, 1))
                else:
                    ptr = self.builder.alloca(array_ptr_type, name=var_name)
                    self.llvm_var_table[var_name] = ptr
                    
                    if node.initializer:
                        if hasattr(node.initializer, 'values'):  # InitializerList
                            create_func = self._array_runtime_func(base, 'create')
                            new_array_ptr = self.builder.call(create_func, [])
                            self.builder.store(new_array_ptr, ptr)
                            
                            append_func = self._array_runtime_func(base, 'append')
                            array_struct_ptr = new_array_ptr
                            expected_elem_type = append_func.function_type.args[1]
                            for val_node in node.initializer.values:
                                raw_val = self.visit(val_node)
                                val = self._coerce_char_array_element(expected_elem_type, raw_val)
                                if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                    val = self.builder.sitofp(val, expected_elem_type)
                                if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                    val = self.builder.load(val)
                                self.builder.call(append_func, [array_struct_ptr, val])
                        else:  # Expression (like BinaryOp for concatenation, Identifier for array copy, or SubscriptAccess)
                            # Check if this is an identifier (array copy)
                            if isinstance(node.initializer, Identifier):
                                # Call the copy function to create a new array
                                copy_func = self._array_runtime_func(base, 'copy')
                                source_array_ptr = self.llvm_var_table[node.initializer.name]
                                source_array = self.builder.load(source_array_ptr)
                                new_array_ptr = self.builder.call(copy_func, [source_array])
                                self.builder.store(new_array_ptr, ptr)
                            # Check if this is a subscript access (e.g., nested[0])
                            elif isinstance(node.initializer, SubscriptAccess):
                                # Visit the subscript access to get the inner array pointer
                                source_array = self.visit(node.initializer)
                                # Call the copy function to create a new array
                                copy_func = self._array_runtime_func(base, 'copy')
                                new_array_ptr = self.builder.call(copy_func, [source_array])
                                self.builder.store(new_array_ptr, ptr)
                            else:
                                # Visit the expression and store the result (e.g., array concatenation)
                                result_array = self.visit(node.initializer)
                                self.builder.store(result_array, ptr)
                    else:
                        # Empty array
                        create_func = self._array_runtime_func(base, 'create')
                        new_array_ptr = self.builder.call(create_func, [])
                        self.builder.store(new_array_ptr, ptr)
        else:
            size = int(node.size.value) if node.size else (len(node.initializer.values) if node.initializer else 0)
            array_type = ir.ArrayType(element_type_ir, size)
            if is_global:
                zero_list = []
                if node.initializer:
                    init_vals = []
                    for v in node.initializer.values:
                        init_vals.append(self.visit(v))
                    # Only support ints/floats/chars simple constants here
                    while len(init_vals) < size:
                        if isinstance(element_type_ir, ir.IntType):
                            init_vals.append(ir.Constant(element_type_ir, 0))
                        elif isinstance(element_type_ir, ir.DoubleType):
                            init_vals.append(ir.Constant(element_type_ir, 0.0))
                    initializer = ir.Constant(array_type, init_vals)
                else:
                    if isinstance(element_type_ir, ir.IntType):
                        zero_list = [ir.Constant(element_type_ir, 0) for _ in range(size)]
                    elif isinstance(element_type_ir, ir.DoubleType):
                        zero_list = [ir.Constant(element_type_ir, 0.0) for _ in range(size)]
                    initializer = ir.Constant(array_type, zero_list)
                global_var = ir.GlobalVariable(self.module, array_type, name=var_name)
                global_var.initializer = initializer
                global_var.linkage = 'internal'
                self.global_vars[var_name] = global_var
                self.llvm_var_table[var_name] = global_var
            else:
                ptr = self.builder.alloca(array_type, name=var_name)
                self.llvm_var_table[var_name] = ptr
                if node.initializer:
                    for i, v in enumerate(node.initializer.values):
                        val = self.visit(v)
                        index_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32),0), ir.Constant(ir.IntType(32), i)])
                        self.builder.store(val, index_ptr)

    def visit_assignment(self, node):
        if isinstance(node.lhs, SubscriptAccess):
            sym = self.symbol_table.lookup_symbol(node.lhs.name)
            ti = sym.get('typeinfo') if sym else None
            if ti and ti.is_dynamic:
                base = ti.base
                dimensions = getattr(ti, 'dimensions', 1)
                num_indices = len(node.lhs.indices) if hasattr(node.lhs, 'indices') else 1
                
                # Multi-dimensional array assignment
                if dimensions > 1 and num_indices > 1:
                    # Get the outer array - check both local and global var tables
                    if node.lhs.name in self.llvm_var_table:
                        array_var_ptr = self.llvm_var_table[node.lhs.name]
                    elif node.lhs.name in self.global_vars:
                        array_var_ptr = self.global_vars[node.lhs.name]
                    else:
                        raise Exception(f"Unknown variable: {node.lhs.name}")
                    outer_array = self.builder.load(array_var_ptr)
                    
                    # Get first dimension - pointers stored as two consecutive ints
                    first_index = self._load_if_pointer(self.visit(node.lhs.indices[0]))
                    # Calculate actual index (2 ints per pointer)
                    actual_index = self.builder.mul(first_index, ir.Constant(ir.IntType(32), 2))
                    
                    get_func = self._array_runtime_func('int', 'get')
                    low_32 = self.builder.call(get_func, [outer_array, actual_index], 'ptr_low')
                    high_index = self.builder.add(actual_index, ir.Constant(ir.IntType(32), 1))
                    high_32 = self.builder.call(get_func, [outer_array, high_index], 'ptr_high')
                    
                    # Reconstruct 64-bit pointer
                    low_64 = self.builder.zext(low_32, ir.IntType(64))
                    high_64 = self.builder.zext(high_32, ir.IntType(64))
                    high_shifted = self.builder.shl(high_64, ir.Constant(ir.IntType(64), 32))
                    inner_ptr_as_int64 = self.builder.or_(low_64, high_shifted)
                    
                    # Convert int back to pointer
                    inner_array_type = self.get_llvm_type(f'd_array_{base}')
                    inner_array = self.builder.inttoptr(inner_ptr_as_int64, inner_array_type, 'inner_array')
                    
                    # Set in second dimension
                    second_index = self._load_if_pointer(self.visit(node.lhs.indices[1]))
                    value_val = self._load_if_pointer(self.visit(node.rhs))
                    set_func = self._array_runtime_func(base, 'set')
                    self.builder.call(set_func, [inner_array, second_index, value_val])
                    return
                else:
                    # Single-dimensional dynamic array - check both local and global var tables
                    if node.lhs.name in self.llvm_var_table:
                        array_var_ptr = self.llvm_var_table[node.lhs.name]
                    elif node.lhs.name in self.global_vars:
                        array_var_ptr = self.global_vars[node.lhs.name]
                    else:
                        raise Exception(f"Unknown variable: {node.lhs.name}")
                    array_struct_ptr = self.builder.load(array_var_ptr)
                    index_val = self._load_if_pointer(self.visit(node.lhs.key))
                    value_val = self._load_if_pointer(self.visit(node.rhs))
                    set_func = self._array_runtime_func(base, 'set')
                    self.builder.call(set_func, [array_struct_ptr, index_val, value_val])
                    return
        # Fallback
        ptr = self.visit(node.lhs)
        value_to_store = self.visit(node.rhs)
        
        # Get the target type
        target_type = ptr.type.pointee if hasattr(ptr.type,'pointee') else ptr.type.pointed_type
        
        # Handle variable-to-variable assignment
        # If value_to_store is a pointer to the same type as target_type, load it to get the value
        if isinstance(value_to_store.type, ir.PointerType):
            if value_to_store.type.pointee == target_type:
                # value_to_store is a pointer to a variable of the target type, load it
                value_to_store = self.builder.load(value_to_store)
        
        # Handle int to float conversion
        if target_type != value_to_store.type and isinstance(target_type, ir.DoubleType) and isinstance(value_to_store.type, ir.IntType):
            value_to_store = self.builder.sitofp(value_to_store, target_type)
            
        self.builder.store(value_to_store, ptr)

    def visit_returnstatement(self, node):
        if node.value:
            return_val = self.visit(node.value)
            
            # Get the expected return type from the current function
            expected_return_type = self.current_function.ftype.return_type
            
            # If we have a pointer but need a non-pointer (or different pointer depth)
            # we need to load the value
            if isinstance(return_val.type, ir.PointerType):
                # Check if the pointee type matches the expected return type
                if return_val.type.pointee == expected_return_type:
                    # Load the value (e.g., loading i8* from i8**)
                    return_val = self.builder.load(return_val)
                # If return_val.type already matches expected_return_type, use as-is
            
            self.builder.ret(return_val)
        else:
            self.builder.ret_void()

    def _load_if_pointer(self, value):
        """Loads a value if it's a pointer, otherwise returns the value directly."""
        if isinstance(value.type, ir.PointerType):
            # Check if it's a string constant/literal - don't load it
            if (value.type.pointee == ir.IntType(8)):
                # Always keep string pointers as pointers - don't load them
                return value
            # For other pointer types (variables), load the value
            return self.builder.load(value)
        return value

    def visit_binaryop(self, node):
        # Check for null equality operations first
        if node.op in ['==', '!=']:
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            
            # Debug output
            if self.debug:
                print(f"DEBUG: Binary op {node.op}, left type: {left_val.type}, right type: {right_val.type}")
                print(f"DEBUG: Left is null: {self._is_null_value(left_val)}, Right is null: {self._is_null_value(right_val)}")
            
            # Check if this is a null equality comparison
            null_check = self._check_null_equality(left_val, right_val)
            if null_check is not None:
                if self.debug:
                    print(f"DEBUG: Null equality check successful for {node.op}")
                if node.op == '!=':
                    # Invert the result for !=
                    return self.builder.not_(null_check, 'not_null_check')
                return null_check
            elif self.debug:
                print(f"DEBUG: Null equality check returned None")
        
        # Check for string comparison operations
        if node.op in ['==', '!=', '<', '>', '<=', '>=']:
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            
            # Check if both operands are string pointers (i8*) or string variable pointers (i8**)
            left_is_string = False
            right_is_string = False
            
            # Check left operand
            if isinstance(left_val.type, ir.PointerType):
                if left_val.type.pointee == ir.IntType(8):
                    left_is_string = True
                elif (isinstance(left_val.type.pointee, ir.PointerType) and 
                      left_val.type.pointee.pointee == ir.IntType(8)):
                    left_is_string = True
            
            # Check right operand
            if isinstance(right_val.type, ir.PointerType):
                if right_val.type.pointee == ir.IntType(8):
                    right_is_string = True
                elif (isinstance(right_val.type.pointee, ir.PointerType) and 
                      right_val.type.pointee.pointee == ir.IntType(8)):
                    right_is_string = True
            
            if left_is_string and right_is_string:
                # Handle string comparisons using pie_strcmp
                # First, load the actual string values if they're variable pointers
                if isinstance(left_val.type.pointee, ir.PointerType):
                    left_str = self.builder.load(left_val)
                else:
                    left_str = left_val
                
                if isinstance(right_val.type.pointee, ir.PointerType):
                    right_str = self.builder.load(right_val)
                else:
                    right_str = right_val
                
                strcmp_func = self.module.get_global("pie_strcmp")
                cmp_result = self.builder.call(strcmp_func, [left_str, right_str], 'strcmp_result')
                
                # Convert strcmp result (-1, 0, 1) to boolean based on operator
                if node.op == '==':
                    # Equal: strcmp returns 0
                    return self.builder.icmp_signed('==', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_eq')
                elif node.op == '!=':
                    # Not equal: strcmp returns non-zero
                    return self.builder.icmp_signed('!=', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_ne')
                elif node.op == '<':
                    # Less than: strcmp returns negative
                    return self.builder.icmp_signed('<', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_lt')
                elif node.op == '>':
                    # Greater than: strcmp returns positive
                    return self.builder.icmp_signed('>', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_gt')
                elif node.op == '<=':
                    # Less than or equal: strcmp returns non-positive
                    return self.builder.icmp_signed('<=', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_le')
                elif node.op == '>=':
                    # Greater than or equal: strcmp returns non-negative
                    return self.builder.icmp_signed('>=', cmp_result, ir.Constant(ir.IntType(32), 0), 'str_ge')
            
            # Check for string length comparisons and other string operations
            string_op_result = self._handle_string_operations(left_val, right_val, node.op)
            if string_op_result is not None:
                return string_op_result
        
        # Visiting an expression node should yield a value (r-value).
        # If the operand is an identifier or subscript, visiting it will return a
        # pointer (l-value), so we must load it.
        lhs = self._load_if_pointer(self.visit(node.left))
        rhs = self._load_if_pointer(self.visit(node.right))

        # String or Array concatenation check first
        if node.op == '+':
            # Check for string concatenation (including auto type-to-string conversion)
            def is_string_type(val):
                """Check if a value is a string pointer (i8*)"""
                return (isinstance(val.type, ir.PointerType) and 
                       val.type.pointee == ir.IntType(8))
            
            def convert_to_string(val):
                """Convert a non-string value to string"""
                if is_string_type(val):
                    return val
                elif isinstance(val.type, ir.IntType) and val.type.width == 32:
                    # Convert int to string
                    int_to_str_func = self.module.get_global("int_to_string")
                    return self.builder.call(int_to_str_func, [val], 'int_to_str')
                elif isinstance(val.type, ir.DoubleType):
                    # Convert float to string
                    float_to_str_func = self.module.get_global("float_to_string")
                    return self.builder.call(float_to_str_func, [val], 'float_to_str')
                elif isinstance(val.type, ir.IntType) and val.type.width == 8:
                    # Convert char to string
                    char_to_str_func = self.module.get_global("char_to_string")
                    return self.builder.call(char_to_str_func, [val], 'char_to_str')
                else:
                    return None
            
            # Check if either operand is a string
            left_is_string = is_string_type(lhs)
            right_is_string = is_string_type(rhs)
            
            if left_is_string or right_is_string:
                # Convert both operands to strings
                lhs_str = convert_to_string(lhs)
                rhs_str = convert_to_string(rhs)
                
                if lhs_str is not None and rhs_str is not None:
                    concat_func = self.module.get_global("concat_strings")
                    return self.builder.call(concat_func, [lhs_str, rhs_str], 'concat_tmp')

            # Check for array concatenation
            if hasattr(node, 'result_type') and node.result_type == 'array':
                element_type = node.element_type.replace('KEYWORD_', '').lower()
                func_name = f"d_array_{element_type}_concat"
                concat_func = self.module.get_global(func_name)

                # For array concatenation, we need the array struct pointers, not the loaded values
                # Visit the identifiers to get the pointers, then load to get the array structs
                lhs_var_ptr = self.visit(node.left)  # This gives us the variable pointer
                rhs_var_ptr = self.visit(node.right)  # This gives us the variable pointer
                lhs_array_ptr = self.builder.load(lhs_var_ptr)  # Load to get the array struct pointer
                rhs_array_ptr = self.builder.load(rhs_var_ptr)  # Load to get the array struct pointer

                return self.builder.call(concat_func, [lhs_array_ptr, rhs_array_ptr], 'concat_array_tmp')

        # Type promotion for float operations
        if isinstance(lhs.type, ir.DoubleType) or isinstance(rhs.type, ir.DoubleType):
            if isinstance(lhs.type, ir.IntType):
                lhs = self.builder.sitofp(lhs, ir.DoubleType())
            if isinstance(rhs.type, ir.IntType):
                rhs = self.builder.sitofp(rhs, ir.DoubleType())

            op_map = {'+': self.builder.fadd, '-': self.builder.fsub, '*': self.builder.fmul, '/': self.builder.fdiv}
            if node.op in op_map:
                return op_map[node.op](lhs, rhs, 'f_tmp')

            # Relational ops for floats
            op_map_rel = {'<': 'olt', '>': 'ogt', '<=': 'ole', '>=': 'oge', '==': 'oeq', '!=': 'one'}
            if node.op in op_map_rel:
                return self.builder.fcmp_ordered(op_map_rel[node.op], lhs, rhs, 'f_cmp_tmp')

        # Integer operations
        elif isinstance(lhs.type, ir.IntType) and isinstance(rhs.type, ir.IntType):
            op_map = {'+': self.builder.add, '-': self.builder.sub, '*': self.builder.mul, '/': self.builder.sdiv, '%': self.builder.srem}
            if node.op in op_map:
                return op_map[node.op](lhs, rhs, 'i_tmp')

            # Relational ops for integers - use correct LLVM comparison ops
            if node.op == '<':
                return self.builder.icmp_signed('<', lhs, rhs, 'i_cmp_tmp')
            elif node.op == '>':
                return self.builder.icmp_signed('>', lhs, rhs, 'i_cmp_tmp')
            elif node.op == '<=':
                return self.builder.icmp_signed('<=', lhs, rhs, 'i_cmp_tmp')
            elif node.op == '>=':
                return self.builder.icmp_signed('>=', lhs, rhs, 'i_cmp_tmp')
            elif node.op == '==':
                return self.builder.icmp_signed('==', lhs, rhs, 'i_cmp_tmp')
            elif node.op == '!=':
                return self.builder.icmp_signed('!=', lhs, rhs, 'i_cmp_tmp')

            # Logical operators (assuming boolean i1 type from relational ops)
            if node.op == '&&':
                return self.builder.and_(lhs, rhs, 'and_tmp')
            if node.op == '||':
                return self.builder.or_(lhs, rhs, 'or_tmp')

        # Debug output for type mismatch
        lhs_type_info = f"{lhs.type} (pointee: {lhs.type.pointee if isinstance(lhs.type, ir.PointerType) else 'N/A'})"
        rhs_type_info = f"{rhs.type} (pointee: {rhs.type.pointee if isinstance(rhs.type, ir.PointerType) else 'N/A'})"
        raise Exception(f"Unknown or incompatible types for binary operator '{node.op}': {lhs_type_info} and {rhs_type_info}")

    def visit_unaryop(self, node):
        operand_val = self._load_if_pointer(self.visit(node.operand))
        if node.op == '-':
            if isinstance(operand_val.type, ir.DoubleType):
                return self.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), operand_val, 'f_neg_tmp')
            else:
                return self.builder.sub(ir.Constant(operand_val.type, 0), operand_val, 'i_neg_tmp')
        raise Exception(f"Unknown unary operator: {node.op}")

    def _process_escape_sequences(self, s):
        """Process escape sequences in a string literal.
        
        Handles common escape sequences:
        \\n - newline
        \\t - tab
        \\r - carriage return
        \\b - backspace
        \\f - form feed
        \\\\ - backslash
        \\" - double quote
        \\' - single quote
        \\0 - null character
        """
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                next_char = s[i + 1]
                if next_char == 'n':
                    result.append('\n')
                    i += 2
                elif next_char == 't':
                    result.append('\t')
                    i += 2
                elif next_char == 'r':
                    result.append('\r')
                    i += 2
                elif next_char == 'b':
                    result.append('\b')
                    i += 2
                elif next_char == 'f':
                    result.append('\f')
                    i += 2
                elif next_char == '\\':
                    result.append('\\')
                    i += 2
                elif next_char == '"':
                    result.append('"')
                    i += 2
                elif next_char == "'":
                    result.append("'")
                    i += 2
                elif next_char == '0':
                    result.append('\0')
                    i += 2
                else:
                    # Unknown escape sequence, keep the backslash
                    result.append(s[i])
                    i += 1
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)

    def visit_primary(self, node):
        val = node.value
        if isinstance(val, str):
            if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                return ir.Constant(ir.IntType(32), int(val))
            try:
                if '.' in val and not val.startswith('"') and not val.startswith("'"):
                    return ir.Constant(ir.DoubleType(), float(val))
            except ValueError:
                pass
            if val == 'true':
                return ir.Constant(ir.IntType(1), 1)
            if val == 'false':
                return ir.Constant(ir.IntType(1), 0)
            if val == 'null':
                # Return a null pointer for null values
                return ir.Constant(ir.IntType(8).as_pointer(), None)
            if val.startswith("'") and val.endswith("'") and len(val) >= 3:
                inner = val[1:-1]
                if inner == '\\n':
                    ch = '\n'
                elif inner == '\\t':
                    ch = '\t'
                else:
                    ch = inner[0]
                return ir.Constant(ir.IntType(8), ord(ch))
            if val.startswith('"') and val.endswith('"'):
                # Process escape sequences in the string
                str_val = self._process_escape_sequences(val[1:-1]) + '\0'
                if str_val in self.global_strings:
                    global_var = self.global_strings[str_val]
                else:
                    c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                    global_var = ir.GlobalVariable(self.module, c_str.type, name=f".str{len(self.global_strings)}")
                    global_var.initializer = c_str
                    global_var.global_constant = True
                    global_var.linkage = 'internal'
                    self.global_strings[str_val] = global_var
                
                # Create a fresh bitcast/GEP for each use to avoid domination issues
                if self.builder:
                    ptr = self.builder.bitcast(global_var, ir.IntType(8).as_pointer())
                else:
                    ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                return ptr
        raise Exception(f"Unsupported primary literal: {val}")

    def _coerce_char_array_element(self, expected_elem_type, raw_val):
        """Fix array element coercion to handle all array types properly"""
        # For char arrays: expecting i8, handle char literals and string pointers
        if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8:
            # If we have an i8 constant (char literal), return it directly
            if isinstance(raw_val.type, ir.IntType) and raw_val.type.width == 8:
                return raw_val
            # If we have a string pointer, load the first character
            elif raw_val.type == ir.IntType(8).as_pointer():
                return self.builder.load(raw_val)
        
        # For string arrays: expecting i8*, return string pointers as-is
        elif expected_elem_type == ir.IntType(8).as_pointer():
            # If we have a string pointer, return it directly
            if raw_val.type == ir.IntType(8).as_pointer():
                return raw_val
        
        # Otherwise normal pointer load semantics
        return self._load_if_pointer(raw_val)

    def _is_null_value(self, value):
        """Check if a value represents null"""
        if isinstance(value, ir.Constant):
            if value.type == ir.IntType(8).as_pointer():
                return value.constant is None
            # Also check for null pointer constants
            if hasattr(value, 'constant') and value.constant is None:
                return True
        return False

    def _check_null_equality(self, left, right):
        """Generate code to check if a value equals null"""
        # Handle null == null case
        if self._is_null_value(left) and self._is_null_value(right):
            return ir.Constant(ir.IntType(1), 1)
        
        # Handle value == null case
        if self._is_null_value(right):
            # Check if left is a pointer type (can be null)
            if isinstance(left.type, ir.PointerType):
                if left.type.pointee == ir.IntType(8):  # i8*
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.builder.icmp_unsigned('==', left, null_ptr, 'null_check')
                elif left.type.pointee == ir.IntType(8).as_pointer():  # i8**
                    # This is a variable pointer, we need to load it first
                    loaded_left = self.builder.load(left)
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.builder.icmp_unsigned('==', loaded_left, null_ptr, 'null_check')
                elif left.type.pointee == ir.IntType(32):  # i32*
                    # This is an int variable pointer, we need to load it first
                    loaded_left = self.builder.load(left)
                    # For int variables, we can't compare with null - they're always defined
                    # Return false (not null) for int variables
                    return ir.Constant(ir.IntType(1), 0)
                elif left.type.pointee == ir.IntType(64):  # i64* (file handle pointer)
                    loaded_left = self.builder.load(left)
                    null_val = ir.Constant(ir.IntType(64), 0)
                    return self.builder.icmp_unsigned('==', loaded_left, null_val, 'null_check')
            elif isinstance(left.type, ir.IntType) and left.type.width == 64:  # i64 (file handle value)
                null_val = ir.Constant(ir.IntType(64), 0)
                return self.builder.icmp_unsigned('==', left, null_val, 'null_check')
            else:
                # Left is not a pointer type, can't be null
                return ir.Constant(ir.IntType(1), 0)
        
        # Handle null == value case
        if self._is_null_value(left):
            if isinstance(right.type, ir.PointerType):
                if right.type.pointee == ir.IntType(8):  # i8*
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.builder.icmp_unsigned('==', right, null_ptr, 'null_check')
                elif right.type.pointee == ir.IntType(8).as_pointer():  # i8**
                    # This is a variable pointer, we need to load it first
                    loaded_right = self.builder.load(right)
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.builder.icmp_unsigned('==', loaded_right, null_ptr, 'null_check')
                elif right.type.pointee == ir.IntType(32):  # i32*
                    # This is an int variable pointer, we need to load it first
                    loaded_right = self.builder.load(right)
                    # For int variables, we can't compare with null - they're always defined
                    # Return false (not null) for int variables
                    return ir.Constant(ir.IntType(1), 0)
                elif right.type.pointee == ir.IntType(64):  # i64* (file handle pointer)
                    loaded_right = self.builder.load(right)
                    null_val = ir.Constant(ir.IntType(64), 0)
                    return self.builder.icmp_unsigned('==', loaded_right, null_val, 'null_check')
            elif isinstance(right.type, ir.IntType) and right.type.width == 64:  # i64 (file handle value)
                null_val = ir.Constant(ir.IntType(64), 0)
                return self.builder.icmp_unsigned('==', right, null_val, 'null_check')
            else:
                # Right is not a pointer type, can't be null
                return ir.Constant(ir.IntType(1), 0)
        
        # Handle string pointer == null case (both are i8*)
        if (isinstance(left.type, ir.PointerType) and left.type.pointee == ir.IntType(8) and
            isinstance(right.type, ir.PointerType) and right.type.pointee == ir.IntType(8)):
            # Check if one of them is a null constant
            if self._is_null_value(left):
                null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                return self.builder.icmp_unsigned('==', right, null_ptr, 'null_check')
            elif self._is_null_value(right):
                null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                return self.builder.icmp_unsigned('==', left, null_ptr, 'null_check')
        
        return None

    def _handle_string_operations(self, left_val, right_val, op):
        """Handle string-specific operations like length comparison"""
        # Check if we're comparing string lengths
        if op in ['<', '>', '<=', '>=']:
            # Helper function to check if a value is a string (either direct pointer or variable pointer)
            def is_string_value(val):
                if isinstance(val.type, ir.PointerType):
                    if val.type.pointee == ir.IntType(8):  # i8* (direct string pointer)
                        return True
                    elif (isinstance(val.type.pointee, ir.PointerType) and 
                          val.type.pointee.pointee == ir.IntType(8)):  # i8** (string variable pointer)
                        return True
                return False
            
            # Helper function to get string length from a string value
            def get_string_length(val):
                if isinstance(val.type.pointee, ir.PointerType):
                    # This is a string variable pointer (i8**), load it first
                    str_ptr = self.builder.load(val)
                else:
                    # This is a direct string pointer (i8*)
                    str_ptr = val
                
                strlen_func = self.module.get_global("pie_strlen")
                return self.builder.call(strlen_func, [str_ptr], 'strlen_result')
            
            # If one operand is a string and the other is an integer, compare string length
            if is_string_value(left_val) and isinstance(right_val.type, ir.IntType):
                # String length < int
                left_len = get_string_length(left_val)
                return self._compare_values(left_len, right_val, op)
            elif is_string_value(right_val) and isinstance(left_val.type, ir.IntType):
                # int < String length
                right_len = get_string_length(right_val)
                return self._compare_values(left_val, right_len, op)
        
        return None

    def _compare_values(self, left_val, right_val, op):
        """Helper method to compare two values with a given operator"""
        if op == '<':
            return self.builder.icmp_signed('<', left_val, right_val, 'cmp_lt')
        elif op == '>':
            return self.builder.icmp_signed('>', left_val, right_val, 'cmp_gt')
        elif op == '<=':
            return self.builder.icmp_signed('<=', left_val, right_val, 'cmp_le')
        elif op == '>=':
            return self.builder.icmp_signed('>=', left_val, right_val, 'cmp_ge')
        return None

    def visit_identifier(self, node):
        # Return the pointer/value associated with an identifier.
        if node.name in self.llvm_var_table:
            return self.llvm_var_table[node.name]
        # Fallback to global symbol lookup if not in table yet
        try:
            gv = self.module.get_global(node.name)
            return gv
        except KeyError:
            pass
        raise Exception(f"Unknown variable referenced: {node.name}")

    def visit_subscriptaccess(self, node):
        sym = self.symbol_table.lookup_symbol(node.name)
        ti = sym.get('typeinfo') if sym else None
        
        # Handle dictionary access
        if sym and sym.get('type') == 'KEYWORD_DICT':
            # Check both local and global var tables
            if node.name in self.llvm_var_table:
                dict_var_ptr = self.llvm_var_table[node.name]
            elif node.name in self.global_vars:
                dict_var_ptr = self.global_vars[node.name]
            else:
                raise Exception(f"Unknown variable: {node.name}")
            dict_val = self.builder.load(dict_var_ptr)
            key_val = self.visit(node.key)  # Don't load string pointers
            
            # Check if key exists first
            dict_has_key_func = self.module.get_global("dict_has_key")
            key_exists = self.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
            
            # Create a conditional block for safe access
            current_block = self.builder.block
            safe_block = self.current_function.append_basic_block('dict_safe_access')
            error_block = self.current_function.append_basic_block('dict_key_error')
            merge_block = self.current_function.append_basic_block('dict_merge')
            
            # Check if key exists
            self.builder.cbranch(key_exists, safe_block, error_block)
            
            # Safe access block - key exists
            self.builder.position_at_end(safe_block)
            dict_get_func = self.module.get_global("dict_get")
            safe_result = self.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
            self.builder.branch(merge_block)
            
            # Error block - key doesn't exist
            self.builder.position_at_end(error_block)
            # For now, return NULL (could be enhanced with runtime error handling)
            dict_value_create_null_func = self.module.get_global("dict_value_create_null")
            error_result = self.builder.call(dict_value_create_null_func, [], 'null_value')
            self.builder.branch(merge_block)
            
            # Merge block
            self.builder.position_at_end(merge_block)
            phi = self.builder.phi(self.dict_value_type, 'dict_access_result')
            phi.add_incoming(safe_result, safe_block)
            phi.add_incoming(error_result, error_block)
            
            return phi
        
        # Handle dynamic arrays
        if ti and ti.is_dynamic:
            base = ti.base
            dimensions = getattr(ti, 'dimensions', 1)
            num_indices = len(node.indices) if hasattr(node, 'indices') else 1
            
            # Multi-dimensional array access
            if dimensions > 1:
                # Get the outer array (contains pointers to inner arrays split across two ints)
                # Check both local and global var tables
                if node.name in self.llvm_var_table:
                    array_var_ptr = self.llvm_var_table[node.name]
                elif node.name in self.global_vars:
                    array_var_ptr = self.global_vars[node.name]
                else:
                    raise Exception(f"Unknown variable: {node.name}")
                outer_array = self.builder.load(array_var_ptr)
                
                # Access first dimension - pointers are stored as two consecutive ints
                first_index = self._load_if_pointer(self.visit(node.indices[0]))
                # Calculate actual index (2 ints per pointer)
                actual_index = self.builder.mul(first_index, ir.Constant(ir.IntType(32), 2))
                
                get_func = self._array_runtime_func('int', 'get')
                low_32 = self.builder.call(get_func, [outer_array, actual_index], 'ptr_low')
                high_index = self.builder.add(actual_index, ir.Constant(ir.IntType(32), 1))
                high_32 = self.builder.call(get_func, [outer_array, high_index], 'ptr_high')
                
                # Reconstruct 64-bit pointer
                low_64 = self.builder.zext(low_32, ir.IntType(64))
                high_64 = self.builder.zext(high_32, ir.IntType(64))
                high_shifted = self.builder.shl(high_64, ir.Constant(ir.IntType(64), 32))
                inner_ptr_as_int64 = self.builder.or_(low_64, high_shifted)
                
                # Convert int back to pointer
                inner_array_type = self.get_llvm_type(f'd_array_{base}')
                inner_array = self.builder.inttoptr(inner_ptr_as_int64, inner_array_type, 'inner_array')
                
                if num_indices == 1:
                    # Return the inner array pointer directly (for cases like graph[0])
                    return inner_array
                else:
                    # Access second dimension
                    second_index = self._load_if_pointer(self.visit(node.indices[1]))
                    get_inner_func = self._array_runtime_func(base, 'get')
                    return self.builder.call(get_inner_func, [inner_array, second_index], 'elem')
            else:
                # Single-dimensional dynamic array - check both local and global var tables
                if node.name in self.llvm_var_table:
                    array_var_ptr = self.llvm_var_table[node.name]
                elif node.name in self.global_vars:
                    array_var_ptr = self.global_vars[node.name]
                else:
                    raise Exception(f"Unknown variable: {node.name}")
                array_struct_ptr = self.builder.load(array_var_ptr)
                index_val = self._load_if_pointer(self.visit(node.key))
                get_func = self._array_runtime_func(base, 'get')
                return self.builder.call(get_func, [array_struct_ptr, index_val], 'dyn_idx_tmp')
        
        # Handle static arrays - check both local and global var tables
        if node.name in self.llvm_var_table:
            array_ptr = self.llvm_var_table[node.name]
        elif node.name in self.global_vars:
            array_ptr = self.global_vars[node.name]
        else:
            raise Exception(f"Unknown variable: {node.name}")
        key_val = self._load_if_pointer(self.visit(node.key))
        return self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32),0), key_val], inbounds=True)

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)

    def visit_array_function_call(self, node):
        func_name = node.name
        args = node.args
        array_node = args[0]
        
        # Handle arr_size on subscript access (e.g., arr_size(graph[0]))
        if isinstance(array_node, SubscriptAccess):
            # This is accessing a sub-array (like graph[0])
            sub_array_ptr = self.visit(array_node)
            # sub_array_ptr is already the inner array pointer
            sym = self.symbol_table.lookup_symbol(array_node.name)
            ti = sym.get('typeinfo') if sym else None
            base = ti.base if ti else 'int'
            
            op_map = {'arr_push':'append','arr_pop':'pop','arr_size':'size','arr_contains':'contains','arr_indexof':'indexof','arr_avg':'avg'}
            suffix = op_map.get(func_name)
            if not suffix:
                raise Exception(f"Unknown array function: {func_name}")
            c_func = self._array_runtime_func(base, suffix)
            call_args = [sub_array_ptr]
            
            if func_name != 'arr_avg':
                for arg_node in args[1:]:
                    raw_arg_val = self.visit(arg_node)
                    if base == 'char' and func_name in ['arr_contains', 'arr_indexof']:
                        expected_elem_type = c_func.function_type.args[len(call_args)]
                        arg_val = self._coerce_char_array_element(expected_elem_type, raw_arg_val)
                    else:
                        arg_val = self._load_if_pointer(raw_arg_val)
                    call_args.append(arg_val)
            return self.builder.call(c_func, call_args, f'{func_name}_call')
        
        # Normal array function call
        array_var_ptr = self.visit(array_node)
        array_struct_ptr = self.builder.load(array_var_ptr)
        sym = self.symbol_table.lookup_symbol(array_node.name)
        ti = sym.get('typeinfo') if sym else None
        base = ti.base
        op_map = {'arr_push':'append','arr_pop':'pop','arr_size':'size','arr_contains':'contains','arr_indexof':'indexof','arr_avg':'avg'}
        suffix = op_map.get(func_name)
        if not suffix:
            raise Exception(f"Unknown array function: {func_name}")
        c_func = self._array_runtime_func(base, suffix)
        call_args = [array_struct_ptr]
        if func_name != 'arr_avg':
            for arg_node in args[1:]:
                raw_arg_val = self.visit(arg_node)
                # Handle char array coercion for functions that take element values
                if base == 'char' and func_name in ['arr_contains', 'arr_indexof']:
                    expected_elem_type = c_func.function_type.args[len(call_args)]
                    arg_val = self._coerce_char_array_element(expected_elem_type, raw_arg_val)
                else:
                    arg_val = self._load_if_pointer(raw_arg_val)
                call_args.append(arg_val)
        return self.builder.call(c_func, call_args, f'{func_name}_call')
    
    def visit_module_function_call(self, node):
        """Handle calls to module functions like http.get() or json.parse()"""
        # Convert module.function to module_function (C name)
        c_name = node.name.replace('.', '_')
        
        # Get the function from the module
        try:
            func = self.module.get_global(c_name)
        except KeyError:
            raise Exception(f"Module function '{node.name}' not declared. C name: {c_name}")
        
        # Process arguments
        args = []
        for i, arg in enumerate(node.args):
            # Special handling for function identifiers passed as arguments
            if isinstance(arg, Identifier):
                # Check if this argument is a function reference
                try:
                    # Try to get the function from the module
                    func_ref = self.module.get_global(arg.name)
                    if isinstance(func_ref, ir.Function):
                        # This is a function - bitcast it to i8* (generic function pointer)
                        func_ptr = self.builder.bitcast(func_ref, ir.IntType(8).as_pointer())
                        args.append(func_ptr)
                        continue
                except (KeyError, AttributeError):
                    pass
            
            arg_val = self.visit(arg)
            
            # Load from pointer if needed, but be careful with strings and opaque types
            if i < len(func.args):
                expected_type = func.args[i].type
                # If expecting a pointer and we have a pointer, check pointer levels
                if isinstance(arg_val.type, ir.PointerType):
                    if isinstance(expected_type, ir.PointerType):
                        # Both are pointers - but check if we have a double pointer
                        # when we only need a single pointer (common with ptr params)
                        if isinstance(arg_val.type.pointee, ir.PointerType) and not isinstance(expected_type.pointee, ir.PointerType):
                            # We have i8** but need i8* - load once
                            args.append(self.builder.load(arg_val))
                        else:
                            args.append(arg_val)  # Both pointers at same level, keep as is
                    else:
                        args.append(self.builder.load(arg_val))  # Load the value
                else:
                    args.append(arg_val)  # Already a value
            else:
                args.append(self._load_if_pointer(arg_val))
        
        # Call the module function
        result_name = f'{c_name}_result' if not isinstance(func.function_type.return_type, ir.VoidType) else ''
        return self.builder.call(func, args, result_name)

    def visit_functioncall(self, node):
        if node.name.startswith('arr_'):
            return self.visit_array_function_call(node)
        
        # Check if this is a module function call (contains '.')
        if '.' in node.name:
            return self.visit_module_function_call(node)
        
        # Special handling for dict_get with type inference

        if node.name == 'dict_get':

            dict_val = self._load_if_pointer(self.visit(node.args[0]))

            key_val = self._load_if_pointer(self.visit(node.args[1]))

 

            # Get the inferred return type from semantic analysis

            inferred_type = getattr(node, 'inferred_return_type', None)

 

            if inferred_type == 'KEYWORD_INT' or inferred_type == 'int':

                func = self.module.get_global("dict_get_int")

                return self.builder.call(func, [dict_val, key_val], 'dict_get_int_result')

            elif inferred_type == 'KEYWORD_FLOAT' or inferred_type == 'float':

                func = self.module.get_global("dict_get_float")

                return self.builder.call(func, [dict_val, key_val], 'dict_get_float_result')

            elif inferred_type == 'KEYWORD_STRING' or inferred_type == 'string':

                func = self.module.get_global("dict_get_string")

                return self.builder.call(func, [dict_val, key_val], 'dict_get_string_result')

            else:

                # Default to dict_get (returns void*)

                func = self.module.get_global("dict_get")

                return self.builder.call(func, [dict_val, key_val], 'dict_get_result')

 

        # Special handling for dict_set with type inference

        if node.name == 'dict_set':

            dict_val = self._load_if_pointer(self.visit(node.args[0]))

            key_val = self.visit(node.args[1])  # Don't load string pointers

            value_val = self.visit(node.args[2])

 

            # Get the value type from semantic analysis

            value_type = getattr(node, 'value_type', None)

 

            # Create the appropriate DictValue wrapper

            if value_type == 'KEYWORD_INT' or value_type == 'int':

                value_val = self._load_if_pointer(value_val)

                new_int_func = self.module.get_global("new_int")

                dict_value = self.builder.call(new_int_func, [value_val], 'dict_value_int')

            elif value_type == 'KEYWORD_FLOAT' or value_type == 'float':

                value_val = self._load_if_pointer(value_val)

                new_float_func = self.module.get_global("new_float")

                dict_value = self.builder.call(new_float_func, [value_val], 'dict_value_float')

            elif value_type == 'KEYWORD_STRING' or value_type == 'string':

                value_val = self._load_if_pointer(value_val)

                new_string_func = self.module.get_global("new_string")

                dict_value = self.builder.call(new_string_func, [value_val], 'dict_value_string')

            else:

                # Default handling

                value_val = self._load_if_pointer(value_val)

                new_int_func = self.module.get_global("new_int")

                dict_value = self.builder.call(new_int_func, [value_val], 'dict_value_default')

 

            # Call dict_set

            dict_set_func = self.module.get_global("dict_set")

            return self.builder.call(dict_set_func, [dict_val, key_val, dict_value], 'dict_set_result')

       

        # Map PIE function names to their actual LLVM function names
        function_name_map = {
            # Math functions
            'pow': 'pie_pow',
            'sqrt': 'pie_sqrt',
            'sin': 'pie_sin',
            'cos': 'pie_cos',
            'tan': 'pie_tan',
            'asin': 'pie_asin',
            'acos': 'pie_acos',
            'atan': 'pie_atan',
            'log': 'pie_log',
            'log10': 'pie_log10',
            'exp': 'pie_exp',
            'floor': 'pie_floor',
            'ceil': 'pie_ceil',
            'round': 'pie_round',
            'abs': 'pie_abs',
            'abs_int': 'pie_abs_int',
            'min': 'pie_min',
            'max': 'pie_max',
            'min_int': 'pie_min_int',
            'max_int': 'pie_max_int',
            'rand': 'pie_rand',
            'srand': 'pie_srand',
            'rand_range': 'pie_rand_range',
            'pi': 'pie_pi',
            'e': 'pie_e',
            'time': 'pie_time',
            'time_now': 'pie_time_now',
            'time_to_local': 'pie_time_to_local',
            # String functions
            'strlen': 'pie_strlen',
            'strcmp': 'pie_strcmp',
            'strcpy': 'pie_strcpy',
            'strcat': 'pie_strcat'
        }
        
        actual_name = function_name_map.get(node.name, node.name)
        
        # If we're currently generating a user module function and calling another function,
        # check if it's a function from the same module
        if hasattr(self, '_current_generating_module') and self._current_generating_module:
            # Check if it's calling itself (recursion) - use the current function being generated
            if hasattr(self, '_current_function_codegen_name') and self._current_function_codegen_name:
                # Extract the function name from the codegen name
                # e.g., "mathutils_factorial" -> check if node.name == "factorial"
                module_prefix = self._current_generating_module.replace('.', '_') + '_'
                if self._current_function_codegen_name.startswith(module_prefix):
                    func_short_name = self._current_function_codegen_name[len(module_prefix):]
                    if node.name == func_short_name:
                        # Recursive call - use the full codegen name
                        actual_name = self._current_function_codegen_name
                elif self._current_function_codegen_name == f"_{self._current_generating_module}_{node.name}":
                    # Private function calling itself
                    actual_name = self._current_function_codegen_name
            
            # If not a self-call, try to find the function with the module prefix
            if actual_name == function_name_map.get(node.name, node.name):
                prefixed_name = f"_{self._current_generating_module}_{actual_name}"
                try:
                    self.module.get_global(prefixed_name)
                    actual_name = prefixed_name
                except KeyError:
                    # Not a module-local function, try exported function
                    exported_name = f"{self._current_generating_module}_{actual_name}"
                    try:
                        self.module.get_global(exported_name)
                        actual_name = exported_name
                    except KeyError:
                        # Not a module function, use normal name
                        pass
        
        func = self.module.get_global(actual_name)
        if func is None:
            raise Exception(f"Unknown function referenced: {node.name} (mapped to {actual_name})")

        args = []
        for i, arg in enumerate(node.args):
            arg_val = self.visit(arg)
            # Only load from pointer if it's not a return value from functions that should return pointers
            # Functions like new_int, new_float, new_string, dict_create should return pointers
            if isinstance(arg, FunctionCall) and arg.name in ['new_int', 'new_float', 'new_string', 'dict_create', 'dict_get']:
                # These functions return pointers that should not be dereferenced
                args.append(arg_val)
            else:
                # Check if we need to load based on what the function expects
                if i < len(func.args):
                    expected_type = func.args[i].type
                    # If we have i8* but function expects i8, load it (char variable)
                    # If we have i8* and function expects i8*, keep it (string)
                    if isinstance(arg_val.type, ir.PointerType) and arg_val.type.pointee == ir.IntType(8):
                        if expected_type == ir.IntType(8):  # Function wants char by value
                            args.append(self.builder.load(arg_val))
                        else:  # Function wants i8* (string)
                            args.append(arg_val)
                    else:
                        args.append(self._load_if_pointer(arg_val))
                else:
                    args.append(self._load_if_pointer(arg_val))

        new_args = []
        for i, arg in enumerate(args):
            if i < len(func.args) and arg.type != func.args[i].type:
                if isinstance(func.args[i].type, ir.DoubleType) and isinstance(arg.type, ir.IntType):
                    new_args.append(self.builder.sitofp(arg, ir.DoubleType()))
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)

        return self.builder.call(func, new_args, 'call_tmp')

    def visit_ifstatement(self, node):
        cond_val = self._load_if_pointer(self.visit(node.condition))
        
        # Convert integer conditions to boolean (i1) type
        if cond_val.type == ir.IntType(32):  # i32
            zero = ir.Constant(ir.IntType(32), 0)
            cond_val = self.builder.icmp_signed('!=', cond_val, zero, 'bool_cond')

        # Create basic blocks
        then_block = self.current_function.append_basic_block(name='then')

        if node.else_branch:
            else_block = self.current_function.append_basic_block(name='else')
            merge_block = self.current_function.append_basic_block(name='if_cont')
            self.builder.cbranch(cond_val, then_block, else_block)
        else:
            merge_block = self.current_function.append_basic_block(name='if_cont')
            self.builder.cbranch(cond_val, then_block, merge_block)

        # Populate the 'then' block
        self.builder.position_at_end(then_block)
        self.visit(node.then_branch)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # Populate the 'else' block if it exists
        if node.else_branch:
            self.builder.position_at_end(else_block)
            self.visit(node.else_branch)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        # Position builder at the merge block for subsequent instructions
        self.builder.position_at_end(merge_block)

    def visit_whilestatement(self, node):
        loop_header_block = self.current_function.append_basic_block(name='loop_header')
        loop_body_block = self.current_function.append_basic_block(name='loop_body')
        loop_exit_block = self.current_function.append_basic_block(name='loop_exit')

        # Branch to the header to start the loop check
        self.builder.branch(loop_header_block)
        self.builder.position_at_end(loop_header_block)

        # In the header, evaluate the condition
        cond_val = self._load_if_pointer(self.visit(node.condition))
        self.builder.cbranch(cond_val, loop_body_block, loop_exit_block)

        # Populate the loop body
        self.builder.position_at_end(loop_body_block)
        self.visit(node.body)
        # After the body, jump back to the header to re-evaluate
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header_block)

        # Position builder at the exit block
        self.builder.position_at_end(loop_exit_block)

    def visit_forstatement(self, node):
        # Create blocks for the loop structure
        loop_header_block = self.current_function.append_basic_block(name='for_header')
        loop_body_block = self.current_function.append_basic_block(name='for_body')
        loop_update_block = self.current_function.append_basic_block(name='for_update')
        loop_exit_block = self.current_function.append_basic_block(name='for_exit')

        # 1. Initialization
        if node.initializer:
            self.visit(node.initializer)

        # 2. Jump to header for the first condition check
        self.builder.branch(loop_header_block)
        self.builder.position_at_end(loop_header_block)

        # 3. Condition check in the header
        if node.condition:
            cond_val = self._load_if_pointer(self.visit(node.condition))
            self.builder.cbranch(cond_val, loop_body_block, loop_exit_block)
        else: # No condition means an infinite loop
            self.builder.branch(loop_body_block)

        # 4. Populate the loop body
        self.builder.position_at_end(loop_body_block)
        self.visit(node.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_update_block) # Jump to update after body

        # 5. Populate the update block
        self.builder.position_at_end(loop_update_block)
        if node.update:
            self.visit(node.update)
        self.builder.branch(loop_header_block) # Jump back to header

        # 6. Position builder at the exit block
        self.builder.position_at_end(loop_exit_block)

    def visit_switchstatement(self, node):
        # Get the switch expression value - make sure it's loaded if it's a pointer
        switch_val = self._load_if_pointer(self.visit(node.expression))
        
        # Create blocks for each case and default
        case_blocks = []
        default_block = None
        exit_block = self.current_function.append_basic_block("switch_exit")
        
        # Create blocks for each case
        for i, case in enumerate(node.cases):
            if hasattr(case, 'value') and case.value == 'default':
                default_block = self.current_function.append_basic_block("default")
            else:
                case_block = self.current_function.append_basic_block(f"case_{i}")
                case_blocks.append((case, case_block))
        
        # If no default case, create one that jumps to exit
        if default_block is None:
            default_block = exit_block
        
        # Create the switch instruction
        switch_instr = self.builder.switch(switch_val, default_block)
        
        # Add cases to the switch instruction
        for case, case_block in case_blocks:
            case_val = self.visit(case.value)
            switch_instr.add_case(case_val, case_block)
        
        # Generate code for each case
        for case, case_block in case_blocks:
            self.builder.position_at_end(case_block)
            for stmt in case.statements:
                self.visit(stmt)
                # If this is a return statement, don't add a branch
                if stmt.__class__.__name__ == 'ReturnStatement':
                    break
            else:
                # If no return statement, branch to exit
                self.builder.branch(exit_block)
        
        # Generate code for default case if it exists and is not the exit block
        if default_block != exit_block:
            self.builder.position_at_end(default_block)
            # Find the default case
            for case in node.cases:
                if hasattr(case, 'value') and case.value == 'default':
                    for stmt in case.statements:
                        self.visit(stmt)
                        if stmt.__class__.__name__ == 'ReturnStatement':
                            break
                    else:
                        self.builder.branch(exit_block)
                    break
        
        # Position builder at exit block
        self.builder.position_at_end(exit_block)

    # visit_switchstatement and others would follow a similar pattern
    # of creating blocks and using branching instructions.
    def visit_systemoutput(self, node):
        output_type = node.output_type.type_name.replace('KEYWORD_', '').lower()
        is_bool_output = (output_type == 'bool')

        if is_bool_output:
            output_type = 'int'

        if output_type == 'array':
            array_node = node.expression
            array_var_ptr = self.visit(array_node)
            array_struct_ptr = self.builder.load(array_var_ptr)

            array_name = array_node.name
            symbol = self.symbol_table.lookup_symbol(array_name)
            
            # Get element type from symbol table or infer from LLVM type
            if symbol and 'element_type' in symbol:
                element_type = symbol['element_type'].replace('KEYWORD_', '').lower()
            else:
                # Fallback: infer element type from LLVM struct type
                # The array struct ptr type is like %DArrayInt*, %DArrayString*, etc.
                struct_type_name = str(array_struct_ptr.type)
                if 'DArrayInt' in struct_type_name:
                    element_type = 'int'
                elif 'DArrayString' in struct_type_name:
                    element_type = 'string'
                elif 'DArrayFloat' in struct_type_name:
                    element_type = 'float'
                elif 'DArrayChar' in struct_type_name:
                    element_type = 'char'
                else:
                    raise Exception(f"Cannot determine element type for array '{array_name}' with type {struct_type_name}")

            func_name = f"print_{element_type}_array"
            print_func = self.module.get_global(func_name)
            self.builder.call(print_func, [array_struct_ptr])
            return

        # Get the raw value first
        raw_val = self.visit(node.expression)
        
        # For string output, we need to handle loading values for conversion
        if output_type == 'string':
            # If it's a double pointer (string variable), load it to get i8*
            if isinstance(raw_val.type, ir.PointerType) and isinstance(raw_val.type.pointee, ir.PointerType):
                output_val = self.builder.load(raw_val)
            # If it's a pointer to a basic type (i32*, double*, i8* for char)
            elif isinstance(raw_val.type, ir.PointerType):
                # Check what it points to
                if raw_val.type.pointee == ir.IntType(8):
                    # Could be char variable (i8*) or string literal (i8*)
                    # Only load if it's a char variable (check if identifier with char type)
                    if isinstance(node.expression, Identifier):
                        # It's an identifier - check if it's a char variable
                        symbol = self.symbol_table.lookup_symbol(node.expression.name)
                        if symbol and symbol.get('type') == 'KEYWORD_CHAR':
                            # It's a char variable - load it
                            output_val = self.builder.load(raw_val)
                        else:
                            # It's a string variable or other - use as is
                            output_val = raw_val
                    else:
                        # String literal - use as is (already i8*)
                        output_val = raw_val
                elif isinstance(raw_val.type.pointee, (ir.IntType, ir.DoubleType)):
                    # Int or float variable - load the value for conversion
                    output_val = self.builder.load(raw_val)
                else:
                    # Other pointer type - use as is
                    output_val = raw_val
            else:
                # It's already a value
                output_val = raw_val
        elif output_type == 'char':
            # For char, we always need to load the value (i8) from the pointer (i8*)
            if isinstance(raw_val.type, ir.PointerType):
                output_val = self.builder.load(raw_val)
            else:
                output_val = raw_val
        else:
            # For other types, load if it's a pointer
            output_val = self._load_if_pointer(raw_val)

        if is_bool_output:
            if isinstance(output_val.type, ir.IntType) and output_val.type.width == 1:
                output_val = self.builder.zext(output_val, ir.IntType(32))

        # Handle automatic type conversions for string output
        actual_output_type = output_type  # Track what we're actually outputting
        if output_type == 'string':
            # If we have a char (i8) but need string (i8*), convert it
            if isinstance(output_val.type, ir.IntType) and output_val.type.width == 8:
                char_to_str_func = self.module.get_global("char_to_string")
                output_val = self.builder.call(char_to_str_func, [output_val], 'char_to_str')
            # If we have an int (i32) but need string (i8*), convert it
            elif isinstance(output_val.type, ir.IntType) and output_val.type.width == 32:
                int_to_str_func = self.module.get_global("int_to_string")
                output_val = self.builder.call(int_to_str_func, [output_val], 'int_to_str')
            # If we have a float (double) but need string (i8*), convert it
            elif isinstance(output_val.type, ir.DoubleType):
                float_to_str_func = self.module.get_global("float_to_string")
                output_val = self.builder.call(float_to_str_func, [output_val], 'float_to_str')

        func_name = f"output_{actual_output_type}"
        output_func = self.module.get_global(func_name)

        if not output_func:
            raise Exception(f"Runtime function {func_name} not found.")

        args = [output_val]
        # Only add precision if we're actually outputting as float (not converted to string)
        if actual_output_type == 'float' and output_type == 'float':
            precision = self._load_if_pointer(self.visit(node.precision)) if node.precision else ir.Constant(ir.IntType(32), 2)
            args.append(precision)

        self.builder.call(output_func, args)

    def visit_systeminput(self, node):
        var_ptr = self.visit(node.variable) # visit_identifier returns a pointer
        input_type = node.input_type.type_name.replace('KEYWORD_', '').lower()

        func_name = f"input_{input_type}"
        input_func = self.module.get_global(func_name)

        if not input_func:
            raise Exception(f"Runtime function {func_name} not found.")

        if input_type == 'string':
             # For string, the runtime function expects a char* buffer
             self.builder.call(input_func, [var_ptr])
        else:
             # For other types, it expects a pointer to the variable
             self.builder.call(input_func, [var_ptr])

    def visit_systemexit(self, node):
        exit_func = self.module.get_global("pie_exit")
        self.builder.call(exit_func, [])

    def visit_systemsleep(self, node):
        sleep_func = self.module.get_global("pie_sleep")
        # Visit the duration expression and load if it's a pointer
        duration_val = self._load_if_pointer(self.visit(node.duration))
        self.builder.call(sleep_func, [duration_val])

    def visit_arraypush(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.builder.load(array_ptr)
        raw_value_val = self.visit(node.value)
        array_type = array_val.type
        if array_type == self.d_array_int_type:
            push_func = self.module.get_global("d_array_int_push")
            value_val = self._load_if_pointer(raw_value_val)
        elif array_type == self.d_array_string_type:
            push_func = self.module.get_global("d_array_string_push")
            # For string variables, we need to load the string pointer
            # For string literals, we already have the pointer
            if isinstance(raw_value_val.type, ir.PointerType) and raw_value_val.type.pointee == ir.IntType(8).as_pointer():
                # This is a string variable (i8**), load it to get the string pointer (i8*)
                value_val = self.builder.load(raw_value_val)
            else:
                # This is already a string pointer (i8*) from a literal
                value_val = raw_value_val
        elif array_type == self.d_array_float_type:
            push_func = self.module.get_global("d_array_float_push")
            value_val = self._load_if_pointer(raw_value_val)
        elif array_type == self.d_array_char_type:
            # use append as push alias for char
            push_func = self.module.get_global("d_array_char_append")
            expected_elem_type = push_func.function_type.args[1]
            value_val = self._coerce_char_array_element(expected_elem_type, raw_value_val)
        else:
            raise Exception(f"Unsupported array type for push: {array_type}")
        self.builder.call(push_func, [array_val, value_val])

    def visit_arraypop(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.builder.load(array_ptr)
        array_type = array_val.type
        if array_type == self.d_array_int_type:
            pop_func = self.module.get_global("d_array_int_pop")
        elif array_type == self.d_array_string_type:
            pop_func = self.module.get_global("d_array_string_pop")
        elif array_type == self.d_array_float_type:
            pop_func = self.module.get_global("d_array_float_pop")
        elif array_type == self.d_array_char_type:
            pop_func = self.module.get_global("d_array_char_pop")
        else:
            raise Exception(f"Unsupported array type for pop: {array_type}")
        return self.builder.call(pop_func, [array_val])

    def visit_arraysize(self, node):
        result = self.visit(node.array)
        
        # Check if this is a multi-dimensional array (not a subscript access)
        is_multidim_outer = False
        if isinstance(node.array, Identifier):
            sym = self.symbol_table.lookup_symbol(node.array.name)
            ti = sym.get('typeinfo') if sym else None
            if ti and getattr(ti, 'dimensions', 1) > 1:
                is_multidim_outer = True
        
        # For multi-dimensional arrays accessed via subscript (e.g., graph[0]),
        # result is already the inner array pointer
        # For simple array variables, result is a pointer to the array pointer
        
        # Check if we need to load or if we already have the array struct pointer
        if isinstance(result.type, ir.PointerType):
            # Check if it points to one of our array types
            pointee = result.type.pointee if hasattr(result.type, 'pointee') else None
            if pointee in [self.d_array_int_type, self.d_array_string_type, 
                          self.d_array_float_type, self.d_array_char_type]:
                # result is a pointer to an array pointer, load it
                array_val = self.builder.load(result)
            elif result.type in [self.d_array_int_type, self.d_array_string_type,
                                self.d_array_float_type, self.d_array_char_type]:
                # result is already the array struct pointer
                array_val = result
            else:
                # Assume it needs loading
                array_val = self.builder.load(result)
        else:
            # Not a pointer at all, use as-is
            array_val = result
            
        array_type = array_val.type
        if array_type == self.d_array_int_type:
            size_func = self.module.get_global("d_array_int_size")
        elif array_type == self.d_array_string_type:
            size_func = self.module.get_global("d_array_string_size")
        elif array_type == self.d_array_float_type:
            size_func = self.module.get_global("d_array_float_size")
        elif array_type == self.d_array_char_type:
            size_func = self.module.get_global("d_array_char_size")
        else:
            raise Exception(f"Unsupported array type for size: {array_type}")
        
        size_result = self.builder.call(size_func, [array_val])
        
        # If this is a multi-dimensional outer array, divide by 2 since we store
        # each pointer as two integers
        if is_multidim_outer:
            size_result = self.builder.sdiv(size_result, ir.Constant(ir.IntType(32), 2))
        
        return size_result

    def visit_arrayavg(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.builder.load(array_ptr)
        array_type = array_val.type
        if array_type == self.d_array_int_type:
            avg_func = self.module.get_global("d_array_int_avg")
        elif array_type == self.d_array_float_type:
            avg_func = self.module.get_global("d_array_float_avg")
        else:
            raise Exception(f"Unsupported array type for avg: {array_type}")
        return self.builder.call(avg_func, [array_val])

    def visit_arrayindexof(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.builder.load(array_ptr)
        array_type = array_val.type
        value_val = self._load_if_pointer(self.visit(node.value))
        
        if array_type == self.d_array_int_type:
            indexof_func = self.module.get_global("d_array_int_indexof")
        elif array_type == self.d_array_string_type:
            indexof_func = self.module.get_global("d_array_string_indexof")
        elif array_type == self.d_array_float_type:
            indexof_func = self.module.get_global("d_array_float_indexof")
        elif array_type == self.d_array_char_type:
            indexof_func = self.module.get_global("d_array_char_indexof")
        else:
            raise Exception(f"Unsupported array type for indexof: {array_type}")
        return self.builder.call(indexof_func, [array_val, value_val])

    def visit_arraycontains(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.builder.load(array_ptr)
        array_type = array_val.type
        value_val = self._load_if_pointer(self.visit(node.value))
        
        if array_type == self.d_array_int_type:
            contains_func = self.module.get_global("d_array_int_contains")
        elif array_type == self.d_array_string_type:
            contains_func = self.module.get_global("d_array_string_contains")
        elif array_type == self.d_array_float_type:
            contains_func = self.module.get_global("d_array_float_contains")
        elif array_type == self.d_array_char_type:
            contains_func = self.module.get_global("d_array_char_contains")
        else:
            raise Exception(f"Unsupported array type for contains: {array_type}")
        return self.builder.call(contains_func, [array_val, value_val])

    def visit_initializerlist(self, node):
        """Handle InitializerList nodes - for empty arrays, just return None"""
        # For empty arrays, we don't need to do anything special
        # The array creation is handled in the array declaration logic
        return None

    def visit_dictionaryliteral(self, node):
        """Handle dictionary literal: {"key1": value1, "key2": value2}"""
        # Create a new dictionary
        dict_create_func = self.module.get_global("dict_create")
        dict_ptr = self.builder.call(dict_create_func, [])
        
        # Add each key-value pair
        dict_set_func = self.module.get_global("dict_set")
        
        for key_expr, value_expr in node.pairs:
            # Evaluate the key (must be a string)
            key_val = self.visit(key_expr)
            # Don't load string pointers - they should remain as pointers
            
            # Evaluate the value
            value_val = self.visit(value_expr)
            
            # Create a DictValue based on the value type
            if value_val.type == ir.IntType(32):
                # Integer value
                new_int_func = self.module.get_global("new_int")
                dict_value = self.builder.call(new_int_func, [value_val])
            elif value_val.type == ir.DoubleType():
                # Float value
                new_float_func = self.module.get_global("new_float") 
                dict_value = self.builder.call(new_float_func, [value_val])
            elif value_val.type == ir.IntType(8).as_pointer():
                # String value
                new_string_func = self.module.get_global("new_string")
                dict_value = self.builder.call(new_string_func, [value_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.IntType) and value_val.type.pointee.width == 32:
                # Integer pointer - load it first
                loaded_val = self.builder.load(value_val)
                new_int_func = self.module.get_global("new_int")
                dict_value = self.builder.call(new_int_func, [loaded_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.DoubleType):
                # Float pointer - load it first
                loaded_val = self.builder.load(value_val)
                new_float_func = self.module.get_global("new_float") 
                dict_value = self.builder.call(new_float_func, [loaded_val])
            else:
                raise Exception(f"Unsupported dictionary value type: {value_val.type}")
            
            # Set the key-value pair in the dictionary
            self.builder.call(dict_set_func, [dict_ptr, key_val, dict_value])
        
        return dict_ptr

    def visit_safedictionaryaccess(self, node):
        """Handle safe dictionary access with validation and optional default value"""
        dict_var_ptr = self.llvm_var_table[node.dict_name]
        dict_val = self.builder.load(dict_var_ptr)
        key_val = self.visit(node.key)  # Don't load string pointers
        
        # Check if key exists first
        dict_has_key_func = self.module.get_global("dict_has_key")
        key_exists = self.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
        
        # Create a conditional block for safe access
        current_block = self.builder.block
        safe_block = self.current_function.append_basic_block('safe_dict_access')
        default_block = self.current_function.append_basic_block('dict_default_value')
        merge_block = self.current_function.append_basic_block('safe_dict_merge')
        
        # Check if key exists
        self.builder.cbranch(key_exists, safe_block, default_block)
        
        # Safe access block - key exists
        self.builder.position_at_end(safe_block)
        dict_get_func = self.module.get_global("dict_get")
        safe_result = self.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
        self.builder.branch(merge_block)
        
        # Default value block - key doesn't exist
        self.builder.position_at_end(default_block)
        if node.default_value:
            # Use provided default value
            default_result = self.visit(node.default_value)
            # Convert to DictValue if needed
            if default_result.type == ir.IntType(32):
                new_int_func = self.module.get_global("new_int")
                default_result = self.builder.call(new_int_func, [default_result])
            elif default_result.type == ir.DoubleType():
                new_float_func = self.module.get_global("new_float")
                default_result = self.builder.call(new_float_func, [default_result])
            elif default_result.type == ir.IntType(8).as_pointer():
                new_string_func = self.module.get_global("new_string")
                default_result = self.builder.call(new_string_func, [default_result])
        else:
            # Use NULL as default
            dict_value_create_null_func = self.module.get_global("dict_value_create_null")
            default_result = self.builder.call(dict_value_create_null_func, [], 'null_value')
        self.builder.branch(merge_block)
        
        # Merge block
        self.builder.position_at_end(merge_block)
        phi = self.builder.phi(self.dict_value_type, 'safe_dict_result')
        phi.add_incoming(safe_result, safe_block)
        phi.add_incoming(default_result, default_block)
        
        return phi
