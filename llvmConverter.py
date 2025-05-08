import llvmlite.ir as ir
import llvmlite.binding as llvm
import traceback
import sys

class IRToLLVMConverter:
    def __init__(self, debug=True):
        self.debug = debug
        self.module = ir.Module(name="main")
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
        
        # Initialize LLVM - this is critical for proper functioning
        self._initialize_llvm()
        
        # Create main function
        int_type = ir.IntType(32)
        func_type = ir.FunctionType(int_type, [])
        self.function = ir.Function(self.module, func_type, name="main")
        self.block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)
        self.var_table = {}  # Maps variable names to alloca pointers
        self.labels = {}     # Maps label names to basic blocks

        # Declare system-defined functions
        self._declare_system_functions()
        
        if self.debug:
            print("Converter initialized successfully")

    def _initialize_llvm(self):
        """Initialize LLVM with proper error handling."""
        try:
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()
            self.target_machine = llvm.Target.from_default_triple().create_target_machine()
            self.module.triple = self.target_machine.triple
            if self.debug:
                print(f"LLVM initialized with target triple: {self.module.triple}")
        except Exception as e:
            print(f"Error initializing LLVM: {e}")
            traceback.print_exc()
            sys.exit(1)

    def _declare_system_functions(self):
        """Declare system-defined functions in the LLVM module."""
        try:
            # void input_float(float* ptr)
            input_float_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.FloatType())])
            self.input_float_func = ir.Function(self.module, input_float_type, name="input_float")

            # void input_int(int* ptr)
            input_int_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(32))])
            self.input_int_func = ir.Function(self.module, input_int_type, name="input_int")

            # void input_string(char* ptr)
            input_string_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
            self.input_string_func = ir.Function(self.module, input_string_type, name="input_string")

            # void input_char(char* ptr)
            input_char_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
            self.input_char_func = ir.Function(self.module, input_char_type, name="input_char")

            # void output_float(float value)
            output_float_type = ir.FunctionType(ir.VoidType(), [ir.FloatType()])
            self.output_float_func = ir.Function(self.module, output_float_type, name="output_float")

            # void output_int(int value)
            output_int_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
            self.output_int_func = ir.Function(self.module, output_int_type, name="output_int")

            # void output_string(const char* value)
            output_string_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
            self.output_string_func = ir.Function(self.module, output_string_type, name="output_string")

            # void output_char(char value)
            output_char_type = ir.FunctionType(ir.VoidType(), [ir.IntType(8)])
            self.output_char_func = ir.Function(self.module, output_char_type, name="output_char")

            # void exit_program()
            exit_type = ir.FunctionType(ir.VoidType(), [])
            self.exit_func = ir.Function(self.module, exit_type, name="exit_program")
            
            if self.debug:
                print("System functions declared successfully")
        except Exception as e:
            print(f"Error declaring system functions: {e}")
            traceback.print_exc()
            sys.exit(1)

    def declare_variable(self, var_type, var_name):
        """Declare a variable in the LLVM IR."""
        try:
            if var_type == 'int':
                llvm_type = ir.IntType(32)
            elif var_type == 'float':
                llvm_type = ir.FloatType()
            elif var_type == 'string':
                llvm_type = ir.ArrayType(ir.IntType(8), 256)  # Fixed-size string buffer
            elif var_type == 'char':
                llvm_type = ir.IntType(8)  # Single character
            elif var_type == 'boolean':
                llvm_type = ir.IntType(1)  # Boolean as 1-bit integer
            else:
                raise ValueError(f"Unsupported type: {var_type}")
                
            # Allocate memory for the variable
            ptr = self.builder.alloca(llvm_type, name=var_name)
            self.var_table[var_name] = ptr
            
            # Initialize with default values
            if var_type == 'int' or var_type == 'char':
                self.builder.store(ir.Constant(llvm_type, 0), ptr)
            elif var_type == 'float':
                self.builder.store(ir.Constant(llvm_type, 0.0), ptr)
            elif var_type == 'boolean':
                self.builder.store(ir.Constant(llvm_type, 0), ptr)  # False
            elif var_type == 'string':
                # Initialize string with empty (all zeros)
                zero = ir.Constant(ir.IntType(8), 0)
                for i in range(256):
                    idx = ir.Constant(ir.IntType(32), i)
                    elem_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), idx])
                    self.builder.store(zero, elem_ptr)
                    
            if self.debug:
                print(f"Declared variable '{var_name}' of type '{var_type}'")
        except Exception as e:
            print(f"Error declaring variable {var_name} of type {var_type}: {e}")
            traceback.print_exc()
            raise

    def assign(self, var_name, value):
        """Assign a value to a variable."""
        try:
            ptr = self.var_table.get(var_name)
            if ptr is None:
                raise ValueError(f"Undeclared variable: {var_name}")

            # Handle special case for char literals
            if isinstance(value, str) and value.startswith("'") and value.endswith("'") and len(value) == 3:
                char_code = ord(value[1])
                self.builder.store(ir.Constant(ir.IntType(8), char_code), ptr)
                if self.debug:
                    print(f"Assigned char '{value[1]}' to '{var_name}'")
                return
                
            # Handle special case for boolean literals
            if isinstance(value, str) and value.lower() in ('true', 'false'):
                bool_val = 1 if value.lower() == 'true' else 0
                self.builder.store(ir.Constant(ir.IntType(1), bool_val), ptr)
                if self.debug:
                    print(f"Assigned boolean {value} to '{var_name}'")
                return

            # Handle string literals
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                if not isinstance(ptr.type.pointee, ir.ArrayType):
                    raise TypeError(f"Cannot assign string to non-string variable {var_name}")
                    
                # Get string content without quotes
                string_content = value[1:-1]
                
                # Store each character in the string array
                for i, char in enumerate(string_content):
                    if i >= 255:  # Respect the 256 byte limit (including null terminator)
                        break
                        
                    idx = ir.Constant(ir.IntType(32), i)
                    elem_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), idx])
                    self.builder.store(ir.Constant(ir.IntType(8), ord(char)), elem_ptr)
                    
                # Add null terminator
                null_idx = ir.Constant(ir.IntType(32), min(len(string_content), 255))
                null_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), null_idx])
                self.builder.store(ir.Constant(ir.IntType(8), 0), null_ptr)
                
                if self.debug:
                    print(f"Assigned string '{string_content}' to '{var_name}'")
                return

            # Handle variable to variable assignment
            if isinstance(value, str) and value in self.var_table:
                src_ptr = self.var_table[value]
                src_type = src_ptr.type.pointee
                dst_type = ptr.type.pointee
                
                # If types match directly
                if src_type == dst_type:
                    if isinstance(src_type, ir.ArrayType):
                        # For arrays (strings), we need to copy element by element
                        array_len = src_type.count
                        for i in range(array_len):
                            idx = ir.Constant(ir.IntType(32), i)
                            src_elem_ptr = self.builder.gep(src_ptr, [ir.Constant(ir.IntType(32), 0), idx])
                            dst_elem_ptr = self.builder.gep(ptr, [ir.Constant(ir.IntType(32), 0), idx])
                            elem_val = self.builder.load(src_elem_ptr)
                            self.builder.store(elem_val, dst_elem_ptr)
                    else:
                        # For scalar types, just load and store
                        val = self.builder.load(src_ptr)
                        self.builder.store(val, ptr)
                else:
                    # Handle type conversions if needed
                    val = self.builder.load(src_ptr)
                    if isinstance(dst_type, ir.FloatType) and isinstance(src_type, ir.IntType):
                        val = self.builder.sitofp(val, ir.FloatType())
                    elif isinstance(dst_type, ir.IntType) and isinstance(src_type, ir.FloatType):
                        val = self.builder.fptosi(val, ir.IntType(32))
                    self.builder.store(val, ptr)
                    
                if self.debug:
                    print(f"Assigned variable '{value}' to '{var_name}'")
                return

            # Handle numerical literals
            try:
                if isinstance(ptr.type.pointee, ir.FloatType):
                    self.builder.store(ir.Constant(ir.FloatType(), float(value)), ptr)
                    if self.debug:
                        print(f"Assigned float {float(value)} to '{var_name}'")
                elif isinstance(ptr.type.pointee, ir.IntType):
                    bit_width = ptr.type.pointee.width
                    self.builder.store(ir.Constant(ir.IntType(bit_width), int(value)), ptr)
                    if self.debug:
                        print(f"Assigned int {int(value)} to '{var_name}'")
                else:
                    raise ValueError(f"Unsupported target type for assignment to {var_name}")
            except ValueError:
                raise ValueError(f"Invalid value for assignment: {value}")
        except Exception as e:
            print(f"Error in assignment {var_name} = {value}: {e}")
            traceback.print_exc()
            raise

    def create_string_literal(self, string_value):
        """Create a global string literal and return a pointer to its first character."""
        try:
            # Add null terminator
            byte_array = bytearray((string_value + '\0').encode("utf-8"))
            const_array = ir.Constant(ir.ArrayType(ir.IntType(8), len(byte_array)), byte_array)
            
            # Create unique name for the global variable
            global_str_name = f"str_{hash(string_value) & 0xFFFFFFFF}"
            global_str = ir.GlobalVariable(self.module, const_array.type, name=global_str_name)
            global_str.linkage = 'private'
            global_str.global_constant = True
            global_str.initializer = const_array
            global_str.unnamed_addr = True
            
            # Get pointer to first byte
            zero = ir.Constant(ir.IntType(32), 0)
            return self.builder.gep(global_str, [zero, zero])
        except Exception as e:
            print(f"Error creating string literal '{string_value}': {e}")
            traceback.print_exc()
            raise

    def binary_op(self, op, dest, lhs, rhs):
        """Generate LLVM IR for binary operations."""
        try:
            lhs_val = self._load_val(lhs)
            rhs_val = self._load_val(rhs)

            # Type conversion for mixed types
            if lhs_val.type != rhs_val.type:
                if isinstance(lhs_val.type, ir.IntType) and isinstance(rhs_val.type, ir.FloatType):
                    lhs_val = self.builder.sitofp(lhs_val, ir.FloatType())
                    if self.debug:
                        print(f"Converted LHS {lhs} from int to float")
                elif isinstance(lhs_val.type, ir.FloatType) and isinstance(rhs_val.type, ir.IntType):
                    rhs_val = self.builder.sitofp(rhs_val, ir.FloatType())
                    if self.debug:
                        print(f"Converted RHS {rhs} from int to float")

            # Handle logical AND (&&) and OR (||)
            if op == '&&':
                # Create blocks for short-circuiting
                and_true_block = self.function.append_basic_block(name="and_true")
                and_end_block = self.function.append_basic_block(name="and_end")

                # Check LHS
                if not self.builder.block.is_terminated:
                    self.builder.cbranch(lhs_val, and_true_block, and_end_block)

                # In the true block, check RHS
                self.builder.position_at_end(and_true_block)
                if not self.builder.block.is_terminated:
                    self.builder.cbranch(rhs_val, and_end_block, and_end_block)

                # In the end block, create the result
                self.builder.position_at_end(and_end_block)
                result = self.builder.phi(ir.IntType(1))
                result.add_incoming(ir.Constant(ir.IntType(1), 0), self.builder.block)  # False
                result.add_incoming(ir.Constant(ir.IntType(1), 1), and_true_block)  # True

            elif op == '||':
                # Create blocks for short-circuiting
                or_false_block = self.function.append_basic_block(name="or_false")
                or_end_block = self.function.append_basic_block(name="or_end")

                # Check LHS
                self.builder.cbranch(lhs_val, or_end_block, or_false_block)

                # In the false block, check RHS
                self.builder.position_at_end(or_false_block)
                self.builder.cbranch(rhs_val, or_end_block, or_end_block)

                # In the end block, create the result
                self.builder.position_at_end(or_end_block)
                result = self.builder.phi(ir.IntType(1))
                result.add_incoming(ir.Constant(ir.IntType(1), 1), self.builder.block)  # True
                result.add_incoming(ir.Constant(ir.IntType(1), 0), or_false_block)  # False

            else:
                # Handle other binary operations
                if op == '+':
                    result = self.builder.fadd(lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.add(lhs_val, rhs_val)
                elif op == '-':
                    result = self.builder.fsub(lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.sub(lhs_val, rhs_val)
                elif op == '*':
                    result = self.builder.fmul(lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.mul(lhs_val, rhs_val)
                elif op == '/':
                    result = self.builder.fdiv(lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.sdiv(lhs_val, rhs_val)
                elif op == '>':
                    result = self.builder.fcmp_ordered('>', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('>', lhs_val, rhs_val)
                elif op == '==':
                    result = self.builder.fcmp_ordered('==', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('==', lhs_val, rhs_val)
                elif op == '>=':
                    result = self.builder.fcmp_ordered('>=', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('>=', lhs_val, rhs_val)
                elif op == '<':
                    result = self.builder.fcmp_ordered('<', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('<', lhs_val, rhs_val)
                elif op == '<=':
                    result = self.builder.fcmp_ordered('<=', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('<=', lhs_val, rhs_val)
                elif op == '!=':
                    result = self.builder.fcmp_ordered('!=', lhs_val, rhs_val) if isinstance(lhs_val.type, ir.FloatType) else self.builder.icmp_signed('!=', lhs_val, rhs_val)
                else:
                    raise ValueError(f"Unsupported binary op: {op}")

            # Store the result in the destination variable if needed
            if dest not in self.var_table:
                # Create a temporary variable for the result
                if isinstance(result.type, ir.IntType) and result.type.width == 1:
                    # Boolean result from comparison
                    result_ptr = self.builder.alloca(ir.IntType(1), name=dest)
                elif isinstance(result.type, ir.IntType):
                    result_ptr = self.builder.alloca(ir.IntType(32), name=dest)
                elif isinstance(result.type, ir.FloatType):
                    result_ptr = self.builder.alloca(ir.FloatType(), name=dest)
                else:
                    result_ptr = self.builder.alloca(result.type, name=dest)
                
                self.var_table[dest] = result_ptr
                self.builder.store(result, result_ptr)
            else:
                # Store directly in existing variable
                result_ptr = self.var_table[dest]
                if isinstance(result.type, ir.IntType) and result.type.width == 1 and isinstance(result_ptr.type.pointee, ir.IntType) and result_ptr.type.pointee.width > 1:
                    # Convert boolean to int if needed
                    result = self.builder.zext(result, result_ptr.type.pointee)
                elif isinstance(result.type, ir.IntType) and isinstance(result_ptr.type.pointee, ir.FloatType):
                    # Convert int to float if needed
                    result = self.builder.sitofp(result, ir.FloatType())
                
                self.builder.store(result, result_ptr)
                
            if self.debug:
                print(f"Performed binary op: {lhs} {op} {rhs} -> {dest}")
        except Exception as e:
            print(f"Error in binary op {lhs} {op} {rhs} -> {dest}: {e}")
            traceback.print_exc()
            raise

    def system_input(self, var_name, data_type):
        """Generate LLVM IR for the input system function."""
        try:
            ptr = self.var_table.get(var_name)
            if ptr is None:
                raise ValueError(f"Undeclared variable: {var_name}")

            if data_type == 'float':
                self.builder.call(self.input_float_func, [ptr])
            elif data_type == 'int':
                self.builder.call(self.input_int_func, [ptr])
            elif data_type == 'string':
                str_ptr = self.builder.bitcast(ptr, ir.PointerType(ir.IntType(8)))  # Cast to i8*
                self.builder.call(self.input_string_func, [str_ptr])
            elif data_type == 'char':
                char_ptr = self.builder.bitcast(ptr, ir.PointerType(ir.IntType(8)))  # Cast to i8*
                self.builder.call(self.input_char_func, [char_ptr])
            else:
                raise ValueError(f"Unsupported input type: {data_type}")
                
            if self.debug:
                print(f"Generated input for {var_name} of type {data_type}")
        except Exception as e:
            print(f"Error in system_input for {var_name} of type {data_type}: {e}")
            traceback.print_exc()
            raise

    def system_output(self, value, data_type):
        """Generate LLVM IR for the output system function."""
        try:
            if data_type == 'string':
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    # Handle string literals
                    str_content = value.strip('"')
                    str_ptr = self.create_string_literal(str_content)
                    self.builder.call(self.output_string_func, [str_ptr])
                    if self.debug:
                        print(f"Generated output for string literal: {str_content}")
                else:
                    # Handle string variables
                    if value in self.var_table:
                        ptr = self.var_table[value]
                        # For string variables, we need to bitcast the array pointer to i8*
                        str_ptr = self.builder.bitcast(ptr, ir.PointerType(ir.IntType(8)))
                        self.builder.call(self.output_string_func, [str_ptr])
                        if self.debug:
                            print(f"Generated output for string variable: {value}")
                    else:
                        raise ValueError(f"Unknown string variable: {value}")
            elif data_type == 'float' or data_type == 'int' or data_type == 'char':
                val = self._load_val(value)
                if data_type == 'float':
                    self.builder.call(self.output_float_func, [val])
                elif data_type == 'int':
                    self.builder.call(self.output_int_func, [val])
                elif data_type == 'char':
                    self.builder.call(self.output_char_func, [val])
                if self.debug:
                    print(f"Generated output for {data_type} value: {value}")
            else:
                raise ValueError(f"Unsupported output type: {data_type}")
        except Exception as e:
            print(f"Error in system_output for {value} of type {data_type}: {e}")
            traceback.print_exc()
            raise

    def system_exit(self):
        """Generate LLVM IR for the exit system function."""
        try:
            self.builder.call(self.exit_func, [])
            if self.debug:
                print("Generated exit call")
        except Exception as e:
            print(f"Error in system_exit: {e}")
            traceback.print_exc()
            raise

    def handle_label(self, label_name):
        """Handle a label in the IR."""
        try:
            # If the label already exists, just branch to it
            if label_name in self.labels:
                if not self.builder.block.is_terminated:
                    self.builder.branch(self.labels[label_name])
                    if self.debug:
                        print(f"Branched to existing label: {label_name}")
            else:
                # Create a new basic block for this label
                self.labels[label_name] = self.function.append_basic_block(name=label_name)
                if not self.builder.block.is_terminated:
                    self.builder.branch(self.labels[label_name])
                    if self.debug:
                        print(f"Created and branched to new label: {label_name}")
            
            # Position the builder at the end of the label's block
            self.builder.position_at_end(self.labels[label_name])

            # Ensure the block is not empty by adding a placeholder instruction
            if not self.builder.block.is_terminated:
                self.builder.unreachable()  # Add an unreachable instruction as a placeholder
        except Exception as e:
            print(f"Error handling label {label_name}: {e}")
            traceback.print_exc()
            raise

    def handle_if_false(self, condition, label_name):
        """Handle an IF_FALSE instruction."""
        try:
            # Load the condition value
            cond_val = self._load_val(condition)
            
            # Get or create the false block
            if label_name not in self.labels:
                self.labels[label_name] = self.function.append_basic_block(name=label_name)
            false_block = self.labels[label_name]
            
            # Create the next block for the true branch
            next_block = self.function.append_basic_block(name="next")
            
            # Add the conditional branch if the current block is not terminated
            if not self.builder.block.is_terminated:
                self.builder.cbranch(cond_val, next_block, false_block)
                if self.debug:
                    print(f"Added conditional branch for condition {condition} to label {label_name}")
            
            # Position the builder at the end of the next block
            self.builder.position_at_end(next_block)
        except Exception as e:
            print(f"Error in if_false for condition {condition} to label {label_name}: {e}")
            traceback.print_exc()
            raise

    def _load_val(self, name):
        """Load a value (variable or constant) into LLVM IR."""
        try:
            # Check if the value is a variable
            if name in self.var_table:
                return self.builder.load(self.var_table[name], name=name)
            
            # Handle integer literals
            if name.isdigit():
                return ir.Constant(ir.IntType(32), int(name))
            
            # Handle float literals
            try:
                float_val = float(name)
                return ir.Constant(ir.FloatType(), float_val)
            except ValueError:
                pass
            
            # Handle boolean literals
            if name.lower() == "true":
                return ir.Constant(ir.IntType(1), 1)  # Boolean true as 1-bit integer
            if name.lower() == "false":
                return ir.Constant(ir.IntType(1), 0)  # Boolean false as 1-bit integer
            
            # Handle character literals
            if name.startswith("'") and name.endswith("'") and len(name) == 3:
                return ir.Constant(ir.IntType(8), ord(name[1]))
            
            # Handle string literals
            if name.startswith('"') and name.endswith('"'):
                return self.create_string_literal(name[1:-1])
            
            # If the value is not recognized, raise an error
            raise ValueError(f"Unknown value: {name}")
        except Exception as e:
            print(f"Error loading value {name}: {e}")
            traceback.print_exc()
            raise

    def finalize(self):
        """Finalize the LLVM module."""
        try:
            # Ensure the function returns 0 if it doesn't have a return already
            if not self.builder.block.is_terminated:
                self.builder.ret(ir.Constant(ir.IntType(32), 0))
                if self.debug:
                    print("Added implicit return 0")
            
            # Validate the module
            llvm_ir = str(self.module)
            
            # Print the IR for debugging
            if self.debug:
                print("\nGenerated LLVM IR:\n")
                print(llvm_ir)
            
            # Verify the module
            try:
                llvm_module = llvm.parse_assembly(llvm_ir)
                llvm_module.verify()
                if self.debug:
                    print("Module verification successful!")
            except RuntimeError as e:
                print(f"LLVM Module Validation Error: {e}")
                raise ValueError(f"LLVM Module Validation Error: {e}")
            
            return llvm_ir
        except Exception as e:
            print(f"Error in finalize: {e}")
            traceback.print_exc()
            raise

    def convert_ir(self, ir_code):
        """Convert the IR code to LLVM IR."""
        try:
            if self.debug:
                print(f"Starting conversion of {len(ir_code)} IR instructions")
                
            # Validate IR code format
            if not isinstance(ir_code, list):
                raise ValueError("IR code must be a list of instructions")
                
            for i, instr in enumerate(ir_code):
                if not instr:  # Skip empty instructions
                    continue
                
                if self.debug:
                    print(f"Processing instruction {i}: {instr}")
                    
                if not isinstance(instr, (list, tuple)):
                    raise ValueError(f"Invalid instruction format at index {i}: {instr}")
                
                if len(instr) == 0:
                    raise ValueError(f"Empty instruction at index {i}")
                    
                op = instr[0]
                    
                if op == 'START_PROGRAM':
                    if self.debug:
                        print("START_PROGRAM - no action needed")
                    continue  # No action needed for START_PROGRAM
                elif op == 'END_PROGRAM':
                    if len(instr) != 1:
                        raise ValueError(f"Invalid END_PROGRAM instruction at index {i}: {instr}")
                    self.system_exit()
                    if self.debug:
                        print("Generated end program")
                elif op == 'DECLARE':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid DECLARE instruction at index {i}: {instr}")
                    _, var_type, var_name = instr
                    self.declare_variable(var_type, var_name)
                    if self.debug:
                        print(f"Declared variable {var_name} of type {var_type}")
                elif op == 'RETURN':
                    if len(instr) > 1 and instr[1] is not None:
                        return_val = self._load_val(instr[1])
                        # If return value is not an i32, convert it
                        if isinstance(return_val.type, ir.FloatType):
                            return_val = self.builder.fptosi(return_val, ir.IntType(32))
                        elif isinstance(return_val.type, ir.IntType) and return_val.type.width != 32:
                            if return_val.type.width < 32:
                                return_val = self.builder.sext(return_val, ir.IntType(32))
                            else:
                                return_val = self.builder.trunc(return_val, ir.IntType(32))
                        self.builder.ret(return_val)
                        if self.debug:
                            print(f"Generated return with value {instr[1]}")
                    else:
                        # Return 0 by default
                        self.builder.ret(ir.Constant(ir.IntType(32), 0))
                        if self.debug:
                            print("Generated default return 0")
                elif op == 'BINARY_OP':
                    if len(instr) != 5:
                        raise ValueError(f"Invalid BINARY_OP instruction at index {i}: {instr}")
                    _, op_type, dest, lhs, rhs = instr
                    self.binary_op(op_type, dest, lhs, rhs)
                elif op == 'INPUT':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid INPUT instruction at index {i}: {instr}")
                    _, var_name, data_type = instr
                    self.system_input(var_name, data_type)
                elif op == 'OUTPUT':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid OUTPUT instruction at index {i}: {instr}")
                    _, value, data_type = instr
                    self.system_output(value, data_type)
                elif op == 'ASSIGN':
                    if len(instr) < 3 or len(instr) > 4:
                        raise ValueError(f"Invalid ASSIGN instruction at index {i}: {instr}")
                    _, var_name, value = instr[:3]  # Extract the first three components
                    self.assign(var_name, value)
                
                elif op == 'STRING_LITERAL':
                    if len(instr) != 2:
                        raise ValueError(f"Invalid STRING_LITERAL instruction at index {i}: {instr}")
                    _, string_value = instr
                    self.create_string_literal(string_value)
                elif op == 'SYSTEM_EXIT':
                    if len(instr) != 1:
                        raise ValueError(f"Invalid SYSTEM_EXIT instruction at index {i}: {instr}")
                    self.system_exit()
                    if self.debug:
                        print("Generated system exit")
                elif op == 'SYSTEM_INPUT':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid SYSTEM_INPUT instruction at index {i}: {instr}")
                    _, var_name, data_type = instr
                    self.system_input(var_name, data_type)
                    if self.debug:
                        print(f"Generated system input for {var_name} of type {data_type}")
                elif op == 'SYSTEM_OUTPUT':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid SYSTEM_OUTPUT instruction at index {i}: {instr}")
                    _, value, data_type = instr
                    self.system_output(value, data_type)
                    if self.debug:
                        print(f"Generated system output for {value} of type {data_type}")
                elif op == 'EXIT':
                    self.system_exit()
                    # Add an unreachable instruction after EXIT
                    self.builder.unreachable()
                    if self.debug:
                        print("Generated exit with unreachable")
                elif op == 'LABEL':
                    if len(instr) != 2:
                        raise ValueError(f"Invalid LABEL instruction at index {i}: {instr}")
                    _, label_name = instr
                    self.handle_label(label_name)
                elif op == 'IF_FALSE':
                    if len(instr) != 3:
                        raise ValueError(f"Invalid IF_FALSE instruction at index {i}: {instr}")
                    _, condition, label_name = instr
                    self.handle_if_false(condition, label_name)
                elif op == 'GOTO':
                    if len(instr) != 2:
                        raise ValueError(f"Invalid GOTO instruction at index {i}: {instr}")
                    _, label_name = instr
                    self.handle_label(label_name)
                else:
                    raise ValueError(f"Unsupported instruction: {op} at index {i}")
                    
            # Finalize and return the generated LLVM IR
            return self.finalize()
        except Exception as e:
            print(f"Error during IR conversion: {e}")
            traceback.print_exc()
            raise