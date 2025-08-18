"""
LLVM Context Management

This module provides the central context for LLVM generation,
shared across all components.
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
from typing import Dict, List, Optional, Any


class LLVMContext:
    """Central context for LLVM generation, shared across all components."""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.module = ir.Module(name="main_module")
        self.target_machine = None
        self.current_function = None
        self.builder = None
        self.llvm_var_table = {}
        self.global_strings = {}
        self.global_vars = {}
        self.global_dynamic_arrays = []
        self.deferred_initializers = []
        self.symbol_table = None
        
        self._initialize_llvm()
    
    def _initialize_llvm(self):
        """Initialize LLVM bindings and target machine."""
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.target_machine = llvm.Target.from_default_triple().create_target_machine()
        self.module.triple = self.target_machine.triple
        self.module.data_layout = self.target_machine.target_data
    
    def get_global_string(self, str_val: str) -> ir.Value:
        """Get or create a global string constant."""
        if str_val in self.global_strings:
            return self.global_strings[str_val]
        
        c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_val)), 
                           bytearray(str_val.encode("utf8")))
        global_var = ir.GlobalVariable(self.module, c_str.type, 
                                     name=f".str{len(self.global_strings)}")
        global_var.initializer = c_str
        global_var.global_constant = True
        global_var.linkage = 'internal'
        
        if self.builder:
            ptr = self.builder.bitcast(global_var, ir.IntType(8).as_pointer())
        else:
            ptr = global_var.gep([ir.Constant(ir.IntType(32), 0), 
                                ir.Constant(ir.IntType(32), 0)])
        
        self.global_strings[str_val] = ptr
        return ptr
    
    def add_global_variable(self, name: str, var_type: ir.Type, 
                           initializer: Optional[ir.Constant] = None) -> ir.GlobalVariable:
        """Add a global variable to the module."""
        global_var = ir.GlobalVariable(self.module, var_type, name=name)
        if initializer:
            global_var.initializer = initializer
        global_var.linkage = 'internal'
        
        self.global_vars[name] = global_var
        self.llvm_var_table[name] = global_var
        return global_var
    
    def add_global_dynamic_array(self, name: str, element_type: str, 
                                init_nodes: List, is_dynamic: bool, 
                                expr_initializer=None):
        """Add a global dynamic array to the tracking list."""
        self.global_dynamic_arrays.append(
            (name, element_type, init_nodes, is_dynamic, expr_initializer)
        )
    
    def add_deferred_initializer(self, var_name: str, initializer_node):
        """Add a deferred initializer for later processing."""
        self.deferred_initializers.append((var_name, initializer_node))
    
    def clear_function_scope(self):
        """Clear function-local variable table."""
        self.llvm_var_table.clear()
        self.current_function = None
        self.builder = None
