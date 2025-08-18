"""
Modular LLVM Code Generator for PIE Compiler

This module provides a clean, maintainable architecture for LLVM code generation
by breaking down the monolithic generator into focused, single-responsibility components.
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from frontend.visitor import Visitor
from frontend.ast import Declaration, FunctionDefinition, FunctionCall, SubscriptAccess, ArrayDeclaration
from frontend.types import TypeInfo

# ============================================================================
# Core Infrastructure
# ============================================================================

class LLVMContext:
    """Central context for LLVM generation, shared across all components."""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.module = ir.Module(name="main_module")
        self.target_machine = None
        self.current_function = None
        self.builder = None
        self.llvm_var_table = {}
        self.global_strings = {}
        self.global_vars = {}
        self.global_dynamic_arrays = []
        self.deferred_initializers = []
        self.symbol_table = None
        
        self._initialize_llvm()
    
    def _initialize_llvm(self):
        """Initialize LLVM bindings and target machine."""
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.module.triple = self.target_machine.triple
        self.module.data_layout = self.target_machine.target_data

class CodeGeneratorComponent(ABC):
    """Base class for all code generator components."""
    
    def __init__(self, context: LLVMContext):
        self.context = context
    
    @abstractmethod
    def initialize(self):
        """Initialize the component."""
        pass

# ============================================================================
# Type System Management
# ============================================================================

class TypeManager(CodeGeneratorComponent):
    """Manages LLVM type definitions and type conversions."""
    
    def __init__(self, context: LLVMContext):
        super().__init__(context)
        self.d_array_types = {}
        self.dict_types = {}
    
    def initialize(self):
        """Define all LLVM struct types."""
        self._define_array_structs()
        self._define_dict_structs()
    
    def _define_array_structs(self):
        """Define dynamic array struct types."""
        # Integer array
        d_array_int_struct = self.context.module.context.get_identified_type("DArrayInt")
        d_array_int_struct.set_body(
            ir.IntType(32).as_pointer(),  # data
            ir.IntType(64),               # size
            ir.IntType(64)                # capacity
        )
        self.d_array_types['int'] = d_array_int_struct.as_pointer()
        
        # String array
        d_array_string_struct = self.context.module.context.get_identified_type("DArrayString")
        d_array_string_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(),  # data
            ir.IntType(64),                           # size
            ir.IntType(64)                            # capacity
        )
        self.d_array_types['string'] = d_array_string_struct.as_pointer()
        
        # Float array
        d_array_float_struct = self.context.module.context.get_identified_type("DArrayFloat")
        d_array_float_struct.set_body(
            ir.DoubleType().as_pointer(),  # data
            ir.IntType(64),               # size
            ir.IntType(64)                # capacity
        )
        self.d_array_types['float'] = d_array_float_struct.as_pointer()
        
        # Char array
        d_array_char_struct = self.context.module.context.get_identified_type("DArrayChar")
        d_array_char_struct.set_body(
            ir.IntType(8).as_pointer(),  # data
            ir.IntType(64),              # size
            ir.IntType(64)               # capacity
        )
        self.d_array_types['char'] = d_array_char_struct.as_pointer()
    
    def _define_dict_structs(self):
        """Define dictionary struct types."""
        dict_value_struct = self.context.module.context.get_identified_type("DictValue")
        dict_struct = self.context.module.context.get_identified_type("Dictionary")
        
        dict_value_struct.set_body(
            ir.IntType(32),  # type
            ir.IntType(64)   # union (simplified)
        )
        self.dict_types['value'] = dict_value_struct.as_pointer()
        
        dict_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(),  # buckets
            ir.IntType(32),                           # capacity
            ir.IntType(32)                            # size
        )
        self.dict_types['dict'] = dict_struct.as_pointer()
    
    def get_llvm_type(self, type_str: str) -> ir.Type:
        """Convert PIE type string to LLVM type."""
        if type_str.startswith('KEYWORD_'):
            type_str = type_str.split('_')[1].lower()
        
        type_map = {
            'int': ir.IntType(32),
            'float': ir.DoubleType(),
            'char': ir.IntType(8),
            'string': ir.IntType(8).as_pointer(),
            'boolean': ir.IntType(1),
            'void': ir.VoidType(),
            'file': ir.IntType(64),
            'socket': ir.IntType(32),
            'd_array_int': self.d_array_types['int'],
            'd_array_string': self.d_array_types['string'],
            'd_array_float': self.d_array_types['float'],
            'd_array_char': self.d_array_types['char'],
            'dict': self.dict_types['dict'],
            'void*': ir.IntType(8).as_pointer()
        }
        
        if type_str in type_map:
            return type_map[type_str]
        
        # Handle array types
        if type_str.startswith('array_type'):
            element_type_str = type_str.split('(')[1][:-1]
            return self.get_llvm_type(element_type_str).as_pointer()
        
        raise ValueError(f"Unknown type: {type_str}")

# ============================================================================
# Runtime Function Management
# ============================================================================

class RuntimeFunctionManager(CodeGeneratorComponent):
    """Manages declaration of all runtime functions."""
    
    def __init__(self, context: LLVMContext, type_manager: TypeManager):
        super().__init__(context)
        self.type_manager = type_manager
    
    def initialize(self):
        """Declare all runtime functions."""
        self._declare_system_io_functions()
        self._declare_math_functions()
        self._declare_string_functions()
        self._declare_file_functions()
        self._declare_dict_functions()
        self._declare_array_functions()
        self._declare_utility_functions()
    
    def _declare_system_io_functions(self):
        """Declare system I/O functions."""
        int_ptr = self.type_manager.get_llvm_type('int').as_pointer()
        float_ptr = self.type_manager.get_llvm_type('float').as_pointer()
        string_ptr = self.type_manager.get_llvm_type('string').as_pointer()
        char_ptr = self.type_manager.get_llvm_type('char').as_pointer()
        int_type = self.type_manager.get_llvm_type('int')
        string_type = self.type_manager.get_llvm_type('string')
        char_type = self.type_manager.get_llvm_type('char')
        float_type = self.type_manager.get_llvm_type('float')
        
        # Input functions
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [int_ptr]), name="input_int")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [float_ptr]), name="input_float")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [string_ptr]), name="input_string")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [char_ptr]), name="input_char")
        
        # Output functions
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [int_type]), name="output_int")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [string_type]), name="output_string")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [char_type]), name="output_char")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), [float_type, int_type]), name="output_float")
        ir.Function(self.context.module, ir.FunctionType(ir.VoidType(), []), name="pie_exit")
    
    def _declare_math_functions(self):
        """Declare mathematical functions."""
        double_type = self.type_manager.get_llvm_type('float')
        int_type = self.type_manager.get_llvm_type('int')
        
        math_functions = [
            ('pie_sqrt', [double_type], double_type),
            ('pie_pow', [double_type, double_type], double_type),
            ('pie_sin', [double_type], double_type),
            ('pie_cos', [double_type], double_type),
            ('pie_tan', [double_type], double_type),
            ('pie_asin', [double_type], double_type),
            ('pie_acos', [double_type], double_type),
            ('pie_atan', [double_type], double_type),
            ('pie_log', [double_type], double_type),
            ('pie_log10', [double_type], double_type),
            ('pie_exp', [double_type], double_type),
            ('pie_floor', [double_type], double_type),
            ('pie_ceil', [double_type], double_type),
            ('pie_round', [double_type], double_type),
            ('pie_abs', [double_type], double_type),
            ('pie_abs_int', [int_type], int_type),
            ('pie_min', [double_type, double_type], double_type),
            ('pie_max', [double_type, double_type], double_type),
            ('pie_min_int', [int_type, int_type], int_type),
            ('pie_max_int', [int_type, int_type], int_type),
            ('pie_rand', [], int_type),
            ('pie_srand', [int_type], ir.VoidType()),
            ('pie_rand_range', [int_type, int_type], int_type),
            ('pie_pi', [], double_type),
            ('pie_e', [], double_type),
            ('pie_time', [], int_type)
        ]
        
        for name, arg_types, return_type in math_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_string_functions(self):
        """Declare string manipulation functions."""
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        
        string_functions = [
            ('concat_strings', [string_type, string_type], string_type),
            ('pie_strlen', [string_type], int_type),
            ('pie_strcmp', [string_type, string_type], int_type),
            ('pie_strcpy', [string_type, string_type], string_type),
            ('pie_strcat', [string_type, string_type], string_type),
            ('string_contains', [string_type, string_type], int_type),
            ('string_starts_with', [string_type, string_type], int_type),
            ('string_ends_with', [string_type, string_type], int_type),
            ('string_is_empty', [string_type], int_type)
        ]
        
        for name, arg_types, return_type in string_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_file_functions(self):
        """Declare file I/O functions."""
        file_type = self.type_manager.get_llvm_type('file')
        string_type = self.type_manager.get_llvm_type('string')
        
        file_functions = [
            ('file_open', [string_type, string_type], file_type),
            ('file_close', [file_type], ir.VoidType()),
            ('file_write', [file_type, string_type], ir.VoidType()),
            ('file_read_all', [file_type], string_type),
            ('file_read_line', [file_type], string_type)
        ]
        
        for name, arg_types, return_type in file_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_dict_functions(self):
        """Declare dictionary functions."""
        dict_type = self.type_manager.dict_types['dict']
        dict_value_type = self.type_manager.dict_types['value']
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        float_type = self.type_manager.get_llvm_type('float')
        
        dict_functions = [
            ('dict_create', [], dict_type),
            ('dict_set', [dict_type, string_type, dict_value_type], ir.VoidType()),
            ('dict_get', [dict_type, string_type], dict_value_type),
            ('dict_get_int', [dict_type, string_type], int_type),
            ('dict_get_float', [dict_type, string_type], float_type),
            ('dict_get_string', [dict_type, string_type], string_type),
            ('dict_has_key', [dict_type, string_type], int_type),
            ('dict_key_exists', [dict_type, string_type], int_type),
            ('dict_delete', [dict_type, string_type], ir.VoidType()),
            ('dict_free', [dict_type], ir.VoidType()),
            ('dict_value_create_int', [int_type], dict_value_type),
            ('dict_value_create_float', [float_type], dict_value_type),
            ('dict_value_create_string', [string_type], dict_value_type),
            ('dict_value_create_null', [], dict_value_type),
            ('new_int', [int_type], dict_value_type),
            ('new_float', [float_type], dict_value_type),
            ('new_string', [string_type], dict_value_type)
        ]
        
        for name, arg_types, return_type in dict_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_array_functions(self):
        """Declare dynamic array functions."""
        self._declare_int_array_functions()
        self._declare_string_array_functions()
        self._declare_float_array_functions()
        self._declare_char_array_functions()
        self._declare_array_utility_functions()
    
    def _declare_int_array_functions(self):
        """Declare integer array functions."""
        int_array_ptr = self.type_manager.d_array_types['int']
        int_type = self.type_manager.get_llvm_type('int')
        float_type = self.type_manager.get_llvm_type('float')
        
        int_array_functions = [
            ('d_array_int_push', [int_array_ptr, int_type], ir.VoidType()),
            ('d_array_int_pop', [int_array_ptr], int_type),
            ('d_array_int_size', [int_array_ptr], int_type),
            ('d_array_int_contains', [int_array_ptr, int_type], int_type),
            ('d_array_int_indexof', [int_array_ptr, int_type], int_type),
            ('d_array_int_concat', [int_array_ptr, int_array_ptr], int_array_ptr),
            ('d_array_int_avg', [int_array_ptr], float_type),
            ('d_array_int_get', [int_array_ptr, int_type], int_type),
            ('d_array_int_set', [int_array_ptr, int_type, int_type], ir.VoidType()),
            ('d_array_int_create', [], int_array_ptr),
            ('d_array_int_append', [int_array_ptr, int_type], ir.VoidType()),
            ('print_int_array', [int_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in int_array_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_string_array_functions(self):
        """Declare string array functions."""
        string_array_ptr = self.type_manager.d_array_types['string']
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        
        string_array_functions = [
            ('d_array_string_push', [string_array_ptr, string_type], ir.VoidType()),
            ('d_array_string_pop', [string_array_ptr], string_type),
            ('d_array_string_size', [string_array_ptr], int_type),
            ('d_array_string_contains', [string_array_ptr, string_type], int_type),
            ('d_array_string_indexof', [string_array_ptr, string_type], int_type),
            ('d_array_string_concat', [string_array_ptr, string_array_ptr], string_array_ptr),
            ('d_array_string_get', [string_array_ptr, int_type], string_type),
            ('d_array_string_set', [string_array_ptr, int_type, string_type], ir.VoidType()),
            ('d_array_string_create', [], string_array_ptr),
            ('d_array_string_append', [string_array_ptr, string_type], ir.VoidType()),
            ('print_string_array', [string_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in string_array_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_float_array_functions(self):
        """Declare float array functions."""
        float_array_ptr = self.type_manager.d_array_types['float']
        float_type = self.type_manager.get_llvm_type('float')
        int_type = self.type_manager.get_llvm_type('int')
        
        float_array_functions = [
            ('d_array_float_push', [float_array_ptr, float_type], ir.VoidType()),
            ('d_array_float_pop', [float_array_ptr], float_type),
            ('d_array_float_size', [float_array_ptr], int_type),
            ('d_array_float_contains', [float_array_ptr, float_type], int_type),
            ('d_array_float_indexof', [float_array_ptr, float_type], int_type),
            ('d_array_float_avg', [float_array_ptr], float_type),
            ('d_array_float_get', [float_array_ptr, int_type], float_type),
            ('d_array_float_set', [float_array_ptr, int_type, float_type], ir.VoidType()),
            ('d_array_float_create', [], float_array_ptr),
            ('d_array_float_append', [float_array_ptr, float_type], ir.VoidType()),
            ('d_array_float_free', [float_array_ptr], ir.VoidType()),
            ('print_float_array', [float_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in float_array_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_char_array_functions(self):
        """Declare char array functions."""
        char_array_ptr = self.type_manager.d_array_types['char']
        char_type = self.type_manager.get_llvm_type('char')
        int_type = self.type_manager.get_llvm_type('int')
        bool_type = self.type_manager.get_llvm_type('boolean')
        
        char_array_functions = [
            ('d_array_char_create', [], char_array_ptr),
            ('d_array_char_append', [char_array_ptr, char_type], ir.VoidType()),
            ('d_array_char_get', [char_array_ptr, int_type], char_type),
            ('d_array_char_set', [char_array_ptr, int_type, char_type], ir.VoidType()),
            ('d_array_char_size', [char_array_ptr], int_type),
            ('d_array_char_free', [char_array_ptr], ir.VoidType()),
            ('d_array_char_pop', [char_array_ptr], char_type),
            ('d_array_char_contains', [char_array_ptr, char_type], bool_type),
            ('d_array_char_indexof', [char_array_ptr, char_type], int_type),
            ('d_array_char_concat', [char_array_ptr, char_array_ptr], char_array_ptr),
            ('print_char_array', [char_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in char_array_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def _declare_array_utility_functions(self):
        """Declare array utility functions."""
        int_type = self.type_manager.get_llvm_type('int')
        
        utility_functions = [
            ('is_variable_defined', [ir.IntType(8).as_pointer()], int_type),
            ('is_variable_null', [ir.IntType(8).as_pointer()], int_type)
        ]
        
        for name, arg_types, return_type in utility_functions:
            ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)

# ============================================================================
# Expression Generation
# ============================================================================

class ExpressionGenerator(CodeGeneratorComponent):
    """Handles generation of LLVM IR for expressions."""
    
    def __init__(self, context: LLVMContext, type_manager: TypeManager):
        super().__init__(context)
        self.type_manager = type_manager
    
    def initialize(self):
        """Initialize the expression generator."""
        pass
    
    def generate_binary_operation(self, node, left_val, right_val, op):
        """Generate LLVM IR for binary operations."""
        # Handle string concatenation
        if op == '+' and self._are_both_strings(left_val, right_val):
            concat_func = self.context.module.get_global("concat_strings")
            left_str = self._load_string_value(left_val)
            right_str = self._load_string_value(right_val)
            return self.context.builder.call(concat_func, [left_str, right_str], 'concat_tmp')
        # Handle string operations
        if self._is_string_operation(left_val, right_val, op):
            return self._generate_string_operation(left_val, right_val, op)
        
        # Handle array concatenation
        if op == '+' and self._is_array_concatenation(node):
            return self._generate_array_concatenation(node)
        
        # Handle type promotion for float operations
        if isinstance(left_val.type, ir.DoubleType) or isinstance(right_val.type, ir.DoubleType):
            return self._generate_float_operation(left_val, right_val, op)
        
        # Handle integer operations
        if isinstance(left_val.type, ir.IntType) and isinstance(right_val.type, ir.IntType):
            return self._generate_integer_operation(left_val, right_val, op)
        
        raise Exception(f"Unsupported binary operation: {op} with types {left_val.type} and {right_val.type}")
    
    def _is_string_operation(self, left_val, right_val, op):
        """Check if this is a string operation."""
        return (op in ['==', '!=', '<', '>', '<=', '>='] and 
                self._is_string_value(left_val) and self._is_string_value(right_val))
    
    def _is_string_value(self, val):
        """Check if a value is a string."""
        if isinstance(val.type, ir.PointerType):
            if val.type.pointee == ir.IntType(8):
                return True
            elif (isinstance(val.type.pointee, ir.PointerType) and 
                  val.type.pointee.pointee == ir.IntType(8)):
                return True
        return False
    
    def _are_both_strings(self, left_val, right_val):
        return self._is_string_value(left_val) and self._is_string_value(right_val)
    
    def _generate_string_operation(self, left_val, right_val, op):
        """Generate string comparison operations."""
        # Load string values if they're variable pointers
        left_str = self._load_string_value(left_val)
        right_str = self._load_string_value(right_val)
        
        strcmp_func = self.context.module.get_global("pie_strcmp")
        cmp_result = self.context.builder.call(strcmp_func, [left_str, right_str], 'strcmp_result')
        
        # Convert strcmp result to boolean based on operator
        op_map = {
            '==': ('==', 0),
            '!=': ('!=', 0),
            '<': ('<', 0),
            '>': ('>', 0),
            '<=': ('<=', 0),
            '>=': ('>=', 0)
        }
        
        if op in op_map:
            cmp_op, target = op_map[op]
            return self.context.builder.icmp_signed(cmp_op, cmp_result, 
                                                 ir.Constant(ir.IntType(32), target), f'str_{op}')
        
        return None
    
    def _load_string_value(self, val):
        """Load string value from variable pointer if needed."""
        if isinstance(val.type.pointee, ir.PointerType):
            return self.context.builder.load(val)
        return val
    
    def _is_array_concatenation(self, node):
        """Check if this is an array concatenation operation."""
        return hasattr(node, 'result_type') and node.result_type == 'array'
    
    def _generate_array_concatenation(self, node):
        """Generate array concatenation operation."""
        element_type = node.element_type.replace('KEYWORD_', '').lower()
        func_name = f"d_array_{element_type}_concat"
        concat_func = self.context.module.get_global(func_name)
        
        # Get array struct pointers
        lhs_var_ptr = self.context.visit(node.left)
        rhs_var_ptr = self.context.visit(node.right)
        lhs_array_ptr = self.context.builder.load(lhs_var_ptr)
        rhs_array_ptr = self.context.builder.load(rhs_var_ptr)
        
        return self.context.builder.call(concat_func, [lhs_array_ptr, rhs_array_ptr], 'concat_array_tmp')
    
    def _generate_float_operation(self, left_val, right_val, op):
        """Generate float operations with type promotion."""
        # Promote integers to floats
        if isinstance(left_val.type, ir.IntType):
            left_val = self.context.builder.sitofp(left_val, ir.DoubleType())
        if isinstance(right_val.type, ir.IntType):
            right_val = self.context.builder.sitofp(right_val, ir.DoubleType())
        
        # Arithmetic operations
        op_map = {
            '+': self.context.builder.fadd,
            '-': self.context.builder.fsub,
            '*': self.context.builder.fmul,
            '/': self.context.builder.fdiv
        }
        
        if op in op_map:
            return op_map[op](left_val, right_val, 'f_tmp')
        
        # Relational operations
        op_map_rel = {
            '<': 'olt', '>': 'ogt', '<=': 'ole', '>=': 'oge', 
            '==': 'oeq', '!=': 'one'
        }
        
        if op in op_map_rel:
            return self.context.builder.fcmp_ordered(op_map_rel[op], left_val, right_val, 'f_cmp_tmp')
        
        return None
    
    def _generate_integer_operation(self, left_val, right_val, op):
        """Generate integer operations."""
        # Arithmetic operations
        op_map = {
            '+': self.context.builder.add,
            '-': self.context.builder.sub,
            '*': self.context.builder.mul,
            '/': self.context.builder.sdiv,
            '%': self.context.builder.srem
        }
        
        if op in op_map:
            return op_map[op](left_val, right_val, 'i_tmp')
        
        # Relational operations
        op_map_rel = {
            '<': '<', '>': '>', '<=': '<=', '>=': '>=', 
            '==': '==', '!=': '!='
        }
        
        if op in op_map_rel:
            return self.context.builder.icmp_signed(op_map_rel[op], left_val, right_val, f'i_cmp_{op}')
        
        # Logical operations
        if op == '&&':
            return self.context.builder.and_(left_val, right_val, 'and_tmp')
        if op == '||':
            return self.context.builder.or_(left_val, right_val, 'or_tmp')
        
        return None

# ============================================================================
# Control Flow Generation
# ============================================================================

class ControlFlowGenerator(CodeGeneratorComponent):
    """Handles generation of LLVM IR for control flow structures."""
    
    def __init__(self, context: LLVMContext):
        super().__init__(context)
    
    def initialize(self):
        """Initialize the control flow generator."""
        pass
    
    def generate_if_statement(self, node):
        """Generate if statement with optional else branch."""
        cond_val = self._load_if_pointer(self.context.visit(node.condition))
        
        # Convert integer conditions to boolean
        if cond_val.type == ir.IntType(32):
            zero = ir.Constant(ir.IntType(32), 0)
            cond_val = self.context.builder.icmp_signed('!=', cond_val, zero, 'bool_cond')
        
        # Create basic blocks
        then_block = self.context.current_function.append_basic_block(name='then')
        
        if node.else_branch:
            else_block = self.context.current_function.append_basic_block(name='else')
            merge_block = self.context.current_function.append_basic_block(name='if_cont')
            self.context.builder.cbranch(cond_val, then_block, else_block)
        else:
            merge_block = self.context.current_function.append_basic_block(name='if_cont')
            self.context.builder.cbranch(cond_val, then_block, merge_block)
        
        # Generate then block
        self.context.builder.position_at_end(then_block)
        self.context.visit(node.then_branch)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(merge_block)
        
        # Generate else block if it exists
        if node.else_branch:
            self.context.builder.position_at_end(else_block)
            self.context.visit(node.else_branch)
            if not self.context.builder.block.is_terminated:
                self.context.builder.branch(merge_block)
        
        # Position builder at merge block
        self.context.builder.position_at_end(merge_block)
    
    def generate_while_statement(self, node):
        """Generate while loop."""
        loop_header = self.context.current_function.append_basic_block(name='loop_header')
        loop_body = self.context.current_function.append_basic_block(name='loop_body')
        loop_exit = self.context.current_function.append_basic_block(name='loop_exit')
        
        # Branch to header
        self.context.builder.branch(loop_header)
        self.context.builder.position_at_end(loop_header)
        
        # Evaluate condition
        cond_val = self._load_if_pointer(self.context.visit(node.condition))
        self.context.builder.cbranch(cond_val, loop_body, loop_exit)
        
        # Generate loop body
        self.context.builder.position_at_end(loop_body)
        self.context.visit(node.body)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(loop_header)
        
        # Position at exit block
        self.context.builder.position_at_end(loop_exit)
    
    def generate_for_statement(self, node):
        """Generate for loop."""
        loop_header = self.context.current_function.append_basic_block(name='for_header')
        loop_body = self.context.current_function.append_basic_block(name='for_body')
        loop_update = self.context.current_function.append_basic_block(name='for_update')
        loop_exit = self.context.current_function.append_basic_block(name='for_exit')
        
        # Initialization
        if node.initializer:
            self.context.visit(node.initializer)
        
        # Jump to header
        self.context.builder.branch(loop_header)
        self.context.builder.position_at_end(loop_header)
        
        # Condition check
        if node.condition:
            cond_val = self._load_if_pointer(self.context.visit(node.condition))
            self.context.builder.cbranch(cond_val, loop_body, loop_exit)
        else:
            self.context.builder.branch(loop_body)
        
        # Generate loop body
        self.context.builder.position_at_end(loop_body)
        self.context.visit(node.body)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(loop_update)
        
        # Generate update block
        self.context.builder.position_at_end(loop_update)
        if node.update:
            self.context.visit(node.update)
        self.context.builder.branch(loop_header)
        
        # Position at exit block
        self.context.builder.position_at_end(loop_exit)
    
    def _load_if_pointer(self, value):
        """Load value if it's a pointer, otherwise return as-is."""
        if isinstance(value.type, ir.PointerType):
            if value.type.pointee == ir.IntType(8):
                return value  # Keep string pointers as pointers
            return self.context.builder.load(value)
        return value

