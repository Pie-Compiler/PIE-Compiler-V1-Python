from frontend.symbol_table import SymbolTable, TypeChecker
from frontend.visitor import Visitor
from frontend.ast import *
from frontend.types import TypeInfo, canonicalize

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
        element_type = canonicalize(node.var_type.type_name)
        if self.symbol_table.lookup_symbol_current_scope(node.identifier):
            self.add_error(f"Array '{node.identifier}' already defined in this scope.")
            return None

        size = None
        if node.size:
            # For now, we only support integer literals for array sizes.
            # A more advanced implementation would handle constant expressions.
            if isinstance(node.size, Primary) and node.size.value.isdigit():
                size = int(node.size.value)
            else:
                self.add_error("Array size must be a constant integer.")

        if node.initializer:
            if isinstance(node.initializer, InitializerList):
                init_list_exprs = node.initializer.values

                # If size is declared, check if initializer is too long
                if size is not None and size < len(init_list_exprs):
                    self.add_error(f"Too many initializers for array '{node.identifier}'")

                # If no size is given, it's inferred from the initializer
                if size is None:
                    size = len(init_list_exprs)

                # Type-check each element in the initializer list
                for expr in init_list_exprs:
                    expr_type = self.visit(expr)
                    if not self.type_checker.is_compatible(element_type, expr_type):
                        self.add_error(f"Type mismatch in initializer for array '{node.identifier}'. Expected {element_type}, got {expr_type}")
            else: # Initializer is an expression
                expr_type = self.visit(node.initializer)
                if not expr_type or not isinstance(expr_type, TypeInfo) or not expr_type.is_array:
                    self.add_error(f"Array '{node.identifier}' must be initialized with an array or an initializer list.")
                elif expr_type.base != element_type:
                    self.add_error(f"Type mismatch in array assignment. Cannot assign array of {expr_type.base} to array of {element_type}")

        # All arrays are dynamic in the new model.
        # The 'size' is treated as an initial capacity/size.
        ti = TypeInfo(base=element_type, is_array=True, is_dynamic=True, size=size)
        self.symbol_table.add_symbol(node.identifier, ti, is_initialized=True)
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
        arr_info = self.symbol_table.get_array_info(node.name)
        if not arr_info:
            self.add_error(f"Undefined array: '{node.name}'")
            return None
        key_type = self.visit(node.key)
        if key_type != 'KEYWORD_INT':
            self.add_error("Array index must be an integer.")
        node.element_type = 'KEYWORD_' + arr_info.base.upper()
        return node.element_type

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

        arr_type = self.visit(args[0])
        if not isinstance(arr_type, TypeInfo) or not arr_type.is_array:
            self.add_error(f"First argument to '{func_name}' must be an array.")
            return None

        elem_type_str = arr_type.base

        def get_arg_type_str(index):
            arg_type = self.visit(args[index])
            return arg_type.base if isinstance(arg_type, TypeInfo) else arg_type

        if func_name == 'arr_push':
            if len(args) != 2:
                self.add_error("arr_push expects 2 args")
                return None
            vtype_str = get_arg_type_str(1)
            if not self.type_checker.is_compatible(elem_type_str, vtype_str):
                self.add_error(f"Type mismatch push {vtype_str} into {elem_type_str}")
            return 'void'
        if func_name == 'arr_pop':
            if len(args) != 1:
                self.add_error("arr_pop expects 1 arg")
            return elem_type_str
        if func_name == 'arr_size':
            if len(args) != 1:
                self.add_error("arr_size expects 1 arg")
            return 'int'
        if func_name in ['arr_contains', 'arr_indexof']:
            if len(args) != 2:
                self.add_error(f"{func_name} expects 2 args")
                return None
            vtype_str = get_arg_type_str(1)
            if not self.type_checker.is_compatible(elem_type_str, vtype_str):
                self.add_error(f"{func_name} type mismatch")
            return 'boolean' if func_name == 'arr_contains' else 'int'
        if func_name == 'arr_avg':
            if elem_type_str not in ('int', 'float'):
                self.add_error("arr_avg only on int/float arrays")
            if len(args) not in (1, 2):
                self.add_error("arr_avg expects 1 or 2 args")
                return None
            if len(args) == 2 and get_arg_type_str(1) != 'int':
                self.add_error("arr_avg precision must be int")
            return 'float'

        self.add_error(f"Unknown array function '{func_name}'")
        return None

    def visit_functioncall(self, node):
        if node.name.startswith('arr_'):
            return self.visit_array_function_call(node)
        function_symbol = self.symbol_table.lookup_function(node.name)
        if not function_symbol:
            if hasattr(self, f'visit_{node.name.lower()}'):
                 return getattr(self, f'visit_{node.name.lower()}')(node)
            self.add_error(f"Undefined function: '{node.name}'")
            return None

        param_types = function_symbol.get('param_types', [])
        if len(node.args) != len(param_types):
            self.add_error(f"Incorrect number of arguments for function '{node.name}'. Expected {len(param_types)}, got {len(node.args)}.")

        for i, arg_expr in enumerate(node.args):
            arg_type = self.visit(arg_expr)
            arg_type_str = arg_type.base if isinstance(arg_type, TypeInfo) else arg_type
            if i < len(param_types):
                param_type_str = param_types[i]
                if not self.type_checker.is_compatible(param_type_str, arg_type_str):
                    is_math_func = node.name in ["sqrt", "pow", "sin", "cos"]
                    if not (is_math_func and param_type_str == 'float' and arg_type_str == 'int'):
                        self.add_error(f"Type mismatch for argument {i+1} of function '{node.name}'. Expected {param_type_str}, got {arg_type_str}.")

        return_type = function_symbol.get('return_type')
        if return_type.endswith('[]'): # e.g. "int[]"
            base_type = return_type[:-2]
            return TypeInfo(base=base_type, is_array=True, is_dynamic=True)
        return return_type

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

        lhs_type_str = lhs_type.base if isinstance(lhs_type, TypeInfo) else lhs_type
        expr_type_str = expr_type.base if isinstance(expr_type, TypeInfo) else expr_type

        if lhs_type and expr_type and not self.type_checker.is_compatible(lhs_type_str, expr_type_str):
             # Special case for assigning an array to another
            if isinstance(lhs_type, TypeInfo) and isinstance(expr_type, TypeInfo) and lhs_type.is_array and expr_type.is_array:
                if lhs_type.base != expr_type.base:
                    self.add_error(f"Type mismatch in array assignment: Cannot assign array of {expr_type.base} to array of {lhs_type.base}")
            else:
                self.add_error(f"Type mismatch in assignment: Cannot assign {expr_type_str} to {lhs_type_str}")

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

        is_left_array = isinstance(left_type, TypeInfo) and left_type.is_array
        is_right_array = isinstance(right_type, TypeInfo) and right_type.is_array

        if node.op == '+' and is_left_array and is_right_array:
            if left_type.base == right_type.base:
                return TypeInfo(base=left_type.base, is_array=True, is_dynamic=True)
            else:
                self.add_error(f"Cannot concatenate arrays of different element types: {left_type.base} and {right_type.base}")
                return None

        left_type_str = left_type.base if isinstance(left_type, TypeInfo) else left_type
        right_type_str = right_type.base if isinstance(right_type, TypeInfo) else right_type

        result_type = self.type_checker.check_binary_op(op_token_name, left_type_str, right_type_str)
        if not result_type:
            self.add_error(f"Invalid operation: {left_type_str} {node.op} {right_type_str}")
            return None

        node.result_type = result_type
        return result_type

    def visit_unaryop(self, node):
        expr_type = self.visit(node.operand)
        if not expr_type:
            return None

        expr_type_str = expr_type.base if isinstance(expr_type, TypeInfo) else expr_type
        if node.op == '-' and expr_type_str in ('int', 'float'):
            return expr_type
        else:
            self.add_error(f"Invalid unary operation: {node.op} {expr_type_str}")
            return None

    def visit_primary(self, node):
        value = node.value
        if not isinstance(value, str):
            return None

        if value.startswith('"') and value.endswith('"'):
            return 'string'
        elif value.startswith("'") and value.endswith("'"):
            return 'char'
        elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
            return 'int'
        elif '.' in value:
            try:
                float(value)
                return 'float'
            except ValueError:
                pass # Not a float, might be something else
        elif value in ['true', 'false']:
            return 'boolean'
        elif value == 'null':
            return 'null'

        # Fallback for identifiers that are not keywords but are parsed as primary.
        # This can happen in certain grammar contexts. Let's try to resolve it.
        if self.symbol_table.lookup_symbol(value):
             return self.visit_identifier(Identifier(value))

        self.add_error(f"Internal error or undefined symbol: Unhandled primary value '{value}'")
        return None

    def visit_identifier(self, node):
        symbol = self.symbol_table.lookup_symbol(node.name)
        if symbol:
            return symbol.get('type')
        else:
            self.add_error(f"Undefined variable: '{node.name}'")
            return None

    def visit_ifstatement(self, node):
        cond_type = self.visit(node.condition)
        cond_type_str = cond_type.base if isinstance(cond_type, TypeInfo) else cond_type
        if cond_type_str and cond_type_str not in ('boolean', 'null'):
            self.add_error(f"Condition must be boolean, got {cond_type_str}")

        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)
        return None

    def visit_whilestatement(self, node):
        cond_type = self.visit(node.condition)
        cond_type_str = cond_type.base if isinstance(cond_type, TypeInfo) else cond_type
        if cond_type_str and cond_type_str not in ('boolean', 'null'):
            self.add_error(f"Loop condition must be boolean, got {cond_type_str}")

        self.visit(node.body)
        return None

    def visit_dowhilestatement(self, node):
        self.visit(node.body)
        cond_type = self.visit(node.condition)
        cond_type_str = cond_type.base if isinstance(cond_type, TypeInfo) else cond_type
        if cond_type_str and cond_type_str not in ('boolean', 'null'):
            self.add_error(f"Loop condition must be boolean, got {cond_type_str}")
        return None

    def visit_switchstatement(self, node):
        expr_type = self.visit(node.expression)
        expr_type_str = expr_type.base if isinstance(expr_type, TypeInfo) else expr_type
        if expr_type_str != 'int':
            self.add_error("Switch expression must be an integer.")

        was_in_switch = self.in_switch
        self.in_switch = True

        case_labels = set()
        for case_clause in node.cases:
            self.visit(case_clause)
            if case_clause.value != 'default':
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
            cond_type_str = cond_type.base if isinstance(cond_type, TypeInfo) else cond_type
            if cond_type_str and cond_type_str not in ('boolean', 'null'):
                self.add_error(f"Loop condition must be boolean, got {cond_type_str}")
        if node.update:
            self.visit(node.update)

        self.visit(node.body)
        self.symbol_table.exit_scope()
        return None

    def visit_systemoutput(self, node):
        expr_type = self.visit(node.expression)
        expected_type_name = node.output_type.type_name

        if expected_type_name == 'array':
            if not (isinstance(expr_type, TypeInfo) and expr_type.is_array):
                 self.add_error('Output of type "array" expects an array variable.')
            return None

        expr_type_str = expr_type.base if isinstance(expr_type, TypeInfo) else expr_type

        # Allow printing bools with 'int' type specifier for simplicity
        if expected_type_name == 'int' and expr_type_str == 'boolean':
             return None

        if expr_type_str and expr_type_str != expected_type_name:
            self.add_error(f"Type mismatch in output: Expression is {expr_type_str}, but output type is {expected_type_name}")

        if node.precision:
            precision_type = self.visit(node.precision)
            precision_type_str = precision_type.base if isinstance(precision_type, TypeInfo) else precision_type
            if precision_type_str != 'int':
                self.add_error('Output precision must be int')
        return None

    def visit_systeminput(self, node):
        self.visit(node.variable)
        return None

    def visit_systemexit(self, node):
        return None

    def visit_returnstatement(self, node):
        if not self.current_function:
            self.add_error("Return statement outside of a function.")
            return None

        return_type = self.current_function.get('return_type')
        return_type_str = return_type.base if isinstance(return_type, TypeInfo) else return_type

        if node.value:
            expr_type = self.visit(node.value)
            expr_type_str = expr_type.base if isinstance(expr_type, TypeInfo) else expr_type
            if return_type_str == 'void':
                self.add_error(f"Function with void return type cannot return a value.")
            elif not self.type_checker.is_compatible(return_type_str, expr_type_str):
                self.add_error(f"Type mismatch in return statement. Expected {return_type_str}, got {expr_type_str}.")
        else:
            if return_type_str != 'void':
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