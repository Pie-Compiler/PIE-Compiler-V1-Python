from parser import Parser,print_ast
# Add import for semantic analyzer
from semanticAnalysis import SemanticAnalyzer

# Update the main function
def main():
    # Create an instance of our parser
    parser = Parser()
    
    # Example program
    with open("test4.pie", "r") as file: 
        input_program = file.read()

    try:
        # Parse the program
        ast = parser.parse(input_program)
        print("Parsing successful!")
        print("AST:")
        print_ast(ast)  # Use prettier printing
        
        # Perform semantic analysis
        analyzer = SemanticAnalyzer(parser.symbol_table)
        is_valid = analyzer.analyze(ast)
        
        # Print semantic errors/warnings
        if analyzer.errors:
            print("\nSemantic Errors:")
            for error in analyzer.errors:
                print(f"  - {error}")
        
        if analyzer.warnings:
            print("\nSemantic Warnings:")
            for warning in analyzer.warnings:
                print(f"  - {warning}")
        
        if is_valid:
            print("\nProgram is semantically valid!")
        else:
            print("\nProgram contains semantic errors!")
        
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