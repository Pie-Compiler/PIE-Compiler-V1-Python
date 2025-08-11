from frontend.parser import Parser, print_ast
from frontend.semanticAnalysis import SemanticAnalyzer
from backend.llvm_generator import LLVMCodeGenerator
import subprocess
import traceback
import sys
import os

import llvmlite.binding as llvm

def build_and_link(llvm_module):
    obj_files = []
    try:
        # Create a target machine from the default triple
        target_machine = llvm.Target.from_default_triple().create_target_machine()

        # Emit the object file from the LLVM module
        obj_code = target_machine.emit_object(llvm_module)
        with open("output.o", "wb") as f:
            f.write(obj_code)

        # --- Compile C runtime files ---
        llvm_bin_path = "/usr/lib/llvm-18/bin/"
        clang_path = os.path.join(llvm_bin_path, "clang")
        runtime_path = "src/runtime/"
        c_files = [f for f in os.listdir(runtime_path) if f.endswith('.c')]

        for c_file in c_files:
            obj_file = c_file.replace('.c', '.o')
            subprocess.run(
                [clang_path, "-c", "-fPIC", os.path.join(runtime_path, c_file), "-o", obj_file],
                check=True
            )
            obj_files.append(obj_file)

        # --- Link all object files ---
        link_command = [clang_path, "output.o"] + obj_files + ["-o", "program", "-lm"]
        subprocess.run(link_command, check=True)

        print("Build and linking successful! Executable: ./program")

    except subprocess.CalledProcessError as e:
        print(f"Error during build and linking process: {e}")
        raise
    finally:
        # Clean up temporary object files
        for obj_file in obj_files + ['output.o']:
             if os.path.exists(obj_file):
                os.remove(obj_file)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/main.py <path_to_pie_file>")
        # Default to a test file for development
        input_file = "tests/test_functions.pie"
        print(f"No file provided. Compiling default file: {input_file}")
    else:
        input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    with open(input_file, "r") as file:
        input_program = file.read()

    parser = Parser()

    try:
        ast = parser.parse(input_program)
        print_ast(ast)
        print("Parsing successful!")

        analyzer = SemanticAnalyzer(parser.symbol_table)
        is_valid, ast = analyzer.analyze(ast)

        if analyzer.errors:
            print("\n--- Semantic Errors ---")
            for error in analyzer.errors:
                print(f"- {error}")

        if is_valid:
            print("\nProgram is semantically valid!")

            # Code Generation returns the compiled llvmlite module object
            llvm_generator = LLVMCodeGenerator(parser.symbol_table)
            llvm_module = llvm_generator.generate(ast)

            # Save the human-readable IR for debugging
            with open("output.ll", "w") as f:
                f.write(str(llvm_module))

            # Build and Link using the module object
            build_and_link(llvm_module)

        else:
            print("\nCompilation failed due to semantic errors.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()