# ============================================================================
# Main LLVM Generator
# ============================================================================

class ModularLLVMGenerator(Visitor):
    """Main LLVM code generator that orchestrates all components."""
    
    def __init__(self, symbol_table, debug=True):
        self.symbol_table = symbol_table
        
        # Create context and components
        self.context = LLVMContext(debug)
        self.context.symbol_table = symbol_table
        
        self.type_manager = TypeManager(self.context)
        self.runtime_manager = RuntimeFunctionManager(self.context, self.type_manager)
        self.expression_generator = ExpressionGenerator(self.context, self.type_manager)
        self.control_flow_generator = ControlFlowGenerator(self.context)
        
        # Initialize all components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all generator components."""
        self.type_manager.initialize()
        self.runtime_manager.initialize()
        self.expression_generator.initialize()
        self.control_flow_generator.initialize()
    
    def generate(self, ast):
        """Generate LLVM IR from the AST."""
        # First pass: declare global variables and function definitions
        for stmt in ast.statements:
            if isinstance(stmt, (Declaration, FunctionDefinition)):
                self.visit(stmt)
        
        # Create main function wrapper if needed
        self._create_main_function_if_needed(ast)
        
        return self.finalize()
    
    def _create_main_function_if_needed(self, ast):
        """Create main function wrapper for global statements."""
        # Check if main function already exists
        main_func = None
        try:
            main_func = self.context.module.get_global("main")
        except KeyError:
            pass
        
        if main_func is None:
            # Create main function
            main_type = ir.FunctionType(ir.IntType(32), [])
            main_func = ir.Function(self.context.module, main_type, name="main")
            
            # Create entry block
            entry_block = main_func.append_basic_block(name='entry')
            self.context.builder = ir.IRBuilder(entry_block)
            self.context.current_function = main_func
            
            # Process global statements
            self._process_global_statements(ast)
            
            # Return 0 from main
            if not self.context.builder.block.is_terminated:
                self.context.builder.ret(ir.Constant(ir.IntType(32), 0))
            
            self.context.current_function = None
            self.context.builder = None
    
    def _process_global_statements(self, ast):
        """Process global statements in the main function."""
        # Initialize global dynamic arrays
        for array_info in self.context.global_dynamic_arrays:
            self._initialize_global_array(array_info)
        
        # Process deferred initializers
        for var_name, initializer_node in self.context.deferred_initializers:
            if var_name in self.context.global_vars:
                init_val = self.visit(initializer_node)
                self.context.builder.store(init_val, self.context.global_vars[var_name])
        
        # Visit non-declaration, non-function-definition statements
        for stmt in ast.statements:
            if not isinstance(stmt, (Declaration, FunctionDefinition)):
                self.visit(stmt)
    
    def _initialize_global_array(self, array_info):
        """Initialize a global dynamic array."""
        if len(array_info) == 4:
            name, element_type_str, init_nodes, is_dynamic = array_info
            expr_initializer = None
        else:
            name, element_type_str, init_nodes, is_dynamic, expr_initializer = array_info
        
        if is_dynamic:
            create_func = self.context.module.get_global(f"d_array_{element_type_str}_create")
            new_array_ptr = self.context.builder.call(create_func, [])
            self.context.builder.store(new_array_ptr, self.context.global_vars[name])
            
            if init_nodes:
                self._initialize_array_with_values(name, element_type_str, init_nodes)
            elif expr_initializer:
                result_array = self.visit(expr_initializer)
                if result_array is not None:
                    self.context.builder.store(result_array, self.context.global_vars[name])
    
    def _initialize_array_with_values(self, name, element_type_str, init_nodes):
        """Initialize array with initial values."""
        append_func = self.context.module.get_global(f"d_array_{element_type_str}_append")
        array_struct_ptr = self.context.builder.load(self.context.global_vars[name])
        expected_elem_type = append_func.function_type.args[1]
        
        for val_node in init_nodes:
            raw_val = self.visit(val_node)
            val = self._coerce_array_element(expected_elem_type, raw_val)
            self.context.builder.call(append_func, [array_struct_ptr, val])
    
    def _coerce_array_element(self, expected_elem_type, raw_val):
        """Coerce array element to expected type."""
        # Handle char array coercion
        if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8:
            if isinstance(raw_val.type, ir.IntType) and raw_val.type.width == 8:
                return raw_val
            elif isinstance(raw_val.type, ir.IntType(8).as_pointer()):
                return self.context.builder.load(raw_val)
        
        # Handle string array coercion
        elif isinstance(expected_elem_type, ir.IntType(8).as_pointer()):
            if isinstance(raw_val.type, ir.IntType(8).as_pointer()):
                return raw_val
        
        # Normal pointer load semantics
        return self._load_if_pointer(raw_val)
    
    def _load_if_pointer(self, value):
        """Load value if it's a pointer, otherwise return as-is."""
        if isinstance(value.type, ir.PointerType):
            if value.type.pointee == ir.IntType(8):
                return value  # Keep string pointers as pointers
            return self.context.builder.load(value)
        return value
    
    def finalize(self):
        """Finalize the LLVM module and return the parsed module object."""
        llvm_ir = str(self.context.module)
        if self.context.debug:
            print("\n--- Generated LLVM IR ---\n")
            print(llvm_ir)
        
        try:
            llvm_module = llvm.parse_assembly(llvm_ir)
            llvm_module.verify()
            if self.context.debug:
                print("LLVM Module verification successful!")
            return llvm_module
        except RuntimeError as e:
            print(f"LLVM Module Validation Error: {e}")
            print(f"Failing IR:\n{llvm_ir}")
            raise
    
    # Visitor methods would be implemented here, delegating to appropriate components
    # For brevity, I'll show a few key examples:
    
    def visit_binaryop(self, node):
        """Visit binary operation node."""
        # Null equality checks first
        if node.op in ['==', '!=']:
            left_raw = self.visit(node.left)
            right_raw = self.visit(node.right)
            null_check = self._check_null_equality(left_raw, right_raw)
            if null_check is not None:
                if node.op == '!=':
                    return self.context.builder.not_(null_check, 'not_null_check')
                return null_check

        # String-specific operations: string vs string comparisons and length comparisons
        if node.op in ['==', '!=', '<', '>', '<=', '>=']:
            left_raw = self.visit(node.left)
            right_raw = self.visit(node.right)
            # Try string vs string using expression generator
            if (self.expression_generator._is_string_value(left_raw) and 
                self.expression_generator._is_string_value(right_raw)):
                left_val_str = self.expression_generator._load_string_value(left_raw)
                right_val_str = self.expression_generator._load_string_value(right_raw)
                res = self.expression_generator._generate_string_operation(left_val_str, right_val_str, node.op)
                if res is not None:
                    return res
            # Handle length comparisons where one side is string and the other is int
            length_cmp = self._handle_string_length_operations(left_raw, right_raw, node.op)
            if length_cmp is not None:
                return length_cmp

        # Fallback to general binary op handling
        left_val = self._load_if_pointer(self.visit(node.left))
        right_val = self._load_if_pointer(self.visit(node.right))
        return self.expression_generator.generate_binary_operation(node, left_val, right_val, node.op)
    
    def visit_ifstatement(self, node):
        """Visit if statement node."""
        self.control_flow_generator.generate_if_statement(node)
    
    def visit_whilestatement(self, node):
        """Visit while statement node."""
        self.control_flow_generator.generate_while_statement(node)
    
    def visit_forstatement(self, node):
        """Visit for statement node."""
        self.control_flow_generator.generate_for_statement(node)
    
    # Additional visitor methods would be implemented here...
    # This is a simplified version showing the modular structure

    # ------------------------------------------------------------------
    # Added comprehensive visitor methods to match monolithic generator
    # ------------------------------------------------------------------

    def visit_block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_functiondefinition(self, node):
        func_symbol = self.context.symbol_table.lookup_function(node.name)
        return_type = self.type_manager.get_llvm_type(func_symbol['return_type'])
        param_types = [self.type_manager.get_llvm_type(pt) for pt in func_symbol['param_types']]
        func_type = ir.FunctionType(return_type, param_types)
        self.context.current_function = ir.Function(self.context.module, func_type, name=node.name)
        entry_block = self.context.current_function.append_basic_block(name='entry')
        self.context.builder = ir.IRBuilder(entry_block)
        self.context.llvm_var_table.clear()
        for i, arg in enumerate(self.context.current_function.args):
            param_name = func_symbol['params'][i][1]
            arg.name = param_name
            ptr = self.context.builder.alloca(param_types[i], name=param_name)
            self.context.builder.store(arg, ptr)
            self.context.llvm_var_table[param_name] = ptr
        self.visit(node.body)
        if not self.context.builder.block.is_terminated:
            if return_type == ir.VoidType():
                self.context.builder.ret_void()
            else:
                zero = ir.Constant(return_type, 0)
                self.context.builder.ret(zero)
        self.context.current_function = None
        self.context.builder = None

    def visit_declaration(self, node):
        var_name = node.identifier
        var_type = self.type_manager.get_llvm_type(node.var_type.type_name)
        if self.context.builder is None:
            if node.initializer and not self._is_function_call_initializer(node.initializer):
                init_val = self._evaluate_constant_expression(node.initializer)
                initializer = init_val
            else:
                if isinstance(var_type, ir.IntType):
                    initializer = ir.Constant(var_type, 0)
                elif isinstance(var_type, ir.DoubleType):
                    initializer = ir.Constant(var_type, 0.0)
                elif isinstance(var_type, ir.PointerType):
                    initializer = ir.Constant(var_type, None)
                else:
                    initializer = ir.Constant(var_type, 0)
            global_var = ir.GlobalVariable(self.context.module, var_type, name=var_name)
            global_var.initializer = initializer
            global_var.linkage = 'internal'
            self.context.global_vars[var_name] = global_var
            self.context.llvm_var_table[var_name] = global_var
            if node.initializer and self._is_function_call_initializer(node.initializer):
                self.context.deferred_initializers.append((node.identifier, node.initializer))
        else:
            ptr = self.context.builder.alloca(var_type, name=var_name)
            self.context.llvm_var_table[var_name] = ptr
            if node.initializer:
                init_val = self.visit(node.initializer)
                self.context.builder.store(init_val, ptr)

    def visit_arraydeclaration(self, node):
        var_name = node.identifier
        sym = self.context.symbol_table.lookup_symbol(var_name)
        ti = sym.get('typeinfo') if sym else None
        base = ti.base if ti else node.var_type.type_name.replace('KEYWORD_','').lower()
        is_dyn = ti.is_dynamic if ti else node.is_dynamic
        element_type_ir = self.type_manager.get_llvm_type(node.var_type.type_name)
        is_global = self.context.builder is None
        if is_dyn:
            array_ptr_type = self.type_manager.get_llvm_type(f'd_array_{base}')
            if is_global:
                global_var = ir.GlobalVariable(self.context.module, array_ptr_type, name=var_name)
                global_var.initializer = ir.Constant(array_ptr_type, None)
                global_var.linkage = 'internal'
                self.context.global_vars[var_name] = global_var
                self.context.llvm_var_table[var_name] = global_var
                init_nodes = []
                if node.initializer:
                    if hasattr(node.initializer, 'values'):
                        init_nodes = node.initializer.values
                    else:
                        init_nodes = []
                self.context.global_dynamic_arrays.append((var_name, base, init_nodes, True, node.initializer))
            else:
                ptr = self.context.builder.alloca(array_ptr_type, name=var_name)
                self.context.llvm_var_table[var_name] = ptr
                if node.initializer:
                    if hasattr(node.initializer, 'values'):
                        create_func = self._array_runtime_func(base, 'create')
                        new_array_ptr = self.context.builder.call(create_func, [])
                        self.context.builder.store(new_array_ptr, ptr)
                        append_func = self._array_runtime_func(base, 'append')
                        array_struct_ptr = new_array_ptr
                        expected_elem_type = append_func.function_type.args[1]
                        for val_node in node.initializer.values:
                            raw_val = self.visit(val_node)
                            val = self._coerce_char_array_element(expected_elem_type, raw_val)
                            if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                val = self.context.builder.sitofp(val, expected_elem_type)
                            if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                val = self.context.builder.load(val)
                            self.context.builder.call(append_func, [array_struct_ptr, val])
                    else:
                        result_array = self.visit(node.initializer)
                        self.context.builder.store(result_array, ptr)
                else:
                    create_func = self._array_runtime_func(base, 'create')
                    new_array_ptr = self.context.builder.call(create_func, [])
                    self.context.builder.store(new_array_ptr, ptr)
        else:
            size = int(node.size.value) if node.size else (len(node.initializer.values) if node.initializer else 0)
            array_type = ir.ArrayType(element_type_ir, size)
            if is_global:
                zero_list = []
                if node.initializer:
                    init_vals = []
                    for v in node.initializer.values:
                        init_vals.append(self.visit(v))
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
                global_var = ir.GlobalVariable(self.context.module, array_type, name=var_name)
                global_var.initializer = initializer
                global_var.linkage = 'internal'
                self.context.global_vars[var_name] = global_var
                self.context.llvm_var_table[var_name] = global_var
            else:
                ptr = self.context.builder.alloca(array_type, name=var_name)
                self.context.llvm_var_table[var_name] = ptr
                if node.initializer:
                    for i, v in enumerate(node.initializer.values):
                        val = self.visit(v)
                        index_ptr = self.context.builder.gep(ptr, [ir.Constant(ir.IntType(32),0), ir.Constant(ir.IntType(32), i)])
                        self.context.builder.store(val, index_ptr)

    def visit_assignment(self, node):
        if isinstance(node.lhs, SubscriptAccess):
            sym = self.context.symbol_table.lookup_symbol(node.lhs.name)
            ti = sym.get('typeinfo') if sym else None
            if ti and ti.is_dynamic:
                base = ti.base
                array_var_ptr = self.context.llvm_var_table[node.lhs.name]
                array_struct_ptr = self.context.builder.load(array_var_ptr)
                index_val = self._load_if_pointer(self.visit(node.lhs.key))
                value_val = self._load_if_pointer(self.visit(node.rhs))
                set_func = self._array_runtime_func(base, 'set')
                self.context.builder.call(set_func, [array_struct_ptr, index_val, value_val])
                return
        ptr = self.visit(node.lhs)
        value_to_store = self.visit(node.rhs)
        target_type = ptr.type.pointee if hasattr(ptr.type,'pointee') else ptr.type.pointed_type
        if target_type != value_to_store.type and isinstance(target_type, ir.DoubleType) and isinstance(value_to_store.type, ir.IntType):
            value_to_store = self.context.builder.sitofp(value_to_store, target_type)
        self.context.builder.store(value_to_store, ptr)

    def visit_returnstatement(self, node):
        if node.value:
            return_val = self.visit(node.value)
            self.context.builder.ret(return_val)
        else:
            self.context.builder.ret_void()

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
                str_val = val[1:-1].replace('\\n', '\n') + '\0'
                if str_val in self.context.global_strings:
                    ptr = self.context.global_strings[str_val]
                else:
                    c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                    global_var = ir.GlobalVariable(self.context.module, c_str.type, name=f".str{len(self.context.global_strings)}")
                    global_var.initializer = c_str
                    global_var.global_constant = True
                    global_var.linkage = 'internal'
                    if self.context.builder:
                        ptr = self.context.builder.bitcast(global_var, ir.IntType(8).as_pointer())
                    else:
                        ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                    self.context.global_strings[str_val] = ptr
                return ptr
        raise Exception(f"Unsupported primary literal: {val}")

    def visit_unaryop(self, node):
        operand_val = self._load_if_pointer(self.visit(node.operand))
        if node.op == '-':
            if isinstance(operand_val.type, ir.DoubleType):
                return self.context.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), operand_val, 'f_neg_tmp')
            else:
                return self.context.builder.sub(ir.Constant(operand_val.type, 0), operand_val, 'i_neg_tmp')
        raise Exception(f"Unknown unary operator: {node.op}")

    def visit_identifier(self, node):
        if node.name in self.context.llvm_var_table:
            return self.context.llvm_var_table[node.name]
        try:
            gv = self.context.module.get_global(node.name)
            return gv
        except KeyError:
            pass
        raise Exception(f"Unknown variable referenced: {node.name}")

    def visit_subscriptaccess(self, node):
        sym = self.context.symbol_table.lookup_symbol(node.name)
        ti = sym.get('typeinfo') if sym else None
        if sym and sym.get('type') == 'KEYWORD_DICT':
            dict_var_ptr = self.context.llvm_var_table[node.name]
            dict_val = self.context.builder.load(dict_var_ptr)
            key_val = self.visit(node.key)
            dict_has_key_func = self.context.module.get_global("dict_has_key")
            key_exists = self.context.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
            safe_block = self.context.current_function.append_basic_block('dict_safe_access')
            error_block = self.context.current_function.append_basic_block('dict_key_error')
            merge_block = self.context.current_function.append_basic_block('dict_merge')
            self.context.builder.cbranch(key_exists, safe_block, error_block)
            self.context.builder.position_at_end(safe_block)
            dict_get_func = self.context.module.get_global("dict_get")
            safe_result = self.context.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
            self.context.builder.branch(merge_block)
            self.context.builder.position_at_end(error_block)
            dict_value_create_null_func = self.context.module.get_global("dict_value_create_null")
            error_result = self.context.builder.call(dict_value_create_null_func, [], 'null_value')
            self.context.builder.branch(merge_block)
            self.context.builder.position_at_end(merge_block)
            phi = self.context.builder.phi(self.type_manager.dict_types['value'].pointee.as_pointer(), 'dict_access_result')
            phi.add_incoming(safe_result, safe_block)
            phi.add_incoming(error_result, error_block)
            return phi
        if ti and ti.is_dynamic:
            base = ti.base
            array_var_ptr = self.context.llvm_var_table[node.name]
            array_struct_ptr = self.context.builder.load(array_var_ptr)
            index_val = self._load_if_pointer(self.visit(node.key))
            get_func = self._array_runtime_func(base, 'get')
            return self.context.builder.call(get_func, [array_struct_ptr, index_val], 'dyn_idx_tmp')
        array_ptr = self.context.llvm_var_table[node.name]
        key_val = self._load_if_pointer(self.visit(node.key))
        return self.context.builder.gep(array_ptr, [ir.Constant(ir.IntType(32),0), key_val], inbounds=True)

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)

    def visit_array_function_call(self, node):
        func_name = node.name
        args = node.args
        array_node = args[0]
        array_var_ptr = self.visit(array_node)
        array_struct_ptr = self.context.builder.load(array_var_ptr)
        sym = self.context.symbol_table.lookup_symbol(array_node.name)
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
                if base == 'char' and func_name in ['arr_contains', 'arr_indexof']:
                    expected_elem_type = c_func.function_type.args[len(call_args)]
                    arg_val = self._coerce_char_array_element(expected_elem_type, raw_arg_val)
                else:
                    arg_val = self._load_if_pointer(raw_arg_val)
                call_args.append(arg_val)
        return self.context.builder.call(c_func, call_args, f'{func_name}_call')

    def visit_functioncall(self, node):
        if node.name.startswith('arr_'):
            return self.visit_array_function_call(node)
        math_function_map = {
            'pow': 'pie_pow','sqrt': 'pie_sqrt','sin': 'pie_sin','cos': 'pie_cos','tan': 'pie_tan',
            'asin': 'pie_asin','acos': 'pie_acos','atan': 'pie_atan','log': 'pie_log','log10': 'pie_log10',
            'exp': 'pie_exp','floor': 'pie_floor','ceil': 'pie_ceil','round': 'pie_round','abs': 'pie_abs',
            'abs_int': 'pie_abs_int','min': 'pie_min','max': 'pie_max','min_int': 'pie_min_int','max_int': 'pie_max_int',
            'rand': 'pie_rand','srand': 'pie_srand','rand_range': 'pie_rand_range','pi': 'pie_pi','e': 'pie_e','time': 'pie_time'
        }
        actual_name = math_function_map.get(node.name, node.name)
        func = self.context.module.get_global(actual_name)
        if func is None:
            raise Exception(f"Unknown function referenced: {node.name} (mapped to {actual_name})")
        args = []
        for arg in node.args:
            arg_val = self.visit(arg)
            if isinstance(arg, FunctionCall) and arg.name in ['new_int', 'new_float', 'new_string', 'dict_create', 'dict_get']:
                args.append(arg_val)
            else:
                args.append(self._load_if_pointer(arg_val))
        new_args = []
        for i, arg in enumerate(args):
            if i < len(func.args) and arg.type != func.args[i].type:
                if isinstance(func.args[i].type, ir.DoubleType) and isinstance(arg.type, ir.IntType):
                    new_args.append(self.context.builder.sitofp(arg, ir.DoubleType()))
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)
        return self.context.builder.call(func, new_args, 'call_tmp')

    def visit_switchstatement(self, node):
        switch_val = self._load_if_pointer(self.visit(node.expression))
        case_blocks = []
        default_block = None
        exit_block = self.context.current_function.append_basic_block("switch_exit")
        for i, case in enumerate(node.cases):
            if hasattr(case, 'value') and case.value == 'default':
                default_block = self.context.current_function.append_basic_block("default")
            else:
                case_block = self.context.current_function.append_basic_block(f"case_{i}")
                case_blocks.append((case, case_block))
        if default_block is None:
            default_block = exit_block
        switch_instr = self.context.builder.switch(switch_val, default_block)
        for case, case_block in case_blocks:
            case_val = self.visit(case.value)
            switch_instr.add_case(case_val, case_block)
        for case, case_block in case_blocks:
            self.context.builder.position_at_end(case_block)
            for stmt in case.statements:
                self.visit(stmt)
                if stmt.__class__.__name__ == 'ReturnStatement':
                    break
            else:
                self.context.builder.branch(exit_block)
        if default_block != exit_block:
            self.context.builder.position_at_end(default_block)
            for case in node.cases:
                if hasattr(case, 'value') and case.value == 'default':
                    for stmt in case.statements:
                        self.visit(stmt)
                        if stmt.__class__.__name__ == 'ReturnStatement':
                            break
                    else:
                        self.context.builder.branch(exit_block)
                    break
        self.context.builder.position_at_end(exit_block)

    def visit_systemoutput(self, node):
        output_type = node.output_type.type_name.replace('KEYWORD_', '').lower()
        if output_type == 'array':
            array_node = node.expression
            array_var_ptr = self.visit(array_node)
            array_struct_ptr = self.context.builder.load(array_var_ptr)
            array_name = array_node.name
            symbol = self.context.symbol_table.lookup_symbol(array_name)
            element_type = symbol['element_type'].replace('KEYWORD_', '').lower()
            func_name = f"print_{element_type}_array"
            print_func = self.context.module.get_global(func_name)
            self.context.builder.call(print_func, [array_struct_ptr])
            return
        raw_val = self.visit(node.expression)
        if output_type == 'string':
            if isinstance(raw_val.type, ir.PointerType) and isinstance(raw_val.type.pointee, ir.PointerType):
                output_val = self.context.builder.load(raw_val)
            else:
                output_val = raw_val
        else:
            output_val = self._load_if_pointer(raw_val)
        func_name = f"output_{output_type}"
        output_func = self.context.module.get_global(func_name)
        if not output_func:
            raise Exception(f"Runtime function {func_name} not found.")
        args = [output_val]
        if output_type == 'float':
            precision = self._load_if_pointer(self.visit(node.precision)) if node.precision else ir.Constant(ir.IntType(32), 2)
            args.append(precision)
        self.context.builder.call(output_func, args)

    def visit_systeminput(self, node):
        var_ptr = self.visit(node.variable)
        input_type = node.input_type.type_name.replace('KEYWORD_', '').lower()
        func_name = f"input_{input_type}"
        input_func = self.context.module.get_global(func_name)
        if not input_func:
            raise Exception(f"Runtime function {func_name} not found.")
        self.context.builder.call(input_func, [var_ptr])

    def visit_systemexit(self, node):
        exit_func = self.context.module.get_global("pie_exit")
        self.context.builder.call(exit_func, [])

    def visit_arraypush(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        raw_value_val = self.visit(node.value)
        array_type = array_val.type
        if array_type == self.type_manager.d_array_types['int']:
            push_func = self.context.module.get_global("d_array_int_push")
            value_val = self._load_if_pointer(raw_value_val)
        elif array_type == self.type_manager.d_array_types['string']:
            push_func = self.context.module.get_global("d_array_string_push")
            if isinstance(raw_value_val.type, ir.PointerType) and raw_value_val.type.pointee == ir.IntType(8).as_pointer():
                value_val = self.context.builder.load(raw_value_val)
            else:
                value_val = raw_value_val
        elif array_type == self.type_manager.d_array_types['float']:
            push_func = self.context.module.get_global("d_array_float_push")
            value_val = self._load_if_pointer(raw_value_val)
        elif array_type == self.type_manager.d_array_types['char']:
            push_func = self.context.module.get_global("d_array_char_append")
            expected_elem_type = push_func.function_type.args[1]
            value_val = self._coerce_char_array_element(expected_elem_type, raw_value_val)
        else:
            raise Exception(f"Unsupported array type for push: {array_type}")
        self.context.builder.call(push_func, [array_val, value_val])

    def visit_arraypop(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        array_type = array_val.type
        if array_type == self.type_manager.d_array_types['int']:
            pop_func = self.context.module.get_global("d_array_int_pop")
        elif array_type == self.type_manager.d_array_types['string']:
            pop_func = self.context.module.get_global("d_array_string_pop")
        elif array_type == self.type_manager.d_array_types['float']:
            pop_func = self.context.module.get_global("d_array_float_pop")
        elif array_type == self.type_manager.d_array_types['char']:
            pop_func = self.context.module.get_global("d_array_char_pop")
        else:
            raise Exception(f"Unsupported array type for pop: {array_type}")
        return self.context.builder.call(pop_func, [array_val])

    def visit_arraysize(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        array_type = array_val.type
        if array_type == self.type_manager.d_array_types['int']:
            size_func = self.context.module.get_global("d_array_int_size")
        elif array_type == self.type_manager.d_array_types['string']:
            size_func = self.context.module.get_global("d_array_string_size")
        elif array_type == self.type_manager.d_array_types['float']:
            size_func = self.context.module.get_global("d_array_float_size")
        elif array_type == self.type_manager.d_array_types['char']:
            size_func = self.context.module.get_global("d_array_char_size")
        else:
            raise Exception(f"Unsupported array type for size: {array_type}")
        return self.context.builder.call(size_func, [array_val])

    def visit_arrayavg(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        array_type = array_val.type
        if array_type == self.type_manager.d_array_types['int']:
            avg_func = self.context.module.get_global("d_array_int_avg")
        elif array_type == self.type_manager.d_array_types['float']:
            avg_func = self.context.module.get_global("d_array_float_avg")
        else:
            raise Exception(f"Unsupported array type for avg: {array_type}")
        return self.context.builder.call(avg_func, [array_val])

    def visit_arrayindexof(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        array_type = array_val.type
        value_val = self._load_if_pointer(self.visit(node.value))
        if array_type == self.type_manager.d_array_types['int']:
            indexof_func = self.context.module.get_global("d_array_int_indexof")
        elif array_type == self.type_manager.d_array_types['string']:
            indexof_func = self.context.module.get_global("d_array_string_indexof")
        elif array_type == self.type_manager.d_array_types['float']:
            indexof_func = self.context.module.get_global("d_array_float_indexof")
        elif array_type == self.type_manager.d_array_types['char']:
            indexof_func = self.context.module.get_global("d_array_char_indexof")
        else:
            raise Exception(f"Unsupported array type for indexof: {array_type}")
        return self.context.builder.call(indexof_func, [array_val, value_val])

    def visit_arraycontains(self, node):
        array_ptr = self.visit(node.array)
        array_val = self.context.builder.load(array_ptr)
        array_type = array_val.type
        value_val = self._load_if_pointer(self.visit(node.value))
        if array_type == self.type_manager.d_array_types['int']:
            contains_func = self.context.module.get_global("d_array_int_contains")
        elif array_type == self.type_manager.d_array_types['string']:
            contains_func = self.context.module.get_global("d_array_string_contains")
        elif array_type == self.type_manager.d_array_types['float']:
            contains_func = self.context.module.get_global("d_array_float_contains")
        elif array_type == self.type_manager.d_array_types['char']:
            contains_func = self.context.module.get_global("d_array_char_contains")
        else:
            raise Exception(f"Unsupported array type for contains: {array_type}")
        return self.context.builder.call(contains_func, [array_val, value_val])

    def visit_initializerlist(self, node):
        return None

    def visit_dictionaryliteral(self, node):
        dict_create_func = self.context.module.get_global("dict_create")
        dict_ptr = self.context.builder.call(dict_create_func, [])
        dict_set_func = self.context.module.get_global("dict_set")
        for key_expr, value_expr in node.pairs:
            key_val = self.visit(key_expr)
            value_val = self.visit(value_expr)
            if value_val.type == ir.IntType(32):
                new_int_func = self.context.module.get_global("new_int")
                dict_value = self.context.builder.call(new_int_func, [value_val])
            elif value_val.type == ir.DoubleType():
                new_float_func = self.context.module.get_global("new_float")
                dict_value = self.context.builder.call(new_float_func, [value_val])
            elif value_val.type == ir.IntType(8).as_pointer():
                new_string_func = self.context.module.get_global("new_string")
                dict_value = self.context.builder.call(new_string_func, [value_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.IntType) and value_val.type.pointee.width == 32:
                loaded_val = self.context.builder.load(value_val)
                new_int_func = self.context.module.get_global("new_int")
                dict_value = self.context.builder.call(new_int_func, [loaded_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.DoubleType):
                loaded_val = self.context.builder.load(value_val)
                new_float_func = self.context.module.get_global("new_float")
                dict_value = self.context.builder.call(new_float_func, [loaded_val])
            else:
                raise Exception(f"Unsupported dictionary value type: {value_val.type}")
            self.context.builder.call(dict_set_func, [dict_ptr, key_val, dict_value])
        return dict_ptr

    def visit_safedictionaryaccess(self, node):
        dict_var_ptr = self.context.llvm_var_table[node.dict_name]
        dict_val = self.context.builder.load(dict_var_ptr)
        key_val = self.visit(node.key)
        dict_has_key_func = self.context.module.get_global("dict_has_key")
        key_exists = self.context.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
        safe_block = self.context.current_function.append_basic_block('safe_dict_access')
        default_block = self.context.current_function.append_basic_block('dict_default_value')
        merge_block = self.context.current_function.append_basic_block('safe_dict_merge')
        self.context.builder.cbranch(key_exists, safe_block, default_block)
        self.context.builder.position_at_end(safe_block)
        dict_get_func = self.context.module.get_global("dict_get")
        safe_result = self.context.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
        self.context.builder.branch(merge_block)
        self.context.builder.position_at_end(default_block)
        if node.default_value:
            default_result = self.visit(node.default_value)
            if default_result.type == ir.IntType(32):
                new_int_func = self.context.module.get_global("new_int")
                default_result = self.context.builder.call(new_int_func, [default_result])
            elif default_result.type == ir.DoubleType():
                new_float_func = self.context.module.get_global("new_float")
                default_result = self.context.builder.call(new_float_func, [default_result])
            elif default_result.type == ir.IntType(8).as_pointer():
                new_string_func = self.context.module.get_global("new_string")
                default_result = self.context.builder.call(new_string_func, [default_result])
        else:
            dict_value_create_null_func = self.context.module.get_global("dict_value_create_null")
            default_result = self.context.builder.call(dict_value_create_null_func, [], 'null_value')
        self.context.builder.branch(merge_block)
        self.context.builder.position_at_end(merge_block)
        phi = self.context.builder.phi(self.type_manager.dict_types['value'].pointee.as_pointer(), 'safe_dict_result')
        phi.add_incoming(safe_result, safe_block)
        phi.add_incoming(default_result, default_block)
        return phi

    # ------------------------ Helpers ------------------------

    def _array_runtime_func(self, base_type, operation):
        func_name = f"d_array_{base_type}_{operation}"
        return self.context.module.get_global(func_name)

    def _coerce_char_array_element(self, expected_elem_type, raw_val):
        if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8:
            if isinstance(raw_val.type, ir.IntType) and raw_val.type.width == 8:
                return raw_val
            elif isinstance(raw_val.type, ir.IntType(8).as_pointer()):
                return self.context.builder.load(raw_val)
        elif isinstance(expected_elem_type, ir.IntType(8).as_pointer()):
            if isinstance(raw_val.type, ir.IntType(8).as_pointer()):
                return raw_val
        return self._load_if_pointer(raw_val)

    def _evaluate_constant_expression(self, node):
        if hasattr(node, 'value'):
            val = node.value
            if isinstance(val, str):
                if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                    return ir.Constant(ir.IntType(32), int(val))
                if val.startswith('"') and val.endswith('"'):
                    str_val = val[1:-1].replace('\\n', '\n') + '\0'
                    if str_val in self.context.global_strings:
                        return self.context.global_strings[str_val]
                    c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                    global_var = ir.GlobalVariable(self.context.module, c_str.type, name=f".str{len(self.context.global_strings)}")
                    global_var.initializer = c_str
                    global_var.global_constant = True
                    global_var.linkage = 'internal'
                    ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                    self.context.global_strings[str_val] = ptr
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
                if val.startswith("'") and val.endswith("'") and len(val) == 3:
                    ch = val[1]
                    return ir.Constant(ir.IntType(8), ord(ch))
        return ir.Constant(ir.IntType(32), 0)

    def _is_function_call_initializer(self, node):
        class_name = type(node).__name__
        if class_name in ['ArrayIndexOf', 'ArrayContains', 'ArrayPush', 'ArrayPop', 'ArraySize', 'ArrayAvg', 'SystemOutput', 'FunctionCall', 'DictionaryLiteral']:
            return True
        if class_name == 'BinaryOp':
            return self._contains_global_reference(node)
        return False

    def _contains_global_reference(self, node):
        class_name = type(node).__name__
        if class_name == 'Identifier':
            return node.name in self.context.global_vars
        if class_name == 'BinaryOp':
            return (self._contains_global_reference(node.left) or self._contains_global_reference(node.right))
        if class_name == 'FunctionCall':
            return True
        return False

    def _is_null_value(self, value):
        if isinstance(value, ir.Constant):
            if value.type == ir.IntType(8).as_pointer():
                return value.constant is None
            if hasattr(value, 'constant') and value.constant is None:
                return True
        return False

    def _check_null_equality(self, left, right):
        # null == null
        if self._is_null_value(left) and self._is_null_value(right):
            return ir.Constant(ir.IntType(1), 1)
        # value == null
        if self._is_null_value(right):
            if isinstance(left.type, ir.PointerType):
                if left.type.pointee == ir.IntType(8):
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.context.builder.icmp_unsigned('==', left, null_ptr, 'null_check')
                elif left.type.pointee == ir.IntType(8).as_pointer():
                    loaded_left = self.context.builder.load(left)
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.context.builder.icmp_unsigned('==', loaded_left, null_ptr, 'null_check')
                elif left.type.pointee == ir.IntType(32):
                    loaded_left = self.context.builder.load(left)
                    return ir.Constant(ir.IntType(1), 0)
            else:
                return ir.Constant(ir.IntType(1), 0)
        # null == value
        if self._is_null_value(left):
            if isinstance(right.type, ir.PointerType):
                if right.type.pointee == ir.IntType(8):
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.context.builder.icmp_unsigned('==', right, null_ptr, 'null_check')
                elif right.type.pointee == ir.IntType(8).as_pointer():
                    loaded_right = self.context.builder.load(right)
                    null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                    return self.context.builder.icmp_unsigned('==', loaded_right, null_ptr, 'null_check')
                elif right.type.pointee == ir.IntType(32):
                    loaded_right = self.context.builder.load(right)
                    return ir.Constant(ir.IntType(1), 0)
            else:
                return ir.Constant(ir.IntType(1), 0)
        # string ptr vs string ptr where one may be null const
        if (isinstance(left.type, ir.PointerType) and left.type.pointee == ir.IntType(8) and
            isinstance(right.type, ir.PointerType) and right.type.pointee == ir.IntType(8)):
            if self._is_null_value(left):
                null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                return self.context.builder.icmp_unsigned('==', right, null_ptr, 'null_check')
            elif self._is_null_value(right):
                null_ptr = ir.Constant(ir.IntType(8).as_pointer(), None)
                return self.context.builder.icmp_unsigned('==', left, null_ptr, 'null_check')
        return None

    def _handle_string_length_operations(self, left_val, right_val, op):
        if op not in ['<', '>', '<=', '>=']:
            return None
        def is_string_value(val):
            if isinstance(val.type, ir.PointerType):
                if val.type.pointee == ir.IntType(8):
                    return True
                elif (isinstance(val.type.pointee, ir.PointerType) and 
                      val.type.pointee.pointee == ir.IntType(8)):
                    return True
            return False
        def get_strlen(val):
            if isinstance(val.type.pointee, ir.PointerType):
                str_ptr = self.context.builder.load(val)
            else:
                str_ptr = val
            strlen_func = self.context.module.get_global("pie_strlen")
            return self.context.builder.call(strlen_func, [str_ptr], 'strlen_result')
        if is_string_value(left_val) and isinstance(right_val.type, ir.IntType):
            left_len = get_strlen(left_val)
            return self._compare_values(left_len, right_val, op)
        if is_string_value(right_val) and isinstance(left_val.type, ir.IntType):
            right_len = get_strlen(right_val)
            return self._compare_values(left_val, right_len, op)
        return None

    def _compare_values(self, left_val, right_val, op):
        if op == '<':
            return self.context.builder.icmp_signed('<', left_val, right_val, 'cmp_lt')
        elif op == '>':
            return self.context.builder.icmp_signed('>', left_val, right_val, 'cmp_gt')
        elif op == '<=':
            return self.context.builder.icmp_signed('<=', left_val, right_val, 'cmp_le')
        elif op == '>=':
            return self.context.builder.icmp_signed('>=', left_val, right_val, 'cmp_ge')
        return None
