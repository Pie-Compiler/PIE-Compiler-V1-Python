"""
Main LLVM Generator

This module provides the main LLVM code generator that orchestrates all components.
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
from frontend.visitor import Visitor
from frontend.ast import Declaration, FunctionDefinition, FunctionCall, SubscriptAccess, ArrayDeclaration
from frontend.types import TypeInfo
from typing import Optional, Any

from .context import LLVMContext
from .type_manager import TypeManager
from .runtime_manager import RuntimeFunctionManager
from .expression_generator import ExpressionGenerator
from .control_flow_generator import ControlFlowGenerator


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
        
        # Set up cross-references for components that need to call visit methods
        self.expression_generator.generator = self
        self.control_flow_generator.generator = self
    
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
            
            self.context.clear_function_scope()
    
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
    
    # ============================================================================
    # Visitor Methods - Delegating to appropriate components
    # ============================================================================
    
    def visit_binaryop(self, node):
        """Visit binary operation node."""
        left_val = self._load_if_pointer(self.visit(node.left))
        right_val = self._load_if_pointer(self.visit(node.right))
        
        return self.expression_generator.generate_binary_operation(node, left_val, right_val, node.op)
    
    def visit_unaryop(self, node):
        """Visit unary operation node."""
        operand_val = self._load_if_pointer(self.visit(node.operand))
        return self.expression_generator.generate_unary_operation(node, operand_val, node.op)
    
    def visit_primary(self, node):
        """Visit primary expression node."""
        return self.expression_generator.generate_primary(node)
    
    def visit_functioncall(self, node):
        """Visit function call node."""
        return self.expression_generator.generate_function_call(node)
    
    def visit_ifstatement(self, node):
        """Visit if statement node."""
        self.control_flow_generator.generate_if_statement(node)
    
    def visit_whilestatement(self, node):
        """Visit while statement node."""
        self.control_flow_generator.generate_while_statement(node)
    
    def visit_forstatement(self, node):
        """Visit for statement node."""
        self.control_flow_generator.generate_for_statement(node)
    
    def visit_switchstatement(self, node):
        """Visit switch statement node."""
        self.control_flow_generator.generate_switch_statement(node)
    
    # ============================================================================
    # Additional visitor methods would be implemented here...
    # This is a simplified version showing the modular structure
    # ============================================================================
    
    def visit_program(self, node):
        """Handle program nodes."""
        # This method is called from the old code path, but we handle program generation differently now
        # Just pass through to avoid issues
        pass
    
    def visit_block(self, node):
        """Handle block statements."""
        # Each block has its own symbol table scope, managed by the semantic analyzer.
        # Here, we just visit the statements within the block.
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_functiondefinition(self, node):
        """Handle function definitions."""
        # 1. Get function type from symbol table (or construct it)
        func_symbol = self.symbol_table.lookup_function(node.name)
        return_type = self.type_manager.get_llvm_type(func_symbol['return_type'])
        param_types = [self.type_manager.get_llvm_type(pt) for pt in func_symbol['param_types']]
        func_type = ir.FunctionType(return_type, param_types)

        # 2. Declare the function in the module
        self.context.current_function = ir.Function(self.context.module, func_type, name=node.name)

        # 3. Create entry block and IR builder
        entry_block = self.context.current_function.append_basic_block(name='entry')
        self.context.builder = ir.IRBuilder(entry_block)

        # 4. Allocate space for parameters and store their initial values
        self.context.llvm_var_table.clear() # Clear vars for new function scope
        for i, arg in enumerate(self.context.current_function.args):
            param_name = func_symbol['params'][i][1]
            arg.name = param_name

            # Allocate space for the parameter on the stack
            ptr = self.context.builder.alloca(param_types[i], name=param_name)
            # Store the argument's value in the allocated space
            self.context.builder.store(arg, ptr)
            # Add the pointer to our variable table
            self.context.llvm_var_table[param_name] = ptr

        # 5. Visit the function body
        self.visit(node.body)

        # 6. Add a return statement if one is missing
        if not self.context.builder.block.is_terminated:
            if return_type == ir.VoidType():
                self.context.builder.ret_void()
            else:
                # Default return for non-void functions (e.g., return 0 for int main)
                zero = ir.Constant(return_type, 0)
                self.context.builder.ret(zero)

        # 7. Clean up for the next function
        self.context.current_function = None
        self.context.builder = None
    
    def visit_declaration(self, node):
        """Handle variable declarations."""
        var_name = node.identifier
        var_type = self.type_manager.get_llvm_type(node.var_type.type_name)

        if self.context.builder is None:
            # Global variable declaration
            if node.initializer and not self._is_function_call_initializer(node.initializer):
                # For global variables with constant initializers, evaluate to get a constant
                try:
                    init_val = self._evaluate_constant_expression(node.initializer)
                    initializer = init_val
                except Exception:
                    # If we can't evaluate at compile time, use default initialization
                    initializer = self._get_default_initializer(var_type)
                    # Defer the initialization for later processing
                    self.context.deferred_initializers.append((node.identifier, node.initializer))
            else:
                # Default initialization (used for function call initializers too)
                initializer = self._get_default_initializer(var_type)
                
                # If this has a function call initializer, defer it for later processing
                if node.initializer and self._is_function_call_initializer(node.initializer):
                    self.context.deferred_initializers.append((node.identifier, node.initializer))

            # Create global variable
            global_var = ir.GlobalVariable(self.context.module, var_type, name=var_name)
            global_var.initializer = initializer
            global_var.linkage = 'internal'
            
            # Store reference for later use
            self.context.global_vars[var_name] = global_var
            self.context.llvm_var_table[var_name] = global_var
        else:
            # Local variable declaration (inside a function)
            ptr = self.context.builder.alloca(var_type, name=var_name)
            self.context.llvm_var_table[var_name] = ptr

            # If there's an initializer, visit it and store its value
            if node.initializer:
                init_val = self.visit(node.initializer)
                self.context.builder.store(init_val, ptr)
    
    def visit_returnstatement(self, node):
        """Handle return statements."""
        if node.value:
            ret_val = self.visit(node.value)
            self.context.builder.ret(ret_val)
        else:
            self.context.builder.ret_void()
    
    def visit_identifier(self, node):
        """Handle identifier references."""
        var_name = node.name
        if var_name in self.context.llvm_var_table:
            return self.context.llvm_var_table[var_name]
        else:
            raise Exception(f"Undefined variable: {var_name}")
    
    def visit_binaryop(self, node):
        """Handle binary operations by delegating to the expression generator."""
        return self.expression_generator.generate_binary_operation(node)
    
    def visit_unaryop(self, node):
        """Handle unary operations by delegating to the expression generator."""
        return self.expression_generator.generate_unary_operation(node)
    
    def visit_primary(self, node):
        """Handle primary expressions by delegating to the expression generator."""
        return self.expression_generator.generate_primary(node)
    
    def visit_functioncall(self, node):
        """Handle function calls by delegating to the expression generator."""
        return self.expression_generator.generate_function_call(node)
    
    def _is_function_call_initializer(self, node):
        """Check if a node is a function call initializer."""
        return hasattr(node, 'name') and node.name in [
            'dict_create', 'd_array_int_create', 'd_array_string_create', 
            'd_array_float_create', 'd_array_char_create'
        ]
    
    def _evaluate_constant_expression(self, node):
        """Evaluate an expression at compile time to get a constant value."""
        if hasattr(node, 'value'):
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
                if val.startswith('"') and val.endswith('"'):
                    # String literal
                    return self.context.get_global_string(val[1:-1])
                if val == 'null':
                    return ir.Constant(ir.IntType(8).as_pointer(), None)
        
        # Handle dictionary literals and other complex initializers
        if hasattr(node, '__class__'):
            class_name = node.__class__.__name__
            if class_name == 'DictionaryLiteral':
                # For dictionary literals, we can't evaluate at compile time
                # Return None to indicate this needs runtime initialization
                return None
            elif class_name == 'FunctionCall':
                # For function calls, we can't evaluate at compile time
                # Return None to indicate this needs runtime initialization
                return None
        
        # For other types, we can't evaluate at compile time
        raise Exception(f"Cannot evaluate constant expression: {node}")
    
    def _get_default_initializer(self, var_type):
        """Get default initializer for a type."""
        if isinstance(var_type, ir.IntType):
            return ir.Constant(var_type, 0)
        elif isinstance(var_type, ir.DoubleType):
            return ir.Constant(var_type, 0.0)
        elif isinstance(var_type, ir.PointerType):
            return ir.Constant(var_type, None)
        else:
            return ir.Constant(var_type, 0)
    
    def _check_null_equality(self, left_val, right_val):
        """Check if this is a null equality comparison."""
        # Check if either operand is null
        left_is_null = self._is_null_value(left_val)
        right_is_null = self._is_null_value(right_val)
        
        if left_is_null and right_is_null:
            # null == null is always true
            return ir.Constant(ir.IntType(1), 1)
        elif left_is_null or right_is_null:
            # One is null, one is not - compare with null
            non_null_val = right_val if left_is_null else left_val
            return self.context.builder.icmp_signed('==', non_null_val, 
                                                 ir.Constant(non_null_val.type, None), 'null_check')
        
        return None
    
    def _is_null_value(self, val):
        """Check if a value represents null."""
        if isinstance(val, ir.Constant):
            if val.type == ir.IntType(8).as_pointer():
                return val.value is None
        return False
    
    def visit_dictionaryliteral(self, node):
        """Handle dictionary literal: {"key1": value1, "key2": value2}"""
        # Create a new dictionary
        dict_create_func = self.context.module.get_global("dict_create")
        dict_ptr = self.context.builder.call(dict_create_func, [])
        
        # Add each key-value pair
        dict_set_func = self.context.module.get_global("dict_set")
        
        for key_expr, value_expr in node.pairs:
            # Evaluate the key (must be a string)
            key_val = self.visit(key_expr)
            # Don't load string pointers - they should remain as pointers
            
            # Evaluate the value
            value_val = self.visit(value_expr)
            
            # Create a DictValue based on the value type
            if value_val.type == ir.IntType(32):
                # Integer value
                new_int_func = self.context.module.get_global("new_int")
                dict_value = self.context.builder.call(new_int_func, [value_val])
            elif value_val.type == ir.DoubleType():
                # Float value
                new_float_func = self.context.module.get_global("new_float") 
                dict_value = self.context.builder.call(new_float_func, [value_val])
            elif value_val.type == ir.IntType(8).as_pointer():
                # String value
                new_string_func = self.context.module.get_global("new_string")
                dict_value = self.context.builder.call(new_string_func, [value_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.IntType) and value_val.type.pointee.width == 32:
                # Integer pointer - load it first
                loaded_val = self.context.builder.load(value_val)
                new_int_func = self.context.module.get_global("new_int")
                dict_value = self.context.builder.call(new_int_func, [loaded_val])
            elif isinstance(value_val.type, ir.PointerType) and isinstance(value_val.type.pointee, ir.DoubleType):
                # Float pointer - load it first
                loaded_val = self.context.builder.load(value_val)
                new_float_func = self.context.module.get_global("new_float") 
                dict_value = self.context.builder.call(new_float_func, [loaded_val])
            else:
                raise Exception(f"Unsupported dictionary value type: {value_val.type}")
            
            # Set the key-value pair in the dictionary
            self.context.builder.call(dict_set_func, [dict_ptr, key_val, dict_value])
        
        return dict_ptr
    
    def visit_arraydeclaration(self, node):
        """Handle array declarations."""
        var_name = node.identifier
        sym = self.symbol_table.lookup_symbol(var_name)
        ti = sym.get('typeinfo') if sym else None
        base = ti.base if ti else node.var_type.type_name.replace('KEYWORD_','').lower()
        is_dyn = ti.is_dynamic if ti else node.is_dynamic
        element_type_ir = self.type_manager.get_llvm_type(node.var_type.type_name)
        is_global = self.context.builder is None
        
        if is_dyn:
            array_ptr_type = self.type_manager.get_array_type(base)
            if is_global:
                global_var = self.context.add_global_variable(var_name, array_ptr_type, 
                                                          ir.Constant(array_ptr_type, None))
                
                # Handle different types of initializers
                init_nodes = []
                if node.initializer:
                    if hasattr(node.initializer, 'values'):  # InitializerList
                        init_nodes = node.initializer.values
                    else:  # Expression (like BinaryOp for concatenation)
                        # For global arrays with expression initializers, we'll handle it in main
                        init_nodes = []
                self.context.add_global_dynamic_array(var_name, base, init_nodes, True, node.initializer)
            else:
                ptr = self.context.builder.alloca(array_ptr_type, name=var_name)
                self.context.llvm_var_table[var_name] = ptr
                
                if node.initializer:
                    if hasattr(node.initializer, 'values'):  # InitializerList
                        create_func = self.context.module.get_global(f"d_array_{base}_create")
                        new_array_ptr = self.context.builder.call(create_func, [])
                        self.context.builder.store(new_array_ptr, ptr)
                        
                        append_func = self.context.module.get_global(f"d_array_{base}_append")
                        array_struct_ptr = new_array_ptr
                        expected_elem_type = append_func.function_type.args[1]
                        for val_node in node.initializer.values:
                            raw_val = self.visit(val_node)
                            val = self._coerce_array_element(expected_elem_type, raw_val)
                            if val.type != expected_elem_type and isinstance(expected_elem_type, ir.DoubleType) and isinstance(val.type, ir.IntType):
                                val = self.context.builder.sitofp(val, expected_elem_type)
                            if isinstance(expected_elem_type, ir.IntType) and expected_elem_type.width == 8 and isinstance(val.type, ir.PointerType):
                                val = self.context.builder.load(val)
                            self.context.builder.call(append_func, [array_struct_ptr, val])
                    else:  # Expression (like BinaryOp for concatenation)
                        # Visit the expression and store the result
                        result_array = self.visit(node.initializer)
                        self.context.builder.store(result_array, ptr)
                else:
                    # Empty array
                    create_func = self.context.module.get_global(f"d_array_{base}_create")
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
                global_var = self.context.add_global_variable(var_name, array_type, initializer)
            else:
                ptr = self.context.builder.alloca(array_type, name=var_name)
                self.context.llvm_var_table[var_name] = ptr
                if node.initializer:
                    for i, v in enumerate(node.initializer.values):
                        val = self.visit(v)
                        index_ptr = self.context.builder.gep(ptr, [ir.Constant(ir.IntType(32),0), ir.Constant(ir.IntType(32), i)])
                        self.context.builder.store(val, index_ptr)
    
    def visit_assignment(self, node):
        """Handle assignment statements."""
        if hasattr(node, 'lhs') and hasattr(node, 'rhs'):
            # Handle array subscript assignment
            if hasattr(node.lhs, 'name') and hasattr(node.lhs, 'key'):
                # This is an array assignment like arr[i] = value
                sym = self.symbol_table.lookup_symbol(node.lhs.name)
                ti = sym.get('typeinfo') if sym else None
                if ti and ti.is_dynamic:
                    base = ti.base
                    array_var_ptr = self.context.llvm_var_table[node.lhs.name]
                    array_struct_ptr = self.context.builder.load(array_var_ptr)
                    index_val = self._load_if_pointer(self.visit(node.lhs.key))
                    value_val = self._load_if_pointer(self.visit(node.rhs))
                    set_func = self.context.module.get_global(f"d_array_{base}_set")
                    self.context.builder.call(set_func, [array_struct_ptr, index_val, value_val])
                    return
            
            # Regular assignment
            ptr = self.visit(node.lhs)
            value_to_store = self.visit(node.rhs)
            target_type = ptr.type.pointee if hasattr(ptr.type,'pointee') else ptr.type.pointed_type
            if target_type != value_to_store.type and isinstance(target_type, ir.DoubleType) and isinstance(value_to_store.type, ir.IntType):
                value_to_store = self.context.builder.sitofp(value_to_store, target_type)
            self.context.builder.store(value_to_store, ptr)
    
    def visit_subscriptaccess(self, node):
        """Handle array and dictionary subscript access."""
        sym = self.symbol_table.lookup_symbol(node.name)
        ti = sym.get('typeinfo') if sym else None
        
        # Handle dictionary access
        if sym and sym.get('type') == 'KEYWORD_DICT':
            dict_var_ptr = self.context.llvm_var_table[node.name]
            dict_val = self.context.builder.load(dict_var_ptr)
            key_val = self.visit(node.key)  # Don't load string pointers
            
            # Check if key exists first
            dict_has_key_func = self.context.module.get_global("dict_has_key")
            key_exists = self.context.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
            
            # Create a conditional block for safe access
            current_block = self.context.builder.block
            safe_block = self.context.current_function.append_basic_block('dict_safe_access')
            error_block = self.context.current_function.append_basic_block('dict_key_error')
            merge_block = self.context.current_function.append_basic_block('dict_merge')
            
            # Check if key exists
            self.context.builder.cbranch(key_exists, safe_block, error_block)
            
            # Safe access block - key exists
            self.context.builder.position_at_end(safe_block)
            dict_get_func = self.context.module.get_global("dict_get")
            safe_result = self.context.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
            self.context.builder.branch(merge_block)
            
            # Error block - key doesn't exist
            self.context.builder.position_at_end(error_block)
            # For now, return NULL (could be enhanced with runtime error handling)
            dict_value_create_null_func = self.context.module.get_global("dict_value_create_null")
            error_result = self.context.builder.call(dict_value_create_null_func, [], 'null_value')
            self.context.builder.branch(merge_block)
            
            # Merge block
            self.context.builder.position_at_end(merge_block)
            phi = self.context.builder.phi(self.type_manager.get_dict_value_type(), 'dict_access_result')
            phi.add_incoming(safe_result, safe_block)
            phi.add_incoming(error_result, error_block)
            
            return phi
        
        # Handle dynamic arrays
        if ti and ti.is_dynamic:
            base = ti.base
            array_var_ptr = self.context.llvm_var_table[node.name]
            array_struct_ptr = self.context.builder.load(array_var_ptr)
            index_val = self._load_if_pointer(self.visit(node.key))
            get_func = self.context.module.get_global(f"d_array_{base}_get")
            return self.context.builder.call(get_func, [array_struct_ptr, index_val], 'dyn_idx_tmp')
        
        # Handle static arrays
        array_ptr = self.context.llvm_var_table[node.name]
        key_val = self._load_if_pointer(self.visit(node.key))
        return self.context.builder.gep(array_ptr, [ir.Constant(ir.IntType(32),0), key_val], inbounds=True)
    
    def visit_functioncallstatement(self, node):
        """Handle function call statements."""
        if hasattr(node, 'function_call'):
            self.visit(node.function_call)
    
    def visit_systemoutput(self, node):
        """Handle system output statements."""
        if hasattr(node, 'output_type') and hasattr(node, 'expression'):
            output_type = node.output_type.type_name.replace('KEYWORD_', '').lower()
            
            if output_type == 'array':
                array_node = node.expression
                array_var_ptr = self.visit(array_node)
                array_struct_ptr = self.context.builder.load(array_var_ptr)
                
                array_name = array_node.name
                symbol = self.symbol_table.lookup_symbol(array_name)
                element_type = symbol['element_type'].replace('KEYWORD_', '').lower()
                
                func_name = f"print_{element_type}_array"
                print_func = self.context.module.get_global(func_name)
                self.context.builder.call(print_func, [array_struct_ptr])
                return
            
            # Get the raw value first
            raw_val = self.visit(node.expression)
            
            # For string output, we need to handle both string literals and string variables
            if output_type == 'string':
                # If it's a double pointer (string variable), load it to get i8*
                if isinstance(raw_val.type, ir.PointerType) and isinstance(raw_val.type.pointee, ir.PointerType):
                    output_val = self.context.builder.load(raw_val)
                else:
                    # It's already an i8* (string literal)
                    output_val = raw_val
            else:
                # For other types, load if it's a pointer
                output_val = self._load_if_pointer(raw_val)
            
            func_name = f"output_{output_type}"
            output_func = self.context.module.get_global(func_name)
            
            if not output_func:
                raise Exception(f"Runtime function {func_name} not found.")
            
            args = [output_val]
            if output_type == 'float':
                precision = self._load_if_pointer(self.visit(node.precision)) if hasattr(node, 'precision') and node.precision else ir.Constant(ir.IntType(32), 2)
                args.append(precision)
            
            self.context.builder.call(output_func, args)
    
    def visit_systeminput(self, node):
        """Handle system input statements."""
        if hasattr(node, 'variable') and hasattr(node, 'input_type'):
            var_ptr = self.visit(node.variable)  # visit_identifier returns a pointer
            input_type = node.input_type.type_name.replace('KEYWORD_', '').lower()
            
            func_name = f"input_{input_type}"
            input_func = self.context.module.get_global(func_name)
            
            if not input_func:
                raise Exception(f"Runtime function {func_name} not found.")
            
            if input_type == 'string':
                # For string, the runtime function expects a char* buffer
                self.context.builder.call(input_func, [var_ptr])
            else:
                # For other types, it expects a pointer to the variable
                self.context.builder.call(input_func, [var_ptr])
    
    def visit_systemexit(self, node):
        """Handle system exit statements."""
        exit_func = self.context.module.get_global("pie_exit")
        self.context.builder.call(exit_func, [])
    
    def visit_initializerlist(self, node):
        """Handle initializer lists for arrays."""
        # For empty arrays, we don't need to do anything special
        # The array creation is handled in the array declaration logic
        return None
    
    def visit_array_function_call(self, node):
        """Handle array function calls like arr_push, arr_pop, etc."""
        if hasattr(node, 'name') and hasattr(node, 'args'):
            func_name = node.name
            args = node.args
            array_node = args[0]
            array_var_ptr = self.visit(array_node)
            array_struct_ptr = self.context.builder.load(array_var_ptr)
            sym = self.symbol_table.lookup_symbol(array_node.name)
            ti = sym.get('typeinfo') if sym else None
            base = ti.base
            op_map = {'arr_push':'append','arr_pop':'pop','arr_size':'size','arr_contains':'contains','arr_indexof':'indexof','arr_avg':'avg'}
            suffix = op_map.get(func_name)
            if not suffix:
                raise Exception(f"Unknown array function: {func_name}")
            c_func = self.context.module.get_global(f"d_array_{base}_{suffix}")
            call_args = [array_struct_ptr]
            if func_name != 'arr_avg':
                for arg_node in args[1:]:
                    raw_arg_val = self.visit(arg_node)
                    # Handle char array coercion for functions that take element values
                    if base == 'char' and func_name in ['arr_contains', 'arr_indexof']:
                        expected_elem_type = c_func.function_type.args[len(call_args)]
                        arg_val = self._coerce_array_element(expected_elem_type, raw_arg_val)
                    else:
                        arg_val = self._load_if_pointer(raw_arg_val)
                    call_args.append(arg_val)
            return self.context.builder.call(c_func, call_args, f'{func_name}_call')
    
    def visit_safedictionaryaccess(self, node):
        """Handle safe dictionary access with validation and optional default value."""
        if hasattr(node, 'dict_name') and hasattr(node, 'key'):
            dict_var_ptr = self.context.llvm_var_table[node.dict_name]
            dict_val = self.context.builder.load(dict_var_ptr)
            key_val = self.visit(node.key)  # Don't load string pointers
            
            # Check if key exists first
            dict_has_key_func = self.context.module.get_global("dict_has_key")
            key_exists = self.context.builder.call(dict_has_key_func, [dict_val, key_val], 'key_exists')
            
            # Create a conditional block for safe access
            current_block = self.context.builder.block
            safe_block = self.context.current_function.append_basic_block('safe_dict_access')
            default_block = self.context.current_function.append_basic_block('dict_default_value')
            merge_block = self.context.current_function.append_basic_block('safe_dict_merge')
            
            # Check if key exists
            self.context.builder.cbranch(key_exists, safe_block, default_block)
            
            # Safe access block - key exists
            self.context.builder.position_at_end(safe_block)
            dict_get_func = self.context.module.get_global("dict_get")
            safe_result = self.context.builder.call(dict_get_func, [dict_val, key_val], 'dict_value')
            self.context.builder.branch(merge_block)
            
            # Default value block - key doesn't exist
            self.context.builder.position_at_end(default_block)
            if hasattr(node, 'default_value') and node.default_value:
                # Use provided default value
                default_result = self.visit(node.default_value)
                # Convert to DictValue if needed
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
                # Use NULL as default
                dict_value_create_null_func = self.context.module.get_global("dict_value_create_null")
                default_result = self.context.builder.call(dict_value_create_null_func, [], 'null_value')
            self.context.builder.branch(merge_block)
            
            # Merge block
            self.context.builder.position_at_end(merge_block)
            phi = self.context.builder.phi(self.type_manager.get_dict_value_type(), 'safe_dict_result')
            phi.add_incoming(safe_result, safe_block)
            phi.add_incoming(default_result, default_block)
            
            return phi
    
    def visit_arraypush(self, node):
        """Handle array push operations."""
        if hasattr(node, 'array') and hasattr(node, 'value'):
            array_ptr = self.visit(node.array)
            array_val = self.context.builder.load(array_ptr)
            raw_value_val = self.visit(node.value)
            array_type = array_val.type
            
            if array_type == self.type_manager.d_array_types['int']:
                push_func = self.context.module.get_global("d_array_int_push")
                value_val = self._load_if_pointer(raw_value_val)
            elif array_type == self.type_manager.d_array_types['string']:
                push_func = self.context.module.get_global("d_array_string_push")
                # For string variables, we need to load the string pointer
                # For string literals, we already have the pointer
                if isinstance(raw_value_val.type, ir.PointerType) and raw_value_val.type.pointee == ir.IntType(8).as_pointer():
                    # This is a string variable (i8**), load it to get the string pointer (i8*)
                    value_val = self.context.builder.load(raw_value_val)
                else:
                    # This is already a string pointer (i8*) from a literal
                    value_val = raw_value_val
            elif array_type == self.type_manager.d_array_types['float']:
                push_func = self.context.module.get_global("d_array_float_push")
                value_val = self._load_if_pointer(raw_value_val)
            elif array_type == self.type_manager.d_array_types['char']:
                # use append as push alias for char
                push_func = self.context.module.get_global("d_array_char_append")
                expected_elem_type = push_func.function_type.args[1]
                value_val = self._coerce_array_element(expected_elem_type, raw_value_val)
            else:
                raise Exception(f"Unsupported array type for push: {array_type}")
            self.context.builder.call(push_func, [array_val, value_val])
    
    def visit_arraypop(self, node):
        """Handle array pop operations."""
        if hasattr(node, 'array'):
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
        """Handle array size operations."""
        if hasattr(node, 'array'):
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
        """Handle array average operations."""
        if hasattr(node, 'array'):
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
        """Handle array indexOf operations."""
        if hasattr(node, 'array') and hasattr(node, 'value'):
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
        """Handle array contains operations."""
        if hasattr(node, 'array') and hasattr(node, 'value'):
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
