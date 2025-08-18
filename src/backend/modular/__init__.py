"""
Modular LLVM Code Generator Package

This package provides a clean, maintainable architecture for LLVM code generation
by breaking down the monolithic generator into focused, single-responsibility components.
"""

from .context import LLVMContext
from .type_manager import TypeManager
from .runtime_manager import RuntimeFunctionManager
from .expression_generator import ExpressionGenerator
from .control_flow_generator import ControlFlowGenerator
from .main_generator import ModularLLVMGenerator

__all__ = [
    'LLVMContext',
    'TypeManager', 
    'RuntimeFunctionManager',
    'ExpressionGenerator',
    'ControlFlowGenerator',
    'ModularLLVMGenerator'
]
