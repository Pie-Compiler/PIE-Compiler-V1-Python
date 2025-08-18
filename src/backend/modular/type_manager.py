"""
Type Management Component

This module handles LLVM type definitions and type conversions.
"""

import llvmlite.ir as ir
from typing import Dict, Optional
from .base import CodeGeneratorComponent


class TypeManager(CodeGeneratorComponent):
    """Manages LLVM type definitions and type conversions."""
    
    def __init__(self, context):
        super().__init__(context)
        self.d_array_types = {}
        self.dict_types = {}
    
    def initialize(self):
        """Define all LLVM struct types."""
        self._define_array_structs()
        self._define_dict_structs()
    
    def _define_array_structs(self):
        """Define dynamic array struct types."""
        # Integer array
        d_array_int_struct = self.context.module.context.get_identified_type("DArrayInt")
        d_array_int_struct.set_body(
            ir.IntType(32).as_pointer(),  # data
            ir.IntType(64),               # size
            ir.IntType(64)                # capacity
        )
        self.d_array_types['int'] = d_array_int_struct.as_pointer()
        
        # String array
        d_array_string_struct = self.context.module.context.get_identified_type("DArrayString")
        d_array_string_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(),  # data
            ir.IntType(64),                           # size
            ir.IntType(64)                            # capacity
        )
        self.d_array_types['string'] = d_array_string_struct.as_pointer()
        
        # Float array
        d_array_float_struct = self.context.module.context.get_identified_type("DArrayFloat")
        d_array_float_struct.set_body(
            ir.DoubleType().as_pointer(),  # data
            ir.IntType(64),               # size
            ir.IntType(64)                # capacity
        )
        self.d_array_types['float'] = d_array_float_struct.as_pointer()
        
        # Char array
        d_array_char_struct = self.context.module.context.get_identified_type("DArrayChar")
        d_array_char_struct.set_body(
            ir.IntType(8).as_pointer(),  # data
            ir.IntType(64),              # size
            ir.IntType(64)               # capacity
        )
        self.d_array_types['char'] = d_array_char_struct.as_pointer()
    
    def _define_dict_structs(self):
        """Define dictionary struct types."""
        dict_value_struct = self.context.module.context.get_identified_type("DictValue")
        dict_struct = self.context.module.context.get_identified_type("Dictionary")
        
        dict_value_struct.set_body(
            ir.IntType(32),  # type
            ir.IntType(64)   # union (simplified)
        )
        self.dict_types['value'] = dict_value_struct.as_pointer()
        
        dict_struct.set_body(
            ir.IntType(8).as_pointer().as_pointer(),  # buckets
            ir.IntType(32),                           # capacity
            ir.IntType(32)                            # size
        )
        self.dict_types['dict'] = dict_struct.as_pointer()
    
    def get_llvm_type(self, type_str: str) -> ir.Type:
        """Convert PIE type string to LLVM type."""
        if type_str.startswith('KEYWORD_'):
            type_str = type_str.split('_')[1].lower()
        
        type_map = {
            'int': ir.IntType(32),
            'float': ir.DoubleType(),
            'char': ir.IntType(8),
            'string': ir.IntType(8).as_pointer(),
            'boolean': ir.IntType(1),
            'void': ir.VoidType(),
            'file': ir.IntType(64),
            'socket': ir.IntType(32),
            'd_array_int': self.d_array_types['int'],
            'd_array_string': self.d_array_types['string'],
            'd_array_float': self.d_array_types['float'],
            'd_array_char': self.d_array_types['char'],
            'dict': self.dict_types['dict'],
            'void*': ir.IntType(8).as_pointer()
        }
        
        if type_str in type_map:
            return type_map[type_str]
        
        # Handle array types
        if type_str.startswith('array_type'):
            element_type_str = type_str.split('(')[1][:-1]
            return self.get_llvm_type(element_type_str).as_pointer()
        
        raise ValueError(f"Unknown type: {type_str}")
    
    def get_array_type(self, element_type: str) -> ir.Type:
        """Get the LLVM type for a dynamic array of the given element type."""
        if element_type in self.d_array_types:
            return self.d_array_types[element_type]
        raise ValueError(f"Unknown array element type: {element_type}")
    
    def get_dict_value_type(self) -> ir.Type:
        """Get the LLVM type for dictionary values."""
        return self.dict_types['value']
    
    def get_dict_type(self) -> ir.Type:
        """Get the LLVM type for dictionaries."""
        return self.dict_types['dict']
    
    def is_array_type(self, type_str: str) -> bool:
        """Check if a type string represents an array type."""
        return (type_str.startswith('d_array_') or 
                type_str.startswith('array_type') or
                type_str in self.d_array_types)
    
    def is_dict_type(self, type_str: str) -> bool:
        """Check if a type string represents a dictionary type."""
        return type_str == 'dict' or type_str == 'KEYWORD_DICT'
