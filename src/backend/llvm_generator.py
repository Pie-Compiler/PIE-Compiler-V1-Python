import llvmlite.ir as ir
import llvmlite.binding as llvm
from frontend.visitor import Visitor
from frontend.ast import Declaration, FunctionDefinition, FunctionCall, SubscriptAccess, ArrayDeclaration, Identifier
from frontend.types import TypeInfo

class LLVMCodeGenerator(Visitor):
    def __init__(self, symbol_table, debug=True):
        self.debug = debug
        self.symbol_table = symbol_table
        self.module = ir.Module(name="main_module")
        self._initialize_llvm()
        self.current_function = None
        self.builder = None
        self.llvm_var_table = {}
        self.global_strings = {}
        self.global_vars = {}

        self.type_map = {
            'int': ir.IntType(32),
            'float': ir.DoubleType(),
            'char': ir.IntType(8),
            'string': ir.IntType(8).as_pointer(),
            'boolean': ir.IntType(1),
            'void': ir.VoidType(),
            'file': ir.IntType(64), # Opaque handle
            'socket': ir.IntType(32) # Opaque handle
        }

        self._define_structs()
        self._declare_runtime_functions()

    def _initialize_llvm(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.module.triple = self.target_machine.triple
        self.module.data_layout = str(self.target_machine.target_data)

    def get_llvm_type(self, type_str):
        if type_str.startswith('KEYWORD_'):
            type_str = type_str.split('_')[1].lower()

        if type_str in self.type_map:
            return self.type_map[type_str]

        # Handle array types
        sym_info = self.symbol_table.lookup_symbol(type_str)
        if sym_info and isinstance(sym_info.get('type'), TypeInfo) and sym_info['type'].is_array:
            return self.d_array_type.as_pointer()

        # Fallback for complex types not in basic map
        if type_str == 'dict':
            return self.dict_type
        if type_str == 'd_array': # Generic array pointer
             return self.d_array_type.as_pointer()

        raise ValueError(f"Unknown type: {type_str}")

    def get_element_size(self, type_str):
        llvm_type = self.get_llvm_type(type_str)
        return llvm_type.get_abi_size(self.module.data_layout)

    def _define_structs(self):
        # Generic DArray struct
        d_array_struct = self.module.context.get_identified_type("DArray")
        d_array_struct.set_body(
            ir.IntType(8).as_pointer(), # data (void*)
            ir.IntType(64),             # size
            ir.IntType(64),             # capacity
            ir.IntType(64)              # element_size
        )
        self.d_array_type = d_array_struct

        # Dictionary struct (remains for now)
        dict_struct = self.module.context.get_identified_type("Dictionary")
        dict_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(), # buckets
            ir.IntType(32), # capacity
            ir.IntType(32)  # size
        )
        self.dict_type = dict_struct.as_pointer()


    def _declare_runtime_functions(self):
        # Generic DArray functions
        d_array_ptr = self.d_array_type.as_pointer()
        void_ptr = ir.IntType(8).as_pointer()
        size_t = ir.IntType(64)

        ir.Function(self.module, ir.FunctionType(d_array_ptr, [size_t, size_t]), name="d_array_create")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr]), name="d_array_free")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr, void_ptr]), name="d_array_push")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr, void_ptr]), name="d_array_pop")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr, ir.IntType(32), void_ptr]), name="d_array_get")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr, ir.IntType(32), void_ptr]), name="d_array_set")
        ir.Function(self.module, ir.FunctionType(ir.IntType(32), [d_array_ptr]), name="d_array_size")
        ir.Function(self.module, ir.FunctionType(d_array_ptr, [d_array_ptr, d_array_ptr]), name="d_array_concat")

        # Comparison function pointer type
        compare_func_type = ir.FunctionType(ir.IntType(32), [void_ptr, void_ptr]).as_pointer()
        ir.Function(self.module, ir.FunctionType(ir.IntType(32), [d_array_ptr, void_ptr, compare_func_type]), name="d_array_contains")
        ir.Function(self.module, ir.FunctionType(ir.IntType(32), [d_array_ptr, void_ptr, compare_func_type]), name="d_array_indexof")

        # Type-specific helpers
        ir.Function(self.module, ir.FunctionType(ir.DoubleType(), [d_array_ptr]), name="d_array_avg_int")
        ir.Function(self.module, ir.FunctionType(ir.DoubleType(), [d_array_ptr]), name="d_array_avg_float")

        # Declare comparison functions so we can get pointers to them
        for t in ['int', 'float', 'char', 'string']:
            ir.Function(self.module, ir.FunctionType(ir.IntType(32), [void_ptr, void_ptr]), name=f"compare_{t}")

        # Printing functions
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr]), name="print_int_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr]), name="print_string_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr]), name="print_float_array")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [d_array_ptr]), name="print_char_array")

        # Other runtime functions (simplified for brevity)
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('string')]), name="output_string")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('int')]), name="output_int")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('float'), self.get_llvm_type('int')]), name="output_float")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('char')]), name="output_char")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('boolean')]), name="output_bool")


    def generate(self, ast):
        """Generate LLVM IR from the AST."""
        # First pass: declare global variables and function definitions
        global_statements = []
        for stmt in ast.statements:
            if isinstance(stmt, (Declaration, ArrayDeclaration)):
                self.visit(stmt)
                if stmt.initializer:
                     global_statements.append(stmt)
            elif isinstance(stmt, FunctionDefinition):
                self.visit(stmt)
            else:
                global_statements.append(stmt)

        # Create a main function to wrap global statements if no main() is defined
        self._create_main_wrapper(global_statements)
        
        return self.finalize()

    def _create_main_wrapper(self, global_statements):
        main_func = self.module.globals.get("main")
        if not main_func:
            main_type = ir.FunctionType(ir.IntType(32), [])
            main_func = ir.Function(self.module, main_type, name="main")
            entry_block = main_func.append_basic_block(name='entry')
            self.builder = ir.IRBuilder(entry_block)
            self.current_function = main_func
            
            for stmt in global_statements:
                self.visit(stmt)

            if not self.builder.block.is_terminated:
                self.builder.ret(ir.Constant(ir.IntType(32), 0))
            
            self.current_function = None
            self.builder = None

    def finalize(self):
        llvm_ir = str(self.module)
        if self.debug:
            print("\n--- Generated LLVM IR ---\n")
            print(llvm_ir)

        try:
            llvm_module = llvm.parse_assembly(llvm_ir)
            llvm_module.verify()
            return llvm_module
        except Exception as e:
            print("LLVM IR Verification Failed!")
            print(e)
            raise

    # --- Visitor Methods ---

    def visit_program(self, node):
        pass # Handled in generate()

    def visit_block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_functiondefinition(self, node):
        func_symbol = self.symbol_table.lookup_function(node.name)
        return_type = self.get_llvm_type(func_symbol['return_type'])
        param_types = [self.get_llvm_type(pt) for pt in func_symbol['param_types']]
        func_type = ir.FunctionType(return_type, param_types)

        self.current_function = ir.Function(self.module, func_type, name=node.name)

        # Name arguments
        for i, arg in enumerate(self.current_function.args):
            arg.name = func_symbol['params'][i][1]

        entry_block = self.current_function.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(entry_block)

        # Allocate space for parameters
        self.llvm_var_table.clear()
        for arg in self.current_function.args:
            ptr = self.builder.alloca(arg.type, name=arg.name)
            self.builder.store(arg, ptr)
            self.llvm_var_table[arg.name] = ptr

        self.visit(node.body)

        if not self.builder.block.is_terminated:
            if return_type == ir.VoidType():
                self.builder.ret_void()
            else:
                self.builder.ret(ir.Constant(return_type, 0))

        self.current_function = None
        self.builder = None

    def visit_declaration(self, node):
        var_name = node.identifier
        var_type = self.get_llvm_type(node.var_type.type_name)

        if self.builder is None: # Global
            global_var = ir.GlobalVariable(self.module, var_type, name=var_name)
            global_var.initializer = ir.Constant(var_type, 0) # Default init
            self.global_vars[var_name] = global_var
            self.llvm_var_table[var_name] = global_var
        else: # Local
            ptr = self.builder.alloca(var_type, name=var_name)
            self.llvm_var_table[var_name] = ptr
            if node.initializer:
                init_val = self.visit(node.initializer)
                self.builder.store(init_val, ptr)

    def visit_arraydeclaration(self, node):
        var_name = node.identifier
        element_type_str = node.var_type.type_name.replace('KEYWORD_', '').lower()
        element_size = self.get_element_size(element_type_str)
        
        array_ptr_type = self.d_array_type.as_pointer()

        create_func = self.module.get_global("d_array_create")

        # Determine initial capacity
        initial_capacity = 0
        if node.size:
            size_val = self.visit(node.size)
            initial_capacity = size_val.constant
        elif node.initializer:
            initial_capacity = len(node.initializer.values)

        initial_capacity = max(initial_capacity, 4) # Min capacity of 4

        if self.builder is None: # Global array
            # For globals, we create a pointer and initialize it in main
            global_ptr = ir.GlobalVariable(self.module, array_ptr_type, name=var_name)
            global_ptr.initializer = ir.Constant(array_ptr_type, None)
            self.global_vars[var_name] = global_ptr
            self.llvm_var_table[var_name] = global_ptr
            # We'll handle the actual creation and initialization inside the main wrapper
            return

        # Local array
        ptr = self.builder.alloca(array_ptr_type, name=var_name)
        self.llvm_var_table[var_name] = ptr

        new_array = self.builder.call(create_func, [
            ir.Constant(ir.IntType(64), element_size),
            ir.Constant(ir.IntType(64), initial_capacity)
        ])
        self.builder.store(new_array, ptr)

        if node.initializer:
            push_func = self.module.get_global("d_array_push")
            for val_node in node.initializer.values:
                value_to_push = self.visit(val_node)

                # Allocate temporary memory for the value to pass its address
                temp_alloc = self.builder.alloca(value_to_push.type)
                self.builder.store(value_to_push, temp_alloc)

                # Cast the pointer to void*
                void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())

                self.builder.call(push_func, [new_array, void_ptr_val])

    def visit_assignment(self, node):
        value_to_store = self.visit(node.rhs)

        if isinstance(node.lhs, SubscriptAccess):
            array_ptr_ptr = self.visit(node.lhs.name)
            array_ptr = self.builder.load(array_ptr_ptr)
            index = self.visit(node.lhs.key)

            set_func = self.module.get_global("d_array_set")

            temp_alloc = self.builder.alloca(value_to_store.type)
            self.builder.store(value_to_store, temp_alloc)
            void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())

            self.builder.call(set_func, [array_ptr, index, void_ptr_val])
        else:
            ptr = self.visit(node.lhs)
            self.builder.store(value_to_store, ptr)

    def _load_if_pointer(self, value):
        if isinstance(value.type, ir.PointerType):
            # Don't load string literals
            if value.type.pointee.is_array:
                return value
            return self.builder.load(value)
        return value

    def visit_binaryop(self, node):
        # Special case for array concatenation
        if node.op == '+':
            left_type = self.symbol_table.lookup_symbol(node.left.name)['type']
            if isinstance(left_type, TypeInfo) and left_type.is_array:
                lhs_ptr = self.builder.load(self.visit(node.left))
                rhs_ptr = self.builder.load(self.visit(node.right))
                concat_func = self.module.get_global("d_array_concat")
                return self.builder.call(concat_func, [lhs_ptr, rhs_ptr])

        lhs = self._load_if_pointer(self.visit(node.left))
        rhs = self._load_if_pointer(self.visit(node.right))

        # Promote int to float if necessary
        if isinstance(lhs.type, ir.DoubleType) or isinstance(rhs.type, ir.DoubleType):
            if isinstance(lhs.type, ir.IntType): lhs = self.builder.sitofp(lhs, ir.DoubleType())
            if isinstance(rhs.type, ir.IntType): rhs = self.builder.sitofp(rhs, ir.DoubleType())
            op_map = {'+': self.builder.fadd, '-': self.builder.fsub, '*': self.builder.fmul, '/': self.builder.fdiv,
                      '<': 'olt', '>': 'ogt', '<=': 'ole', '>=': 'oge', '==': 'oeq', '!=': 'one'}
            if node.op in ['+', '-', '*', '/']:
                return op_map[node.op](lhs, rhs)
            else:
                return self.builder.fcmp_ordered(op_map[node.op], lhs, rhs)
        
        # Integer and Boolean operations
        op_map = {'+': self.builder.add, '-': self.builder.sub, '*': self.builder.mul, '/': self.builder.sdiv, '%': self.builder.srem,
                  '<': 'slt', '>': 'sgt', '<=': 'sle', '>=': 'sge', '==': 'eq', '!=': 'ne',
                  '&&': self.builder.and_, '||': self.builder.or_}
        if node.op in ['+', '-', '*', '/', '%', '&&', '||']:
            return op_map[node.op](lhs, rhs)
        else:
            return self.builder.icmp_signed(op_map[node.op], lhs, rhs)

    def visit_identifier(self, node):
        return self.llvm_var_table[node.name]

    def visit_primary(self, node):
        val_str = node.value
        if val_str.startswith('"'):
            str_val = val_str[1:-1].replace('\\n', '\n') + '\0'
            if str_val not in self.global_strings:
                c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                global_var = ir.GlobalVariable(self.module, c_str.type, name=f".str{len(self.global_strings)}")
                global_var.initializer = c_str
                global_var.global_constant = True
                self.global_strings[str_val] = self.builder.bitcast(global_var, ir.IntType(8).as_pointer())
            return self.global_strings[str_val]
        if val_str.startswith("'"):
            return ir.Constant(ir.IntType(8), ord(val_str[1]))
        if val_str == 'true': return ir.Constant(ir.IntType(1), 1)
        if val_str == 'false': return ir.Constant(ir.IntType(1), 0)
        if '.' in val_str: return ir.Constant(ir.DoubleType(), float(val_str))
        return ir.Constant(ir.IntType(32), int(val_str))

    def visit_subscriptaccess(self, node):
        array_ptr_ptr = self.visit(node.name)
        array_ptr = self.builder.load(array_ptr_ptr)
        index = self.visit(node.key)

        sym_info = self.symbol_table.lookup_symbol(node.name)
        element_type_str = sym_info['type'].base
        element_type = self.get_llvm_type(element_type_str)

        get_func = self.module.get_global("d_array_get")

        temp_alloc = self.builder.alloca(element_type)
        void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())

        self.builder.call(get_func, [array_ptr, index, void_ptr_val])
        return self.builder.load(temp_alloc)

    def visit_functioncall(self, node):
        # Handle array functions separately
        if node.name.startswith("arr_"):
            return self.visit_array_function_call(node)

        func = self.module.get_global(node.name)
        args = [self.visit(arg) for arg in node.args]

        # Coerce loaded values if necessary
        loaded_args = []
        for i, arg in enumerate(args):
            loaded_arg = self._load_if_pointer(arg)
            # Check for type mismatch and coerce (e.g. int to float)
            if i < len(func.args):
                expected_type = func.args[i].type
                if isinstance(expected_type, ir.DoubleType) and isinstance(loaded_arg.type, ir.IntType):
                    loaded_arg = self.builder.sitofp(loaded_arg, expected_type)
            loaded_args.append(loaded_arg)

        return self.builder.call(func, loaded_args)

    def visit_array_function_call(self, node):
        array_node = node.args[0]
        array_ptr = self.builder.load(self.visit(array_node))

        sym_info = self.symbol_table.lookup_symbol(array_node.name)
        element_type_str = sym_info['type'].base

        if node.name == 'arr_size':
            size_func = self.module.get_global("d_array_size")
            return self.builder.call(size_func, [array_ptr])

        if node.name == 'arr_push':
            push_func = self.module.get_global("d_array_push")
            value_to_push = self.visit(node.args[1])
            temp_alloc = self.builder.alloca(value_to_push.type)
            self.builder.store(value_to_push, temp_alloc)
            void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())
            self.builder.call(push_func, [array_ptr, void_ptr_val])
            return

        if node.name == 'arr_pop':
            pop_func = self.module.get_global("d_array_pop")
            element_type = self.get_llvm_type(element_type_str)
            temp_alloc = self.builder.alloca(element_type)
            void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())
            self.builder.call(pop_func, [array_ptr, void_ptr_val])
            return self.builder.load(temp_alloc)

        # Handle contains and indexof with comparison functions
        if node.name in ['arr_contains', 'arr_indexof']:
            c_func = self.module.get_global(f"d_array_{node.name[4:]}")
            cmp_func = self.module.get_global(f"compare_{element_type_str}")

            value_to_find = self.visit(node.args[1])
            temp_alloc = self.builder.alloca(value_to_find.type)
            self.builder.store(value_to_find, temp_alloc)
            void_ptr_val = self.builder.bitcast(temp_alloc, ir.IntType(8).as_pointer())

            return self.builder.call(c_func, [array_ptr, void_ptr_val, cmp_func])

        # Handle avg
        if node.name == 'arr_avg':
            avg_func = self.module.get_global(f"d_array_avg_{element_type_str}")
            return self.builder.call(avg_func, [array_ptr])

        raise NotImplementedError(f"Array function {node.name} not implemented in generator.")

    def visit_ifstatement(self, node):
        cond = self.visit(node.condition)

        then_block = self.current_function.append_basic_block('then')

        if node.else_branch:
            else_block = self.current_function.append_basic_block('else')

        merge_block = self.current_function.append_basic_block('if_cont')

        if node.else_branch:
            self.builder.cbranch(cond, then_block, else_block)
        else:
            self.builder.cbranch(cond, then_block, merge_block)

        self.builder.position_at_end(then_block)
        self.visit(node.then_branch)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        if node.else_branch:
            self.builder.position_at_end(else_block)
            self.visit(node.else_branch)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)

    def visit_returnstatement(self, node):
        if node.value:
            retval = self.visit(node.value)
            self.builder.ret(retval)
        else:
            self.builder.ret_void()

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)

    def visit_systemoutput(self, node):
        output_type_str = node.output_type.type_name.replace('KEYWORD_', '').lower()

        if output_type_str == 'array':
            array_node = node.expression
            array_ptr = self.builder.load(self.visit(array_node))

            sym_info = self.symbol_table.lookup_symbol(array_node.name)
            element_type = sym_info['type'].base

            print_func = self.module.get_global(f"print_{element_type}_array")
            self.builder.call(print_func, [array_ptr])
            return

        value = self.visit(node.expression)
        
        if output_type_str == 'float' and node.precision:
            precision_val = self.visit(node.precision)
            func = self.module.get_global("output_float")
            self.builder.call(func, [value, precision_val])
        else:
            func = self.module.get_global(f"output_{output_type_str}")
            self.builder.call(func, [value])

    # Add other visitor methods as needed (for loops, etc.)
    def visit_whilestatement(self, node):
        loop_header = self.current_function.append_basic_block('loop_header')
        loop_body = self.current_function.append_basic_block('loop_body')
        loop_exit = self.current_function.append_basic_block('loop_exit')

        self.builder.branch(loop_header)
        self.builder.position_at_end(loop_header)

        cond = self.visit(node.condition)
        self.builder.cbranch(cond, loop_body, loop_exit)

        self.builder.position_at_end(loop_body)
        self.visit(node.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header)

        self.builder.position_at_end(loop_exit)
