# Modular LLVM Generator Architecture

This directory contains a modular, maintainable architecture for the PIE compiler's LLVM code generation phase. The original monolithic `LLVMCodeGenerator` class has been broken down into focused, single-responsibility components.

## Architecture Overview

### Core Components

1. **`LLVMContext`** - Central context that manages shared state across all components
2. **`TypeManager`** - Handles LLVM type definitions and type conversions
3. **`RuntimeFunctionManager`** - Manages declaration of all runtime functions
4. **`ExpressionGenerator`** - Handles LLVM IR generation for expressions
5. **`ControlFlowGenerator`** - Handles LLVM IR generation for control flow structures
6. **`ModularLLVMGenerator`** - Main orchestrator that coordinates all components

### Design Principles

- **Single Responsibility**: Each component has one clear purpose
- **Dependency Injection**: Components receive their dependencies through constructor injection
- **Interface Segregation**: Components expose only the methods they need
- **Open/Closed**: Easy to extend with new functionality without modifying existing code
- **Composition over Inheritance**: Uses composition to build complex behavior

## Component Details

### LLVMContext (`context.py`)

The central context that manages:
- LLVM module and target machine
- Current function and IR builder state
- Variable tables and global state
- String constants and global variables
- Dynamic array tracking

**Key Methods:**
- `_initialize_llvm()` - Sets up LLVM bindings
- `get_global_string()` - Manages string constants
- `add_global_variable()` - Adds global variables
- `clear_function_scope()` - Cleans up function state

### TypeManager (`type_manager.py`)

Manages all LLVM type-related operations:
- Dynamic array struct definitions
- Dictionary struct definitions
- PIE type to LLVM type mapping
- Type validation and queries

**Key Methods:**
- `initialize()` - Defines all struct types
- `get_llvm_type()` - Converts PIE types to LLVM types
- `get_array_type()` - Gets array types by element type
- `is_array_type()` / `is_dict_type()` - Type checking utilities

### RuntimeFunctionManager (`runtime_manager.py`)

Declares all runtime functions in organized categories:
- System I/O functions (input/output)
- Mathematical functions (sin, cos, sqrt, etc.)
- String manipulation functions
- File I/O functions
- Dictionary operations
- Dynamic array operations
- Utility functions

**Key Methods:**
- `initialize()` - Declares all function categories
- `_declare_function()` - Helper for function declaration
- `get_function()` - Retrieves declared functions

### ExpressionGenerator (`expression_generator.py`)

Handles expression-specific code generation:
- Binary operations with type promotion
- String operations and comparisons
- Array concatenation
- Unary operations
- Primary expressions (literals, identifiers)
- Function calls with argument processing

**Key Methods:**
- `generate_binary_operation()` - Main binary op handler
- `generate_string_operation()` - String-specific operations
- `generate_float_operation()` - Float operations with promotion
- `generate_integer_operation()` - Integer operations

### ControlFlowGenerator (`control_flow_generator.py`)

Manages control flow structure generation:
- If statements with else branches
- While loops
- For loops
- Switch statements

**Key Methods:**
- `generate_if_statement()` - If/else generation
- `generate_while_statement()` - While loop generation
- `generate_for_statement()` - For loop generation
- `generate_switch_statement()` - Switch statement generation

### ModularLLVMGenerator (`main_generator.py`)

The main orchestrator that:
- Initializes all components
- Coordinates AST traversal
- Delegates to appropriate components
- Manages global statement processing
- Handles function definitions and declarations

**Key Methods:**
- `generate()` - Main entry point
- `_create_main_function_if_needed()` - Main function wrapper
- `_process_global_statements()` - Global statement handling
- Visitor methods that delegate to components

## Usage

### Basic Usage

```python
from src.backend.modular import ModularLLVMGenerator

# Create the generator
generator = ModularLLVMGenerator(symbol_table, debug=True)

# Generate LLVM IR from AST
llvm_module = generator.generate(ast)
```

### Extending the Architecture

#### Adding New Expression Types

1. Extend `ExpressionGenerator` with new methods
2. Add corresponding visitor methods in `ModularLLVMGenerator`
3. Update the delegation logic

#### Adding New Control Flow Structures

1. Extend `ControlFlowGenerator` with new generation methods
2. Add visitor methods in `ModularLLVMGenerator`
3. Implement the control flow logic

#### Adding New Runtime Functions

1. Extend `RuntimeFunctionManager` with new function categories
2. Add function declarations in the appropriate category method
3. Update any related type information in `TypeManager`

## Benefits of This Architecture

### Maintainability
- **Focused Components**: Each file has a single, clear purpose
- **Reduced Complexity**: Easier to understand and modify individual pieces
- **Clear Dependencies**: Dependencies are explicit and manageable

### Extensibility
- **Easy to Add Features**: New functionality can be added without touching existing code
- **Component Reuse**: Components can be reused or extended independently
- **Plugin Architecture**: New components can be added following the established pattern

### Testing
- **Unit Testing**: Each component can be tested in isolation
- **Mock Dependencies**: Easy to mock dependencies for focused testing
- **Clear Interfaces**: Well-defined interfaces make testing straightforward

### Debugging
- **Isolated Issues**: Problems can be isolated to specific components
- **Clear Data Flow**: Data flow between components is explicit
- **Easier Profiling**: Performance issues can be identified at the component level

## Migration from Monolithic Generator

The modular architecture maintains the same external interface as the original `LLVMCodeGenerator`, making it a drop-in replacement. The main differences are:

1. **Component-based**: Functionality is distributed across focused components
2. **Dependency Injection**: Dependencies are explicitly managed
3. **Clearer Separation**: Expression, control flow, and type concerns are separated
4. **Easier Extension**: New features can be added by extending specific components

## Future Enhancements

### Potential New Components
- **`ArrayGenerator`** - Specialized array operation handling
- **`DictionaryGenerator`** - Dictionary-specific code generation
- **`OptimizationPass`** - LLVM optimization passes
- **`DebugInfoGenerator`** - Debug information generation

### Integration Opportunities
- **LLVM Passes**: Easy to integrate custom LLVM optimization passes
- **Code Analysis**: Components can be extended with analysis capabilities
- **Multiple Targets**: Architecture supports multiple target backends
- **Plugin System**: Could be extended with a plugin system for custom components

## Conclusion

This modular architecture transforms the monolithic LLVM generator into a maintainable, extensible system. Each component has a clear responsibility, making the code easier to understand, test, and extend. The architecture follows software engineering best practices and provides a solid foundation for future compiler development.
