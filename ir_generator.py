class IRGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_scope = 0
        self.symbol_map = {}
        self.previous_instruction = None  # Track the last instruction

    def _emit(self, instruction):
        """Emit instruction and auto-insert GOTO before LABEL if needed"""
        if instruction[0] == "LABEL":
            if self.previous_instruction and self.previous_instruction[0] not in ("GOTO", "IF_FALSE", "RETURN", "EXIT"):
                label = instruction[1]
                self.code.append(("GOTO", label))
                self.previous_instruction = ("GOTO", label)
        self.code.append(instruction)
        self.previous_instruction = instruction

    def generate(self, ast, symbol_table):
        self.symbol_table = symbol_table
        self.code = []
        self.previous_instruction = None
        self._process_node(ast)
        return self.code

    def _process_node(self, node):
        if not isinstance(node, tuple):
            return None
        method_name = f"_process_{node[0]}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            self._process_children(node)
            return None

    def _process_children(self, node):
        if isinstance(node, tuple):
            for child in node[1:]:
                self._process_node(child)
        elif isinstance(node, list):
            for child in node:
                self._process_node(child)

    def _get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def _get_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def _get_var_name(self, original_name, is_declaration=False):
        if is_declaration:
            key = (self.current_scope, original_name)
            ir_name = f"{original_name}_{self.current_scope}"
            self.symbol_map[key] = ir_name
            return ir_name
        else:
            for scope_idx in range(self.current_scope, -1, -1):
                key = (scope_idx, original_name)
                if key in self.symbol_map:
                    return self.symbol_map[key]
            raise NameError(f"Variable '{original_name}' not found in scope {self.current_scope} or outer scopes.")

    def _process_program(self, node):
        self._emit(("START_PROGRAM",))
        for statement in node[1]:
            self._process_node(statement)
        self._emit(("END_PROGRAM",))

    def _process_declaration(self, node):
        var_type, var_name, init_expr = node[1], node[2], node[3]
        ir_var = self._get_var_name(var_name, is_declaration=True)
        self._emit(("DECLARE", var_type, ir_var))
        if init_expr:
            expr_result = self._process_expression(init_expr)
            self._emit(("ASSIGN", ir_var, expr_result))

    def _process_assignment(self, node):
        var_name, expr = node[1], node[2]
        ir_var = self._get_var_name(var_name)
        expr_result = self._process_expression(expr)
        self._emit(("ASSIGN", ir_var, expr_result))

    def _process_expression(self, node):
        if not isinstance(node, tuple):
            if isinstance(node, str):
                symbol = self.symbol_table.lookup_symbol(node)
                if symbol:
                    return self._get_var_name(node)
            return str(node)

        node_type = node[0]
        if node_type == 'primary':
            value = node[1]
            if isinstance(value, str):
                symbol = self.symbol_table.lookup_symbol(value)
                if symbol:
                    return self._get_var_name(value)
            return value

        elif node_type == 'binary_op':
            operator, left_expr, right_expr = node[1], node[2], node[3]
            left_result = self._process_expression(left_expr)
            right_result = self._process_expression(right_expr)
            result_var = self._get_temp()
            self._emit(("BINARY_OP", operator, result_var, left_result, right_result))
            return result_var

        elif node_type == 'unary_op':
            operator, expr = node[1], node[2]
            expr_result = self._process_expression(expr)
            result_var = self._get_temp()
            self._emit(("UNARY_OP", operator, result_var, expr_result))
            return result_var

        return self._process_node(node)

    def _process_if(self, node):
        condition, then_stmt, else_stmt = node[1], node[2], node[3]
        else_label = self._get_label()
        end_label = self._get_label()
        condition_result = self._process_expression(condition)

        if else_stmt:
            self._emit(("IF_FALSE", condition_result, else_label))
        else:
            self._emit(("IF_FALSE", condition_result, end_label))

        self._process_node(then_stmt)

        if else_stmt:
            self._emit(("GOTO", end_label))
            self._emit(("LABEL", else_label))
            self._process_node(else_stmt)

        self._emit(("LABEL", end_label))

    def _process_while(self, node):
        condition, body = node[1], node[2]
        start_label = self._get_label()
        end_label = self._get_label()
        self._emit(("LABEL", start_label))
        condition_result = self._process_expression(condition)
        self._emit(("IF_FALSE", condition_result, end_label))
        self._process_node(body)
        self._emit(("GOTO", start_label))
        self._emit(("LABEL", end_label))

    def _process_for(self, node):
        init, condition, update, body = node[1], node[2], node[3], node[4]
        start_label = self._get_label()
        update_label = self._get_label()
        end_label = self._get_label()
        if init:
            self._process_node(init)
        self._emit(("LABEL", start_label))
        if condition:
            condition_result = self._process_expression(condition)
            self._emit(("IF_FALSE", condition_result, end_label))
        self._process_node(body)
        self._emit(("LABEL", update_label))
        if update:
            self._process_node(update)
        self._emit(("GOTO", start_label))
        self._emit(("LABEL", end_label))

    def _process_return(self, node):
        expr = node[1]
        if expr:
            expr_result = self._process_expression(expr)
            self._emit(("RETURN", expr_result))
        else:
            self._emit(("RETURN",))

    def _process_block(self, node):
        statement_list = node[1]
        old_scope = self.current_scope
        self.current_scope += 1
        for statement in statement_list:
            self._process_node(statement)
        self.current_scope = old_scope

    def _process_system_input(self, node):
        var_node, var_type = node[1], node[2]
        var_name = var_node[1] if isinstance(var_node, tuple) and var_node[0] == 'primary' else var_node
        ir_var = self._get_var_name(var_name)
        self._emit(("INPUT", ir_var, var_type))

    def _process_system_output(self, node):
        expr, output_type = node[1], node[2]
        expr_result = self._get_var_name(expr) if isinstance(expr, str) else self._process_expression(expr)
        self._emit(("OUTPUT", expr_result, output_type))

    def _process_system_exit(self, node):
        self._emit(("EXIT",))
        return None
