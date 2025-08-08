# PIE Compiler

A compiler for the PIE programming language, supporting parsing, semantic analysis, intermediate representation (IR) generation, and LLVM-based code generation.

## Project Structure

```
.
├── main.py              # Entry point for the compiler
├── parser.py            # Parser for PIE language
├── lexer.py             # Custom lexer implementation
├── semanticAnalysis.py  # Semantic analysis phase
├── ir_generator.py      # Intermediate representation (3-address code) generator
├── llvmConverter.py     # Converts IR to LLVM IR
├── runtime.c            # Runtime support functions (I/O, etc.)
├── math_lib.c           # Math standard library
├── file_lib.c           # File access standard library
├── net_lib.c            # Network standard library
├── test*.pie            # Sample PIE programs
├── output.ir            # Generated IR code
├── output.ll            # Generated LLVM IR code
├── program              # Final executable
└── ...
```

## Features

### 1. Basic Language Structure

PIE is a C-like language. All executable statements must be inside a function. The program execution starts from the `main` function.

- **Data Types**: `int`, `float`, `string`, `char`, `boolean`, `file`, `socket`.
- **Control Flow**: `if/else`, `for`, `while`, `do...while`.
- **Comments**: `// single line` and `/* multi-line */`.

### 2. User-Defined Functions

Functions can be defined with type-safe arguments and return types.

**Syntax:**
```pie
<return_type> <function_name>(<parameter_list>) {
    <function_body>
}
```

**Example:**
```pie
int add(int a, int b) {
    return a + b;
}

int main() {
    int result;
    result = add(5, 3);
    output(result, int); // Outputs: 8
    return 0;
}
```

### 3. Arrays

One-dimensional arrays are supported.

**Syntax:**
```pie
// Declaration with size
<type> <array_name>[<size>];

// Declaration with initializer list (size is inferred)
<type> <array_name>[] = {<value1>, <value2>, ...};
```

**Example:**
```pie
int main() {
    int numbers[3];
    numbers[0] = 10;

    string names[] = {"Alice", "Bob", "Charlie"};
    output(names[1], string); // Outputs: Bob
    return 0;
}
```

### 4. String Concatenation

Strings can be concatenated using the `+` operator.

**Example:**
```pie
int main() {
    string s1 = "hello";
    string s2 = " world";
    string s3 = s1 + s2;
    output(s3, string); // Outputs: hello world
    return 0;
}
```

### 5. Standard Library

PIE includes a standard library for common operations.

#### System I/O
- `input(variable, type)`: Reads input from the user.
- `output(value, type)`: Prints a value to the console.
- `exit()`: Exits the program.

#### Math Library (`#include <math.h>`)
- `float sqrt(float x)`
- `float pow(float base, float exp)`
- `float sin(float x)`
- `float cos(float x)`

#### File Access Library (`#include <stdio.h>`)
- `file file_open(string filename, string mode)`
- `void file_close(file file_handle)`
- `void file_write(file file_handle, string content)`
- `void file_read(file file_handle, string buffer, int size)`

#### Network Library (`#include <sys/socket.h>`)
- `socket tcp_socket()`
- `int tcp_connect(socket sockfd, string host, int port)`
- `int tcp_send(socket sockfd, string data)`
- `int tcp_recv(socket sockfd, string buffer, int size)`
- `void tcp_close(socket sockfd)`


## How to Run the Compiler

### Prerequisites

- Python 3.x
- [llvmlite](https://github.com/numba/llvmlite)
- Clang and LLVM tools (`llvm-as`, `llc`)

### Steps

1. **Write your PIE program** (e.g., `test.pie`).
2. **Run the compiler:** `python3 main.py`
3. **Run your program:** `./program`
