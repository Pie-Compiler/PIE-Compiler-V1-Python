# Directly Coded Lexer Example Using NFA to DFA Conversion 
# ---------------------------- 
# NFA State Data Structure 
# ---------------------------- 
class NFAState: 
    def __init__(self): 
        self.transitions = {}         # transitions on symbols: {symbol: [state, ...]} 
        self.epsilon_transitions = [] # transitions on epsilon (None) 
        self.is_accepting = False     # indicates whether this state is accepting 
        self.token_type = None        # token type if state is accepting 
 
def add_epsilon_transition(from_state, to_state): 
    from_state.epsilon_transitions.append(to_state) 

def build_literal_nfa(literal):
    start = NFAState()
    current = start
    for ch in literal:
        next_state = NFAState()
        current.transitions.setdefault(ch, []).append(next_state)
        current = next_state
    return start, current
# ---------------------------- 
# Thompson's Construction Functions 
# ---------------------------- 
def literal_nfa(char): 
    """Creates an NFA fragment for a literal character.""" 
    start = NFAState() 
    accept = NFAState() 
    start.transitions[char] = [accept] 
    accept.is_accepting = True 
    return start, accept 
 
def concatenate_nfa(nfa1, nfa2): 
    """Concatenates two NFA fragments.""" 
    nfa1_accept = nfa1[1] 
    nfa2_start = nfa2[0] 
    nfa1_accept.is_accepting = False 
    add_epsilon_transition(nfa1_accept, nfa2_start) 
    return nfa1[0], nfa2[1] 
 
def alternate_nfa(nfa1, nfa2): 
    """Creates an NFA that recognizes either nfa1 or nfa2.""" 
    start = NFAState() 
    accept = NFAState() 
    add_epsilon_transition(start, nfa1[0]) 
    add_epsilon_transition(start, nfa2[0]) 
    nfa1[1].is_accepting = False 
    nfa2[1].is_accepting = False 
    add_epsilon_transition(nfa1[1], accept) 
    add_epsilon_transition(nfa2[1], accept) 
    accept.is_accepting = True 
    return start, accept 
 
def kleene_star_nfa(nfa): 
    """Applies the Kleene star to an NFA fragment.""" 
    start = NFAState() 
    accept = NFAState() 
    add_epsilon_transition(start, nfa[0]) 
    add_epsilon_transition(start, accept) 
    nfa[1].is_accepting = False 
    add_epsilon_transition(nfa[1], nfa[0]) 
    add_epsilon_transition(nfa[1], accept) 
    accept.is_accepting = True 
    return start, accept 
 
# ---------------------------- 
# NFA to DFA Conversion (Subset Construction) 
# ---------------------------- 
def epsilon_closure(states): 
    """Returns the epsilon closure of a set of NFA states.""" 
    stack = list(states) 
    closure = set(states) 
    while stack: 
        state = stack.pop() 
        for next_state in state.epsilon_transitions: 
            if next_state not in closure: 
                closure.add(next_state) 
                stack.append(next_state) 
    return closure 
 
def move(states, symbol): 
    """Returns the set of states reachable on a given symbol.""" 
    result = set() 
    for state in states: 
        if symbol in state.transitions: 
            result.update(state.transitions[symbol]) 
    return result 
 
def get_alphabet(state_set): 
    """Extracts the set of input symbols from a set of NFA states.""" 
    symbols = set() 
    for state in state_set: 
        symbols.update(state.transitions.keys()) 
    return symbols 
 
def nfa_to_dfa(nfa_start): 
    """ 
    Converts an NFA into a DFA using the subset construction method. 
    Returns: 
      - dfa_transitions: dict mapping DFA states (frozensets) to 
transitions { symbol: next DFA state } 
      - dfa_token: dict mapping DFA state to token type (if accepting) 
    """ 
    dfa_transitions = {} 
    dfa_token = {} 
     
    start_set = epsilon_closure({nfa_start}) 
    start_dfa = frozenset(start_set) 
    unmarked_states = [start_dfa] 
    dfa_transitions[start_dfa] = {} 
     
    for state in start_set: 
        if state.is_accepting: 
            dfa_token[start_dfa] = state.token_type 
            break 
 
    while unmarked_states: 
        current = unmarked_states.pop() 
        dfa_transitions[current] = {} 
        symbols = get_alphabet(current) 
        for symbol in symbols: 
            next_states = epsilon_closure(move(current, symbol)) 
            if not next_states: 
                continue 
            next_dfa = frozenset(next_states) 
            dfa_transitions[current][symbol] = next_dfa 
            if next_dfa not in dfa_transitions: 
                unmarked_states.append(next_dfa) 
                for state in next_dfa: 
                    if state.is_accepting: 
                        dfa_token[next_dfa] = state.token_type 
                        break 
    return dfa_transitions, dfa_token 
 
