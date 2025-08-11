import llvmlite.ir as ir
import llvmlite.binding as llvm
from frontend.visitor import Visitor
from frontend.ast import Declaration, FunctionDefinition, FunctionCall

class LLVMCodeGenerator(Visitor):
    def __init__(self, symbol_table, debug=True):
        self.debug = debug
        self.symbol_table = symbol_table
        self.module = ir.Module(name="main_module")
        self._initialize_llvm()

        self.current_function = None
        self.builder = None
        # This table will map variable names to their LLVM pointer values
        self.llvm_var_table = {}
        self.global_strings = {}
        # Track global variables
        self.global_vars = {}

        # Define custom types (structs)
        self._define_structs()

        # Declare all the external C functions we will call
        self._declare_runtime_functions()

    def _initialize_llvm(self):
        llvm.initialize()
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
        elif type_str == 'boolean':
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
        elif type_str == 'dict':
            return self.dict_type
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

        # Math Library
        double_type = self.get_llvm_type('float')
        int_type = self.get_llvm_type('int')
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sqrt")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type, double_type]), name="pie_pow")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sin")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_cos")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_floor")
        ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_ceil")
        ir.Function(self.module, ir.FunctionType(int_type, []), name="pie_rand")

        # String Library
        string_type = self.get_llvm_type('string')
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="concat_strings")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type]), name="pie_strlen")
        ir.Function(self.module, ir.FunctionType(int_type, [string_type, string_type]), name="pie_strcmp")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="pie_strcpy")
        ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="pie_strcat")

        # File I/O Library
        file_type = self.get_llvm_type('file')
        ir.Function(self.module, ir.FunctionType(file_type, [string_type, string_type]), name="file_open")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type]), name="file_close")
        ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type, string_type]), name="file_write")
        ir.Function(self.module, ir.FunctionType(string_type, [file_type]), name="file_read_all")
        ir.Function(self.module, ir.FunctionType(string_type, [file_type]), name="file_read_line")

        # Network Library (if needed)
        # ir.Function(self.module, ir.FunctionType(...), name="...")

        # Dictionary, etc. would be declared here too...
        # (Keeping it concise for this example)


    def generate(self, ast):
        """Generate LLVM IR from the AST."""
        # First pass: declare global variables and function definitions only
        for stmt in ast.statements:
            if isinstance(stmt, (Declaration, FunctionDefinition)):
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
            
            # First, handle global variable initializations that involve function calls
            for stmt in ast.statements:
                if isinstance(stmt, Declaration) and stmt.initializer:
                    # Check if initializer is a function call
                    if isinstance(stmt.initializer, FunctionCall):  # FunctionCall
                        var_name = stmt.identifier
                        if var_name in self.global_vars:
                            # Evaluate the function call and store in the global variable
                            init_val = self.visit(stmt.initializer)
                            self.builder.store(init_val, self.global_vars[var_name])
            
            # Then visit all non-declaration, non-function-definition statements
            for stmt in ast.statements:
                if not isinstance(stmt, (Declaration, FunctionDefinition)):
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

    def visit_block(self, node):
        # Each block has its own symbol table scope, managed by the semantic analyzer.
        # Here, we just visit the statements within the block.
        for stmt in node.statements:
            self.visit(stmt)

    def visit_functiondefinition(self, node):
        # 1. Get function type from symbol table (or construct it)
        func_symbol = self.symbol_table.lookup_function(node.name)
        return_type = self.get_llvm_type(func_symbol['return_type'])
        param_types = [self.get_llvm_type(pt) for pt in func_symbol['param_types']]
        func_type = ir.FunctionType(return_type, param_types)

        # 2. Declare the function in the module
        self.current_function = ir.Function(self.module, func_type, name=node.name)

        # 3. Create entry block and IR builder
        entry_block = self.current_function.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(entry_block)

        # 4. Allocate space for parameters and store their initial values
        self.llvm_var_table.clear() # Clear vars for new function scope
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
            if node.initializer:
                # For global variables, we need to evaluate the initializer to get a constant
                init_val = self._evaluate_constant_expression(node.initializer)
                initializer = init_val
            else:
                # Default initialization
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
        else:
            # Local variable declaration (inside a function)
            ptr = self.builder.alloca(var_type, name=var_name)
            self.llvm_var_table[var_name] = ptr

            # If there's an initializer, visit it and store its value
            if node.initializer:
                init_val = self.visit(node.initializer)
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
        
        # For function calls and other expressions, we'll need more sophisticated handling
        # For now, return a default value
        return ir.Constant(ir.IntType(64), 0)  # file type default

    def visit_arraydeclaration(self, node):
        var_name = node.identifier
        element_type = self.get_llvm_type(node.var_type.type_name)

        if node.is_dynamic:
            # Dynamic arrays are pointers to a struct. We just allocate the pointer.
            # The actual struct is created by a runtime function call.
            array_ptr_type = self.get_llvm_type(f'd_array_{node.var_type.type_name.lower()}')
            ptr = self.builder.alloca(array_ptr_type, name=var_name)
            self.llvm_var_table[var_name] = ptr
            # Initialization of dynamic arrays is handled by function calls
            if node.initializer:
                # This would typically involve calling an `array_create` and then `array_append` for each element.
                # This logic will be in the visit_functioncall for those specific functions.
                pass # For now, assume initialization is handled elsewhere
        else:
            # Static arrays
            size = int(node.size.value) # Assumes size is a primary int literal
            array_type = ir.ArrayType(element_type, size)
            ptr = self.builder.alloca(array_type, name=var_name)
            self.llvm_var_table[var_name] = ptr

            if node.initializer:
                init_vals = [self.visit(expr) for expr in node.initializer.values]
                for i, val in enumerate(init_vals):
                    index_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)])
                    self.builder.store(val, index_ptr)

    def visit_assignment(self, node):
        # The visit method for the LHS (l-value) should return a pointer.
        ptr = self.visit(node.lhs)
        # The visit method for the RHS (r-value) should return a value.
        value_to_store = self.visit(node.rhs)

        # Before storing, we might need to cast the value to the pointer's element type
        target_type = ptr.type.pointee if hasattr(ptr.type, 'pointee') else ptr.type.pointed_type
        if target_type != value_to_store.type:
             if isinstance(target_type, ir.DoubleType) and isinstance(value_to_store.type, ir.IntType):
                 value_to_store = self.builder.sitofp(value_to_store, target_type)
             # Add other casting logic as needed

        self.builder.store(value_to_store, ptr)

    def visit_returnstatement(self, node):
        if node.value:
            return_val = self.visit(node.value)
            self.builder.ret(return_val)
        else:
            self.builder.ret_void()

    def _load_if_pointer(self, value):
        """Loads a value if it's a pointer, otherwise returns the value directly."""
        if isinstance(value.type, ir.PointerType):
            # Check if it's a string constant/literal - don't load it
            if (value.type.pointee == ir.IntType(8) and 
                hasattr(value, 'name') and 
                (value.name.startswith('.str') or 
                 str(value).startswith('bitcast') or
                 str(value).startswith('getelementptr'))):
                return value
            # For other pointer types (variables), load the value
            return self.builder.load(value)
        return value

    def visit_binaryop(self, node):
        # Visiting an expression node should yield a value (r-value).
        # If the operand is an identifier or subscript, visiting it will return a
        # pointer (l-value), so we must load it.
        lhs = self._load_if_pointer(self.visit(node.left))
        rhs = self._load_if_pointer(self.visit(node.right))

        # String concatenation check first
        if node.op == '+':
            # Check if both operands are string pointers (i8*)
            if (isinstance(lhs.type, ir.PointerType) and 
                isinstance(rhs.type, ir.PointerType) and
                lhs.type.pointee == ir.IntType(8) and 
                rhs.type.pointee == ir.IntType(8)):
                concat_func = self.module.get_global("concat_strings")
                return self.builder.call(concat_func, [lhs, rhs], 'concat_tmp')

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

    def visit_primary(self, node):
        val = node.value
        if isinstance(val, str):
            # Check for integer literals first
            if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                return ir.Constant(ir.IntType(32), int(val))
            # Check for float literals
            try:
                if '.' in val and not val.startswith('"'):
                    return ir.Constant(ir.DoubleType(), float(val))
            except ValueError:
                pass
            # Boolean literals
            if val == 'true':
                return ir.Constant(ir.IntType(1), 1)
            if val == 'false':
                return ir.Constant(ir.IntType(1), 0)
            # String literals
            if val.startswith('"') and val.endswith('"'):
                str_val = val[1:-1].replace('\\n', '\n') + '\0'
                if str_val in self.global_strings:
                    ptr = self.global_strings[str_val]
                else:
                    c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode("utf8")))
                    global_var = ir.GlobalVariable(self.module, c_str.type, name=f".str{len(self.global_strings)}")
                    global_var.initializer = c_str
                    global_var.global_constant = True
                    global_var.linkage = 'internal'
                    
                    if self.builder:
                        # We have a builder, so we can create a bitcast
                        ptr = self.builder.bitcast(global_var, ir.IntType(8).as_pointer())
                    else:
                        # No builder, return a GEP to get the pointer
                        ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                    
                    self.global_strings[str_val] = ptr
                return ptr
            # Character literals
            if val.startswith("'") and val.endswith("'") and len(val) == 3:
                return ir.Constant(ir.IntType(8), ord(val[1]))
        raise Exception(f"Unknown primary value: {val}")

    def visit_identifier(self, node):
        # An identifier can be an l-value (its pointer) or an r-value (its loaded value).
        # The calling context (e.g., visit_assignment vs. visit_binaryop) determines
        # whether to load the value. Here, we return the pointer.
        if node.name in self.llvm_var_table:
            return self.llvm_var_table[node.name]
        else:
            raise Exception(f"Unknown variable referenced: {node.name}")

    def visit_subscriptaccess(self, node):
        # A subscript access is an l-value, so it should return a pointer.
        array_ptr = self.llvm_var_table[node.name]
        key_val = self._load_if_pointer(self.visit(node.key))
        # GEP (Get Element Pointer) instruction
        return self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), key_val], inbounds=True)

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)

    def visit_functioncall(self, node):
        func = self.module.get_global(node.name)
        if func is None:
            raise Exception(f"Unknown function referenced: {node.name}")

        args = [self._load_if_pointer(self.visit(arg)) for arg in node.args]

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

    # visit_switchstatement and others would follow a similar pattern
    # of creating blocks and using branching instructions.
    def visit_systemoutput(self, node):
        output_val = self._load_if_pointer(self.visit(node.expression))
        output_type = node.output_type.type_name.replace('KEYWORD_', '').lower()

        func_name = f"output_{output_type}"
        output_func = self.module.get_global(func_name)

        if not output_func:
            raise Exception(f"Runtime function {func_name} not found.")

        args = [output_val]
        if output_type == 'float':
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
