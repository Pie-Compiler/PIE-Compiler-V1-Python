# Parser using PLY (Python Lex-Yacc)
import yacc as yacc
from lexer import Lexer, build_master_nfa, nfa_to_dfa, epsilon_closure
from lex import LexToken  # Import LexToken from the correct module
from plyAdapter import PLYLexerAdapter  # Import the adapter for PLY
from symbol_table import SymbolTable  # Import the symbol table class
# Parser class that integrates with our lexer
class Parser:
    def __init__(self):
        self.tokens = [
            'IDENTIFIER', 'INT_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',  # Added CHAR_LITERAL
            'KEYWORD_IF', 'KEYWORD_ELSE', 'KEYWORD_FOR', 'KEYWORD_WHILE',
            'KEYWORD_RETURN', 'KEYWORD_BREAK', 'KEYWORD_CONTINUE',
            'KEYWORD_INT', 'KEYWORD_FLOAT', 'KEYWORD_CHAR', 'KEYWORD_VOID',
            'KEYWORD_STRING', 'KEYWORD_BOOL', 'KEYWORD_TRUE', 'KEYWORD_FALSE', 
            'KEYWORD_NULL', 'KEYWORD_EXIT',
            'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
            'SEMICOLON', 'COMMA', 'DOT',
            'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
            'GT', 'LT', 'GEQ', 'LEQ', 'EQ', 'NEQ', 'AND', 'OR', 'ASSIGN',
            'SYSTEM_INPUT', 'SYSTEM_OUTPUT', 'SYSTEM_EXIT', 'COMMENT'
        ]
        
        self.precedence = (
            ('left', 'OR'),
            ('left', 'AND'),
            ('left', 'EQ', 'NEQ'),
            ('left', 'GT', 'LT', 'GEQ', 'LEQ'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'MUL', 'DIV', 'MOD'),
            ('right', 'UMINUS'),  # Unary minus operator
            ('nonassoc', 'LOWER_THAN_ELSE'),  # To handle the dangling else
            ('nonassoc', 'KEYWORD_ELSE')
        )
        
        self.symbol_table = SymbolTable()
        self.lexer_instance = None
        self.parser = yacc.yacc(module=self)
        
    def setup_lexer(self):
        """Create and configure the lexer instance."""
        nfa_start = build_master_nfa()
        dfa_transitions, dfa_token = nfa_to_dfa(nfa_start)
        start_set = frozenset(epsilon_closure({nfa_start}))
        lexer = Lexer(dfa_transitions, dfa_token, start_set)
        lexer.symbol_table = self.symbol_table  # Pass symbol table
        return lexer
        
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
        if not self.lexer_instance:
            self.lexer_instance = self.setup_lexer()
        
        # Get tokens from your custom lexer
        token_list = self.lexer_instance.tokenize(input_text)
        
        # Debug: Print tokens before conversion
        print("Raw tokens from lexer:")
        for token in token_list:
            print(f"  {token}")
        
        # Convert to PLY tokens
        ply_tokens = []
        for token in token_list:
            # Check if we're getting 2-tuples or 3-tuples
            if len(token) == 2:
                token_type, token_text = token
                line_num = 1  # Default line number
            else:
                token_type, token_text, line_num = token
                
            if token_type == "COMMENT":
                continue  # Skip comments
            
            # Create a token object
            tok = LexToken()
            tok.type = token_type
            tok.value = token_text
            tok.lineno = line_num
            tok.lexpos = 0
            ply_tokens.append(tok)
        
        # Create adapter
        lexer_adapter = PLYLexerAdapter(ply_tokens)
        
        # Parse with the adapter
        return self.parser.parse(lexer=lexer_adapter)
    
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
    
    def p_assignment_statement_no_semi(self, p):
        '''assignment_statement_no_semi : IDENTIFIER ASSIGN expression'''
        # Check if identifier exists in symbol table
        symbol = self.symbol_table.lookup_symbol(p[1])
        if not symbol:
            print(f"Error: Variable '{p[1]}' used before declaration")
        else:
            self.symbol_table.update_symbol(p[1], initialized=True)
        p[0] = ('assignment', p[1], p[3])
    
    def p_if_statement(self, p):
        '''if_statement : KEYWORD_IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
                        | KEYWORD_IF LPAREN expression RPAREN statement KEYWORD_ELSE statement'''
        if len(p) == 6:
            p[0] = ('if', p[3], p[5], None)
        else:
            p[0] = ('if', p[3], p[5], p[7])
    
    def p_while_statement(self, p):
        '''while_statement : KEYWORD_WHILE LPAREN expression RPAREN statement'''
        p[0] = ('while', p[3], p[5])
    
    def p_for_statement(self, p):
        '''for_statement : KEYWORD_FOR LPAREN for_init expression_opt SEMICOLON expression_opt RPAREN statement'''
        p[0] = ('for', p[3], p[4], p[6], p[8])

    def p_for_init(self, p):
        '''for_init : assignment_statement_no_semi SEMICOLON
                    | declaration_statement
                    | SEMICOLON'''
        if len(p) == 2 and p[1] == ';':
            p[0] = None  # Empty initialization
        elif len(p) == 3:
            p[0] = p[1]  # assignment with semicolon
        else:
            p[0] = p[1]  # declaration with its own semicolon

    def p_expression_statement(self, p):
        '''expression_statement : expression SEMICOLON
                               | SEMICOLON'''
        if len(p) == 2:
            p[0] = None  # Empty expression
        else:
            p[0] = p[1]

    def p_expression_opt(self, p):
        '''expression_opt : expression
                         | assignment_statement_no_semi
                         | empty'''
        p[0] = p[1]

    def p_empty(self, p):
        'empty :'
        p[0] = None
    
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
    
    # Add KEYWORD_EXIT to function call rule
    def p_function_call(self, p):
        '''function_call : IDENTIFIER LPAREN argument_list RPAREN
                        | IDENTIFIER LPAREN RPAREN
                        | SYSTEM_INPUT LPAREN IDENTIFIER COMMA type_specifier RPAREN
                        | SYSTEM_OUTPUT LPAREN expression COMMA type_specifier RPAREN
                        | KEYWORD_EXIT LPAREN RPAREN
                        | IDENTIFIER LPAREN expression COMMA type_specifier RPAREN'''
        if p[1] == 'input' or p.slice[1].type == 'SYSTEM_INPUT':
            # input(variable, type)
            p[0] = ('system_input', p[3], p[5])
        elif p[1] == 'output' or p.slice[1].type == 'SYSTEM_OUTPUT':
            # output(expression, type)
            p[0] = ('system_output', p[3], p[5])
        elif p[1] == 'exit' or p.slice[1].type == 'KEYWORD_EXIT':
            # exit()
            p[0] = ('system_exit',)
        elif len(p) == 6:
            # This handles both system function patterns
            if p[1] in ['input', 'output']:
                p[0] = ('system_' + p[1], p[3], p[5])
            else:
                # Other functions with expression, type syntax
                p[0] = ('function_call', p[1], [p[3], p[5]])
        elif len(p) == 4:
            # Regular function with no args
            p[0] = ('function_call', p[1], [])
        else:
            # Regular function with args
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
                             | FLOAT_LITERAL
                             | STRING_LITERAL
                             | CHAR_LITERAL
                             | KEYWORD_TRUE
                             | KEYWORD_FALSE
                             | KEYWORD_NULL
                             | LPAREN expression RPAREN
                             | function_call'''
        if len(p) == 2:
            # Check if identifier exists in symbol table
            if p.slice[1].type == 'IDENTIFIER':
                symbol = self.symbol_table.lookup_symbol(p[1])
                if not symbol:
                    print(f"Error: Variable '{p[1]}' used before declaration")
            p[0] = ('primary', p[1])
        else:
            p[0] = p[2]
    
    def p_error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token='{p.value}', type={p.type}")
            print(f"Parser state: {p.parser.state}")
            
            # Print expected tokens
            expected = []
            for token_type in p.parser.action[p.parser.state]:
                if token_type > 0:  # Skip EOF and error tokens
                    expected.append(p.parser.symstack[token_type])
            if expected:
                print(f"Expected one of: {', '.join(expected)}")
        else:
            print("Syntax error at EOF - unexpected end of input")

def print_ast(node, indent=0):
    indent_str = "  " * indent
    if isinstance(node, tuple):
        print(f"{indent_str}{node[0]}")
        for i in range(1, len(node)):
            if isinstance(node[i], (list, tuple)):
                print_ast(node[i], indent + 1)
            else:
                print(f"{indent_str}  {node[i]}")
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    else:
        print(f"{indent_str}{node}")
