from llvmConverter import IRToLLVMConverter
def parse_ir_code(ir_text):
    """Parse IR code from text format to a list of tuples."""
    ir_code = []
    for line in ir_text.strip().split('\n'):
        # Remove the single quotes around the whole tuple
        line = line.strip()
        if not line:
            continue
            
        # Extract the tuple content
        content = line[1:-1]  # Remove outer parentheses
        
        # Split by commas, but respect quotes
        parts = []
        current = ""
        in_quotes = False
        in_single_quotes = False
        
        for char in content:
            if char == '"' and not in_single_quotes:
                in_quotes = not in_quotes
                current += char
            elif char == "'" and not in_quotes:
                in_single_quotes = not in_single_quotes
                current += char
            elif char == ',' and not in_quotes and not in_single_quotes:
                parts.append(current.strip())
                current = ""
            else:
                current += char
                
        if current:
            parts.append(current.strip())
        
        # Convert parts to appropriate types
        processed_parts = []
        for part in parts:
            if part == '':
                processed_parts.append(None)
            elif part.startswith('"') and part.endswith('"'):
                processed_parts.append(part)  # Keep string literals as is
            elif part.startswith("'") and part.endswith("'"):
                processed_parts.append(part)  # Keep char literals as is
            elif part.lower() in ('true', 'false'):
                processed_parts.append(part)  # Keep boolean literals as is
            elif part.replace('.', '', 1).isdigit():
                # Convert numeric strings
                if '.' in part:
                    processed_parts.append(float(part))
                else:
                    processed_parts.append(int(part))
            else:
                processed_parts.append(part)
                
        ir_code.append(tuple(processed_parts))
        
    return ir_code

# Your IR code as a string
ir_text = """
('DECLARE', 'int', 'n_0')
('DECLARE', 'int', 'total_0')
('DECLARE', 'int', 'i_0')
('DECLARE', 'float', 'avg_0')
('DECLARE', 'string', 'prompt_0')
('DECLARE', 'char', 'grade_0')
('DECLARE', 'boolean', 'valid_0')
('ASSIGN', 'prompt_0', '"Enter the number of test scores:"')
('OUTPUT', 'prompt_0', 'string')
('INPUT', 'n_0', 'int')
('ASSIGN', 'total_0', '0')
('ASSIGN', 'i_0', '0')
('LABEL', 'L0')
('BINARY_OP', '<', 't0', 'i_0', 'n_0')
('IF_FALSE', 't0', 'L2')
('DECLARE', 'int', 'score_1')
('ASSIGN', 'prompt_0', '"Enter test score:"')
('OUTPUT', 'prompt_0', 'string')
('INPUT', 'score_1', 'int')
('BINARY_OP', '+', 't1', 'total_0', 'score_1')
('ASSIGN', 'total_0', 't1')
('LABEL', 'L1')
('BINARY_OP', '+', 't2', 'i_0', '1')
('ASSIGN', 'i_0', 't2')
('GOTO', 'L0')
('LABEL', 'L2')
('BINARY_OP', '==', 't3', 'n_0', '0')
('IF_FALSE', 't3', 'L3')
('ASSIGN', 'valid_0', 'false')
('GOTO', 'L4')
('LABEL', 'L3')
('ASSIGN', 'valid_0', 'true')
('LABEL', 'L4')
('BINARY_OP', '==', 't4', 'valid_0', 'true')
('IF_FALSE', 't4', 'L5')
('BINARY_OP', '/', 't5', 'total_0', 'n_0')
('ASSIGN', 'avg_0', 't5')
('GOTO', 'L6')
('LABEL', 'L5')
('ASSIGN', 'avg_0', '0.0')
('LABEL', 'L6')
('BINARY_OP', '>=', 't6', 'avg_0', '90.0')
('IF_FALSE', 't6', 'L7')
('ASSIGN', 'grade_0', "'A'")
('GOTO', 'L8')
('LABEL', 'L7')
('BINARY_OP', '>=', 't7', 'avg_0', '80.0')
('IF_FALSE', 't7', 'L9')
('ASSIGN', 'grade_0', "'B'")
('GOTO', 'L10')
('LABEL', 'L9')
('BINARY_OP', '>=', 't8', 'avg_0', '70.0')
('IF_FALSE', 't8', 'L11')
('ASSIGN', 'grade_0', "'C'")
('GOTO', 'L12')
('LABEL', 'L11')
('BINARY_OP', '>=', 't9', 'avg_0', '60.0')
('IF_FALSE', 't9', 'L13')
('ASSIGN', 'grade_0', "'D'")
('GOTO', 'L14')
('LABEL', 'L13')
('ASSIGN', 'grade_0', "'F'")
('LABEL', 'L14')
('LABEL', 'L12')
('LABEL', 'L10')
('LABEL', 'L8')
('ASSIGN', 'prompt_0', '"Average Score:"')
('OUTPUT', 'prompt_0', 'string')
('OUTPUT', 'avg_0', 'float')
('ASSIGN', 'prompt_0', '"Grade:"')
('OUTPUT', 'prompt_0', 'string')
('OUTPUT', 'grade_0', 'char')
('RETURN', '0')
"""

# Parse the IR code
ir_code = parse_ir_code(ir_text)

# Create the converter and convert the IR code
from llvmlite import ir
from llvmlite import binding as llvm

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Create and use the converter
converter = IRToLLVMConverter()
llvm_ir = converter.convert_ir(ir_code)

# Print the generated LLVM IR
print(llvm_ir)

# You can now compile and run the LLVM IR
# For example, to save it to a file:
with open("output.ll", "w") as f:
    f.write(llvm_ir)

print("\nLLVM IR has been saved to 'output.ll'")