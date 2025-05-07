# Parser using PLY (Python Lex-Yacc)
import yacc as yacc
from lexer import Lexer, build_master_nfa, nfa_to_dfa, epsilon_closure
from lex import LexToken  # Import LexToken from the correct module

# Symbol Table Implementation
class SymbolTable:
    def __init__(self):
        self.table = {}
        self.scope_stack = [0]
        self.current_scope = 0
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
    
    def update_symbol(self, name, **updates):
        """Update a symbol's information."""
        symbol = self.lookup_symbol(name)
        if symbol:
            for key, value in updates.items():
                symbol[key] = value
            return True
        return False

# Parser class that integrates with our lexer
class Parser:
    def __init__(self):
        self.tokens = [
            'IDENTIFIER', 'INT_LITERAL', 'STRING_LITERAL',
            'KEYWORD_IF', 'KEYWORD_ELSE', 'KEYWORD_FOR', 'KEYWORD_WHILE',
            'KEYWORD_RETURN', 'KEYWORD_BREAK', 'KEYWORD_CONTINUE',
            'KEYWORD_INT', 'KEYWORD_FLOAT', 'KEYWORD_CHAR', 'KEYWORD_VOID',
            'KEYWORD_STRING', 'KEYWORD_BOOL', 'KEYWORD_TRUE', 'KEYWORD_FALSE', 
            'KEYWORD_NULL', 'KEYWORD_EXIT',
            'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
            'SEMICOLON', 'COMMA', 'DOT',
            'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
            'GT', 'LT', 'GEQ', 'LEQ', 'EQ', 'NEQ', 'AND', 'OR', 'ASSIGN',
            'SYSTEM_INPUT', 'SYSTEM_OUTPUT', 'COMMENT'
        ]
        
        self.precedence = (
            ('left', 'OR'),
            ('left', 'AND'),
            ('left', 'EQ', 'NEQ'),
            ('left', 'GT', 'LT', 'GEQ', 'LEQ'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'MUL', 'DIV', 'MOD'),
            ('right', 'UMINUS'),  # Unary minus operator
        )
        
        self.symbol_table = SymbolTable()
        self.lexer_instance = None
        self.parser = yacc.yacc(module=self)
        
    def setup_lexer(self):
        """Create and configure the lexer instance."""
        nfa_start = build_master_nfa()
        dfa_transitions, dfa_token = nfa_to_dfa(nfa_start)
        start_set = frozenset(epsilon_closure({nfa_start}))
        return Lexer(dfa_transitions, dfa_token, start_set)
        
    def tokenize_input(self, input_text):
        """Tokenize the input text using our lexer."""
        if not self.lexer_instance:
            self.lexer_instance = self.setup_lexer()
        
        token_list = self.lexer_instance.tokenize(input_text)
        
        # Convert our lexer's token format to PLY's format
        ply_tokens = []
        for token_type, token_text in token_list:
            token = LexToken()  # Use LexToken from ply.lex
            token.type = token_type
            token.value = token_text
            token.lineno = 0  # You might want to track line numbers in your lexer
            token.lexpos = 0  # And character positions
            ply_tokens.append(token)
            
        return ply_tokens
    
    def parse(self, input_text):
        """Parse the input text and build the AST."""
        tokens = self.tokenize_input(input_text)
        return self.parser.parse(tokens=tokens)
    
    # Grammar rules defined below
    
    def p_program(self, p):
        '''program : statement_list'''
        p[0] = ('program', p[1])
    
    def p_statement_list(self, p):
        '''statement_list : statement
                         | statement_list statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_statement(self, p):
        '''statement : declaration_statement
                    | assignment_statement
                    | if_statement
                    | while_statement
                    | for_statement
                    | return_statement
                    | function_call_statement
                    | block_statement'''
        p[0] = p[1]
    
    def p_declaration_statement(self, p):
        '''declaration_statement : type_specifier IDENTIFIER SEMICOLON
                                | type_specifier IDENTIFIER ASSIGN expression SEMICOLON'''
        if len(p) == 4:
            # Add to symbol table - uninitialized
            self.symbol_table.add_symbol(p[2], p[1], is_initialized=False)
            p[0] = ('declaration', p[1], p[2], None)
        else:
            # Add to symbol table - initialized
            self.symbol_table.add_symbol(p[2], p[1], is_initialized=True)
            p[0] = ('declaration', p[1], p[2], p[4])
    
    def p_type_specifier(self, p):
        '''type_specifier : KEYWORD_INT
                         | KEYWORD_FLOAT
                         | KEYWORD_CHAR
                         | KEYWORD_VOID
                         | KEYWORD_STRING
                         | KEYWORD_BOOL'''
        p[0] = p[1]
    
    def p_assignment_statement(self, p):
        '''assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON'''
        # Check if identifier exists in symbol table
        symbol = self.symbol_table.lookup_symbol(p[1])
        if not symbol:
            print(f"Error: Variable '{p[1]}' used before declaration")
        else:
            self.symbol_table.update_symbol(p[1], initialized=True)
        p[0] = ('assignment', p[1], p[3])
    
    def p_if_statement(self, p):
        '''if_statement : KEYWORD_IF LPAREN expression RPAREN statement
                       | KEYWORD_IF LPAREN expression RPAREN statement KEYWORD_ELSE statement'''
        if len(p) == 6:
            p[0] = ('if', p[3], p[5], None)
        else:
            p[0] = ('if', p[3], p[5], p[7])
    
    def p_while_statement(self, p):
        '''while_statement : KEYWORD_WHILE LPAREN expression RPAREN statement'''
        p[0] = ('while', p[3], p[5])
    
    def p_for_statement(self, p):
        '''for_statement : KEYWORD_FOR LPAREN statement expression SEMICOLON expression RPAREN statement'''
        p[0] = ('for', p[3], p[4], p[6], p[8])
    
    def p_return_statement(self, p):
        '''return_statement : KEYWORD_RETURN SEMICOLON
                           | KEYWORD_RETURN expression SEMICOLON'''
        if len(p) == 3:
            p[0] = ('return', None)
        else:
            p[0] = ('return', p[2])
    
    def p_function_call_statement(self, p):
        '''function_call_statement : function_call SEMICOLON'''
        p[0] = p[1]
    
    def p_function_call(self, p):
        '''function_call : IDENTIFIER LPAREN argument_list RPAREN
                        | IDENTIFIER LPAREN RPAREN
                        | SYSTEM_INPUT LPAREN argument_list RPAREN
                        | SYSTEM_INPUT LPAREN RPAREN
                        | SYSTEM_OUTPUT LPAREN argument_list RPAREN
                        | SYSTEM_OUTPUT LPAREN RPAREN'''
        if len(p) == 4:
            p[0] = ('function_call', p[1], [])
        else:
            p[0] = ('function_call', p[1], p[3])
    
    def p_argument_list(self, p):
        '''argument_list : expression
                        | argument_list COMMA expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    
    def p_block_statement(self, p):
        '''block_statement : LBRACE RBRACE
                          | LBRACE statement_list RBRACE'''
        # Enter a new scope when entering a block
        self.symbol_table.enter_scope()
        
        if len(p) == 3:
            p[0] = ('block', [])
        else:
            p[0] = ('block', p[2])
        
        # Exit the scope when leaving the block
        self.symbol_table.exit_scope()
    
    def p_expression(self, p):
        '''expression : logical_expression'''
        p[0] = p[1]
    
    def p_logical_expression(self, p):
        '''logical_expression : equality_expression
                             | logical_expression AND equality_expression
                             | logical_expression OR equality_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    
    def p_equality_expression(self, p):
        '''equality_expression : relational_expression
                               | equality_expression EQ relational_expression
                               | equality_expression NEQ relational_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    
    def p_relational_expression(self, p):
        '''relational_expression : additive_expression
                                | relational_expression GT additive_expression
                                | relational_expression LT additive_expression
                                | relational_expression GEQ additive_expression
                                | relational_expression LEQ additive_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    
    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                              | additive_expression PLUS multiplicative_expression
                              | additive_expression MINUS multiplicative_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    
    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                    | multiplicative_expression MUL unary_expression
                                    | multiplicative_expression DIV unary_expression
                                    | multiplicative_expression MOD unary_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    
    def p_unary_expression(self, p):
        '''unary_expression : primary_expression
                           | MINUS unary_expression %prec UMINUS'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('unary_op', p[1], p[2])
    
    def p_primary_expression(self, p):
        '''primary_expression : IDENTIFIER
                             | INT_LITERAL
                             | STRING_LITERAL
                             | KEYWORD_TRUE
                             | KEYWORD_FALSE
                             | KEYWORD_NULL
                             | LPAREN expression RPAREN
                             | function_call'''
        if len(p) == 2:
            # Check if identifier exists in symbol table
            if p[1] in ['IDENTIFIER']:
                symbol = self.symbol_table.lookup_symbol(p[1])
                if not symbol:
                    print(f"Error: Variable '{p[1]}' used before declaration")
            p[0] = ('primary', p[1])
        else:
            p[0] = p[2]
    
    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

# Usage example
def main():
    # Create an instance of our parser
    parser = Parser()
    
    # Example program
    test_program = """int x=5;
if(x>5){
    output("It is greater than 5",string)
}"""
    
    try:
        # Parse the program
        ast = parser.parse(test_program)
        print("Parsing successful!")
        print("AST:", ast)
        
        # Print symbol table for demonstration
        print("\nSymbol Table:")
        for scope, symbols in parser.symbol_table.table.items():
            print(f"Scope {scope}:")
            for name, info in symbols.items():
                print(f"  {name}: {info}")
                
    except Exception as e:
        print(f"Parsing error: {e}")

if __name__ == "__main__":
    main()