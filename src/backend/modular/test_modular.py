#!/usr/bin/env python3
"""
Simple Test Script for Modular LLVM Generator

This script tests the basic functionality of the modular components
to ensure they work together correctly.
"""

import sys
import os

# Add the current directory to the path so we can import the modules directly
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_modular_imports():
    """Test that all modular components can be imported correctly."""
    try:
        from context import LLVMContext
        from type_manager import TypeManager
        from runtime_manager import RuntimeFunctionManager
        from expression_generator import ExpressionGenerator
        from control_flow_generator import ControlFlowGenerator
        from main_generator import ModularLLVMGenerator
        print("✅ All modular components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_context_creation():
    """Test LLVMContext creation and initialization."""
    try:
        from context import LLVMContext
        
        context = LLVMContext(debug=False)
        assert context.module is not None
        assert context.target_machine is not None
        print("✅ LLVMContext created and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ LLVMContext creation error: {e}")
        return False

def test_type_manager():
    """Test TypeManager functionality."""
    try:
        from context import LLVMContext
        from type_manager import TypeManager
        
        context = LLVMContext(debug=False)
        type_manager = TypeManager(context)
        type_manager.initialize()
        
        # Test basic type conversion
        int_type = type_manager.get_llvm_type('int')
        assert int_type is not None
        assert str(int_type) == 'i32'
        
        # Test array type
        array_type = type_manager.get_array_type('int')
        assert array_type is not None
        
        print("✅ TypeManager functionality verified")
        return True
    except Exception as e:
        print(f"❌ TypeManager error: {e}")
        return False

def test_runtime_manager():
    """Test RuntimeFunctionManager functionality."""
    try:
        from context import LLVMContext
        from type_manager import TypeManager
        from runtime_manager import RuntimeFunctionManager
        
        context = LLVMContext(debug=False)
        type_manager = TypeManager(context)
        runtime_manager = RuntimeFunctionManager(context, type_manager)
        runtime_manager.initialize()
        
        # Test that some functions were declared
        input_int_func = runtime_manager.get_function("input_int")
        output_int_func = runtime_manager.get_function("output_int")
        
        assert input_int_func is not None
        assert output_int_func is not None
        
        print("✅ RuntimeFunctionManager functionality verified")
        return True
    except Exception as e:
        print(f"❌ RuntimeFunctionManager error: {e}")
        return False

def test_expression_generator():
    """Test ExpressionGenerator functionality."""
    try:
        from context import LLVMContext
        from type_manager import TypeManager
        from expression_generator import ExpressionGenerator
        
        context = LLVMContext(debug=False)
        type_manager = TypeManager(context)
        expr_gen = ExpressionGenerator(context, type_manager)
        expr_gen.initialize()
        
        # Test that the component was created
        assert expr_gen is not None
        assert expr_gen.type_manager is not None
        
        print("✅ ExpressionGenerator functionality verified")
        return True
    except Exception as e:
        print(f"❌ ExpressionGenerator error: {e}")
        return False

def test_control_flow_generator():
    """Test ControlFlowGenerator functionality."""
    try:
        from context import LLVMContext
        from control_flow_generator import ControlFlowGenerator
        
        context = LLVMContext(debug=False)
        cf_gen = ControlFlowGenerator(context)
        cf_gen.initialize()
        
        # Test that the component was created
        assert cf_gen is not None
        
        print("✅ ControlFlowGenerator functionality verified")
        return True
    except Exception as e:
        print(f"❌ ControlFlowGenerator error: {e}")
        return False

def test_main_generator():
    """Test ModularLLVMGenerator creation."""
    try:
        from main_generator import ModularLLVMGenerator
        
        # Create a mock symbol table
        class MockSymbolTable:
            def lookup_function(self, name):
                return {
                    'return_type': 'int',
                    'param_types': [],
                    'params': []
                }
        
        symbol_table = MockSymbolTable()
        generator = ModularLLVMGenerator(symbol_table, debug=False)
        
        # Test that all components were created
        assert generator.type_manager is not None
        assert generator.runtime_manager is not None
        assert generator.expression_generator is not None
        assert generator.control_flow_generator is not None
        
        print("✅ ModularLLVMGenerator created successfully")
        return True
    except Exception as e:
        print(f"❌ ModularLLVMGenerator error: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("Running Modular LLVM Generator Tests")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_modular_imports),
        ("LLVMContext Creation", test_context_creation),
        ("TypeManager", test_type_manager),
        ("RuntimeFunctionManager", test_runtime_manager),
        ("ExpressionGenerator", test_expression_generator),
        ("ControlFlowGenerator", test_control_flow_generator),
        ("Main Generator", test_main_generator),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"  ❌ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The modular architecture is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
