import llvmlite.ir as ir
import llvmlite.binding as llvm
import traceback
import sys

class IRToLLVMConverter:
    def __init__(self, debug=True):
        self.debug = debug
        self.module = ir.Module(name="main_module")
        self._initialize_llvm()
        
        self.current_function = None
        self.builder = None
        self.var_table = {}
        self.labels = {}
        self.pending_params = []

        self._declare_system_functions()

    def _initialize_llvm(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.module.triple = self.target_machine.triple
        self.module.data_layout = self.target_machine.target_data

    def get_llvm_type(self, type_str):
        if type_str == 'int':
            return ir.IntType(32)
        elif type_str == 'float':
            return ir.DoubleType()
        elif type_str == 'char':
            return ir.IntType(8)
        elif type_str == 'file':
            return ir.IntType(64)
        elif type_str == 'socket':
            return ir.IntType(32)
        elif type_str == 'string':
            # Strings are pointers to char
            return ir.PointerType(ir.IntType(8))
        elif type_str == 'boolean':
            return ir.IntType(1)
        elif type_str == 'void':
            return ir.VoidType()
        else:
            raise ValueError(f"Unknown type: {type_str}")

    def _declare_system_functions(self):
        # input functions
        self.input_int_func = ir.Function(self.module, ir.FunctionType(self.get_llvm_type('int'), []), name="input_int")
        self.input_float_func = ir.Function(self.module, ir.FunctionType(self.get_llvm_type('float'), []), name="input_float")

        # output functions
        self.output_int_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('int')]), name="output_int")
        self.output_float_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('float'), self.get_llvm_type('int')]), name="output_float")
        self.output_string_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('string')]), name="output_string")
        self.output_char_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [self.get_llvm_type('char')]), name="output_char")

        # exit function
        self.exit_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name="exit_program")

        # Math functions
        double_type = self.get_llvm_type('float')
        self.sqrt_func = ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sqrt")
        self.pow_func = ir.Function(self.module, ir.FunctionType(double_type, [double_type, double_type]), name="pie_pow")
        self.sin_func = ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_sin")
        self.cos_func = ir.Function(self.module, ir.FunctionType(double_type, [double_type]), name="pie_cos")

        # String functions
        string_type = self.get_llvm_type('string')
        self.concat_strings_func = ir.Function(self.module, ir.FunctionType(string_type, [string_type, string_type]), name="concat_strings")

        # File functions
        file_type = self.get_llvm_type('file')
        self.file_open_func = ir.Function(self.module, ir.FunctionType(file_type, [string_type, string_type]), name="file_open")
        self.file_close_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type]), name="file_close")
        self.file_write_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type, string_type]), name="file_write")
        self.file_read_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [file_type, string_type, self.get_llvm_type('int')]), name="file_read")

        # Network functions
        socket_type = self.get_llvm_type('socket')
        int_type = self.get_llvm_type('int')
        self.tcp_socket_func = ir.Function(self.module, ir.FunctionType(socket_type, []), name="tcp_socket")
        self.tcp_connect_func = ir.Function(self.module, ir.FunctionType(int_type, [socket_type, string_type, int_type]), name="tcp_connect")
        self.tcp_send_func = ir.Function(self.module, ir.FunctionType(int_type, [socket_type, string_type]), name="tcp_send")
        self.tcp_recv_func = ir.Function(self.module, ir.FunctionType(int_type, [socket_type, string_type, int_type]), name="tcp_recv")
        self.tcp_close_func = ir.Function(self.module, ir.FunctionType(ir.VoidType(), [socket_type]), name="tcp_close")

    def convert_ir(self, ir_code):
        for instr in ir_code:
            op = instr[0]
            method_name = f"handle_{op}"
            if hasattr(self, method_name):
                getattr(self, method_name)(instr)
            else:
                raise ValueError(f"Unsupported IR instruction: {op}")
        return self.finalize()

    def finalize(self):
        llvm_ir = str(self.module)
        if self.debug:
            print("\nGenerated LLVM IR:\n")
            print(llvm_ir)

        try:
            llvm_module = llvm.parse_assembly(llvm_ir)
            llvm_module.verify()
            if self.debug:
                print("Module verification successful!")
            return llvm_ir
        except RuntimeError as e:
            print(f"LLVM Module Validation Error: {e}")
            raise

    def handle_FUNC_START(self, instr):
        _, name, return_type_str, params = instr

        # Correctly handle parameter type mapping
        param_types = []
        if params:
            # Assuming params is a list of tuples (type, name)
            # We need to extract the type string for get_llvm_type
            param_type_strs = [p[0] for p in params]
            param_types = [self.get_llvm_type(p_type) for p_type in param_type_strs]

        return_type = self.get_llvm_type(return_type_str)

        func_type = ir.FunctionType(return_type, param_types)
        self.current_function = ir.Function(self.module, func_type, name=name)

        entry_block = self.current_function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)

        self.var_table = {}
        self.labels = {}

        # Process parameters
        if params:
            for i, (p_type, p_name) in enumerate(params):
                arg = self.current_function.args[i]
                arg.name = p_name
                ptr = self.builder.alloca(self.get_llvm_type(p_type), name=p_name)
                self.builder.store(arg, ptr)
                self.var_table[p_name] = ptr

    def handle_FUNC_END(self, instr):
        if self.builder and not self.builder.block.is_terminated:
            if self.current_function.return_value.type == ir.VoidType():
                self.builder.ret_void()
            else:
                # Default return for non-void functions, e.g., return 0 for int main
                zero = ir.Constant(self.current_function.return_value.type, 0)
                self.builder.ret(zero)
        self.current_function = None
        self.builder = None

    def handle_DECLARE(self, instr):
        _, var_type_str, var_name = instr
        llvm_type = self.get_llvm_type(var_type_str)
        ptr = self.builder.alloca(llvm_type, name=var_name)
        self.var_table[var_name] = ptr

    def handle_DECLARE_ARRAY(self, instr):
        _, element_type_str, name, size = instr
        element_type = self.get_llvm_type(element_type_str)
        array_type = ir.ArrayType(element_type, int(size))
        ptr = self.builder.alloca(array_type, name=name)
        self.var_table[name] = ptr

    def handle_STORE_ARRAY(self, instr):
        _, name, index, value = instr
        ptr = self.var_table[name]
        index_val = self._load_val(str(index))
        val = self._load_val(value)

        addr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), index_val], inbounds=True)
        self.builder.store(val, addr)

    def handle_LOAD_ARRAY(self, instr):
        _, dest, name, index = instr
        ptr = self.var_table[name]
        index_val = self._load_val(str(index))

        addr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), index_val], inbounds=True)
        val = self.builder.load(addr)
        self.var_table[dest] = val

    def handle_ASSIGN(self, instr):
        _, var_name, value = instr
        ptr = self.var_table[var_name]
        val = self._load_val(value)

        # Type casting if necessary
        if ptr.type.pointee != val.type:
            if isinstance(ptr.type.pointee, ir.FloatType) and isinstance(val.type, ir.IntType):
                val = self.builder.sitofp(val, ptr.type.pointee)
            elif isinstance(ptr.type.pointee, ir.IntType) and isinstance(val.type, ir.FloatType):
                val = self.builder.fptosi(val, ptr.type.pointee)

        self.builder.store(val, ptr)

    def handle_BINARY_OP(self, instr):
        _, op, dest, lhs, rhs = instr
        lhs_val = self._load_val(lhs)
        rhs_val = self._load_val(rhs)

        # Type promotion
        if isinstance(lhs_val.type, ir.FloatType) or isinstance(rhs_val.type, ir.FloatType):
            if isinstance(lhs_val.type, ir.IntType):
                lhs_val = self.builder.sitofp(lhs_val, ir.FloatType())
            if isinstance(rhs_val.type, ir.IntType):
                rhs_val = self.builder.sitofp(rhs_val, ir.FloatType())

        op_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'}
        if op in op_map:
            if isinstance(lhs_val.type, ir.FloatType):
                result = getattr(self.builder, f'f{op_map[op]}')(lhs_val, rhs_val, name=dest)
            else: # sdiv for integer division
                op_func = 'sdiv' if op == '/' else op_map[op]
                result = getattr(self.builder, op_func)(lhs_val, rhs_val, name=dest)
        elif op in ['<', '>', '<=', '>=', '==', '!=']:
            if isinstance(lhs_val.type, ir.FloatType):
                result = self.builder.fcmp_ordered(op, lhs_val, rhs_val, name=dest)
            else:
                result = self.builder.icmp_signed(op, lhs_val, rhs_val, name=dest)
        else:
            raise ValueError(f"Unsupported binary operator: {op}")

        self.var_table[dest] = result

    def handle_CONCAT_STRINGS(self, instr):
        _, dest, s1, s2 = instr
        s1_val = self._load_val(s1)
        s2_val = self._load_val(s2)
        result = self.builder.call(self.concat_strings_func, [s1_val, s2_val], name=dest)
        self.var_table[dest] = result

    def handle_UNARY_OP(self, instr):
        _, op, dest, val_name = instr
        val = self._load_val(val_name)
        if op == '-':
            if isinstance(val.type, ir.DoubleType):
                result = self.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), val, name=dest)
            else:
                result = self.builder.sub(ir.Constant(val.type, 0), val, name=dest)
        else:
            raise ValueError(f"Unsupported unary operator: {op}")
        self.var_table[dest] = result

    def handle_PARAM(self, instr):
        _, value = instr
        self.pending_params.append(self._load_val(value))

    def handle_CALL(self, instr):
        _, name, num_args, dest = instr

        func_map = {
            "sqrt": self.sqrt_func,
            "pow": self.pow_func,
            "sin": self.sin_func,
            "cos": self.cos_func,
            "file_open": self.file_open_func,
            "file_close": self.file_close_func,
            "file_write": self.file_write_func,
            "file_read": self.file_read_func,
            "tcp_socket": self.tcp_socket_func,
            "tcp_connect": self.tcp_connect_func,
            "tcp_send": self.tcp_send_func,
            "tcp_recv": self.tcp_recv_func,
            "tcp_close": self.tcp_close_func,
        }

        if name in func_map:
            func = func_map[name]
        else:
            func = self.module.get_global(name)

        if not func:
            raise ValueError(f"Function {name} not found in module")

        args = self.pending_params[-num_args:]
        self.pending_params = self.pending_params[:-num_args]

        # Handle implicit type casting for math functions
        if name in ["sqrt", "pow", "sin", "cos"]:
            new_args = []
            for i, arg in enumerate(args):
                if isinstance(arg.type, ir.IntType):
                    new_args.append(self.builder.sitofp(arg, self.get_llvm_type('float')))
                else:
                    new_args.append(arg)
            args = new_args

        result = self.builder.call(func, args, name=dest)
        self.var_table[dest] = result

    def handle_RETURN(self, instr):
        _, value = instr
        if value is not None:
            ret_val = self._load_val(value)
            self.builder.ret(ret_val)
        else:
            self.builder.ret_void()

    def handle_LABEL(self, instr):
        _, label_name = instr
        if label_name not in self.labels:
            self.labels[label_name] = self.current_function.append_basic_block(name=label_name)

        if not self.builder.block.is_terminated:
            self.builder.branch(self.labels[label_name])

        self.builder.position_at_end(self.labels[label_name])

    def handle_GOTO(self, instr):
        _, label_name = instr
        if label_name not in self.labels:
            self.labels[label_name] = self.current_function.append_basic_block(name=label_name)

        if not self.builder.block.is_terminated:
            self.builder.branch(self.labels[label_name])

    def handle_IF_FALSE(self, instr):
        _, cond, label_name = instr
        cond_val = self._load_val(cond)

        true_block = self.current_function.append_basic_block(name="if_true")
        if label_name not in self.labels:
            self.labels[label_name] = self.current_function.append_basic_block(name=label_name)
        false_block = self.labels[label_name]

        self.builder.cbranch(cond_val, true_block, false_block)
        self.builder.position_at_end(true_block)

    def handle_IF_TRUE(self, instr):
        _, cond, label_name = instr
        cond_val = self._load_val(cond)

        if label_name not in self.labels:
            self.labels[label_name] = self.current_function.append_basic_block(name=label_name)
        true_block = self.labels[label_name]

        false_block = self.current_function.append_basic_block(name="if_false")

        self.builder.cbranch(cond_val, true_block, false_block)
        self.builder.position_at_end(false_block)

    def handle_INPUT(self, instr):
        _, var_name, var_type = instr
        if var_type == 'int':
            val = self.builder.call(self.input_int_func, [])
        elif var_type == 'float':
            val = self.builder.call(self.input_float_func, [])
        else:
            raise ValueError(f"Unsupported input type: {var_type}")

        ptr = self.var_table[var_name]
        self.builder.store(val, ptr)

    def handle_OUTPUT(self, instr):
        _, value, var_type, precision = instr
        val = self._load_val(value)
        if var_type == 'int':
            self.builder.call(self.output_int_func, [val])
        elif var_type == 'float':
            precision_val = self._load_val(precision)
            self.builder.call(self.output_float_func, [val, precision_val])
        elif var_type == 'string':
            self.builder.call(self.output_string_func, [val])
        elif var_type == 'char':
            self.builder.call(self.output_char_func, [val])
        else:
            raise ValueError(f"Unsupported output type: {var_type}")

    def handle_EXIT(self, instr):
        self.builder.call(self.exit_func, [])

    def _load_val(self, name):
        if isinstance(name, str):
            if name in self.var_table:
                # If it's a temporary variable, it's already a value.
                if name.startswith('t'):
                    return self.var_table[name]
                # Otherwise, it's a declared variable, so it's a pointer that needs to be loaded.
                else:
                    return self.builder.load(self.var_table[name])
            
            if name.isdigit() or (name.startswith('-') and name[1:].isdigit()):
                return ir.Constant(ir.IntType(32), int(name))
            if name.lower() == 'true':
                return ir.Constant(ir.IntType(1), 1)
            if name.lower() == 'false':
                return ir.Constant(ir.IntType(1), 0)
            if name.startswith("'") and name.endswith("'"):
                return ir.Constant(ir.IntType(8), ord(name[1]))
            if name.startswith('"'):
                str_val = name[1:-1].replace('\\n', '\n') + '\0'
                c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), bytearray(str_val.encode('utf8')))
                
                # Check if a similar global string already exists
                str_name = f"str_literal.{hash(str_val)}"
                if str_name in self.module.globals:
                    global_str = self.module.globals[str_name]
                else:
                    global_str = ir.GlobalVariable(self.module, c_str.type, name=str_name)
                    global_str.initializer = c_str
                    global_str.global_constant = True
                    global_str.linkage = 'internal'

                return self.builder.bitcast(global_str, self.get_llvm_type('string'))
            try:
                return ir.Constant(ir.DoubleType(), float(name))
            except ValueError:
                pass

        raise ValueError(f"Unknown value to load: {name}")