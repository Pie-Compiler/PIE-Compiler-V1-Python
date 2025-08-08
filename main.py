from parser import Parser, print_ast
from semanticAnalysis import SemanticAnalyzer
from ir_generator import IRGenerator
from llvmConverter import IRToLLVMConverter
import subprocess
def build_and_link():
    try:
        # Compile the runtime functions to an object file
        subprocess.run(["clang", "-c", "runtime.c", "-o", "runtime.o"], check=True)
        # Compile the math library to an object file
        subprocess.run(["clang", "-c", "math_lib.c", "-o", "math_lib.o"], check=True)
        # Compile the file library to an object file
        subprocess.run(["clang", "-c", "file_lib.c", "-o", "file_lib.o"], check=True)
        # Compile the network library to an object file
        subprocess.run(["clang", "-c", "net_lib.c", "-o", "net_lib.o"], check=True)
        # Convert LLVM IR to bitcode
        subprocess.run(["llvm-as", "output.ll", "-o", "output.bc"], check=True)
        # Generate native object file from bitcode
        subprocess.run(["llc", "-filetype=obj", "output.bc", "-o", "output.o"], check=True)
        # Link everything together to create the executable
        subprocess.run(["clang", "output.o", "runtime.o", "math_lib.o", "file_lib.o", "net_lib.o", "-o", "program", "-lm"], check=True)
        print("Build and linking successful! Executable: ./program")
    except subprocess.CalledProcessError as e:
        print(f"Error during build and linking process: {e}")
        raise
def main():
    # Create an instance of our parser
    parser = Parser()
    
    # Example program
    # test_program_file="test_math_int.pie"
    #make sure that it is a .pie file
    with open("test_math_int.pie", "r") as file:
        input_program = file.read()

    try:
        # Parse the program
        ast = parser.parse(input_program)
        print("Parsing successful!")
        print("AST:")
        print_ast(ast)  # Use prettier printing
        # Perform semantic analysis
        analyzer = SemanticAnalyzer(parser.symbol_table)
        is_valid, new_ast = analyzer.analyze(ast)
        
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
            ir_code = ir_gen.generate(new_ast, parser.symbol_table)
            
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
            with open("output.ll", "w") as llvm_file:
                llvm_file.write(LLVMCODE)
            # for instruction in llvm_code:
            #     print(f"  {instruction}")
            # Build and link the program
            build_and_link()

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