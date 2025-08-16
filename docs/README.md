# PIE Language Documentation

Welcome to the comprehensive documentation for the PIE programming language. This guide covers all aspects of the language from basic syntax to advanced features.

## 📚 Documentation Index

### 🚀 Getting Started
- **[Introduction](introduction.md)** - Overview of PIE language features and design philosophy
- **[Basic Syntax](basic_syntax.md)** - Core language syntax and structure
- **[Data Types](data_types.md)** - Supported data types and their usage
- **[Examples](examples.md)** - Sample programs and code snippets

### 🔧 Core Language Features
- **[Operators](operators.md)** - Arithmetic, comparison, logical, and assignment operators
- **[Control Flow](control_flow.md)** - Conditional statements, loops, and control structures
- **[Functions](functions.md)** - Function definition, parameters, and return values
- **[Arrays](arrays.md)** - Static and dynamic array operations

### 🆕 Advanced Features
- **[Dictionaries](dictionaries.md)** - Hash map data structure with string keys
- **[Dictionary Validation](dictionary_validation.md)** - Safe dictionary access and key existence checking
- **[String Comparisons](string_comparisons.md)** - String comparison operators and utility functions ⭐ **NEW!**
- **[Standard Library](standard_library.md)** - Built-in functions for I/O, math, and utilities

## 🌟 What's New in PIE

### ✨ Latest Features (v1.0+)

#### 🔍 **Enhanced Dictionary Support**
- **Safe Dictionary Access**: Check if keys exist before accessing
- **Key Existence Functions**: `dict_key_exists()`, `dict_has_key()`
- **Null Value Handling**: Return `NULL` for missing keys
- **Runtime Safety**: No more crashes from undefined dictionary keys

#### 🚫 **Null/Undefined Checking**
- **Null Literal**: `null` keyword for explicit null values
- **Variable Validation**: `is_variable_defined()`, `is_variable_null()`
- **Safe Comparisons**: Handle null values in equality operations
- **Initialization Tracking**: Detect uninitialized variable usage

#### 🔤 **Comprehensive String Operations**
- **String Comparisons**: `==`, `!=`, `<`, `>`, `<=`, `>=` for strings
- **Automatic Length Conversion**: `string < 5` → `strlen(string) < 5`
- **String Utility Functions**: `string_contains()`, `string_starts_with()`, `string_ends_with()`, `string_is_empty()`
- **Lexicographic Ordering**: Natural string sorting and comparison

## 🎯 Key Language Capabilities

### **Type Safety & Validation**
- Static type checking at compile time
- Runtime validation for dictionaries and strings
- Null safety and undefined variable detection
- Automatic type coercion where appropriate

### **String Processing**
- Full string comparison support (equality and ordering)
- Automatic string length conversion for integer comparisons
- Rich set of string utility functions
- Safe string operations with proper error handling

### **Data Structures**
- Dynamic arrays with automatic resizing
- Hash map dictionaries with type-safe access
- Comprehensive array and dictionary operations
- Memory-efficient data structure implementations

### **Runtime Safety**
- Bounds checking for array access
- Safe dictionary key access
- Null pointer protection
- Graceful error handling

## 🚀 Quick Start Examples

### **Basic String Operations**
```pie
string name = "Alice";
string greeting = "Hello";

// String comparisons
if(name < "Bob"){
    output("Alice comes before Bob", string);
}

// String length validation
if(name < 10){
    output("Name is short enough", string);
}

// String utilities
if(string_starts_with(greeting, "He")){
    output("Greeting starts with 'He'", string);
}
```

### **Safe Dictionary Usage**
```pie
dict person = {"name": "John", "age": 30};

// Safe access with key checking
if(dict_key_exists(person, "email")){
    string email = dict_get_string(person, "email");
    output(email, string);
} else {
    output("Email not found", string);
}
```

### **Input Validation**
```pie
string password = "secret123";

// Comprehensive validation
if(password < 8){
    output("Password too short", string);
} else if(string_contains(password, "123")){
    output("Password too weak", string);
} else {
    output("Password strength OK", string);
}
```

## 🔧 Compiler Features

### **LLVM Backend**
- Generates optimized LLVM Intermediate Representation
- Cross-platform compilation support
- Efficient code generation and optimization
- Integration with LLVM toolchain

### **Frontend Processing**
- Custom lexer and parser implementation
- Abstract Syntax Tree (AST) generation
- Comprehensive semantic analysis
- Type checking and validation

### **Runtime System**
- C-based runtime library for performance
- Memory management and garbage collection
- Standard library function implementations
- Platform-independent runtime support

## 📖 Learning Path

### **Beginner Level**
1. Start with [Introduction](introduction.md) and [Basic Syntax](basic_syntax.md)
2. Learn [Data Types](data_types.md) and [Operators](operators.md)
3. Practice with [Examples](examples.md) and basic programs
4. Understand [Control Flow](control_flow.md) and [Functions](functions.md)

### **Intermediate Level**
1. Master [Arrays](arrays.md) and [Dictionaries](dictionaries.md)
2. Learn [Dictionary Validation](dictionary_validation.md) for safe data access
3. Explore [Standard Library](standard_library.md) functions
4. Practice building data processing applications

### **Advanced Level**
1. Deep dive into [String Comparisons](string_comparisons.md) and utilities
2. Build complex data validation systems
3. Optimize performance with LLVM features
4. Contribute to compiler development

## 🛠️ Development & Contributing

### **Project Structure**
- **Frontend**: Lexer, parser, semantic analysis
- **Backend**: LLVM code generation
- **Runtime**: C libraries for performance-critical operations
- **Tests**: Comprehensive test suite for all features

### **Building from Source**
```bash
# Clone the repository
git clone <repository-url>
cd PIE-Compiler-V1-Python

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Compile a PIE program
python3 src/main.py your_program.pie
```

### **Testing Features**
- Run test programs in `test*.pie` files
- Verify compiler output and generated LLVM IR
- Test runtime behavior and error handling
- Validate type safety and semantic analysis

## 📝 Language Specification

### **Syntax Highlights**
- C-style syntax with modern enhancements
- No required `main()` function for simple programs
- Automatic type inference where possible
- Rich standard library for common operations

### **Type System**
- Static typing with compile-time error checking
- Support for primitive types and complex data structures
- Type-safe operations and automatic conversions
- Null safety and undefined variable detection

### **Memory Management**
- Automatic memory management for strings and arrays
- Manual memory control for dictionaries and custom structures
- Efficient memory allocation and deallocation
- Garbage collection for long-running programs

## 🔮 Future Roadmap

### **Planned Features**
- **Object-Oriented Programming**: Classes and inheritance
- **Generic Types**: Template-based programming
- **Concurrency**: Multi-threading and async operations
- **Package Management**: Module system and dependencies
- **Web Assembly**: Compilation to WASM for web applications

### **Performance Improvements**
- **JIT Compilation**: Just-in-time code generation
- **Advanced Optimizations**: LLVM optimization passes
- **Memory Profiling**: Built-in memory usage analysis
- **Parallel Processing**: Multi-core execution support

## 📞 Support & Community

### **Getting Help**
- Check this documentation for common solutions
- Review example programs and test cases
- Examine compiler error messages for debugging
- Use the test suite to verify feature behavior

### **Contributing**
- Report bugs and feature requests
- Submit improvements to documentation
- Enhance compiler features and optimizations
- Add new standard library functions

---

**PIE Language** - Making programming simple, safe, and powerful! 🥧✨

*Last updated: Version 1.0 - String Comparison Release*
