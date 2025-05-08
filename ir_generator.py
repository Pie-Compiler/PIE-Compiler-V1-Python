class IRGenerator:
    def __init__(self):
        self.code = []          # List to store generated IR instructions
        self.temp_counter = 0   # Counter for temporary variables
        self.label_counter = 0  # Counter for labels
        self.current_scope = 0  # Track current scope for variable renaming
        self.symbol_map = {}    # Map original names to IR-friendly names

    def generate(self, ast, symbol_table):
        """Generate IR code from the AST"""
        self.symbol_table = symbol_table
        self.code = []
        
        # Process the AST from the root
        self._process_node(ast)
        
        return self.code
    
    def _process_node(self, node):
        """Process a node in the AST"""
        if not isinstance(node, tuple):
            return None
        
        node_type = node[0]
        
        # Dispatch to appropriate handler method
        method_name = f"_process_{node_type}"
        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            return handler(node)
        else:
            # Process children for unhandled node types
            self._process_children(node)
            return None
    
    def _process_children(self, node):
        """Process all children of a node"""
        if isinstance(node, tuple):
            for child in node[1:]:
                self._process_node(child)
        elif isinstance(node, list):
            for child in node:
                self._process_node(child)
    
    def _get_temp(self):
        """Get a new temporary variable name"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def _get_label(self):
        """Get a new label name"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def _get_var_name(self, original_name, is_declaration=False):
            if is_declaration:
                # This is a declaration, create the variable in the current scope
                key = (self.current_scope, original_name)
                ir_name = f"{original_name}_{self.current_scope}"
                self.symbol_map[key] = ir_name
                return ir_name
            else:
                # This is a variable access, search from current scope outwards
                for scope_idx in range(self.current_scope, -1, -1):
                    key = (scope_idx, original_name)
                    if key in self.symbol_map:
                        return self.symbol_map[key]
                
                # Variable not found in any accessible scope.
                # This indicates an undeclared variable, which should ideally be caught
                # by semantic analysis. For IR generation, you might raise an error
                # or have a strategy for it (e.g., assume global if not found).
                # For now, let's raise an error as it's cleaner.
                raise NameError(f"Variable '{original_name}' not found in scope {self.current_scope} or outer scopes.")
    
    # === Process methods for different node types ===
    
    def _process_program(self, node):
        """Process the program node (root of AST)"""
        # node structure: ('program', statement_list)
        statement_list = node[1]
        
        # Add program start
        self.code.append(("START_PROGRAM",))
        
        # Process all statements
        for statement in statement_list:
            self._process_node(statement)
        
        # Add program end
        self.code.append(("END_PROGRAM",))
    
    def _process_declaration(self, node):
        """Process variable declarations"""
        # node structure: ('declaration', type, name, init_expr)
        var_type, var_name, init_expr = node[1], node[2], node[3]
        
        # Generate IR-friendly variable name (mark as declaration)
        ir_var = self._get_var_name(var_name, is_declaration=True)
        
        # Add declaration to IR
        self.code.append(("DECLARE", var_type, ir_var))
        
        # If there's an initializer, process it
        if init_expr:
            expr_result = self._process_expression(init_expr)
            self.code.append(("ASSIGN", ir_var, expr_result))
    
    def _process_assignment(self, node):
        """Process assignment statements"""
        # node structure: ('assignment', var_name, expr)
        var_name, expr = node[1], node[2]
        
        # Generate IR-friendly variable name
        ir_var = self._get_var_name(var_name)
        
        # Process the expression and get its result
        expr_result = self._process_expression(expr)
        
        # Add assignment to IR
        self.code.append(("ASSIGN", ir_var, expr_result))
    
    def _process_expression(self, node):
        """Process expressions and return the result variable/value"""
        if not isinstance(node, tuple):
            # Check if this is a variable name that needs resolution
            if isinstance(node, str):
                symbol = self.symbol_table.lookup_symbol(node)
                if symbol:
                    return self._get_var_name(node)
            return str(node)
        
        node_type = node[0]
        
        if node_type == 'primary':
            value = node[1]
            # Resolve variable names but not literals
            if isinstance(value, str):
                symbol = self.symbol_table.lookup_symbol(value)
                if symbol:
                    return self._get_var_name(value)
            return value
        
        elif node_type == 'binary_op':
            # node structure: ('binary_op', operator, left_expr, right_expr)
            operator, left_expr, right_expr = node[1], node[2], node[3]
            
            # Process left and right expressions
            left_result = self._process_expression(left_expr)
            right_result = self._process_expression(right_expr)
            
            # Create a temporary for the result
            result_var = self._get_temp()
            
            # Add binary operation to IR
            self.code.append(("BINARY_OP", operator, result_var, left_result, right_result))
            
            return result_var
        
        elif node_type == 'unary_op':
            # node structure: ('unary_op', operator, expr)
            operator, expr = node[1], node[2]
            
            # Process the expression
            expr_result = self._process_expression(expr)
            
            # Create a temporary for the result
            result_var = self._get_temp()
            
            # Add unary operation to IR
            self.code.append(("UNARY_OP", operator, result_var, expr_result))
            
            return result_var
        
        # Process other expression types recursively
        return self._process_node(node)
    
    def _process_if(self, node):
        """Process if statements"""
        # node structure: ('if', condition, then_stmt, else_stmt)
        condition, then_stmt, else_stmt = node[1], node[2], node[3]
        
        # Create labels for branching
        else_label = self._get_label()
        end_label = self._get_label()
        
        # Process condition using current scope
        condition_result = self._process_expression(condition)
        
        # Add branch instruction
        if else_stmt:
            self.code.append(("IF_FALSE", condition_result, else_label))
        else:
            self.code.append(("IF_FALSE", condition_result, end_label))
        
        # Process then branch in same scope as parent
        self._process_node(then_stmt)
        
        # If there's an else branch, add jump over it
        if else_stmt:
            self.code.append(("GOTO", end_label))
            self.code.append(("LABEL", else_label))
            # Process else branch in same scope as parent
            self._process_node(else_stmt)
        
        # End of if statement
        self.code.append(("LABEL", end_label))
    
    def _process_while(self, node):
        """Process while loops"""
        # node structure: ('while', condition, body)
        condition, body = node[1], node[2]
        
        # Create labels
        start_label = self._get_label()
        end_label = self._get_label()
        
        # Add loop start label
        self.code.append(("LABEL", start_label))
        
        # Process condition
        condition_result = self._process_expression(condition)
        
        # Add conditional branch
        self.code.append(("IF_FALSE", condition_result, end_label))
        
        # Process loop body
        self._process_node(body)
        
        # Jump back to condition
        self.code.append(("GOTO", start_label))
        
        # Add loop end label
        self.code.append(("LABEL", end_label))
    
    def _process_for(self, node):
        """Process for loops"""
        # node structure: ('for', init, condition, update, body)
        init, condition, update, body = node[1], node[2], node[3], node[4]
        
        # Create labels
        start_label = self._get_label()
        update_label = self._get_label()
        end_label = self._get_label()
        
        # Process initialization
        if init:
            self._process_node(init)
        
        # Add loop start label
        self.code.append(("LABEL", start_label))
        
        # Process condition (if any)
        if condition:
            condition_result = self._process_expression(condition)
            self.code.append(("IF_FALSE", condition_result, end_label))
        
        # Process loop body
        self._process_node(body)
        
        # Add update label
        self.code.append(("LABEL", update_label))
        
        # Process update (if any)
        if update:
            self._process_node(update)
        
        # Jump back to condition check
        self.code.append(("GOTO", start_label))
        
        # Add loop end label
        self.code.append(("LABEL", end_label))
    
    def _process_return(self, node):
        """Process return statements"""
        # node structure: ('return', expr)
        expr = node[1]
        
        if expr:
            # Process the return expression
            expr_result = self._process_expression(expr)
            self.code.append(("RETURN", expr_result))
        else:
            # Void return
            self.code.append(("RETURN",))
    
    def _process_block(self, node):
        """Process block statements"""
        # node structure: ('block', statement_list)
        statement_list = node[1]
        
        # Enter new scope
        old_scope = self.current_scope
        self.current_scope += 1
        
        # Process all statements in the block
        for statement in statement_list:
            self._process_node(statement)
        
        # Restore previous scope
        self.current_scope = old_scope
    
    def _process_system_input(self, node):
        """Process system input calls"""
        # node structure: ('system_input', var_name, type)
        var_node, var_type = node[1], node[2]
        
        # Extract variable name
        if isinstance(var_node, tuple) and var_node[0] == 'primary':
            var_name = var_node[1]
        else:
            var_name = var_node
        
        # Generate IR-friendly variable name
        ir_var = self._get_var_name(var_name)
        
        # Add input instruction to IR
        self.code.append(("INPUT", ir_var, var_type))
    
    def _process_system_output(self, node):
        """Process system output calls"""
        # node structure: ('system_output', expr, type)
        expr, output_type = node[1], node[2]
        
        # Check if expr is a simple variable name
        if isinstance(expr, str):
            expr_result = self._get_var_name(expr)
        else:
            # Process the expression to output
            expr_result = self._process_expression(expr)
        
        # Add output instruction to IR
        self.code.append(("OUTPUT", expr_result, output_type))
    
    def _process_system_exit(self, node):
        """Process system exit calls"""
        # node structure: ('system_exit',)
        # Add exit instruction to IR
        self.code.append(("EXIT",))
        
        return None