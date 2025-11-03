from frontend.symbol_table import SymbolTable, TypeChecker
from frontend.visitor import Visitor
from frontend.ast import *
from frontend.types import TypeInfo, canonicalize
from frontend.module_resolver import ModuleResolver, ModuleNotFoundError, ModuleError
from pathlib import Path

class SemanticAnalyzer(Visitor):
    def __init__(self, symbol_table, module_resolver=None):
        self.symbol_table = symbol_table
        self.type_checker = TypeChecker(self.symbol_table)
        self.errors = []
        self.warnings = []
        self.error_set = set()
        self.current_function = None
        self.in_switch = False
        self.module_resolver = module_resolver or ModuleResolver()
        self.imported_modules = {}  # Track imported modules: {namespace: ModuleInfo}
        self._register_builtin_functions()

    def _register_builtin_functions(self):
        """Register all built-in functions in the symbol table"""
        builtins = [
            # Type conversion functions
            ('string_to_int', 'int', [('string', 'str')]),
            ('string_to_float', 'float', [('string', 'str')]),
            ('string_to_char', 'char', [('string', 'str')]),
            ('char_to_int', 'int', [('char', 'c')]),
            ('int_to_char', 'char', [('int', 'value')]),
            ('int_to_float', 'float', [('int', 'value')]),
            ('float_to_int', 'int', [('float', 'value')]),
            
            # Cryptography functions
            ('caesar_cipher', 'string', [('string', 'text'), ('int', 'shift')]),
            ('caesar_decipher', 'string', [('string', 'text'), ('int', 'shift')]),
            ('rot13', 'string', [('string', 'text')]),
            ('char_shift', 'string', [('string', 'text'), ('int', 'shift')]),
            ('reverse_string', 'string', [('string', 'text')]),
            ('xor_cipher', 'string', [('string', 'text'), ('string', 'key')]),
            
            # String utilities
            ('string_to_upper', 'string', [('string', 'str')]),
            ('string_to_lower', 'string', [('string', 'str')]),
            ('string_trim', 'string', [('string', 'str')]),
            ('string_substring', 'string', [('string', 'str'), ('int', 'start'), ('int', 'length')]),
            ('string_index_of', 'int', [('string', 'haystack'), ('string', 'needle')]),
            ('string_replace_char', 'string', [('string', 'str'), ('char', 'old'), ('char', 'new')]),
            ('string_reverse', 'string', [('string', 'str')]),
            ('string_count_char', 'int', [('string', 'str'), ('char', 'ch')]),
            ('strlen', 'int', [('string', 'str')]),
            ('string_char_at', 'char', [('string', 'str'), ('int', 'index')]),
            ('string_split', 'string[]', [('string', 'str'), ('string', 'delimiter'), ('int', 'count')]),
            ('string_split_to_array', 'string[]', [('string', 'str'), ('string', 'delimiter')]),
            
            # File I/O
            ('file_open', 'file', [('string', 'path'), ('string', 'mode')]),
            ('file_close', 'void', [('file', 'f')]),
            ('file_write', 'void', [('file', 'f'), ('string', 'data')]),
            ('file_flush', 'void', [('file', 'f')]),
            ('file_read_all', 'string', [('file', 'f')]),
            ('file_read_line', 'string', [('file', 'f')]),
            
            # Math functions
            ('sqrt', 'float', [('float', 'x')]),
            ('pow', 'float', [('float', 'base'), ('float', 'exp')]),
            ('abs', 'float', [('float', 'x')]),
            ('floor', 'float', [('float', 'x')]),
            ('ceil', 'float', [('float', 'x')]),
            ('round', 'float', [('float', 'x')]),
            ('sin', 'float', [('float', 'x')]),
            ('cos', 'float', [('float', 'x')]),
            ('tan', 'float', [('float', 'x')]),
            
            # Regex
            ('regex_compile', 'regex', [('string', 'pattern')]),
            ('regex_match', 'int', [('regex', 'pattern'), ('string', 'str')]),
            ('regex_free', 'void', [('regex', 'pattern')]),
            
            # Time functions
            ('get_timestamp', 'int', []),
            ('format_time', 'string', [('int', 'timestamp'), ('string', 'format')]),
        ]
        
        for func_name, return_type, params in builtins:
            param_list = [{'type': ptype, 'name': pname} for ptype, pname in params]
            param_types = [ptype for ptype, pname in params]
            self.symbol_table.add_symbol(
                func_name,
                'function',
                params=param_list,
                param_types=param_types,
                return_type=return_type
            )

    def add_error(self, error_msg):
        if error_msg not in self.error_set:
            self.error_set.add(error_msg)
            self.errors.append(error_msg)

    def analyze(self, ast, source_file=None):
        if not ast:
            return False, None
        
        # Store source file directory for module resolution
        if source_file:
            from pathlib import Path
            self.source_file_dir = Path(source_file).parent
        else:
            self.source_file_dir = None

        self.visit(ast)

        # The AST is modified in-place, so we return the original AST object
        return len(self.errors) == 0, ast

    def visit_program(self, node):
        for stmt in node.statements:
            self.visit(stmt)
        return None
    
    def visit_importstatement(self, node):
        """Process import statements and register module symbols."""
        try:
            # Get source file directory for relative imports
            source_file_dir = getattr(self, 'source_file_dir', None)
            
            # Resolve the module
            module_info = self.module_resolver.resolve_module(node.module_name, source_file_dir)
            node.resolved_path = module_info.pie_file
            node.module_info = module_info
            
            # Register module namespace
            namespace = node.alias or node.module_name
            self.imported_modules[namespace] = module_info
            
            # If it's a user-defined module, parse it to extract exports
            if module_info.is_user_module:
                self._process_user_module(module_info, namespace)
            else:
                # For stdlib modules, use metadata
                # Register module functions in symbol table with namespace
                for func in module_info.get_functions():
                    full_name = f"{namespace}.{func['name']}"
                    self._register_module_function(full_name, func)
                
                # Register module types
                for type_def in module_info.get_types():
                    type_name = f"{namespace}.{type_def['name']}"
                    self.symbol_table.add_symbol(
                        type_name,
                        'type',
                        type_kind=type_def['type']
                    )
                
        except (ModuleNotFoundError, ModuleError) as e:
            self.add_error(str(e))
        
        return None
    
    def _process_user_module(self, module_info, namespace):
        """
        Parse a user-defined .pie module and extract exported functions.
        
        Args:
            module_info: ModuleInfo object for the user module
            namespace: Namespace to use for imported symbols
        """
        from frontend.parser import Parser
        
        # Read the module file
        with open(module_info.pie_file, 'r') as f:
            source_code = f.read()
        
        # Create a new parser and parse the module
        parser = Parser()
        try:
            module_ast = parser.parse(source_code)
        except Exception as e:
            self.add_error(f"Failed to parse user module {module_info.name}: {e}")
            return
        
        if not module_ast or not module_ast.statements:
            self.add_error(f"User module {module_info.name} has no statements")
            return
        
        # FIRST: Process any imports in this module (transitive dependencies)
        # This ensures that if testlayers imports mathutils, mathutils gets processed
        module_dir = Path(module_info.pie_file).parent
        for stmt in module_ast.statements:
            if isinstance(stmt, ImportStatement):
                import_name = stmt.module_name
                # Only process if not already imported
                if import_name not in self.imported_modules:
                    try:
                        # Resolve the transitive import
                        transitive_module_info = self.module_resolver.resolve_module(import_name, module_dir)
                        self.imported_modules[import_name] = transitive_module_info
                        
                        # If it's also a user module, recursively process it
                        if transitive_module_info.is_user_module:
                            self._process_user_module(transitive_module_info, import_name)
                        else:
                            # For stdlib modules, register functions
                            for func in transitive_module_info.get_functions():
                                full_name = f"{import_name}.{func['name']}"
                                self._register_module_function(full_name, func)
                            # Register module types
                            for type_def in transitive_module_info.get_types():
                                type_name = f"{import_name}.{type_def['name']}"
                                self.symbol_table.add_symbol(
                                    type_name,
                                    'type',
                                    type_kind=type_def['type']
                                )
                    except (ModuleNotFoundError, ModuleError) as e:
                        self.add_error(f"Failed to import transitive dependency {import_name} from {module_info.name}: {e}")
        
        # SECOND: Extract exported functions and register them (NO semantic analysis on module)
        for stmt in module_ast.statements:
            if isinstance(stmt, FunctionDefinition) and stmt.is_exported:
                # Register the exported function in the symbol table
                full_name = f"{namespace}.{stmt.name}"
                
                # Build parameter list
                params = []
                param_types = []
                for param in stmt.params:
                    # Extract type string from TypeSpecifier
                    if hasattr(param.param_type, 'type_name'):
                        type_str = param.param_type.type_name
                        if param.param_type.is_array:
                            type_str += '[]'
                    else:
                        type_str = str(param.param_type)
                    
                    params.append((type_str, param.name))  # Store as tuple (type, name)
                    param_types.append(type_str)
                
                # Get return type
                if hasattr(stmt.return_type, 'type_name'):
                    return_type = stmt.return_type.type_name
                    if stmt.return_type.is_array:
                        return_type += '[]'
                else:
                    return_type = str(stmt.return_type)
                
                self.symbol_table.add_symbol(
                    full_name,
                    'function',
                    return_type=return_type,
                    params=params,
                    param_types=param_types,
                    is_module_function=True,
                    is_user_module_function=True,
                    module_ast_node=stmt  # Store the AST node for code generation
                )
                
                # Also store the function in module metadata for later access
                if 'exported_functions' not in module_info.metadata:
                    module_info.metadata['exported_functions'] = {}
                module_info.metadata['exported_functions'][stmt.name] = stmt
    
    def _register_module_function(self, full_name, func_metadata):
        """Register a module function in the symbol table."""
        # Parse signature: "string(string url, string body)"
        signature = func_metadata['signature']
        
        # Simple signature parsing - expects format: "return_type(param_type param_name, ...)"
        if '(' not in signature:
            self.add_error(f"Invalid function signature in module: {signature}")
            return
        
        return_type_str, params_str = signature.split('(', 1)
        return_type = return_type_str.strip()
        params_str = params_str.rstrip(')')
        
        params = []
        param_types = []
        
        if params_str.strip():
            # Split by comma and parse each parameter
            param_parts = params_str.split(',')
            for param in param_parts:
                param = param.strip()
                if not param:
                    continue
                # Expected format: "type name"
                parts = param.split()
                if len(parts) >= 2:
                    param_type = ' '.join(parts[:-1])  # Handle "json.object" type
                    param_name = parts[-1]
                    params.append({'type': param_type, 'name': param_name})
                    param_types.append(param_type)
                elif len(parts) == 1:
                    # Just type, generate a name
                    param_type = parts[0]
                    param_name = f"arg{len(params)}"
                    params.append({'type': param_type, 'name': param_name})
                    param_types.append(param_type)
        
        self.symbol_table.add_symbol(
            full_name,
            'function',
            return_type=return_type,
            params=params,
            param_types=param_types,
            is_module_function=True
        )
    
    def visit_exportstatement(self, node):
        """Export statements are handled during parsing - just visit the wrapped statement."""
        # The is_exported flag has already been set on the node
        return self.visit(node)

    def visit_declaration(self, node):
        var_type_name = node.var_type.type_name
        if self.symbol_table.lookup_symbol_current_scope(node.identifier):
            self.add_error(f"Variable '{node.identifier}' already defined in this scope.")
            return None

        is_initialized = node.initializer is not None
        self.symbol_table.add_symbol(node.identifier, var_type_name, is_initialized=is_initialized)

        if node.initializer:
            # Store expected type for dict_get type inference
            old_expected_type = getattr(self, 'expected_type', None)
            self.expected_type = var_type_name
            expr_type = self.visit(node.initializer)
            if expr_type and not self.type_checker.is_compatible(var_type_name, expr_type):
                self.add_error(f"Type mismatch in declaration: Cannot assign {expr_type} to {var_type_name} variable '{node.identifier}'")
            self.expected_type = old_expected_type
        return None

    def visit_arraydeclaration(self, node):
        element_type = canonicalize(node.var_type.type_name)
        if self.symbol_table.lookup_symbol_current_scope(node.identifier):
            self.add_error(f"Array '{node.identifier}' already defined in this scope.")
            return None
        
        size = None
        dimensions = getattr(node, 'dimensions', 1)
        dimension_sizes = getattr(node, 'dimension_sizes', None)
        
        if node.size:
            if isinstance(node.size, Primary) and node.size.value.isdigit():
                size = int(node.size.value)
            else:
                self.add_error("Array size must be a constant integer.")
        
        if node.initializer:
            if isinstance(node.initializer, InitializerList):
                # Handle initializer list
                init_list_exprs = node.initializer.values
                
                # For multi-dimensional arrays, check if elements are also initializer lists
                if dimensions > 1:
                    # Each element should be an array (InitializerList)
                    for i, expr in enumerate(init_list_exprs):
                        if not isinstance(expr, InitializerList):
                            self.add_error(f"Multi-dimensional array initializer: row {i} must be an array")
                        else:
                            # Validate inner elements
                            for inner_expr in expr.values:
                                inner_type = self.visit(inner_expr)
                                if not self.type_checker.is_compatible(element_type, inner_type):
                                    self.add_error(f"Type mismatch in multi-dimensional array initializer. Expected {element_type}, got {inner_type}")
                else:
                    # Single dimensional array
                    if size is None and not node.is_dynamic:
                        size = len(init_list_exprs)
                    if size is not None and not node.is_dynamic and size < len(init_list_exprs):
                        self.add_error(f"Too many initializers for array '{node.identifier}'")
                    for expr in init_list_exprs:
                        expr_type = self.visit(expr)
                        if not self.type_checker.is_compatible(element_type, expr_type):
                            self.add_error(f"Type mismatch in initializer for array '{node.identifier}'. Expected {element_type}, got {expr_type}")
            else:
                # Handle expression initializer (like array concatenation, identifier, or subscript access)
                expr_type = self.visit(node.initializer)
                
                # Handle dynamic array types (d_array_int, d_array_string, d_array_float, d_array_char)
                if expr_type and expr_type.startswith('d_array_'):
                    # Extract the element type from d_array_TYPE
                    darray_element = expr_type.split('_', 2)[2]  # d_array_string -> string
                    if not self.type_checker.is_compatible(element_type, darray_element):
                        self.add_error(f"Type mismatch in array initialization: Cannot assign d_array of {darray_element} to array of {element_type}")
                elif expr_type == 'array':
                    # Check if this is an identifier referring to another array
                    if isinstance(node.initializer, Identifier):
                        # Get the symbol info for the source array
                        source_sym = self.symbol_table.lookup_symbol(node.initializer.name)
                        if source_sym:
                            source_ti = source_sym.get('typeinfo')
                            if source_ti and source_ti.base != element_type:
                                self.add_error(f"Type mismatch in array initialization: Cannot assign array of {source_ti.base} to array of {element_type}")
                    # Check if this is a subscript access on a multi-dimensional array
                    elif isinstance(node.initializer, SubscriptAccess):
                        # Get the symbol info for the source array
                        source_sym = self.symbol_table.lookup_symbol(node.initializer.name)
                        if source_sym:
                            source_ti = source_sym.get('typeinfo')
                            # For multi-dimensional arrays, subscript access returns an array of the base type
                            if source_ti and source_ti.base != element_type:
                                self.add_error(f"Type mismatch in array initialization: Cannot assign array of {source_ti.base} to array of {element_type}")
                    # For array concatenation, check that the element types match
                    elif hasattr(node.initializer, 'element_type') and node.initializer.element_type != element_type:
                        self.add_error(f"Type mismatch in array initialization: Cannot assign array of {node.initializer.element_type} to array of {element_type}")
                else:
                    self.add_error(f"Invalid initializer for array '{node.identifier}'. Expected array or initializer list, got {expr_type}")
                    return None
        
        ti = TypeInfo(
            base=element_type, 
            is_dynamic=node.is_dynamic, 
            is_array=not node.is_dynamic, 
            size=size,
            dimensions=dimensions,
            dimension_sizes=dimension_sizes
        )
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

    def visit_safedictionaryaccess(self, node):
        # Check if the dictionary variable exists
        dict_sym = self.symbol_table.lookup_symbol(node.dict_name)
        if not dict_sym or dict_sym.get('type') != 'KEYWORD_DICT':
            self.add_error(f"'{node.dict_name}' is not a dictionary")
            return None
        
        # Check key type
        key_type = self.visit(node.key)
        if key_type != 'KEYWORD_STRING':
            self.add_error("Dictionary keys must be strings")
            return None
        
        # Check default value type if provided
        if node.default_value:
            default_type = self.visit(node.default_value)
            # Validate that default value type is compatible with dictionary values
            # For now, we'll allow common types
            if default_type not in ['KEYWORD_INT', 'KEYWORD_FLOAT', 'KEYWORD_STRING']:
                self.add_error(f"Default value type {default_type} is not supported for dictionaries")
        
        # Return the type of the dictionary value (could be enhanced to track specific value types)
        return 'KEYWORD_DICT_VALUE'

    def visit_subscriptaccess(self, node):
        arr_info = self.symbol_table.get_array_info(node.name)
        if not arr_info:
            self.add_error(f"Undefined array: '{node.name}'")
            return None
        
        # Get the number of indices being accessed
        num_indices = len(node.indices) if hasattr(node, 'indices') else 1
        
        # Check all indices are integers
        for i, index_expr in enumerate(node.indices if hasattr(node, 'indices') else [node.key]):
            idx_type = self.visit(index_expr)
            if idx_type != 'KEYWORD_INT':
                self.add_error(f"Array index {i} must be an integer, got {idx_type}")
        
        # Determine the result type based on dimensions accessed
        if arr_info.dimensions > num_indices:
            # Still an array with reduced dimensions
            node.element_type = 'array'
        else:
            # Accessing the final element
            node.element_type = 'KEYWORD_' + arr_info.base.upper()
        
        return node.element_type

    def visit_functiondefinition(self, node):
        # Skip if this is a user module function definition being visited during module import
        # (it's already been registered)
        if hasattr(self, '_skip_function_definitions') and self._skip_function_definitions:
            return None
            
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
        first = args[0]
        if not isinstance(first, Identifier):
            self.add_error(f"First argument to '{func_name}' must be an array identifier.")
            return None
        arr_info = self.symbol_table.get_array_info(first.name)
        if not arr_info:
            self.add_error(f"'{first.name}' is not an array.")
            return None
        elem_kw = 'KEYWORD_' + arr_info.base.upper()
        def check_val(idx):
            return self.visit(args[idx])
        if func_name == 'arr_push':
            if not arr_info.is_dynamic:
                self.add_error("arr_push requires dynamic array.")
            if len(args)!=2:
                self.add_error("arr_push expects 2 args")
                return None
            vtype = check_val(1)
            if not self.type_checker.is_compatible(elem_kw, vtype):
                self.add_error(f"Type mismatch push {vtype} into {elem_kw}")
            return 'void'
        if func_name == 'arr_pop':
            if not arr_info.is_dynamic:
                self.add_error("arr_pop requires dynamic array.")
            if len(args)!=1:
                self.add_error("arr_pop expects 1 arg")
            return elem_kw
        if func_name == 'arr_size':
            if len(args)!=1:
                self.add_error("arr_size expects 1 arg")
            return 'KEYWORD_INT'
        if func_name == 'arr_contains':
            if len(args)!=2:
                self.add_error("arr_contains expects 2 args")
                return None
            vtype = check_val(1)
            if not self.type_checker.is_compatible(elem_kw, vtype):
                self.add_error("arr_contains type mismatch")
            return 'KEYWORD_BOOL'
        if func_name == 'arr_indexof':
            if len(args)!=2:
                self.add_error("arr_indexof expects 2 args")
                return None
            vtype = check_val(1)
            if not self.type_checker.is_compatible(elem_kw, vtype):
                self.add_error("arr_indexof type mismatch")
            return 'KEYWORD_INT'
        if func_name == 'arr_avg':
            if arr_info.base not in ('int','float'):
                self.add_error("arr_avg only on int/float")
            if len(args) not in (1,2):
                self.add_error("arr_avg expects 1 or 2 args")
                return None
            if len(args)==2 and self.visit(args[1])!='KEYWORD_INT':
                self.add_error("arr_avg precision must be int")
            return 'KEYWORD_FLOAT'
        self.add_error(f"Unknown array function '{func_name}'")
        return None
    
    def visit_module_function_call(self, node):
        """Handle calls to module functions like http.get()"""
        # Function name contains '.' - it's a module function
        function_symbol = self.symbol_table.lookup_function(node.name)
        
        if not function_symbol:
            # Module might not be imported
            module_namespace = node.name.split('.')[0]
            if module_namespace not in self.imported_modules:
                self.add_error(f"Module '{module_namespace}' not imported. Did you forget 'import {module_namespace};'?")
            else:
                self.add_error(f"Undefined module function: '{node.name}'")
            return None
        
        param_types = function_symbol.get('param_types', [])
        if len(node.args) != len(param_types):
            self.add_error(f"Incorrect number of arguments for function '{node.name}'. Expected {len(param_types)}, got {len(node.args)}.")
        
        # Type check arguments
        for i, arg_expr in enumerate(node.args):
            arg_type = self.visit(arg_expr)
            if i < len(param_types):
                param_type = param_types[i]
                # For module functions, we're more lenient with type checking for now
                # since we might have opaque types like json.object
                # TODO: Improve type checking for module types
        
        return function_symbol.get('return_type')

    def visit_functioncall(self, node):
        if node.name.startswith('arr_'):
            return self.visit_array_function_call(node)
        
        # Check if this is a module function call (contains '.')
        if '.' in node.name:
            return self.visit_module_function_call(node)
        
        # Special handling for dict_get with type inference

        if node.name == 'dict_get':

            # Validate arguments

            if len(node.args) != 2:

                self.add_error(f"dict_get requires 2 arguments (dict, key), got {len(node.args)}")

                return None

 

            # Check argument types

            dict_type = self.visit(node.args[0])

            key_type = self.visit(node.args[1])

 

            if dict_type != 'KEYWORD_DICT' and dict_type != 'dict':

                self.add_error(f"First argument to dict_get must be a dict, got {dict_type}")

            if key_type != 'KEYWORD_STRING' and key_type != 'string':

                self.add_error(f"Second argument to dict_get must be a string, got {key_type}")

 

            # Return type based on context (expected_type from declaration/assignment)

            expected = getattr(self, 'expected_type', None)

            if expected:

                # Store the inferred type on the node for code generation

                node.inferred_return_type = expected

                return expected

            else:

                # Default to void* if no context

                return 'void*'

 

        # Special handling for dict_set with type inference

        if node.name == 'dict_set':

            # Validate arguments

            if len(node.args) != 3:

                self.add_error(f"dict_set requires 3 arguments (dict, key, value), got {len(node.args)}")

                return 'void'

 

            # Check argument types

            dict_type = self.visit(node.args[0])

            key_type = self.visit(node.args[1])

            value_type = self.visit(node.args[2])

 

            if dict_type != 'KEYWORD_DICT' and dict_type != 'dict':

                self.add_error(f"First argument to dict_set must be a dict, got {dict_type}")

            if key_type != 'KEYWORD_STRING' and key_type != 'string':

                self.add_error(f"Second argument to dict_set must be a string, got {key_type}")

 

            # Store the value type on the node for code generation

            node.value_type = value_type

            return 'void'
        
        # Special handling for file_read_lines with optional parameters
        if node.name == 'file_read_lines':
            num_args = len(node.args)
            
            # Validate number of arguments (1, 2, or 3)
            if num_args < 1 or num_args > 3:
                self.add_error(f"file_read_lines requires 1-3 arguments (file[, start_line[, end_line]]), got {num_args}")
                return 'd_array_string'
            
            # Check first argument is a file handle
            file_type = self.visit(node.args[0])
            if file_type != 'KEYWORD_FILE' and file_type != 'file':
                self.add_error(f"First argument to file_read_lines must be a file, got {file_type}")
            
            # Check optional arguments are integers
            if num_args >= 2:
                start_type = self.visit(node.args[1])
                if start_type != 'KEYWORD_INT' and start_type != 'int':
                    self.add_error(f"Second argument to file_read_lines must be an int, got {start_type}")
            
            if num_args == 3:
                end_type = self.visit(node.args[2])
                if end_type != 'KEYWORD_INT' and end_type != 'int':
                    self.add_error(f"Third argument to file_read_lines must be an int, got {end_type}")
            
            return 'd_array_string'
        
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
                    is_math_func = node.name in ["sqrt", "pow", "sin", "cos", "tan", "asin", "acos", "atan", "log", "log10", "exp", "floor", "ceil", "round", "abs", "min", "max"]
                    if not (is_math_func and param_type == 'float' and arg_type == 'KEYWORD_INT'):
                        self.add_error(f"Type mismatch for argument {i+1} of function '{node.name}'. Expected {param_type}, got {arg_type}.")

        return function_symbol.get('return_type')

    def visit_functioncallstatement(self, node):
        self.visit(node.function_call)
        return None

    def visit_assignment(self, node):
        lhs_type = self.visit(node.lhs)
        # Store expected type for dict_get type inference
        old_expected_type = getattr(self, 'expected_type', None)
        self.expected_type = lhs_type
        expr_type = self.visit(node.rhs)
        # Restore previous expected type
        self.expected_type = old_expected_type

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
                left_element_type = left_symbol.get('element_type')
                right_element_type = right_symbol.get('element_type')
                if left_element_type == right_element_type:
                    node.result_type = 'array'
                    node.element_type = left_element_type
                    return 'array'
                else:
                    self.add_error(f"Cannot concatenate arrays of different element types: {left_element_type} vs {right_element_type}")
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

    def _check_variable_initialization(self, var_name, context=""):
        """Check if a variable is properly initialized before use"""
        symbol = self.symbol_table.lookup_symbol(var_name)
        if symbol and not symbol.get('is_initialized', False):
            # Only warn for variables that are used in expressions that require a value
            # Don't warn for simple comparisons with null
            self.add_error(f"Variable '{var_name}' may be used before initialization{context}")
            return False
        return True

    def visit_identifier(self, node):
        symbol = self.symbol_table.lookup_symbol(node.name)
        if symbol:
            # Check if this is an array by looking at typeinfo first
            type_info = symbol.get('typeinfo')
            if type_info and type_info.kind == 'array':
                return 'array'
            
            # Check variable initialization for non-array variables
            # But don't warn if we're just checking for null/undefined
            if not type_info:  # Only check for regular variables, not arrays
                # For now, let's be less strict about initialization checking
                # This will be improved in future versions
                pass
            
            # Fall back to regular type checking
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
        if expected_type_name == 'array':
            # Allow printing dynamic arrays; semantic check ensures identifier is array
            if not isinstance(node.expression, Identifier):
                self.add_error('Output of array requires array identifier.')
                return None
            arr_info = self.symbol_table.get_array_info(node.expression.name)
            if not arr_info:
                self.add_error('Output expects an array variable.')
            return None
        norm_expr_type = self.type_checker._normalize_type(expr_type)
        norm_expected_type = self.type_checker._normalize_type(expected_type_name)
        
        # Allow automatic type conversion to string for output
        if norm_expected_type == 'KEYWORD_STRING':
            # Any basic type can be auto-converted to string for output
            if norm_expr_type in ['KEYWORD_INT', 'KEYWORD_FLOAT', 'KEYWORD_CHAR', 'KEYWORD_STRING']:
                # Valid conversion, no error
                pass
            elif norm_expr_type and norm_expr_type != norm_expected_type:
                self.add_error(f"Type mismatch in output: Expression is {expr_type}, but output type is {expected_type_name}")
        elif norm_expr_type and norm_expr_type != norm_expected_type:
            self.add_error(f"Type mismatch in output: Expression is {expr_type}, but output type is {expected_type_name}")
        
        if node.precision:
            precision_type = self.visit(node.precision)
            if precision_type != 'KEYWORD_INT':
                self.add_error('Output precision must be int')
        return None

    def visit_systeminput(self, node):
        # The parser creates an Identifier node for the variable
        self.visit(node.variable)
        return None

    def visit_systemexit(self, node):
        return None

    def visit_systemsleep(self, node):
        # Check that the duration expression is an integer
        duration_type = self.visit(node.duration)
        if duration_type and duration_type != 'KEYWORD_INT':
            self.add_error(f"sleep() expects an integer argument, got {duration_type}")
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