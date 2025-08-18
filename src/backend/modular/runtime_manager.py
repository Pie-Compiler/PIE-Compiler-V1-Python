"""
Runtime Function Management Component

This module handles declaration of all runtime functions.
"""

import llvmlite.ir as ir
from typing import List, Tuple
from .base import CodeGeneratorComponent


class RuntimeFunctionManager(CodeGeneratorComponent):
    """Manages declaration of all runtime functions."""
    
    def __init__(self, context, type_manager):
        super().__init__(context)
        self.type_manager = type_manager
    
    def initialize(self):
        """Declare all runtime functions."""
        self._declare_system_io_functions()
        self._declare_math_functions()
        self._declare_string_functions()
        self._declare_file_functions()
        self._declare_dict_functions()
        self._declare_array_functions()
        self._declare_utility_functions()
    
    def _declare_system_io_functions(self):
        """Declare system I/O functions."""
        int_ptr = self.type_manager.get_llvm_type('int').as_pointer()
        float_ptr = self.type_manager.get_llvm_type('float').as_pointer()
        string_ptr = self.type_manager.get_llvm_type('string').as_pointer()
        char_ptr = self.type_manager.get_llvm_type('char').as_pointer()
        int_type = self.type_manager.get_llvm_type('int')
        string_type = self.type_manager.get_llvm_type('string')
        char_type = self.type_manager.get_llvm_type('char')
        float_type = self.type_manager.get_llvm_type('float')
        
        # Input functions
        self._declare_function("input_int", [int_ptr], ir.VoidType())
        self._declare_function("input_float", [float_ptr], ir.VoidType())
        self._declare_function("input_string", [string_ptr], ir.VoidType())
        self._declare_function("input_char", [char_ptr], ir.VoidType())
        
        # Output functions
        self._declare_function("output_int", [int_type], ir.VoidType())
        self._declare_function("output_string", [string_type], ir.VoidType())
        self._declare_function("output_char", [char_type], ir.VoidType())
        self._declare_function("output_float", [float_type, int_type], ir.VoidType())
        self._declare_function("pie_exit", [], ir.VoidType())
    
    def _declare_math_functions(self):
        """Declare mathematical functions."""
        double_type = self.type_manager.get_llvm_type('float')
        int_type = self.type_manager.get_llvm_type('int')
        
        math_functions = [
            ('pie_sqrt', [double_type], double_type),
            ('pie_pow', [double_type, double_type], double_type),
            ('pie_sin', [double_type], double_type),
            ('pie_cos', [double_type], double_type),
            ('pie_tan', [double_type], double_type),
            ('pie_asin', [double_type], double_type),
            ('pie_acos', [double_type], double_type),
            ('pie_atan', [double_type], double_type),
            ('pie_log', [double_type], double_type),
            ('pie_log10', [double_type], double_type),
            ('pie_exp', [double_type], double_type),
            ('pie_floor', [double_type], double_type),
            ('pie_ceil', [double_type], double_type),
            ('pie_round', [double_type], double_type),
            ('pie_abs', [double_type], double_type),
            ('pie_abs_int', [int_type], int_type),
            ('pie_min', [double_type, double_type], double_type),
            ('pie_max', [double_type, double_type], double_type),
            ('pie_min_int', [int_type, int_type], int_type),
            ('pie_max_int', [int_type, int_type], int_type),
            ('pie_rand', [], int_type),
            ('pie_srand', [int_type], ir.VoidType()),
            ('pie_rand_range', [int_type, int_type], int_type),
            ('pie_pi', [], double_type),
            ('pie_e', [], double_type),
            ('pie_time', [], int_type)
        ]
        
        for name, arg_types, return_type in math_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_string_functions(self):
        """Declare string manipulation functions."""
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        
        string_functions = [
            ('concat_strings', [string_type, string_type], string_type),
            ('pie_strlen', [string_type], int_type),
            ('pie_strcmp', [string_type, string_type], int_type),
            ('pie_strcpy', [string_type, string_type], string_type),
            ('pie_strcat', [string_type, string_type], string_type),
            ('string_contains', [string_type, string_type], int_type),
            ('string_starts_with', [string_type, string_type], int_type),
            ('string_ends_with', [string_type, string_type], int_type),
            ('string_is_empty', [string_type], int_type)
        ]
        
        for name, arg_types, return_type in string_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_file_functions(self):
        """Declare file I/O functions."""
        file_type = self.type_manager.get_llvm_type('file')
        string_type = self.type_manager.get_llvm_type('string')
        
        file_functions = [
            ('file_open', [string_type, string_type], file_type),
            ('file_close', [file_type], ir.VoidType()),
            ('file_write', [file_type, string_type], ir.VoidType()),
            ('file_read_all', [file_type], string_type),
            ('file_read_line', [file_type], string_type)
        ]
        
        for name, arg_types, return_type in file_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_dict_functions(self):
        """Declare dictionary functions."""
        dict_type = self.type_manager.get_dict_type()
        dict_value_type = self.type_manager.get_dict_value_type()
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        float_type = self.type_manager.get_llvm_type('float')
        
        dict_functions = [
            ('dict_create', [], dict_type),
            ('dict_set', [dict_type, string_type, dict_value_type], ir.VoidType()),
            ('dict_get', [dict_type, string_type], dict_value_type),
            ('dict_get_int', [dict_type, string_type], int_type),
            ('dict_get_float', [dict_type, string_type], float_type),
            ('dict_get_string', [dict_type, string_type], string_type),
            ('dict_has_key', [dict_type, string_type], int_type),
            ('dict_key_exists', [dict_type, string_type], int_type),
            ('dict_delete', [dict_type, string_type], ir.VoidType()),
            ('dict_free', [dict_type], ir.VoidType()),
            ('dict_value_create_int', [int_type], dict_value_type),
            ('dict_value_create_float', [float_type], dict_value_type),
            ('dict_value_create_string', [string_type], dict_value_type),
            ('dict_value_create_null', [], dict_value_type),
            ('new_int', [int_type], dict_value_type),
            ('new_float', [float_type], dict_value_type),
            ('new_string', [string_type], dict_value_type)
        ]
        
        for name, arg_types, return_type in dict_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_array_functions(self):
        """Declare dynamic array functions."""
        self._declare_int_array_functions()
        self._declare_string_array_functions()
        self._declare_float_array_functions()
        self._declare_char_array_functions()
    
    def _declare_int_array_functions(self):
        """Declare integer array functions."""
        int_array_ptr = self.type_manager.get_array_type('int')
        int_type = self.type_manager.get_llvm_type('int')
        float_type = self.type_manager.get_llvm_type('float')
        
        int_array_functions = [
            ('d_array_int_push', [int_array_ptr, int_type], ir.VoidType()),
            ('d_array_int_pop', [int_array_ptr], int_type),
            ('d_array_int_size', [int_array_ptr], int_type),
            ('d_array_int_contains', [int_array_ptr, int_type], int_type),
            ('d_array_int_indexof', [int_array_ptr, int_type], int_type),
            ('d_array_int_concat', [int_array_ptr, int_array_ptr], int_array_ptr),
            ('d_array_int_avg', [int_array_ptr], float_type),
            ('d_array_int_get', [int_array_ptr, int_type], int_type),
            ('d_array_int_set', [int_array_ptr, int_type, int_type], ir.VoidType()),
            ('d_array_int_create', [], int_array_ptr),
            ('d_array_int_append', [int_array_ptr, int_type], ir.VoidType()),
            ('print_int_array', [int_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in int_array_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_string_array_functions(self):
        """Declare string array functions."""
        string_array_ptr = self.type_manager.get_array_type('string')
        string_type = self.type_manager.get_llvm_type('string')
        int_type = self.type_manager.get_llvm_type('int')
        
        string_array_functions = [
            ('d_array_string_push', [string_array_ptr, string_type], ir.VoidType()),
            ('d_array_string_pop', [string_array_ptr], string_type),
            ('d_array_string_size', [string_array_ptr], int_type),
            ('d_array_string_contains', [string_array_ptr, string_type], int_type),
            ('d_array_string_indexof', [string_array_ptr, string_type], int_type),
            ('d_array_string_concat', [string_array_ptr, string_array_ptr], string_array_ptr),
            ('d_array_string_get', [string_array_ptr, int_type], string_type),
            ('d_array_string_set', [string_array_ptr, int_type, string_type], ir.VoidType()),
            ('d_array_string_create', [], string_array_ptr),
            ('d_array_string_append', [string_array_ptr, string_type], ir.VoidType()),
            ('print_string_array', [string_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in string_array_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_float_array_functions(self):
        """Declare float array functions."""
        float_array_ptr = self.type_manager.get_array_type('float')
        float_type = self.type_manager.get_llvm_type('float')
        int_type = self.type_manager.get_llvm_type('int')
        
        float_array_functions = [
            ('d_array_float_push', [float_array_ptr, float_type], ir.VoidType()),
            ('d_array_float_pop', [float_array_ptr], float_type),
            ('d_array_float_size', [float_array_ptr], int_type),
            ('d_array_float_contains', [float_array_ptr, float_type], int_type),
            ('d_array_float_indexof', [float_array_ptr, float_type], int_type),
            ('d_array_float_avg', [float_array_ptr], float_type),
            ('d_array_float_get', [float_array_ptr, int_type], float_type),
            ('d_array_float_set', [float_array_ptr, int_type, float_type], ir.VoidType()),
            ('d_array_float_create', [], float_array_ptr),
            ('d_array_float_append', [float_array_ptr, float_type], ir.VoidType()),
            ('d_array_float_free', [float_array_ptr], ir.VoidType()),
            ('print_float_array', [float_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in float_array_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_char_array_functions(self):
        """Declare char array functions."""
        char_array_ptr = self.type_manager.get_array_type('char')
        char_type = self.type_manager.get_llvm_type('char')
        int_type = self.type_manager.get_llvm_type('int')
        bool_type = self.type_manager.get_llvm_type('boolean')
        
        char_array_functions = [
            ('d_array_char_create', [], char_array_ptr),
            ('d_array_char_append', [char_array_ptr, char_type], ir.VoidType()),
            ('d_array_char_get', [char_array_ptr, int_type], char_type),
            ('d_array_char_set', [char_array_ptr, int_type, char_type], ir.VoidType()),
            ('d_array_char_size', [char_array_ptr], int_type),
            ('d_array_char_free', [char_array_ptr], ir.VoidType()),
            ('d_array_char_pop', [char_array_ptr], char_type),
            ('d_array_char_contains', [char_array_ptr, char_type], bool_type),
            ('d_array_char_indexof', [char_array_ptr, char_type], int_type),
            ('d_array_char_concat', [char_array_ptr, char_array_ptr], char_array_ptr),
            ('print_char_array', [char_array_ptr], ir.VoidType())
        ]
        
        for name, arg_types, return_type in char_array_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_utility_functions(self):
        """Declare utility functions."""
        int_type = self.type_manager.get_llvm_type('int')
        
        utility_functions = [
            ('is_variable_defined', [ir.IntType(8).as_pointer()], int_type),
            ('is_variable_null', [ir.IntType(8).as_pointer()], int_type)
        ]
        
        for name, arg_types, return_type in utility_functions:
            self._declare_function(name, arg_types, return_type)
    
    def _declare_function(self, name: str, arg_types: List[ir.Type], return_type: ir.Type):
        """Declare a function in the module."""
        ir.Function(self.context.module, ir.FunctionType(return_type, arg_types), name=name)
    
    def get_function(self, name: str):
        """Get a declared function by name."""
        try:
            return self.context.module.get_global(name)
        except KeyError:
            return None
