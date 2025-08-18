"""
Base Component Classes

This module provides the base classes for all code generator components.
"""

from abc import ABC, abstractmethod
from typing import Any
from .context import LLVMContext


class CodeGeneratorComponent(ABC):
    """Base class for all code generator components."""
    
    def __init__(self, context):
        self.context = context
    
    def initialize(self):
        """Initialize the component."""
        pass
    
    def get_context(self):
        """Get the LLVM context."""
        return self.context
    
    def get_module(self):
        """Get the LLVM module."""
        return self.context.module
    
    def get_builder(self):
        """Get the current IR builder."""
        return self.context.builder
    
    def get_current_function(self):
        """Get the current function being generated."""
        return self.context.current_function