# ---------------------------- 
# Lexer Class Using the DFA 
# ---------------------------- 
class Lexer: 
    def __init__(self, dfa_transitions, dfa_token, start_state): 
        self.dfa = dfa_transitions      # DFA transition table 
        self.token_map = dfa_token      # Mapping from DFA state to token type 
        self.start_state = start_state  # DFA start state 
 
    def tokenize(self, input_string): 
        pos = 0 
        tokens = [] 
        while pos < len(input_string): 
            if input_string[pos].isspace(): 
                pos += 1 
                continue 
            current_state = self.start_state 
            last_accepting = None 
            last_accepting_pos = pos 
            current_pos = pos 
            while current_pos < len(input_string): 
                symbol = input_string[current_pos] 
                if symbol in self.dfa[current_state]: 
                    current_state = self.dfa[current_state][symbol] 
                    current_pos += 1 
                    if current_state in self.token_map: 
                        last_accepting = current_state 
                        last_accepting_pos = current_pos 
                else: 
                    break 
            if last_accepting is None: 
                raise Exception(f"Lexical error at position {pos}") 
            token_text = input_string[pos:last_accepting_pos] 
            token_type = self.token_map[last_accepting] 
            tokens.append((token_type, token_text)) 
            pos = last_accepting_pos 
        return tokens 
 
# ---------------------------- 
# Building the Master NFA 
# ---------------------------- 
def build_master_nfa():
    master_start = NFAState()

    # Keywords
    keywords = {
        "if": "KEYWORD_IF",
        "else": "KEYWORD_ELSE",
        "for": "KEYWORD_FOR",
        "while": "KEYWORD_WHILE",
        "return": "KEYWORD_RETURN",
        "break": "KEYWORD_BREAK",
        "continue": "KEYWORD_CONTINUE",
        "exit": "KEYWORD_EXIT",
        "int": "KEYWORD_INT",
        "float": "KEYWORD_FLOAT",
        "char": "KEYWORD_CHAR",
        "void": "KEYWORD_VOID",
        "string": "KEYWORD_STRING",
        "bool": "KEYWORD_BOOL",
        "true": "KEYWORD_TRUE",
        "false": "KEYWORD_FALSE",
        "null": "KEYWORD_NULL",
    }
    for word, token_name in keywords.items():
        nfa_start, nfa_end = build_literal_nfa(word)
        nfa_end.is_accepting = True
        nfa_end.token_type = token_name
        add_epsilon_transition(master_start, nfa_start)

    # Identifiers: [A-Za-z_][A-Za-z0-9_]*
    id_start = NFAState()
    id_accept = NFAState()
    for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        id_start.transitions.setdefault(ch, []).append(id_accept)
    for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
        id_accept.transitions.setdefault(ch, []).append(id_accept)
    id_accept.is_accepting = True
    id_accept.token_type = "IDENTIFIER"
    add_epsilon_transition(master_start, id_start)

    # Integer literal: [0-9]+
    int_start = NFAState()
    int_accept = NFAState()
    for d in "0123456789":
        int_start.transitions.setdefault(d, []).append(int_accept)
        int_accept.transitions.setdefault(d, []).append(int_accept)
    int_accept.is_accepting = True
    int_accept.token_type = "INT_LITERAL"
    add_epsilon_transition(master_start, int_start)

    # Punctuation
    punctuations = {
        '(': "LPAREN", ')': "RPAREN",
        '{': "LBRACE", '}': "RBRACE",
        ';': "SEMICOLON", ',': "COMMA"
    }
    for p, token_name in punctuations.items():
        start, end = build_literal_nfa(p)
        end.is_accepting = True
        end.token_type = token_name
        add_epsilon_transition(master_start, start)

    # Operators
    operators = {
        '+': "PLUS", '-': "MINUS", '*': "MUL", '/': "DIV",
        '=': "ASSIGN", '==': "EQ", '&&': "AND", '||': "OR"
    }
    for op, token_name in operators.items():
        start, end = build_literal_nfa(op)
        end.is_accepting = True
        end.token_type = token_name
        add_epsilon_transition(master_start, start)

    return master_start
 
# ---------------------------- 
# Main Function 
# ---------------------------- 
def main(): 
    # Build the master NFA. 
    nfa_start = build_master_nfa() 
    # Convert the NFA into a DFA. 
    dfa_transitions, dfa_token = nfa_to_dfa(nfa_start) 
    start_set = frozenset(epsilon_closure({nfa_start})) 
    # Create the Lexer instance. 
    lexer = Lexer(dfa_transitions, dfa_token, start_set) 
    # Tokenize an example input. 
    input_program = "if(x){ x = 10; " 
    tokens = lexer.tokenize(input_program) 
    print("Tokens:") 
    for token in tokens: 
        print(token) 
 
if __name__ == "__main__": 
    main() 