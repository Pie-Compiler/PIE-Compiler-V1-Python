# Symbol Table Implementation
class SymbolTable:
    def __init__(self):
        # Main table structure: { scope_id: { symbol_name: symbol_info } }
        self.table = {}
        
        # Stack to track nested scopes
        self.scope_stack = [0]  # Start with global scope (0)
        
        # Current active scope
        self.current_scope = 0
        
        # Next available scope ID
        self.next_scope = 1
    
    def enter_scope(self):
        """Create a new scope and make it the current scope."""
        self.scope_stack.append(self.next_scope)
        self.current_scope = self.next_scope
        self.next_scope += 1
        return self.current_scope
    
    def exit_scope(self):
        """Exit the current scope and return to the previous scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
        return self.current_scope
    
    def add_symbol(self, name, type_info, line_num=None, is_initialized=False, **kwargs):
        """Add a symbol to the current scope."""
        if self.current_scope not in self.table:
            self.table[self.current_scope] = {}
        
        symbol_info = {
            'type': type_info,
            'line': line_num,
            'initialized': is_initialized
        }
        symbol_info.update(kwargs)
        
        self.table[self.current_scope][name] = symbol_info
        return symbol_info
    
    def lookup_symbol(self, name):
        """Look up a symbol in the current scope and parent scopes."""
        # Search from current scope up through parent scopes
        for scope in reversed(self.scope_stack):
            if scope in self.table and name in self.table[scope]:
                return self.table[scope][name]
        return None
    
    def lookup_function(self, name):
        """Looks up a function in the symbol table."""
        # Functions are typically in the global scope
        if 0 in self.table and name in self.table[0]:
            symbol = self.table[0][name]
            if symbol['type'] == 'function':
                return symbol
        return None

    def lookup_symbol_current_scope(self, name):
        """Look up a symbol in ONLY the current scope."""
        if self.current_scope in self.table and name in self.table[self.current_scope]:
            return self.table[self.current_scope][name]
        return None
    
    def update_symbol(self, name, **updates):
        """Update a symbol's information."""
        symbol = self.lookup_symbol(name)
        if symbol:
            for key, value in updates.items():
                symbol[key] = value
            return True
        return False
        
    def __str__(self):
        """String representation of the symbol table for debugging."""
        result = []
        for scope, symbols in self.table.items():
            result.append(f"Scope {scope}:")
            for name, info in symbols.items():
                if info['type'] == 'function':
                    params = ", ".join(f"{p['type']} {p['name']}" for p in info.get('params', []))
                    result.append(f"  {info.get('return_type')} {name}({params})")
                else:
                    result.append(f"  {name}: {info}")
        return "\n".join(result)

