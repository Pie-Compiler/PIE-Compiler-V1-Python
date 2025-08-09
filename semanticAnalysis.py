from symbol_table import SymbolTable, TypeChecker

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.type_checker = TypeChecker(self.symbol_table)
        self.errors = []
        self.warnings = []
        self.error_set = set()
        self.current_function = None
        self.in_switch = False

    def add_error(self, error_msg):
        if error_msg not in self.error_set:
            self.error_set.add(error_msg)
            self.errors.append(error_msg)

    def analyze(self, ast):
        if not ast:
            return False, None
        
        new_ast, _ = self._analyze_node(ast)
        
        return len(self.errors) == 0, new_ast

    def _analyze_node(self, node, expected_type=None):
        if not isinstance(node, tuple):
            return node, None
        
        node_type = node[0]
        
        method_name = f"_analyze_{node_type}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node, expected_type)
        else:
            new_children = []
            for child in node[1:]:
                new_child, _ = self._analyze_node(child)
                new_children.append(new_child)
            return (node[0], *new_children), None

    def _analyze_program(self, node, _):
        _, declarations = node
        new_declarations = []
        for declaration in declarations:
            new_declaration, _ = self._analyze_node(declaration)
            new_declarations.append(new_declaration)
        return ('program', new_declarations), None

    def _analyze_declaration(self, node, _):
        var_type, var_name, init_expr = node[1], node[2], node[3]
        
        if self.symbol_table.lookup_symbol_current_scope(var_name):
            self.add_error(f"Variable '{var_name}' already defined in this scope.")
            return node, None

        is_initialized = init_expr is not None
        self.symbol_table.add_symbol(var_name, var_type, is_initialized=is_initialized)

        new_init_expr = None
        if init_expr:
            new_init_expr, expr_type = self._analyze_node(init_expr)
            if expr_type and not self.type_checker.is_compatible(var_type, expr_type):
                self.add_error(f"Type mismatch in declaration: Cannot assign {expr_type} to {var_type} variable '{var_name}'")

        return ('declaration', var_type, var_name, new_init_expr), None

    def _analyze_array_declaration(self, node, _):
        element_type, name, size_expr, init_list = node[1], node[2], node[3], node[4]

        if self.symbol_table.lookup_symbol_current_scope(name):
            self.add_error(f"Array '{name}' already defined in this scope.")
            return node, None

        size = None
        if size_expr:
            if size_expr[0] == 'primary' and isinstance(size_expr[1], str) and size_expr[1].isdigit():
                size = int(size_expr[1])
            else:
                self.add_error("Array size must be a constant integer.")

        new_init_list = None
        if init_list:
            init_list_exprs = init_list[1]
            new_init_list_exprs = []
            if size is None:
                size = len(init_list_exprs)
            elif size < len(init_list_exprs):
                self.add_error(f"Too many initializers for array '{name}'")

            for expr in init_list_exprs:
                new_expr, expr_type = self._analyze_node(expr)
                new_init_list_exprs.append(new_expr)
                if not self.type_checker.is_compatible(element_type, expr_type):
                    self.add_error(f"Type mismatch in initializer for array '{name}'. Expected {element_type}, got {expr_type}")
            new_init_list = ('initializer_list', new_init_list_exprs)

        self.symbol_table.add_symbol(name, 'array', element_type=element_type, size=size)
        return ('array_declaration', element_type, name, size_expr, new_init_list), None

    def _analyze_array_access(self, node, _):
        name, index_expr = node[1], node[2]

        symbol = self.symbol_table.lookup_symbol(name)
        if not symbol or symbol.get('type') != 'array':
            self.add_error(f"'{name}' is not an array.")
            return node, None

        new_index_expr, index_type = self._analyze_node(index_expr)
        if index_type != 'KEYWORD_INT':
            self.add_error(f"Array index must be an integer, got {index_type}.")

        element_type = symbol.get('element_type')
        return ('array_access', name, new_index_expr, element_type), element_type

    def _analyze_function_definition(self, node, _):
        if self.current_function:
            self.add_error("Nested function definitions are not allowed.")
            return node, None

        return_type, name, params, body = node[1], node[2], node[3], node[4]

        if self.symbol_table.lookup_symbol_current_scope(name):
            self.add_error(f"Function '{name}' already defined.")
            return node, None

        param_types = [p[0] for p in params]
        self.symbol_table.add_symbol(name, 'function', return_type=return_type, param_types=param_types, params=params)

        self.current_function = self.symbol_table.lookup_function(name)
        self.symbol_table.enter_scope()
        for param_type, param_name in params:
            self.symbol_table.add_symbol(param_name, param_type, is_initialized=True)

        new_body, _ = self._analyze_node(body)

        self.symbol_table.exit_scope()
        self.current_function = None
        return ('function_definition', return_type, name, params, new_body), None

    def _analyze_block(self, node, _):
        _, statement_list = node
        self.symbol_table.enter_scope()
        new_statement_list = []
        for statement in statement_list:
            new_statement, _ = self._analyze_node(statement)
            new_statement_list.append(new_statement)
        self.symbol_table.exit_scope()
        return ('block', new_statement_list), None

    def _analyze_function_call(self, node, _):
        name, args = node[1], node[2]
        function_symbol = self.symbol_table.lookup_function(name)

        if not function_symbol:
            self.add_error(f"Undefined function: '{name}'")
            return node, None

        param_types = function_symbol.get('param_types', [])
        if len(args) != len(param_types):
            self.add_error(f"Incorrect number of arguments for function '{name}'. Expected {len(param_types)}, got {len(args)}.")

        new_args = []
        for i, arg_expr in enumerate(args):
            new_arg, arg_type = self._analyze_node(arg_expr)
            new_args.append(new_arg)
            if i < len(param_types):
                param_type = param_types[i]
                if not self.type_checker.is_compatible(param_type, arg_type):
                    # Allow int to float conversion for math functions
                    is_math_func = name in ["sqrt", "pow", "sin", "cos"]
                    if not (is_math_func and param_type == 'float' and arg_type == 'KEYWORD_INT'):
                        self.add_error(f"Type mismatch for argument {i+1} of function '{name}'. Expected {param_type}, got {arg_type}.")

        return_type = function_symbol.get('return_type')
        return ('function_call', name, new_args, return_type), return_type

    def _analyze_assignment(self, node, _):
        lhs, expr = node[1], node[2]

        new_lhs, lhs_type = self._analyze_node(lhs)
        new_expr, expr_type = self._analyze_node(expr)

        if lhs_type and expr_type and not self.type_checker.is_compatible(lhs_type, expr_type):
            self.add_error(f"Type mismatch in assignment: Cannot assign {expr_type} to {lhs_type}")

        if isinstance(lhs, str):
            self.symbol_table.update_symbol(lhs, initialized=True)

        return ('assignment', new_lhs, new_expr), None

    def _analyze_binary_op(self, node, _):
        operator, left_expr, right_expr = node[1], node[2], node[3]
        
        op_map = {
            '+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV', '%': 'MOD',
            '<': 'LT', '>': 'GT', '<=': 'LEQ', '>=': 'GEQ',
            '==': 'EQ', '!=': 'NEQ', '&&': 'AND', '||': 'OR'
        }
        op_token_name = op_map.get(operator, operator)

        new_left, left_type = self._analyze_node(left_expr)
        new_right, right_type = self._analyze_node(right_expr)
        
        if not left_type or not right_type:
            return node, None
        
        result_type = self.type_checker.check_binary_op(op_token_name, left_type, right_type)
        if not result_type:
            self.add_error(f"Invalid operation: {left_type} {operator} {right_type}")
            return node, None
        
        return ('binary_op', operator, new_left, new_right, result_type), result_type

    def _analyze_unary_op(self, node, _):
        operator, expr = node[1], node[2]
        new_expr, expr_type = self._analyze_node(expr)
        
        if not expr_type:
            return node, None
        
        if operator == '-' and expr_type in ('KEYWORD_INT', 'KEYWORD_FLOAT'):
            return ('unary_op', operator, new_expr, expr_type), expr_type
        else:
            self.add_error(f"Invalid unary operation: {operator} {expr_type}")
            return node, None

    def _analyze_primary(self, node, _):
        value = node[1]
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return ('primary', value, 'string'), 'KEYWORD_STRING'
            elif value.startswith("'") and value.endswith("'"):
                return ('primary', value, 'char'), 'KEYWORD_CHAR'
            elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
                return ('primary', value, 'int'), 'KEYWORD_INT'
            elif '.' in value:
                return ('primary', value, 'float'), 'KEYWORD_FLOAT'
            elif value in ['true', 'false']:
                return ('primary', value, 'boolean'), 'KEYWORD_BOOL'
            elif value == 'null':
                return ('primary', value, 'null'), 'KEYWORD_NULL'
            else:
                symbol = self.symbol_table.lookup_symbol(value)
                if symbol:
                    var_type = self.type_checker._normalize_type(symbol.get('type'))
                    return ('primary', value, var_type), var_type
                else:
                    self.add_error(f"Undefined variable: '{value}'")
                    return node, None
        return node, None

    def _analyze_if(self, node, _):
        condition, then_stmt, else_stmt = node[1], node[2], node[3]
        
        new_condition, cond_type = self._analyze_node(condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL','KEYWORD_NULL'):
            self.add_error(f"Condition must be boolean, got {cond_type}")
        
        new_then, _ = self._analyze_node(then_stmt)
        new_else = None
        if else_stmt:
            new_else, _ = self._analyze_node(else_stmt)

        return ('if', new_condition, new_then, new_else), None

    def _analyze_while(self, node, _):
        condition, body = node[1], node[2]
        new_condition, cond_type = self._analyze_node(condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL','KEYWORD_NULL'):
            self.add_error(f"Loop condition must be boolean, got {cond_type}")
        
        new_body, _ = self._analyze_node(body)
        return ('while', new_condition, new_body), None

    def _analyze_do_while(self, node, _):
        body, condition = node[1], node[2]
        new_body, _ = self._analyze_node(body)
        new_condition, cond_type = self._analyze_node(condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL','KEYWORD_NULL'):
            self.add_error(f"Loop condition must be boolean, got {cond_type}")
        return ('do_while', new_body, new_condition), None

    def _analyze_switch_statement(self, node, _):
        expression, case_list = node[1], node[2]
        new_expression, expr_type = self._analyze_node(expression)
        if expr_type != 'KEYWORD_INT':
            self.add_error("Switch expression must be an integer.")

        was_in_switch = self.in_switch
        self.in_switch = True

        new_case_list = []
        case_labels = set()
        for case_clause in case_list:
            new_case_clause, _ = self._analyze_node(case_clause)
            new_case_list.append(new_case_clause)
            # Check for duplicate case labels
            if new_case_clause[0] == 'case':
                case_label_node = new_case_clause[1]
                if case_label_node[0] == 'primary' and isinstance(case_label_node[1], str) and case_label_node[1].isdigit():
                    label = int(case_label_node[1])
                    if label in case_labels:
                        self.add_error(f"Duplicate case label: {label}")
                    case_labels.add(label)
                else:
                    self.add_error("Case label must be a constant integer.")

        self.in_switch = was_in_switch
        return ('switch', new_expression, new_case_list), None

    def _analyze_break_statement(self, node, _):
        if not self.in_switch:
            self.add_error("Break statement not within a switch statement.")
        return node, None

    def _analyze_case(self, node, _):
        label, statements = node[1], node[2]
        new_label, _ = self._analyze_node(label)
        new_statements = []
        for stmt in statements:
            new_stmt, _ = self._analyze_node(stmt)
            new_statements.append(new_stmt)
        return ('case', new_label, new_statements), None

    def _analyze_default(self, node, _):
        statements = node[1]
        new_statements = []
        for stmt in statements:
            new_stmt, _ = self._analyze_node(stmt)
            new_statements.append(new_stmt)
        return ('default', new_statements), None

    def _analyze_for(self, node, _):
        init, condition, update, body = node[1], node[2], node[3], node[4]

        self.symbol_table.enter_scope()
        new_init, _ = self._analyze_node(init)
        new_condition, cond_type = self._analyze_node(condition)
        if condition and cond_type and cond_type not in ('KEYWORD_BOOL','KEYWORD_NULL'):
            self.add_error(f"Loop condition must be boolean, got {cond_type}")
        new_update, _ = self._analyze_node(update)
        new_body, _ = self._analyze_node(body)
        self.symbol_table.exit_scope()

        return ('for', new_init, new_condition, new_update, new_body), None

    def _analyze_system_output(self, node, _):
        expr, expected_type, precision_expr = node[1], node[2], node[3]
        new_expr, expr_type = self._analyze_node(expr)
        norm_expr_type = self.type_checker._normalize_type(expr_type)
        norm_expected_type = self.type_checker._normalize_type(expected_type)
        if norm_expr_type and norm_expr_type != norm_expected_type:
            self.add_error(f"Type mismatch in output: Expression is {expr_type}, but output type is {expected_type}")

        new_precision_expr = None
        if precision_expr:
            new_precision_expr, precision_type = self._analyze_node(precision_expr)
            if precision_type != 'KEYWORD_INT':
                self.add_error("Output precision must be an integer.")

        return ('system_output', new_expr, expected_type, new_precision_expr), None

    def _analyze_return(self, node, _):
        expr = node[1]
        new_expr = None
        if not self.current_function:
            self.add_error("Return statement outside of a function.")
            return node, None

        return_type = self.current_function.get('return_type')

        if expr:
            new_expr, expr_type = self._analyze_node(expr)
            if return_type == 'void':
                self.add_error(f"Function with void return type cannot return a value.")
            elif not self.type_checker.is_compatible(return_type, expr_type):
                self.add_error(f"Type mismatch in return statement. Expected {return_type}, got {expr_type}.")
        else:
            if return_type != 'void':
                self.add_error(f"Function with non-void return type must return a value.")

        return ('return', new_expr), None