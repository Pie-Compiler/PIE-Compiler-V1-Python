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
    
    def add_symbol(self, name, type_info, line_num=None, is_initialized=False):
        """Add a symbol to the current scope."""
        if self.current_scope not in self.table:
            self.table[self.current_scope] = {}
        
        symbol_info = {
            'type': type_info,
            'line': line_num,
            'initialized': is_initialized
        }
        
        self.table[self.current_scope][name] = symbol_info
        return symbol_info
    
    def lookup_symbol(self, name):
        """Look up a symbol in the current scope and parent scopes."""
        # Search from current scope up through parent scopes
        for scope in reversed(self.scope_stack):
            if scope in self.table and name in self.table[scope]:
                return self.table[scope][name]
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
                result.append(f"  {name}: {info}")
        return "\n".join(result)

# Function Symbol Table (for function declarations/definitions)
class FunctionSymbolTable:
    def __init__(self):
        self.functions = {}
    
    def add_function(self, name, return_type, parameters=None, is_defined=False):
        """Add a function to the symbol table."""
        if parameters is None:
            parameters = []
            
        # Store function signature
        self.functions[name] = {
            'return_type': return_type,
            'parameters': parameters,  # List of (param_type, param_name) tuples
            'is_defined': is_defined   # False for declarations, True for definitions
        }
        return self.functions[name]
    
    def lookup_function(self, name):
        """Look up a function in the symbol table."""
        if name in self.functions:
            return self.functions[name]
        return None
    
    def update_function(self, name, **updates):
        """Update a function's information."""
        if name in self.functions:
            for key, value in updates.items():
                self.functions[name][key] = value
            return True
        return False
    
    def __str__(self):
        """String representation of the function table for debugging."""
        result = ["Function Table:"]
        for name, info in self.functions.items():
            params = ", ".join(f"{p_type} {p_name}" for p_type, p_name in info['parameters'])
            result.append(f"  {info['return_type']} {name}({params}) {'[defined]' if info['is_defined'] else '[declared]'}")
        return "\n".join(result)

# Type Checking Helper
class TypeChecker:
    def __init__(self, symbol_table, function_table):
        self.symbol_table = symbol_table
        self.function_table = function_table
        
        # Define type compatibility rules
        self.compatible_types = {
            'KEYWORD_INT': ['KEYWORD_INT', 'KEYWORD_FLOAT'],
            'KEYWORD_FLOAT': ['KEYWORD_FLOAT', 'KEYWORD_INT'],
            'KEYWORD_BOOL': ['KEYWORD_BOOL'],
            'KEYWORD_STRING': ['KEYWORD_STRING'],
            'KEYWORD_CHAR': ['KEYWORD_CHAR']
        }
    
    def is_compatible(self, type1, type2):
        """Check if type2 can be assigned to type1."""
        if type1 in self.compatible_types and type2 in self.compatible_types[type1]:
            return True
        return False
    
    def check_binary_op(self, op, left_type, right_type):
        """Check if a binary operation is valid for the given types."""
        # Arithmetic operations
        if op in ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD']:
            if left_type in ['KEYWORD_INT', 'KEYWORD_FLOAT'] and right_type in ['KEYWORD_INT', 'KEYWORD_FLOAT']:
                # Return the "wider" type
                if 'FLOAT' in left_type or 'FLOAT' in right_type:
                    return 'KEYWORD_FLOAT'
                return 'KEYWORD_INT'
            return None
        
        # String concatenation
        if op == 'PLUS' and left_type == 'KEYWORD_STRING' and right_type == 'KEYWORD_STRING':
            return 'KEYWORD_STRING'
        
        # Comparison operations
        if op in ['EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ']:
            if left_type in ['KEYWORD_INT', 'KEYWORD_FLOAT'] and right_type in ['KEYWORD_INT', 'KEYWORD_FLOAT']:
                return 'KEYWORD_BOOL'
            if left_type == right_type:  # Same types can be compared for equality
                return 'KEYWORD_BOOL'
            return None
        
        # Logical operations
        if op in ['AND', 'OR']:
            if left_type == 'KEYWORD_BOOL' and right_type == 'KEYWORD_BOOL':
                return 'KEYWORD_BOOL'
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
    function_table = FunctionSymbolTable()
    function_table.add_function("calculateArea", "KEYWORD_FLOAT", [("KEYWORD_FLOAT", "width"), ("KEYWORD_FLOAT", "height")])
    function_table.add_function("main", "KEYWORD_INT")
    
    print("\nFunction Table:")
    print(function_table)
    
    # Test type checker
    type_checker = TypeChecker(symbol_table, function_table)
    print("\nType compatibility checks:")
    print("int + float =", type_checker.check_binary_op("PLUS", "KEYWORD_INT", "KEYWORD_FLOAT"))
    print("bool && bool =", type_checker.check_binary_op("AND", "KEYWORD_BOOL", "KEYWORD_BOOL"))
    print("int > float =", type_checker.check_binary_op("GT", "KEYWORD_INT", "KEYWORD_FLOAT"))
    print("string + int =", type_checker.check_binary_op("PLUS", "KEYWORD_STRING", "KEYWORD_INT"))

if __name__ == "__main__":
    test_symbol_table()