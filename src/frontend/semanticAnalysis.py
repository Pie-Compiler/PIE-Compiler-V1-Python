from frontend.symbol_table import SymbolTable, TypeChecker
from frontend.visitor import Visitor
from frontend.ast import *

class SemanticAnalyzer(Visitor):
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

        self.visit(ast)

        # The AST is modified in-place, so we return the original AST object
        return len(self.errors) == 0, ast

    def visit_program(self, node):
        for stmt in node.statements:
            self.visit(stmt)
        return None

    def visit_declaration(self, node):
        var_type_name = node.var_type.type_name
        if self.symbol_table.lookup_symbol_current_scope(node.identifier):
            self.add_error(f"Variable '{node.identifier}' already defined in this scope.")
            return None

        is_initialized = node.initializer is not None
        self.symbol_table.add_symbol(node.identifier, var_type_name, is_initialized=is_initialized)

        if node.initializer:
            expr_type = self.visit(node.initializer)
            if expr_type and not self.type_checker.is_compatible(var_type_name, expr_type):
                self.add_error(f"Type mismatch in declaration: Cannot assign {expr_type} to {var_type_name} variable '{node.identifier}'")
        return None

    def visit_arraydeclaration(self, node):
        element_type = node.var_type.type_name
        if self.symbol_table.lookup_symbol_current_scope(node.identifier):
            self.add_error(f"Array '{node.identifier}' already defined in this scope.")
            return None

        size = None
        if node.size:
            if isinstance(node.size, Primary) and isinstance(node.size.value, str) and node.size.value.isdigit():
                size = int(node.size.value)
            else:
                self.add_error("Array size must be a constant integer.")

        if node.initializer:
            if not isinstance(node.initializer, InitializerList):
                 self.add_error(f"Array '{node.identifier}' must be initialized with an initializer list.")
                 return None

            init_list_exprs = node.initializer.values
            if size is None:
                size = len(init_list_exprs)
            elif size < len(init_list_exprs):
                self.add_error(f"Too many initializers for array '{node.identifier}'")

            for expr in init_list_exprs:
                expr_type = self.visit(expr)
                if not self.type_checker.is_compatible(element_type, expr_type):
                    self.add_error(f"Type mismatch in initializer for array '{node.identifier}'. Expected {element_type}, got {expr_type}")

        self.symbol_table.add_symbol(node.identifier, 'array', element_type=element_type, size=size, is_dynamic=node.is_dynamic)
        return None

    def visit_initializerlist(self, node, expected_type=None):
        # This visitor is tricky because it needs context (the expected type).
        # For now, we assume the check is done in the declaration visitor.
        for expr in node.values:
            self.visit(expr)
        # The type of an initializer list itself is not well-defined without context.
        return 'initializer_list'

    def visit_dictionaryliteral(self, node):
        for key_expr, value_expr in node.pairs:
            key_type = self.visit(key_expr)
            if key_type != 'KEYWORD_STRING':
                self.add_error(f"Dictionary keys must be strings, but got {key_type}")
            self.visit(value_expr)
        return 'KEYWORD_DICT'

    def visit_subscriptaccess(self, node):
        symbol = self.symbol_table.lookup_symbol(node.name)
        if not symbol:
            self.add_error(f"Undefined variable: '{node.name}'")
            return None

        var_type = symbol.get('type')
        if var_type == 'array':
            key_type = self.visit(node.key)
            if key_type != 'KEYWORD_INT':
                self.add_error(f"Array index must be an integer, got {key_type}.")
            element_type = symbol.get('element_type')
            node.element_type = element_type # Annotate the node
            return element_type
        elif var_type == 'KEYWORD_DICT':
            key_type = self.visit(node.key)
            if key_type != 'KEYWORD_STRING':
                self.add_error(f"Dictionary key must be a string, got {key_type}.")
            # The value type is dynamic, so we can't know it at compile time.
            node.element_type = 'void*' # Annotate the node
            return 'void*'
        else:
            self.add_error(f"'{node.name}' is not a subscriptable type (array or dictionary).")
            return None

    def visit_functiondefinition(self, node):
        if self.current_function:
            self.add_error("Nested function definitions are not allowed.")
            return None

        if self.symbol_table.lookup_symbol_current_scope(node.name):
            self.add_error(f"Function '{node.name}' already defined.")
            return None

        param_types = [p.param_type.type_name for p in node.params]
        self.symbol_table.add_symbol(node.name, 'function', return_type=node.return_type.type_name, param_types=param_types, params=[(p.param_type.type_name, p.name) for p in node.params])

        self.current_function = self.symbol_table.lookup_function(node.name)
        self.symbol_table.enter_scope()
        for param in node.params:
            self.symbol_table.add_symbol(param.name, param.param_type.type_name, is_initialized=True)

        self.visit(node.body)

        self.symbol_table.exit_scope()
        self.current_function = None
        return None

    def visit_block(self, node):
        self.symbol_table.enter_scope()
        for statement in node.statements:
            self.visit(statement)
        self.symbol_table.exit_scope()
        return None

    def visit_array_function_call(self, node):
        func_name = node.name
        args = node.args

        if not args:
            self.add_error(f"Array function '{func_name}' called with no arguments.")
            return None

        # First argument must be an identifier pointing to an array
        array_arg_node = args[0]
        if not isinstance(array_arg_node, Identifier):
            self.add_error(f"First argument to '{func_name}' must be an array variable.")
            return None

        array_name = array_arg_node.name
        array_symbol = self.symbol_table.lookup_symbol(array_name)
        if not array_symbol or array_symbol.get('type') != 'array':
            self.add_error(f"'{array_name}' is not an array.")
            return None

        element_type = array_symbol.get('element_type')
        is_dynamic = array_symbol.get('is_dynamic')

        # Now, handle each function
        if func_name == 'arr_push':
            if not is_dynamic:
                self.add_error(f"'arr_push' can only be used on dynamic arrays.")
            if len(args) != 2:
                self.add_error(f"'arr_push' expects 2 arguments, got {len(args)}.")
                return None
            value_type = self.visit(args[1])
            if not self.type_checker.is_compatible(element_type, value_type):
                self.add_error(f"Type mismatch in 'arr_push'. Cannot push {value_type} to an array of {element_type}.")
            return 'void' # arr_push returns void

        elif func_name == 'arr_pop':
            if not is_dynamic:
                self.add_error(f"'arr_pop' can only be used on dynamic arrays.")
            if len(args) != 1:
                self.add_error(f"'arr_pop' expects 1 argument, got {len(args)}.")
            return element_type # arr_pop returns a value of the element type

        elif func_name == 'arr_size':
            if len(args) != 1:
                self.add_error(f"'arr_size' expects 1 argument, got {len(args)}.")
            return 'KEYWORD_INT'

        elif func_name == 'arr_contains':
            if len(args) != 2:
                self.add_error(f"'arr_contains' expects 2 arguments, got {len(args)}.")
                return None
            value_type = self.visit(args[1])
            if not self.type_checker.is_compatible(element_type, value_type):
                self.add_error(f"Type mismatch in 'arr_contains'. Cannot check for {value_type} in an array of {element_type}.")
            return 'KEYWORD_BOOL'

        elif func_name == 'arr_indexof':
            if len(args) != 2:
                self.add_error(f"'arr_indexof' expects 2 arguments, got {len(args)}.")
                return None
            value_type = self.visit(args[1])
            if not self.type_checker.is_compatible(element_type, value_type):
                self.add_error(f"Type mismatch in 'arr_indexof'. Cannot find index of {value_type} in an array of {element_type}.")
            return 'KEYWORD_INT'

        elif func_name == 'arr_avg':
            if element_type not in ('KEYWORD_INT', 'KEYWORD_FLOAT'):
                self.add_error(f"'arr_avg' can only be used on int or float arrays.")
            if len(args) not in [1, 2]:
                self.add_error(f"'arr_avg' expects 1 or 2 arguments, got {len(args)}.")
                return None
            if len(args) == 2:
                precision_type = self.visit(args[1])
                if precision_type != 'KEYWORD_INT':
                    self.add_error(f"Precision for 'arr_avg' must be an integer.")
            return 'KEYWORD_FLOAT'

        self.add_error(f"Unknown array function '{func_name}'")
        return None

    def visit_functioncall(self, node):
        if node.name.startswith('arr_'):
            return self.visit_array_function_call(node)
        function_symbol = self.symbol_table.lookup_function(node.name)
        if not function_symbol:
            # Could be a system call, handle separately
            if hasattr(self, f'visit_{node.name.lower()}'):
                 return getattr(self, f'visit_{node.name.lower()}')(node)
            self.add_error(f"Undefined function: '{node.name}'")
            return None

        param_types = function_symbol.get('param_types', [])
        if len(node.args) != len(param_types):
            self.add_error(f"Incorrect number of arguments for function '{node.name}'. Expected {len(param_types)}, got {len(node.args)}.")

        for i, arg_expr in enumerate(node.args):
            arg_type = self.visit(arg_expr)
            if i < len(param_types):
                param_type = param_types[i]
                if not self.type_checker.is_compatible(param_type, arg_type):
                    is_math_func = node.name in ["sqrt", "pow", "sin", "cos"]
                    if not (is_math_func and param_type == 'float' and arg_type == 'KEYWORD_INT'):
                        self.add_error(f"Type mismatch for argument {i+1} of function '{node.name}'. Expected {param_type}, got {arg_type}.")

        return function_symbol.get('return_type')

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)
        return None

    def visit_assignment(self, node):
        lhs_type = self.visit(node.lhs)
        expr_type = self.visit(node.rhs)

        if isinstance(node.lhs, SubscriptAccess):
            symbol = self.symbol_table.lookup_symbol(node.lhs.name)
            if symbol and symbol.get('type') == 'KEYWORD_DICT':
                return None # Allow any assignment to dict value

        if lhs_type and expr_type and not self.type_checker.is_compatible(lhs_type, expr_type):
            self.add_error(f"Type mismatch in assignment: Cannot assign {expr_type} to {lhs_type}")

        if isinstance(node.lhs, Identifier):
            self.symbol_table.update_symbol(node.lhs.name, initialized=True)

        return None

    def visit_binaryop(self, node):
        op_map = {'+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV', '%': 'MOD', '<': 'LT', '>': 'GT', '<=': 'LEQ', '>=': 'GEQ', '==': 'EQ', '!=': 'NEQ', '&&': 'AND', '||': 'OR'}
        op_token_name = op_map.get(node.op, node.op)

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not left_type or not right_type:
            return None

        if op_token_name == 'PLUS' and left_type == 'array' and right_type == 'array':
            if isinstance(node.left, Identifier) and isinstance(node.right, Identifier):
                left_symbol = self.symbol_table.lookup_symbol(node.left.name)
                right_symbol = self.symbol_table.lookup_symbol(node.right.name)
                if left_symbol.get('element_type') == right_symbol.get('element_type'):
                    node.result_type = 'array'
                    node.element_type = left_symbol.get('element_type')
                    return 'array'
                else:
                    self.add_error("Cannot concatenate arrays of different element types.")
                    return None
            else:
                self.add_error("Array concatenation is only supported between array variables.")
                return None

        result_type = self.type_checker.check_binary_op(op_token_name, left_type, right_type)
        if not result_type:
            self.add_error(f"Invalid operation: {left_type} {node.op} {right_type}")
            return None

        node.result_type = result_type # Annotate the node
        return result_type

    def visit_unaryop(self, node):
        expr_type = self.visit(node.operand)
        if not expr_type:
            return None

        if node.op == '-' and expr_type in ('KEYWORD_INT', 'KEYWORD_FLOAT'):
            return expr_type
        else:
            self.add_error(f"Invalid unary operation: {node.op} {expr_type}")
            return None

    def visit_primary(self, node):
        value = node.value
        if not isinstance(value, str):
             # Should not happen if parser is correct, but as a safeguard
            return None

        if value.startswith('"') and value.endswith('"'):
            return 'KEYWORD_STRING'
        elif value.startswith("'") and value.endswith("'"):
            return 'KEYWORD_CHAR'
        elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
            return 'KEYWORD_INT'
        elif '.' in value:
            return 'KEYWORD_FLOAT'
        elif value in ['true', 'false']:
            return 'KEYWORD_BOOL'
        elif value == 'null':
            return 'KEYWORD_NULL'

        # This case is for identifiers, which are now handled by visit_identifier
        self.add_error(f"Internal error: Unhandled primary value '{value}'")
        return None

    def visit_identifier(self, node):
        symbol = self.symbol_table.lookup_symbol(node.name)
        if symbol:
            return self.type_checker._normalize_type(symbol.get('type'))
        else:
            self.add_error(f"Undefined variable: '{node.name}'")
            return None

    def visit_ifstatement(self, node):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL', 'KEYWORD_NULL'):
            self.add_error(f"Condition must be boolean, got {cond_type}")

        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)
        return None

    def visit_whilestatement(self, node):
        cond_type = self.visit(node.condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL', 'KEYWORD_NULL'):
            self.add_error(f"Loop condition must be boolean, got {cond_type}")

        self.visit(node.body)
        return None

    def visit_dowhilestatement(self, node):
        self.visit(node.body)
        cond_type = self.visit(node.condition)
        if cond_type and cond_type not in ('KEYWORD_BOOL', 'KEYWORD_NULL'):
            self.add_error(f"Loop condition must be boolean, got {cond_type}")
        return None

    def visit_switchstatement(self, node):
        expr_type = self.visit(node.expression)
        if expr_type != 'KEYWORD_INT':
            self.add_error("Switch expression must be an integer.")

        was_in_switch = self.in_switch
        self.in_switch = True

        case_labels = set()
        for case_clause in node.cases:
            self.visit(case_clause)
            if case_clause.value != 'default':
                # A proper implementation would evaluate the constant expression
                # For now, we assume it's a primary integer literal
                case_label_node = case_clause.value
                if isinstance(case_label_node, Primary) and case_label_node.value.isdigit():
                    label = int(case_label_node.value)
                    if label in case_labels:
                        self.add_error(f"Duplicate case label: {label}")
                    case_labels.add(label)
                else:
                    self.add_error("Case label must be a constant integer.")

        self.in_switch = was_in_switch
        return None

    def visit_breakstatement(self, node):
        if not self.in_switch:
            self.add_error("Break statement not within a switch statement.")
        return None

    def visit_caseclause(self, node):
        if node.value != 'default':
            self.visit(node.value)
        for stmt in node.statements:
            self.visit(stmt)
        return None

    def visit_forstatement(self, node):
        self.symbol_table.enter_scope()
        if node.initializer:
            self.visit(node.initializer)
        if node.condition:
            cond_type = self.visit(node.condition)
            if cond_type and cond_type not in ('KEYWORD_BOOL', 'KEYWORD_NULL'):
                self.add_error(f"Loop condition must be boolean, got {cond_type}")
        if node.update:
            self.visit(node.update)

        self.visit(node.body)
        self.symbol_table.exit_scope()
        return None

    def visit_systemoutput(self, node):
        expr_type = self.visit(node.expression)
        expected_type_name = node.output_type.type_name
        norm_expr_type = self.type_checker._normalize_type(expr_type)
        norm_expected_type = self.type_checker._normalize_type(expected_type_name)

        if norm_expr_type and norm_expr_type != norm_expected_type:
            self.add_error(f"Type mismatch in output: Expression is {expr_type}, but output type is {expected_type_name}")

        if node.precision:
            precision_type = self.visit(node.precision)
            if precision_type != 'KEYWORD_INT':
                self.add_error("Output precision must be an integer.")
        return None

    def visit_systeminput(self, node):
        # The parser creates an Identifier node for the variable
        self.visit(node.variable)
        return None

    def visit_systemexit(self, node):
        return None

    def visit_returnstatement(self, node):
        if not self.current_function:
            self.add_error("Return statement outside of a function.")
            return None

        return_type = self.current_function.get('return_type')

        if node.value:
            expr_type = self.visit(node.value)
            if return_type == 'void':
                self.add_error(f"Function with void return type cannot return a value.")
            elif not self.type_checker.is_compatible(return_type, expr_type):
                self.add_error(f"Type mismatch in return statement. Expected {return_type}, got {expr_type}.")
        else:
            if return_type != 'void':
                self.add_error(f"Function with non-void return type must return a value.")
        return None

    def generic_visit(self, node):
        """
        Override generic_visit to traverse children for nodes that don't need
        specific logic but contain other nodes.
        """
        if isinstance(node, list):
            for item in node:
                if hasattr(item, 'accept'):
                    self.visit(item)
            return None

        # This is a simple generic visitor. A more robust one would inspect
        # the node's attributes to find visitable children.
        for attr, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, 'accept'): # Check if it's an AST node
                        self.visit(item)
            elif hasattr(value, 'accept'):
                self.visit(value)
        return None