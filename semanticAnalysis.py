from symbol_table import SymbolTable, FunctionSymbolTable, TypeChecker

class SemanticAnalyzer:
    def __init__(self, symbol_table, function_table=None):
        self.symbol_table = symbol_table
        self.function_table = function_table or FunctionSymbolTable()
        self.type_checker = TypeChecker(self.symbol_table, self.function_table)
        self.errors = []
        self.warnings = []
        self.error_set = set()  # Track unique errors

    def add_error(self, error_msg):
        """Add an error if it hasn't been reported yet."""
        if error_msg not in self.error_set:
            self.error_set.add(error_msg)
            self.errors.append(error_msg)
    
    def analyze(self, ast):
        """Analyze the AST for semantic correctness."""
        if not ast:
            return False
        
        # Start analysis from the root
        self._analyze_node(ast)
        
        # Return True if no errors, False otherwise
        return len(self.errors) == 0
    
    def _analyze_node(self, node, expected_type=None):
        """Recursively analyze a node and its children."""
        if not isinstance(node, tuple):
            return None
        
        node_type = node[0]
        
        # Dispatch to the appropriate analysis method based on node type
        if hasattr(self, f"_analyze_{node_type}"):
            method = getattr(self, f"_analyze_{node_type}")
            return method(node, expected_type)
        else:
            # Default handling for unrecognized nodes
            self._analyze_children(node)
            return None
    
    def _analyze_children(self, node):
        """Analyze all children of a node."""
        if isinstance(node, tuple):
            for child in node[1:]:
                self._analyze_node(child)
        elif isinstance(node, list):
            for child in node:
                self._analyze_node(child)
    
    # Add to the SemanticAnalyzer class

    def _analyze_program(self, node, _):
        """Analyze the program node."""
        # Program node contains a statement list
        statements = node[1]
        for statement in statements:
            self._analyze_node(statement)

    def _analyze_declaration(self, node, _):
        """Analyze variable declarations."""
        # node structure: ('declaration', type, name, init_expr)
        var_type, var_name, init_expr = node[1], node[2], node[3]
        
        # If there's an initializer, check type compatibility
        if init_expr:
            expr_type = self._analyze_node(init_expr)
            if expr_type and not self.type_checker.is_compatible(var_type, expr_type):
                self.add_error(f"Type mismatch in declaration: Cannot assign {expr_type} to {var_type} variable '{var_name}'")

    def _analyze_assignment(self, node, _):
        """Analyze assignment statements."""
        # node structure: ('assignment', var_name, expr)
        var_name, expr = node[1], node[2]
        
        # Check if variable exists
        symbol = self.symbol_table.lookup_symbol(var_name)
        if not symbol:
            self.add_error(f"Undefined variable: '{var_name}'")
            return None
        
        # Get the variable's type
        var_type = symbol.get('type')
        
        # Check expression type and compatibility
        expr_type = self._analyze_node(expr)
        if expr_type and not self.type_checker.is_compatible(var_type, expr_type):
            self.add_error(f"Type mismatch in assignment: Cannot assign {expr_type} to {var_type} variable '{var_name}'")
        
        return var_type

    def _analyze_binary_op(self, node, _):
        """Analyze binary operations."""
        # node structure: ('binary_op', operator, left_expr, right_expr)
        operator, left_expr, right_expr = node[1], node[2], node[3]
        
        # Map operator symbols to token names
        op_map = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LEQ',
            '>=': 'GEQ',
            '==': 'EQ',
            '!=': 'NEQ',
            '&&': 'AND',
            '||': 'OR'
        }
        
        # Convert operator to token name
        op_token = op_map.get(operator, operator)
        
        # Get types of operands
        left_type = self._analyze_node(left_expr)
        right_type = self._analyze_node(right_expr)
        
        if not left_type or not right_type:
            return None
        
        # Check if operation is valid for these types
        result_type = self.type_checker.check_binary_op(op_token, left_type, right_type)
        if not result_type:
            self.add_error(f"Invalid operation: {left_type} {operator} {right_type}")
        
        return result_type

    def _analyze_unary_op(self, node, _):
        """Analyze unary operations."""
        # node structure: ('unary_op', operator, expr)
        operator, expr = node[1], node[2]
        
        # Get type of operand
        expr_type = self._analyze_node(expr)
        
        if not expr_type:
            return None
        
        # Check if unary operation is valid for this type
        if operator == 'MINUS' and expr_type in ('KEYWORD_INT', 'KEYWORD_FLOAT'):
            return expr_type
        else:
            self.add_error(f"Invalid unary operation: {operator} {expr_type}")
            return None

    def _analyze_primary(self, node, _):
        """Analyze primary expressions (variables, literals)."""
        value = node[1]
        # Handle literals vs variables based on value format
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return 'KEYWORD_STRING'
            elif value.startswith("'") and value.endswith("'"):
                return 'KEYWORD_CHAR'
            elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
                return 'KEYWORD_INT'
            elif '.' in value and all(c.isdigit() or c == '.' or (i == 0 and c == '-') 
                                   for i, c in enumerate(value.replace('.', '', 1))):
                return 'KEYWORD_FLOAT'
            elif value in ['true', 'false']:
                return 'KEYWORD_BOOL'
            elif value == 'null':
                return 'KEYWORD_NULL'
            else:
                # It's a variable name - look it up
                symbol = self.symbol_table.lookup_symbol(value)
                if symbol:
                    return self.type_checker._normalize_type(symbol.get('type'))
                else:
                    self.add_error(f"Undefined variable: '{value}'")
                    return None
        return None

    # Add to the SemanticAnalyzer class

    def _analyze_if(self, node, _):
        """Analyze if statements."""
        # node structure: ('if', condition, then_stmt, else_stmt)
        condition, then_stmt, else_stmt = node[1], node[2], node[3]
        
        # Check that condition is boolean
        cond_type = self._analyze_node(condition)
        if cond_type:
            if cond_type != 'KEYWORD_BOOL':
                # Check if it's a relational expression that returns bool
                if isinstance(condition, tuple) and condition[0] == 'binary_op' and condition[1] in ['GT', 'LT', 'GEQ', 'LEQ', 'EQ', 'NEQ']:
                    pass  # This is OK - comparison operators produce boolean results
                else:
                    self.add_error(f"Condition must be boolean, got {cond_type}")
        
        # Analyze then and else statements
        self._analyze_node(then_stmt)
        if else_stmt:
            self._analyze_node(else_stmt)

    def _analyze_while(self, node, _):
        """Analyze while loops."""
        # node structure: ('while', condition, body)
        condition, body = node[1], node[2]
        
        # Check that condition is boolean
        cond_type = self._analyze_node(condition)
        if cond_type and cond_type != 'KEYWORD_BOOL':
            self.add_error(f"Loop condition must be boolean, got {cond_type}")
        
        # Analyze loop body
        self._analyze_node(body)

    def _analyze_for(self, node, _):
        """Analyze for loops."""
        # node structure: ('for', init, condition, update, body)
        init, condition, update, body = node[1], node[2], node[3], node[4]
        
        # Analyze initialization
        if init:
            self._analyze_node(init)
        
        # Check that condition is boolean
        if condition:
            cond_type = self._analyze_node(condition)
            if cond_type and cond_type != 'KEYWORD_BOOL':
                self.add_error(f"Loop condition must be boolean, got {cond_type}")
        
        # Analyze update and body
        if update:
            self._analyze_node(update)
        self._analyze_node(body)

        # Add to the SemanticAnalyzer class

    def _analyze_system_input(self, node, _):
        """Analyze system input calls."""
        # node structure: ('system_input', var_name, type)
        var_node, var_type = node[1], node[2]
        # If var_node is a primary node, extract the name
        if isinstance(var_node, tuple) and var_node[0] == 'primary':
            var_name = var_node[1]
        else:
            var_name = var_node

        symbol = self.symbol_table.lookup_symbol(var_name)
        if not symbol:
            self.add_error(f"Undefined variable for input: '{var_name}'")
            return None

        if symbol.get('type') != var_type:
            self.add_error(f"Type mismatch in input: Variable '{var_name}' is {symbol.get('type')}, but input type is {var_type}")

        return None

    def _analyze_system_output(self, node, _):
        """Analyze system output calls."""
        # node structure: ('system_output', expr, type)
        expr, expected_type = node[1], node[2]
        expr_type = self._analyze_node(expr)
        # Normalize types for comparison
        norm_expr_type = self.type_checker._normalize_type(expr_type)
        norm_expected_type = self.type_checker._normalize_type(expected_type)
        if norm_expr_type and norm_expr_type != norm_expected_type:
            self.add_error(f"Type mismatch in output: Expression is {expr_type}, but output type is {expected_type}")
        return None

    def _analyze_return(self, node, _):
        """Analyze return statements."""
        # node structure: ('return', expr)
        expr = node[1]
        
        # If there's no active function, this is a return at global scope
        # We'll just check the expression type
        if expr:
            self._analyze_node(expr)