#!/usr/bin/env python3
"""
Example Usage of Modular LLVM Generator

This script demonstrates how to use the new modular LLVM generator
as a replacement for the monolithic generator.
"""

import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from frontend.lexer import Lexer
from frontend.parser import Parser
from frontend.semanticAnalysis import SemanticAnalyzer
from frontend.symbol_table import SymbolTable
from modular import ModularLLVMGenerator


def compile_pie_code(source_code, debug=True):
    """
    Compile PIE source code using the modular LLVM generator.
    
    Args:
        source_code (str): PIE source code to compile
        debug (bool): Whether to enable debug output
    
    Returns:
        The compiled LLVM module
    """
    try:
        # 1. Lexical Analysis
        print("=== Lexical Analysis ===")
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        print(f"Generated {len(tokens)} tokens")
        
        # 2. Parsing
        print("\n=== Parsing ===")
        parser = Parser()
        ast = parser.parse(tokens)
        print("AST generated successfully")
        
        # 3. Semantic Analysis
        print("\n=== Semantic Analysis ===")
        symbol_table = SymbolTable()
        semantic_analyzer = SemanticAnalyzer(symbol_table)
        semantic_analyzer.analyze(ast)
        print("Semantic analysis completed")
        
        # 4. LLVM Code Generation (using modular generator)
        print("\n=== LLVM Code Generation ===")
        llvm_generator = ModularLLVMGenerator(symbol_table, debug=debug)
        llvm_module = llvm_generator.generate(ast)
        print("LLVM IR generated successfully")
        
        return llvm_module
        
    except Exception as e:
        print(f"Compilation error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return None


def main():
    """Main function demonstrating the modular LLVM generator."""
    
    # Example PIE code
    pie_source = """
    // Simple PIE program demonstrating various features
    int main() {
        int x = 10;
        float y = 3.14;
        string message = "Hello, PIE!";
        
        // Control flow
        if (x > 5) {
            output_string("x is greater than 5");
        } else {
            output_string("x is 5 or less");
        }
        
        // Loop
        int i = 0;
        while (i < 3) {
            output_int(i);
            i = i + 1;
        }
        
        // Array operations
        d_array_int numbers;
        numbers = d_array_int_create();
        d_array_int_append(numbers, 1);
        d_array_int_append(numbers, 2);
        d_array_int_append(numbers, 3);
        
        // Dictionary operations
        dict scores;
        scores = dict_create();
        dict_set(scores, "Alice", new_int(95));
        dict_set(scores, "Bob", new_int(87));
        
        return 0;
    }
    """
    
    print("PIE Compiler - Modular LLVM Generator Example")
    print("=" * 50)
    print("Source Code:")
    print(pie_source)
    print("=" * 50)
    
    # Compile the code
    llvm_module = compile_pie_code(pie_source, debug=True)
    
    if llvm_module:
        print("\n=== Compilation Successful ===")
        print("LLVM Module Details:")
        print(f"  - Functions: {len(list(llvm_module.functions))}")
        print(f"  - Global Variables: {len(list(llvm_module.globals))}")
        
        # Print function names
        print("\nFunctions in module:")
        for func in llvm_module.functions:
            print(f"  - {func.name}: {func.function_type}")
        
        # Print global variables
        print("\nGlobal variables in module:")
        for global_var in llvm_module.globals:
            print(f"  - {global_var.name}: {global_var.type}")
            
    else:
        print("\n=== Compilation Failed ===")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
