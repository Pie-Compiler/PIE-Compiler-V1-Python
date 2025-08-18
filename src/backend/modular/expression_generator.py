"""
Expression Generation Component

This module handles generation of LLVM IR for expressions.
"""

import llvmlite.ir as ir
from typing import Optional, Any
from .base import CodeGeneratorComponent


class ExpressionGenerator(CodeGeneratorComponent):
    """Handles generation of LLVM IR for expressions."""
    
    def __init__(self, context, type_manager):
        super().__init__(context)
        self.type_manager = type_manager
    
    def initialize(self):
        """Initialize the expression generator."""
        pass
    
    def generate_binary_operation(self, node):
        """Generate LLVM IR for binary operations."""
        # Check for string comparison operations first (before null checks)
        if node.op in ['==', '!=', '<', '>', '<=', '>=']:
            left_val = self.generator.visit(node.left)
            right_val = self.generator.visit(node.right)
            
            # Debug output
            print(f"DEBUG: Binary op {node.op}, left type: {left_val.type}, right type: {right_val.type}")
            
            # Check if both operands are string pointers (i8*) or string variable pointers (i8**)
            left_is_string = self._is_string_pointer(left_val)
            right_is_string = self._is_string_pointer(right_val)
            
            print(f"DEBUG: Left is string: {left_is_string}, Right is string: {right_is_string}")
            
            if left_is_string and right_is_string:
                print(f"DEBUG: Generating string operation for {node.op}")
                return self._generate_string_operation(left_val, right_val, node.op)
            
            # Check for string length comparisons and other string operations
            string_op_result = self._handle_string_operations(left_val, right_val, node.op)
            if string_op_result is not None:
                return string_op_result
        
        # Check for null equality operations
        if node.op in ['==', '!=']:
            left_val = self.generator.visit(node.left)
            right_val = self.generator.visit(node.right)
            
            # Check if this is a null equality comparison
            null_check = self._check_null_equality(left_val, right_val)
            if null_check is not None:
                if node.op == '!=':
                    # Invert the result for !=
                    return self.context.builder.not_(null_check, 'not_null_check')
                return null_check
        
        # Check for string or array concatenation
        if node.op == '+':
            left_val = self.generator.visit(node.left)
            right_val = self.generator.visit(node.right)
            if self._is_string_operation(left_val, right_val):
                return self._generate_string_operation(left_val, right_val, '+')
            elif self._is_array_concatenation(left_val, right_val):
                return self._generate_array_concatenation(left_val, right_val)
        
        # Regular binary operations
        lhs = self._load_if_pointer(self.generator.visit(node.left))
        rhs = self._load_if_pointer(self.generator.visit(node.right))
        
        # Type promotion for float operations
        if isinstance(lhs.type, ir.DoubleType) or isinstance(rhs.type, ir.DoubleType):
            return self._generate_float_operation(lhs, rhs, node.op)
        
        # Integer operations
        elif isinstance(lhs.type, ir.IntType) and isinstance(rhs.type, ir.IntType):
            return self._generate_integer_operation(lhs, rhs, node.op)
        
        # Debug output for type mismatch
        lhs_type_info = f"{lhs.type} (pointee: {lhs.type.pointee if isinstance(lhs.type, ir.PointerType) else 'N/A'})"
        rhs_type_info = f"{rhs.type} (pointee: {rhs.type.pointee if isinstance(rhs.type, ir.PointerType) else 'N/A'})"
        raise Exception(f"Unknown or incompatible types for binary operator '{node.op}': {lhs_type_info} and {rhs_type_info}")
    
    def _check_null_equality(self, left_val, right_val):
        """Check if this is a null equality comparison."""
        # Check if either operand is null
        left_is_null = self._is_null_value(left_val)
        right_is_null = self._is_null_value(right_val)
        
        if left_is_null and right_is_null:
            # null == null is always true
            return ir.Constant(ir.IntType(1), 1)
        elif left_is_null or right_is_null:
            # One is null, one is not - compare with null
            non_null_val = right_val if left_is_null else left_val
            return self.context.builder.icmp_signed('==', non_null_val, 
                                                 ir.Constant(non_null_val.type, None), 'null_check')
        
        return None
    
    def _is_null_value(self, val):
        """Check if a value represents null."""
        if isinstance(val, ir.Constant):
            if val.type == ir.IntType(8).as_pointer():
                # For pointer types, check if the constant is None
                return val.constant is None
        return False
    
    def _is_string_pointer(self, val):
        """Check if a value is a string pointer."""
        if isinstance(val.type, ir.PointerType):
            if val.type.pointee == ir.IntType(8):
                # This is i8* (string pointer)
                return True
            elif (isinstance(val.type.pointee, ir.PointerType) and 
                  val.type.pointee.pointee == ir.IntType(8)):
                # This is i8** (pointer to string pointer)
                return True
        return False
    
    def _handle_string_operations(self, left_val, right_val, op):
        """Handle string-specific operations like length comparisons."""
        # This could be extended to handle string length comparisons, etc.
        return None
    
    def _is_string_operation(self, left_val, right_val, op):
        """Check if this is a string operation."""
        return (op in ['==', '!=', '<', '>', '<=', '>='] and 
                self._is_string_value(left_val) and self._is_string_value(right_val))
    
    def _is_string_value(self, val):
        """Check if a value is a string."""
        if isinstance(val.type, ir.PointerType):
            if val.type.pointee == ir.IntType(8):
                return True
            elif (isinstance(val.type.pointee, ir.PointerType) and 
                  val.type.pointee == ir.IntType(8)):
                return True
        return False
    
    def _generate_string_operation(self, left_val, right_val, op):
        """Generate string comparison operations."""
        # Load string values if they're variable pointers
        left_str = self._load_string_value(left_val)
        right_str = self._load_string_value(right_val)
        
        strcmp_func = self.context.module.get_global("pie_strcmp")
        cmp_result = self.context.builder.call(strcmp_func, [left_str, right_str], 'strcmp_result')
        
        # Convert strcmp result to boolean based on operator
        op_map = {
            '==': ('==', 0),
            '!=': ('!=', 0),
            '<': ('<', 0),
            '>': ('>', 0),
            '<=': ('<=', 0),
            '>=': ('>=', 0)
        }
        
        if op in op_map:
            cmp_op, target = op_map[op]
            return self.context.builder.icmp_signed(cmp_op, cmp_result, 
                                                 ir.Constant(ir.IntType(32), target), f'str_{op}')
        
        return None
    
    def _load_string_value(self, val):
        """Load string value from variable pointer if needed."""
        if isinstance(val.type.pointee, ir.PointerType):
            return self.context.builder.load(val)
        return val
    
    def _is_array_concatenation(self, node):
        """Check if this is an array concatenation operation."""
        return hasattr(node, 'result_type') and node.result_type == 'array'
    
    def _generate_array_concatenation(self, node):
        """Generate array concatenation operation."""
        element_type = node.element_type.replace('KEYWORD_', '').lower()
        func_name = f"d_array_{element_type}_concat"
        concat_func = self.context.module.get_global(func_name)
        
        # Get array struct pointers
        lhs_var_ptr = self.context.visit(node.left)
        rhs_var_ptr = self.context.visit(node.right)
        lhs_array_ptr = self.context.builder.load(lhs_var_ptr)
        rhs_array_ptr = self.context.builder.load(rhs_var_ptr)
        
        return self.context.builder.call(concat_func, [lhs_array_ptr, rhs_array_ptr], 'concat_array_tmp')
    
    def _generate_float_operation(self, left_val, right_val, op):
        """Generate float operations with type promotion."""
        # Promote integers to floats
        if isinstance(left_val.type, ir.IntType):
            left_val = self.context.builder.sitofp(left_val, ir.DoubleType())
        if isinstance(right_val.type, ir.IntType):
            right_val = self.context.builder.sitofp(right_val, ir.DoubleType())
        
        # Arithmetic operations
        op_map = {
            '+': self.context.builder.fadd,
            '-': self.context.builder.fsub,
            '*': self.context.builder.fmul,
            '/': self.context.builder.fdiv
        }
        
        if op in op_map:
            return op_map[op](left_val, right_val, 'f_tmp')
        
        # Relational operations
        op_map_rel = {
            '<': 'olt', '>': 'ogt', '<=': 'ole', '>=': 'oge', 
            '==': 'oeq', '!=': 'one'
        }
        
        if op in op_map_rel:
            return self.context.builder.fcmp_ordered(op_map_rel[op], left_val, right_val, 'f_cmp_tmp')
        
        return None
    
    def _generate_integer_operation(self, left_val, right_val, op):
        """Generate integer operations."""
        # Arithmetic operations
        op_map = {
            '+': self.context.builder.add,
            '-': self.context.builder.sub,
            '*': self.context.builder.mul,
            '/': self.context.builder.sdiv,
            '%': self.context.builder.srem
        }
        
        if op in op_map:
            return op_map[op](left_val, right_val, 'i_tmp')
        
        # Relational operations
        op_map_rel = {
            '<': '<', '>': '>', '<=': '<=', '>=': '>=', 
            '==': '==', '!=': '!='
        }
        
        if op in op_map_rel:
            return self.context.builder.icmp_signed(op_map_rel[op], left_val, right_val, f'i_cmp_{op}')
        
        # Logical operations
        if op == '&&':
            return self.context.builder.and_(left_val, right_val, 'and_tmp')
        if op == '||':
            return self.context.builder.or_(left_val, right_val, 'or_tmp')
        
        return None
    
    def generate_unary_operation(self, node, operand_val, op):
        """Generate LLVM IR for unary operations."""
        if op == '-':
            if isinstance(operand_val.type, ir.DoubleType):
                return self.context.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), operand_val, 'f_neg_tmp')
            else:
                return self.context.builder.sub(ir.Constant(operand_val.type, 0), operand_val, 'i_neg_tmp')
        
        raise Exception(f"Unknown unary operator: {op}")
    
    def generate_primary(self, node):
        """Generate LLVM IR for primary expressions (literals, identifiers)."""
        val = node.value
        if isinstance(val, str):
            if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                return ir.Constant(ir.IntType(32), int(val))
            try:
                if '.' in val and not val.startswith('"') and not val.startswith("'"):
                    return ir.Constant(ir.DoubleType(), float(val))
            except ValueError:
                pass
            if val == 'true':
                return ir.Constant(ir.IntType(1), 1)
            if val == 'false':
                return ir.Constant(ir.IntType(1), 0)
            if val == 'null':
                return ir.Constant(ir.IntType(8).as_pointer(), None)
            if val.startswith("'") and val.endswith("'") and len(val) >= 3:
                inner = val[1:-1]
                if inner == '\\n':
                    ch = '\n'
                elif inner == '\\t':
                    ch = '\t'
                else:
                    ch = inner[0]
                return ir.Constant(ir.IntType(8), ord(ch))
            if val.startswith('"') and val.endswith('"'):
                str_val = val[1:-1].replace('\\n', '\n') + '\0'
                return self.context.get_global_string(str_val)
        
        raise Exception(f"Unsupported primary literal: {val}")
    
    def generate_function_call(self, node):
        """Generate LLVM IR for function calls."""
        # Map PIE function names to their actual LLVM function names
        math_function_map = {
            'pow': 'pie_pow',
            'sqrt': 'pie_sqrt',
            'sin': 'pie_sin',
            'cos': 'pie_cos',
            'tan': 'pie_tan',
            'asin': 'pie_asin',
            'acos': 'pie_acos',
            'atan': 'pie_atan',
            'log': 'pie_log',
            'log10': 'pie_log10',
            'exp': 'pie_exp',
            'floor': 'pie_floor',
            'ceil': 'pie_ceil',
            'round': 'pie_round',
            'abs': 'pie_abs',
            'abs_int': 'pie_abs_int',
            'min': 'pie_min',
            'max': 'pie_max',
            'min_int': 'pie_min_int',
            'max_int': 'pie_max_int',
            'rand': 'pie_rand',
            'srand': 'pie_srand',
            'rand_range': 'pie_rand_range',
            'pi': 'pie_pi',
            'e': 'pie_e',
            'time': 'pie_time'
        }
        
        actual_name = math_function_map.get(node.name, node.name)
        func = self.context.module.get_global(actual_name)
        if func is None:
            raise Exception(f"Unknown function referenced: {node.name} (mapped to {actual_name})")
        
        # Process arguments
        args = []
        for arg in node.args:
            # We need to get the generator instance to call visit
            # This is a bit of a hack, but we'll store a reference to the generator
            if hasattr(self, 'generator') and self.generator:
                arg_val = self.generator.visit(arg)
            else:
                # Fallback: try to evaluate the argument directly if possible
                if hasattr(arg, 'value'):
                    arg_val = self.generate_primary(arg)
                else:
                    raise Exception(f"Cannot process function argument {arg} without generator context")
            
            # Only load from pointer if it's not a return value from functions that should return pointers
            # Functions like new_int, new_float, new_string, dict_create, dict_get should return pointers
            if (hasattr(arg, 'name') and arg.name in 
                ['new_int', 'new_float', 'new_string', 'dict_create', 'dict_get']):
                args.append(arg_val)
            else:
                args.append(self._load_if_pointer(arg_val))
        
        # Type coercion for arguments
        new_args = []
        for i, arg in enumerate(args):
            if i < len(func.args) and arg.type != func.args[i].type:
                if isinstance(func.args[i].type, ir.DoubleType) and isinstance(arg.type, ir.IntType):
                    new_args.append(self.context.builder.sitofp(arg, ir.DoubleType()))
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)
        
        return self.context.builder.call(func, new_args, 'call_tmp')
    
    def _load_if_pointer(self, value):
        """Load value if it's a pointer, otherwise return as-is."""
        if isinstance(value.type, ir.PointerType):
            if value.type.pointee == ir.IntType(8):
                return value  # Keep string pointers as pointers
            return self.context.builder.load(value)
        return value