# Type Checking Helper
class TypeChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        
        # This specific compatible_types map might be less needed if is_compatible is robust
        self.compatible_types = {
            'KEYWORD_INT': ['KEYWORD_INT', 'KEYWORD_FLOAT'],
            'KEYWORD_FLOAT': ['KEYWORD_FLOAT', 'KEYWORD_INT'],
            'KEYWORD_BOOL': ['KEYWORD_BOOL'],
            'KEYWORD_STRING': ['KEYWORD_STRING'],
            'KEYWORD_CHAR': ['KEYWORD_CHAR']
        }
        
    def _normalize_type(self, type_name):
        """Convert literal types and language types to standardized keyword types."""
        if not isinstance(type_name, str):
            return None # Or a specific "UNKNOWN_TYPE"

        mapping = {
            'INT_LITERAL': 'KEYWORD_INT',
            'FLOAT_LITERAL': 'KEYWORD_FLOAT',
            'STRING_LITERAL': 'KEYWORD_STRING',
            'CHAR_LITERAL': 'KEYWORD_CHAR',
            'KEYWORD_TRUE': 'KEYWORD_BOOL',
            'KEYWORD_FALSE': 'KEYWORD_BOOL',
            'int': 'KEYWORD_INT',
            'float': 'KEYWORD_FLOAT',
            'string': 'KEYWORD_STRING',
            'char': 'KEYWORD_CHAR',
            'boolean': 'KEYWORD_BOOL', # From test2.pie
            'bool': 'KEYWORD_BOOL',
            'void': 'KEYWORD_VOID',
            'file': 'KEYWORD_FILE',
            'socket': 'KEYWORD_SOCKET',
            'd_array_int': 'KEYWORD_D_ARRAY_INT',
            'd_array_string': 'KEYWORD_D_ARRAY_STRING',
            'array_int': 'KEYWORD_D_ARRAY_INT',
            'array_string': 'KEYWORD_D_ARRAY_STRING',
            # Idempotent entries for already normalized types
            'KEYWORD_INT': 'KEYWORD_INT',
            'KEYWORD_FLOAT': 'KEYWORD_FLOAT',
            'KEYWORD_BOOL': 'KEYWORD_BOOL',
            'KEYWORD_STRING': 'KEYWORD_STRING',
            'KEYWORD_CHAR': 'KEYWORD_CHAR',
            'KEYWORD_VOID': 'KEYWORD_VOID',
            'KEYWORD_NULL': 'KEYWORD_NULL',
            'KEYWORD_D_ARRAY_INT': 'KEYWORD_D_ARRAY_INT',
            'KEYWORD_D_ARRAY_STRING': 'KEYWORD_D_ARRAY_STRING',
        }
        return mapping.get(type_name, type_name) # Return original if not in map, though ideally all types should be mappable or already KEYWORD_

    def is_compatible(self, target_type, source_type):
        """Check if source_type can be assigned to target_type."""
        norm_target_type = self._normalize_type(target_type)
        norm_source_type = self._normalize_type(source_type)

        if norm_target_type is None or norm_source_type is None:
            return False

        if norm_source_type == 'KEYWORD_NULL':
            # Allow assigning null to reference-like types
            return norm_target_type in ['KEYWORD_STRING', 'KEYWORD_FILE', 'KEYWORD_SOCKET', 'KEYWORD_D_ARRAY_INT', 'KEYWORD_D_ARRAY_STRING']

        if norm_target_type == norm_source_type:
            return True
        
        if norm_target_type == 'KEYWORD_FLOAT' and norm_source_type == 'KEYWORD_INT':
            return True
        
        # Add other compatibilities if needed, e.g., char to string
        return False
    
    def check_binary_op(self, op, left_type, right_type):
        """Check if a binary operation is valid for the given types and return result type."""
        norm_left = self._normalize_type(left_type)
        norm_right = self._normalize_type(right_type)

        if norm_left is None or norm_right is None:
            return None

        # Arithmetic operators: +, -, *, /
        if op in ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD']:
            # String concatenation special-case
            if op == 'PLUS' and norm_left == 'KEYWORD_STRING' and norm_right == 'KEYWORD_STRING':
                return 'KEYWORD_STRING'
            # Arithmetic numeric operations
            if norm_left in ['KEYWORD_INT', 'KEYWORD_FLOAT'] and norm_right in ['KEYWORD_INT', 'KEYWORD_FLOAT']:
                if op == 'DIV':
                    # Division always produces float (even int/int)
                    return 'KEYWORD_FLOAT'
                if 'KEYWORD_FLOAT' in [norm_left, norm_right]:
                    return 'KEYWORD_FLOAT'
                # For MOD we still want int result; others int if both ints
                return 'KEYWORD_INT'
            return None

        # Comparison operators: <, >, <=, >=
        if op in ['LT', 'GT', 'LEQ', 'GEQ']:
            if norm_left in ['KEYWORD_INT', 'KEYWORD_FLOAT'] and norm_right in ['KEYWORD_INT', 'KEYWORD_FLOAT']:
                return 'KEYWORD_BOOL'
            else:
                return None

        # Equality operators: ==, !=
        if op in ['EQ', 'NEQ']:
            if norm_left == norm_right:
                return 'KEYWORD_BOOL'
            # Allow int/float comparison
            if {norm_left, norm_right} <= {'KEYWORD_INT', 'KEYWORD_FLOAT'}:
                return 'KEYWORD_BOOL'
            # Allow null equality comparisons with reference-like types
            ref_types = {'KEYWORD_STRING','KEYWORD_FILE','KEYWORD_SOCKET','KEYWORD_D_ARRAY_INT','KEYWORD_D_ARRAY_STRING'}
            if (norm_left == 'KEYWORD_NULL' and norm_right in ref_types) or (norm_right == 'KEYWORD_NULL' and norm_left in ref_types):
                return 'KEYWORD_BOOL'
            return None

        # Logical operators: &&, ||
        if op in ['AND', 'OR']:
            if norm_left == 'KEYWORD_BOOL' and norm_right == 'KEYWORD_BOOL':
                return 'KEYWORD_BOOL'
            else:
                return None

        return None

# Usage Example
def test_symbol_table():
    symbol_table = SymbolTable()
    
    # Add some symbols in global scope
    symbol_table.add_symbol("x", "KEYWORD_INT", line_num=1, is_initialized=True)
    symbol_table.add_symbol("y", "KEYWORD_FLOAT", line_num=2)
    
    # Enter a new scope (e.g., inside a function or block)
    symbol_table.enter_scope()
    
    # Add symbols in the new scope
    symbol_table.add_symbol("z", "KEYWORD_STRING", line_num=3)
    symbol_table.add_symbol("x", "KEYWORD_BOOL", line_num=4)  # Shadows global "x"
    
    # Look up symbols
    print("Looking up 'x' (should find local scope's bool):", symbol_table.lookup_symbol("x"))
    print("Looking up 'y' (should find global scope's float):", symbol_table.lookup_symbol("y"))
    print("Looking up 'z' (should find local scope's string):", symbol_table.lookup_symbol("z"))
    
    # Exit back to global scope
    symbol_table.exit_scope()
    
    # Now "x" should refer to the global int
    print("After exiting scope, looking up 'x':", symbol_table.lookup_symbol("x"))
    
    # "z" is no longer visible
    print("After exiting scope, looking up 'z':", symbol_table.lookup_symbol("z"))
    
    # Test function table
    symbol_table.add_symbol("calculateArea", "function", return_type="KEYWORD_FLOAT", params=[{'type': 'KEYWORD_FLOAT', 'name': 'width'}, {'type': 'KEYWORD_FLOAT', 'name': 'height'}])
    symbol_table.add_symbol("main", "function", return_type="KEYWORD_INT", params=[])
    
    print("\nSymbol Table with Functions:")
    print(symbol_table)
    
    # Test type checker
    type_checker = TypeChecker(symbol_table)
    print("\nType compatibility checks:")
    print("int + float =", type_checker.check_binary_op("PLUS", "KEYWORD_INT", "KEYWORD_FLOAT"))
    print("bool && bool =", type_checker.check_binary_op("AND", "KEYWORD_BOOL", "KEYWORD_BOOL"))
    print("int > float =", type_checker.check_binary_op("GT", "KEYWORD_INT", "KEYWORD_FLOAT"))
    print("string + int =", type_checker.check_binary_op("PLUS", "KEYWORD_STRING", "KEYWORD_INT"))

if __name__ == "__main__":
    test_symbol_table()