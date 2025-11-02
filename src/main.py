from frontend.parser import Parser, print_ast
from frontend.semanticAnalysis import SemanticAnalyzer
from frontend.module_resolver import ModuleResolver
from backend.llvm_generator import LLVMCodeGenerator
import subprocess
import traceback
import sys
import os

import llvmlite.binding as llvm

def build_and_link(llvm_module, c_sources=None, libraries=None):
    """
    Build and link the LLVM module with C runtime and optional module sources.
    
    Args:
        llvm_module: The LLVM module to compile
        c_sources: Additional C source files from modules (list of paths)
        libraries: Additional libraries to link (list of library names)
    """
    obj_files = []
    c_sources = c_sources or []
    libraries = libraries or []
    
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
        
        # Core runtime files (always compiled)
        core_runtime_files = [
            'runtime.c',
            'd_array.c',
            'dict_lib.c',
            'string_lib.c',
            'file_lib.c',
            'crypto_lib.c',
            'time_lib.c',
            'regex_lib.c',
            'math_lib.c',
            'net_lib.c'
        ]
        
        # Track which C files are being compiled
        runtime_c_files = set()
        
        # Compile core runtime files
        for c_file in core_runtime_files:
            if os.path.exists(os.path.join(runtime_path, c_file)):
                obj_file = c_file.replace('.c', '.o')
                subprocess.run(
                    [clang_path, "-c", "-fPIC", os.path.join(runtime_path, c_file), "-o", obj_file],
                    check=True
                )
                obj_files.append(obj_file)
                runtime_c_files.add(c_file)
        
        # Compile module-specific C sources if any (skip duplicates already in runtime/)
        for c_source_path in c_sources:
            c_file = os.path.basename(c_source_path)
            # Skip if this file was already compiled from runtime directory
            if c_file in runtime_c_files:
                continue
            if os.path.exists(c_source_path):
                obj_file = c_file.replace('.c', '.o')
                print(f"Compiling module source: {c_source_path}")
                subprocess.run(
                    [clang_path, "-c", "-fPIC", str(c_source_path), "-o", obj_file],
                    check=True
                )
                obj_files.append(obj_file)

        # --- Link all object files ---
        link_command = [clang_path, "output.o"] + obj_files + ["-o", "program", "-lm"]
        
        # Add additional libraries from modules
        for lib in libraries:
            link_command.append(f"-l{lib}")
        
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

        # Initialize module resolver
        module_resolver = ModuleResolver()
        
        # Semantic analysis with module support
        analyzer = SemanticAnalyzer(parser.symbol_table, module_resolver)
        is_valid, ast = analyzer.analyze(ast, source_file=input_file)

        if analyzer.errors:
            print("\n--- Semantic Errors ---")
            for error in analyzer.errors:
                print(f"- {error}")

        if is_valid:
            print("\nProgram is semantically valid!")

            # Code Generation with imported modules
            llvm_generator = LLVMCodeGenerator(
                parser.symbol_table, 
                analyzer.imported_modules
            )
            llvm_module = llvm_generator.generate(ast)

            # Save the human-readable IR for debugging
            with open("output.ll", "w") as f:
                f.write(str(llvm_module))

            # Collect C sources and libraries from imported modules
            c_sources = []
            libraries = []
            
            for module_name, module_info in analyzer.imported_modules.items():
                # Get C sources from module
                module_c_sources = module_resolver.get_module_c_sources(module_name)
                c_sources.extend(module_c_sources)
                
                # Get libraries from module
                module_libraries = module_resolver.get_module_libraries(module_name)
                libraries.extend(module_libraries)
            
            if analyzer.imported_modules:
                print(f"\nImported modules: {', '.join(analyzer.imported_modules.keys())}")
                if c_sources:
                    print(f"Module C sources: {[str(s) for s in c_sources]}")
                if libraries:
                    print(f"Module libraries: {libraries}")

            # Build and Link with module dependencies
            build_and_link(llvm_module, c_sources, libraries)

        else:
            print("\nCompilation failed due to semantic errors.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
