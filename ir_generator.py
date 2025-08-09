class IRGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.switch_end_labels = []

    def _get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def _get_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate(self, ast, symbol_table):
        self.symbol_table = symbol_table
        self.code = []
        self._process_node(ast)
        return self.code

    def _process_node(self, node):
        if isinstance(node, list):
            for item in node:
                self._process_node(item)
            return

        if not isinstance(node, tuple):
            return None

        method_name = f"_process_{node[0]}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            # Fallback for nodes that don't have a specific processor
            for child in node[1:]:
                self._process_node(child)
            return None

    def _process_program(self, node):
        statements = node[1]

        has_top_level_statements = any(stmt[0] != 'function_definition' for stmt in statements)

        # Process all function definitions first
        for stmt in statements:
            if stmt[0] == 'function_definition':
                self._process_node(stmt)

        # Then, if there are top-level statements, process them in an implicit main function
        if has_top_level_statements:
            self.code.append(("FUNC_START", "main", "int", []))
            for stmt in statements:
                if stmt[0] != 'function_definition':
                    self._process_node(stmt)
            self.code.append(("FUNC_END", "main"))

    def _process_function_definition(self, node):
        _, return_type, name, params, body = node
        self.code.append(("FUNC_START", name, return_type, params))
        self._process_node(body)
        self.code.append(("FUNC_END", name))

    def _process_declaration(self, node):
        var_type, var_name, init_expr = node[1], node[2], node[3]
        self.code.append(("DECLARE", var_type, var_name))
        if init_expr:
            expr_result = self._process_expression(init_expr)
            self.code.append(("ASSIGN", var_name, expr_result))

    def _process_array_declaration(self, node):
        element_type, name, size, init_list, is_dynamic = node[1], node[2], node[3], node[4], node[5]

        if is_dynamic:
            # Dynamic array
            create_func = f"d_array_{element_type.replace('KEYWORD_', '').lower()}_create"
            append_func = f"d_array_{element_type.replace('KEYWORD_', '').lower()}_append"

            self.code.append(("DECLARE", f"d_array_{element_type.replace('KEYWORD_', '').lower()}", name))

            # Call create function
            temp = self._get_temp()
            self.code.append(("CALL", create_func, 0, temp))
            self.code.append(("ASSIGN", name, temp))

            if init_list:
                init_values = [self._process_expression(expr) for expr in init_list[1]]
                for val in init_values:
                    self.code.append(("PARAM", name))
                    self.code.append(("PARAM", val))
                    self.code.append(("CALL", append_func, 2, self._get_temp()))

        else:
            # Static array
            if size:
                size = self._process_expression(size)
            self.code.append(("DECLARE_ARRAY", element_type, name, size))
            if init_list:
                init_values = [self._process_expression(expr) for expr in init_list[1]]
                for i, val in enumerate(init_values):
                    self.code.append(("STORE_ARRAY", name, i, val))

    def _get_value_type(self, node):
        if not isinstance(node, tuple):
            if isinstance(node, str):
                if node.isdigit() or (node.startswith('-') and node[1:].isdigit()):
                    return 'int'
                elif '.' in node:
                    return 'float'
                elif node.startswith('"'):
                    return 'string'
                elif node.startswith("'"):
                    return 'char'
                elif node in ['true', 'false']:
                    return 'boolean'
                elif node == 'null':
                    return 'null'
                else:
                    symbol = self.symbol_table.lookup_symbol(node)
                    if symbol:
                        return symbol.get('type')
            return None

        node_type = node[0]
        if node_type == 'primary':
            return self._get_value_type(node[1])
        elif node_type == 'function_call':
            func_symbol = self.symbol_table.lookup_function(node[1])
            if func_symbol:
                return func_symbol.get('return_type')
        elif node_type == 'binary_op':
            return node[4] # result_type is stored in the node
        return None

    def _process_dictionary_literal(self, node):
        key_value_pairs = node[1]
        dict_var = self._get_temp()
        self.code.append(("CALL", "dict_create", 0, dict_var))

        for key_expr, value_expr in key_value_pairs:
            key = self._process_expression(key_expr)
            value = self._process_expression(value_expr)
            value_type = self._get_value_type(value_expr)

            new_func = f"new_{value_type.replace('KEYWORD_', '').lower()}"

            value_var = self._get_temp()
            self.code.append(("PARAM", value))
            self.code.append(("CALL", new_func, 1, value_var))

            self.code.append(("PARAM", dict_var))
            self.code.append(("PARAM", key))
            self.code.append(("PARAM", value_var))
            self.code.append(("CALL", "dict_set", 3, self._get_temp()))

        return dict_var

    def _process_subscript_access(self, node):
        name, key_expr, element_type = node[1], node[2], node[3]
        symbol = self.symbol_table.lookup_symbol(name)

        if symbol and symbol.get('type') == 'array':
            if symbol.get('is_dynamic'):
                get_func = f"d_array_{element_type.replace('KEYWORD_', '').lower()}_get"
                index = self._process_expression(key_expr)
                temp = self._get_temp()
                self.code.append(("PARAM", name))
                self.code.append(("PARAM", index))
                self.code.append(("CALL", get_func, 2, temp))
                return temp
            else:
                index = self._process_expression(key_expr)
                temp = self._get_temp()
                self.code.append(("LOAD_ARRAY", temp, name, index))
                return temp
        elif symbol and symbol.get('type') == 'KEYWORD_DICT':
            key = self._process_expression(key_expr)
            temp = self._get_temp()
            self.code.append(("PARAM", name))
            self.code.append(("PARAM", key))
            self.code.append(("CALL", "dict_get", 2, temp))
            return temp
        else:
            raise Exception("Subscript access on non-array/dictionary type")

    def _process_assignment(self, node):
        lhs, expr = node[1], node[2]

        if isinstance(lhs, tuple) and lhs[0] == 'subscript_access':
            name, key_expr, element_type = lhs[1], lhs[2], lhs[3]
            symbol = self.symbol_table.lookup_symbol(name)

            if symbol and symbol.get('type') == 'array':
                if symbol.get('is_dynamic'):
                    set_func = f"d_array_{element_type.replace('KEYWORD_', '').lower()}_set"
                    index = self._process_expression(key_expr)
                    value = self._process_expression(expr)
                    self.code.append(("PARAM", name))
                    self.code.append(("PARAM", index))
                    self.code.append(("PARAM", value))
                    self.code.append(("CALL", set_func, 3, self._get_temp()))
                else:
                    index = self._process_expression(key_expr)
                    value = self._process_expression(expr)
                    self.code.append(("STORE_ARRAY", name, index, value))
            elif symbol and symbol.get('type') == 'KEYWORD_DICT':
                key = self._process_expression(key_expr)
                value = self._process_expression(expr)
                value_type = self._get_value_type(expr)

                new_func = f"new_{value_type.replace('KEYWORD_', '').lower()}"

                value_var = self._get_temp()
                self.code.append(("PARAM", value))
                self.code.append(("CALL", new_func, 1, value_var))

                self.code.append(("PARAM", name))
                self.code.append(("PARAM", key))
                self.code.append(("PARAM", value_var))
                self.code.append(("CALL", "dict_set", 3, self._get_temp()))

        else:
            # Regular variable assignment
            expr_result = self._process_expression(expr)
            self.code.append(("ASSIGN", lhs, expr_result))

    def _process_expression(self, node):
        if not isinstance(node, tuple):
            return node

        node_type = node[0]
        if node_type == 'primary':
            return node[1]
        elif node_type == 'function_call':
            return self._process_function_call(node)
        elif node_type == 'binary_op':
            operator, left_expr, right_expr, op_type = node[1], node[2], node[3], node[4]
            left_result = self._process_expression(left_expr)
            right_result = self._process_expression(right_expr)

            result_var = self._get_temp()
            if op_type == 'KEYWORD_STRING':
                 self.code.append(("CONCAT_STRINGS", result_var, left_result, right_result))
            else:
                self.code.append(("BINARY_OP", operator, result_var, left_result, right_result))
            return result_var
        elif node_type == 'unary_op':
            operator, expr = node[1], node[2]
            expr_result = self._process_expression(expr)
            result_var = self._get_temp()
            self.code.append(("UNARY_OP", operator, result_var, expr_result))
            return result_var
        return self._process_node(node)

    def _process_function_call(self, node):
        name, args = node[1], node[2]
        arg_results = [self._process_expression(arg) for arg in args]
        for arg_result in arg_results:
            self.code.append(("PARAM", arg_result))

        result_var = self._get_temp()
        self.code.append(("CALL", name, len(args), result_var))
        return result_var

    def _process_if(self, node):
        condition, then_stmt, else_stmt = node[1], node[2], node[3]
        else_label = self._get_label()
        end_label = self._get_label()
        condition_result = self._process_expression(condition)

        if else_stmt:
            self.code.append(("IF_FALSE", condition_result, else_label))
        else:
            self.code.append(("IF_FALSE", condition_result, end_label))

        self._process_node(then_stmt)

        if else_stmt:
            self.code.append(("GOTO", end_label))
            self.code.append(("LABEL", else_label))
            self._process_node(else_stmt)

        self.code.append(("LABEL", end_label))

    def _process_block(self, node):
        self._process_node(node[1])

    def _process_while(self, node):
        condition, body = node[1], node[2]
        start_label = self._get_label()
        end_label = self._get_label()
        self.code.append(("LABEL", start_label))
        condition_result = self._process_expression(condition)
        self.code.append(("IF_FALSE", condition_result, end_label))
        self._process_node(body)
        self.code.append(("GOTO", start_label))
        self.code.append(("LABEL", end_label))

    def _process_do_while(self, node):
        body, condition = node[1], node[2]
        start_label = self._get_label()
        self.code.append(("LABEL", start_label))
        self._process_node(body)
        condition_result = self._process_expression(condition)
        self.code.append(("IF_TRUE", condition_result, start_label))

    def _process_switch(self, node):
        expression, case_list = node[1], node[2]
        expr_result = self._process_expression(expression)

        end_label = self._get_label()
        self.switch_end_labels.append(end_label)

        default_label = None
        case_targets = []

        case_label_map = {}
        for case_clause in case_list:
            if case_clause[0] == 'case':
                case_value_node = case_clause[1]
                case_value = int(self._process_expression(case_value_node))
                if case_value not in case_label_map:
                    case_label_map[case_value] = self._get_label()
            elif case_clause[0] == 'default':
                if default_label is None:
                    default_label = self._get_label()

        if default_label is None:
            default_label = end_label

        for value, label in case_label_map.items():
            case_targets.append((value, label))

        self.code.append(("SWITCH", expr_result, default_label, case_targets))

        for case_clause in case_list:
            if case_clause[0] == 'case':
                case_value_node, statements = case_clause[1], case_clause[2]
                case_value = int(self._process_expression(case_value_node))
                self.code.append(("LABEL", case_label_map[case_value]))
                self._process_node(statements)
            elif case_clause[0] == 'default':
                self.code.append(("LABEL", default_label))
                self._process_node(case_clause[1])

        self.code.append(("LABEL", end_label))
        self.switch_end_labels.pop()

    def _process_break(self, node):
        if not self.switch_end_labels:
            # This should be caught by the semantic analyzer, but as a safeguard:
            raise Exception("Break statement outside of switch")
        end_label = self.switch_end_labels[-1]
        self.code.append(("GOTO", end_label))

    def _process_for(self, node):
        init, condition, update, body = node[1], node[2], node[3], node[4]
        start_label = self._get_label()
        end_label = self._get_label()

        if init:
            self._process_node(init)

        self.code.append(("LABEL", start_label))

        if condition:
            condition_result = self._process_expression(condition)
            self.code.append(("IF_FALSE", condition_result, end_label))

        self._process_node(body)

        if update:
            self._process_node(update)

        self.code.append(("GOTO", start_label))
        self.code.append(("LABEL", end_label))

    def _process_return(self, node):
        expr = node[1]
        if expr:
            expr_result = self._process_expression(expr)
            self.code.append(("RETURN", expr_result))
        else:
            self.code.append(("RETURN", None))

    def _process_system_input(self, node):
        var_node, var_type = node[1], node[2]
        var_name = var_node[1] if isinstance(var_node, tuple) and var_node[0] == 'primary' else var_node
        self.code.append(("INPUT", var_name, var_type))

    def _process_system_output(self, node):
        expr, output_type, precision = node[1], node[2], node[3]
        expr_result = self._process_expression(expr)
        precision_result = self._process_expression(precision) if precision else '2' # Default to 2dp
        self.code.append(("OUTPUT", expr_result, output_type, precision_result))

    def _process_system_exit(self, node):
        self.code.append(("EXIT",))
