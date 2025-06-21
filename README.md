# PIE Compiler

A compiler for the PIE programming language, supporting parsing, semantic analysis, intermediate representation (IR) generation, and LLVM-based code generation.

## Project Structure

```
.
├── main.py              # Entry point for the compiler
├── parser.py            # Parser for PIE language
├── lexer.py             # Custom lexer implementation
├── lex.py, yacc.py      # PLY-based lexer and parser adapters
├── semanticAnalysis.py  # Semantic analysis phase
├── ir_generator.py      # Intermediate representation (3-address code) generator
├── llvmConverter.py     # Converts IR to LLVM IR
├── runtime.c            # Runtime support functions (I/O, etc.)
├── system.c             # System-level I/O functions (alternative runtime)
├── test*.pie            # Sample PIE programs
├── output.ir            # Generated IR code
├── output.ll            # Generated LLVM IR code
├── output.bc            # LLVM bitcode
├── output.o             # Native object file
├── program              # Final executable
└── ...
```

## PIE Language Structure

PIE is a C-like language with support for:
- Variable declarations: `int`, `float`, `string`, `char`, `boolean`
- Assignments and expressions
- Control flow: `if`, `else`, `while`, `for`
- System I/O: `input`, `output`, `exit`
- Comments

### Example Program

```pie
int n;
float total;
int i;
float avg;
string prompt;
char grade;
boolean valid;

prompt = "Enter the number of test scores:";
output(prompt, string);
input(n, int);

total = 0;
for (i = 0; i < n; i = i + 1) {
    output("Enter score:", string);
    float score;
    input(score, float);
    total = total + score;
}

avg = total / n;
output("Grade:", string);
if (avg >= 90) {
    grade = 'A';
} else if (avg >= 80) {
    grade = 'B';
} else {
    grade = 'C';
}
output(grade, char);
```

See the `test*.pie` files for more examples.

## How to Run the Compiler

### Prerequisites

- Python 3.x
- [llvmlite](https://github.com/numba/llvmlite) (for LLVM IR generation)
- Clang and LLVM tools (`llvm-as`, `llc`)
- A C compiler (for building the runtime, e.g., `clang`)

### Steps

1. **Write your PIE program** (e.g., `test13.pie`).

2. **Run the compiler:**
   ```sh
   python3 main.py
   ```
   By default, it compiles `test13.pie`. You can modify `main.py` to change the input file.

3. **Build and link:**
   The compiler will:
   - Parse and analyze your program
   - Generate IR and LLVM IR (`output.ir`, `output.ll`)
   - Assemble and link with the runtime to produce the executable `program`

4. **Run your program:**
   ```sh
   ./program
   ```

### Notes

- The runtime is implemented in [`runtime.c`](runtime.c) and must be compiled to `runtime.o`.
- The build process is automated in [`main.py`](main.py) via the `build_and_link()` function.
- You can add or modify PIE programs in the `test*.pie` files.
