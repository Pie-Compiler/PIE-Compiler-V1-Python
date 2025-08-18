"""
Control Flow Generation Component

This module handles generation of LLVM IR for control flow structures.
"""

import llvmlite.ir as ir
from typing import Optional, Any
from .base import CodeGeneratorComponent


class ControlFlowGenerator(CodeGeneratorComponent):
    """Handles generation of LLVM IR for control flow structures."""
    
    def __init__(self, context):
        super().__init__(context)
        self.generator = None  # Will be set by the main generator
    
    def initialize(self):
        """Initialize the control flow generator."""
        pass
    
    def generate_if_statement(self, node):
        """Generate if statement with optional else branch."""
        cond_val = self._load_if_pointer(self.generator.visit(node.condition))
        
        # Convert integer conditions to boolean
        if cond_val.type == ir.IntType(32):
            zero = ir.Constant(ir.IntType(32), 0)
            cond_val = self.context.builder.icmp_signed('!=', cond_val, zero, 'bool_cond')
        
        # Create basic blocks
        then_block = self.context.current_function.append_basic_block(name='then')
        
        if node.else_branch:
            else_block = self.context.current_function.append_basic_block(name='else')
            merge_block = self.context.current_function.append_basic_block(name='if_cont')
            self.context.builder.cbranch(cond_val, then_block, else_block)
        else:
            merge_block = self.context.current_function.append_basic_block(name='if_cont')
            self.context.builder.cbranch(cond_val, then_block, merge_block)
        
        # Generate then block
        self.context.builder.position_at_end(then_block)
        self.generator.visit(node.then_branch)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(merge_block)
        
        # Generate else block if it exists
        if node.else_branch:
            self.context.builder.position_at_end(else_block)
            self.generator.visit(node.else_branch)
            if not self.context.builder.block.is_terminated:
                self.context.builder.branch(merge_block)
        
        # Position builder at merge block
        self.context.builder.position_at_end(merge_block)
    
    def generate_while_statement(self, node):
        """Generate while loop."""
        loop_header = self.context.current_function.append_basic_block(name='loop_header')
        loop_body = self.context.current_function.append_basic_block(name='loop_body')
        loop_exit = self.context.current_function.append_basic_block(name='loop_exit')
        
        # Branch to header
        self.context.builder.branch(loop_header)
        self.context.builder.position_at_end(loop_header)
        
        # Evaluate condition
        cond_val = self._load_if_pointer(self.generator.visit(node.condition))
        self.context.builder.cbranch(cond_val, loop_body, loop_exit)
        
        # Generate loop body
        self.context.builder.position_at_end(loop_body)
        self.generator.visit(node.body)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(loop_header)
        
        # Position at exit block
        self.context.builder.position_at_end(loop_exit)
    
    def generate_for_statement(self, node):
        """Generate for loop."""
        loop_header = self.context.current_function.append_basic_block(name='for_header')
        loop_body = self.context.current_function.append_basic_block(name='for_body')
        loop_update = self.context.current_function.append_basic_block(name='for_update')
        loop_exit = self.context.current_function.append_basic_block(name='for_exit')
        
        # Initialization
        if node.initializer:
            self.generator.visit(node.initializer)
        
        # Jump to header
        self.context.builder.branch(loop_header)
        self.context.builder.position_at_end(loop_header)
        
        # Condition check
        if node.condition:
            cond_val = self._load_if_pointer(self.generator.visit(node.condition))
            self.context.builder.cbranch(cond_val, loop_body, loop_exit)
        else:
            self.context.builder.branch(loop_body)
        
        # Generate loop body
        self.context.builder.position_at_end(loop_body)
        self.generator.visit(node.body)
        if not self.context.builder.block.is_terminated:
            self.context.builder.branch(loop_update)
        
        # Generate update block
        self.context.builder.position_at_end(loop_update)
        if node.update:
            self.generator.visit(node.update)
        self.context.builder.branch(loop_header)
        
        # Position at exit block
        self.context.builder.position_at_end(loop_exit)
    
    def generate_switch_statement(self, node):
        """Generate switch statement."""
        # Get the switch expression value
        switch_val = self._load_if_pointer(self.generator.visit(node.expression))
        
        # Create blocks for each case and default
        case_blocks = []
        default_block = None
        exit_block = self.context.current_function.append_basic_block("switch_exit")
        
        # Create blocks for each case
        for i, case in enumerate(node.cases):
            if hasattr(case, 'value') and case.value == 'default':
                default_block = self.context.current_function.append_basic_block("default")
            else:
                case_block = self.context.current_function.append_basic_block(f"case_{i}")
                case_blocks.append((case, case_block))
        
        # If no default case, create one that jumps to exit
        if default_block is None:
            default_block = exit_block
        
        # Create the switch instruction
        switch_instr = self.context.builder.switch(switch_val, default_block)
        
        # Add cases to the switch instruction
        for case, case_block in case_blocks:
            case_val = self.generator.visit(case.value)
            switch_instr.add_case(case_val, case_block)
        
        # Generate code for each case
        for case, case_block in case_blocks:
            self.context.builder.position_at_end(case_block)
            for stmt in case.statements:
                self.generator.visit(stmt)
                # If this is a return statement, don't add a branch
                if stmt.__class__.__name__ == 'ReturnStatement':
                    break
            else:
                # If no return statement, branch to exit
                self.context.builder.branch(exit_block)
        
        # Generate code for default case if it exists and is not the exit block
        if default_block != exit_block:
            self.context.builder.position_at_end(default_block)
            # Find the default case
            for case in node.cases:
                if hasattr(case, 'value') and case.value == 'default':
                    for stmt in case.statements:
                        self.generator.visit(stmt)
                        if stmt.__class__.__name__ == 'ReturnStatement':
                            break
                    else:
                        self.context.builder.branch(exit_block)
                    break
        
        # Position builder at exit block
        self.context.builder.position_at_end(exit_block)
    
    def _load_if_pointer(self, value):
        """Load value if it's a pointer, otherwise return as-is."""
        if isinstance(value.type, ir.PointerType):
            if value.type.pointee == ir.IntType(8):
                return value  # Keep string pointers as pointers
            return self.context.builder.load(value)
        return value
