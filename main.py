from parser import Parser, print_ast
from semanticAnalysis import SemanticAnalyzer
from ir_generator import IRGenerator
from llvmConverter import IRToLLVMConverter
def main():
    # Create an instance of our parser
    parser = Parser()
    
    # Example program
    with open("test2.pie", "r") as file: 
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
            
            # Generate intermediate representation
            ir_gen = IRGenerator()
            ir_code = ir_gen.generate(ast, parser.symbol_table)
            
            print("\nIntermediate Representation (3-Address Code):")

            #save the IR code to a file
            with open("output.ir", "w") as ir_file:
                for instruction in ir_code:
                    ir_file.write(f"{instruction}\n")
            for instruction in ir_code:
                print(f"  {instruction}")
            #Translate the IR code to LLVM
            llvm_converter = IRToLLVMConverter()
            llvm_converter.convert_ir(ir_code)
            LLVMCODE= llvm_converter.finalize()
            # print("\nLLVM Code:")
            # print(llvm_code)
            # #save the LLVM code to a file
            # with open("output.ll", "w") as llvm_file:
            #     for instruction in llvm_code:
            #         llvm_file.write(f"{instruction}\n")
            # for instruction in llvm_code:
            #     print(f"  {instruction}")

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