# PIE Compiler

A compiler for the PIE programming language, supporting parsing, semantic analysis, intermediate representation (IR) generation, and LLVM-based code generation.

## Project Structure

```
.
├── src/
│   ├── main.py              # Entry point for the compiler
│   ├── frontend/
│   │   ├── lexer.py         # Custom lexer implementation
│   │   ├── parser.py        # Parser for PIE language
│   │   ├── ast.py           # Abstract syntax tree nodes
│   │   └── semanticAnalysis.py # Semantic analysis phase
│   ├── backend/
│   │   └── llvm_generator.py # LLVM IR generation
│   └── runtime/
│       ├── runtime.c        # Runtime support functions (I/O, etc.)
│       ├── math_lib.c       # Math standard library
│       ├── file_lib.c       # File access standard library
│       └── net_lib.c        # Network standard library
├── test*.pie            # Sample PIE programs
├── output.ir            # Generated IR code
├── output.ll            # Generated LLVM IR code
├── program              # Final executable
└── ...
```

## Language Features

### 📚 Documentation
- **[Complete Documentation](docs/README.md)** - Comprehensive guide to all PIE features
- **[String Comparisons](docs/string_comparisons.md)** - String operations and utilities
- **[Advanced String Utilities](docs/advanced_string_utilities.md)** - Advanced string manipulation functions ⭐ **NEW!**
- **[Quick Reference](docs/string_quick_reference.md)** - String comparison cheat sheet

### 1. Basic Language Structure

PIE is a C-like language that supports both global statements and user-defined functions. You can write programs in two ways:

1. **Global statements only**: Write your code directly at the top level. The compiler will automatically wrap these statements in a `main()` function.
2. **Explicit main function**: Define your own `main()` function if you prefer traditional C-style structure.

**Data Types:**
- `int` - 32-bit signed integers
- `float` - Double-precision floating point numbers  
- `char` - Single characters
- `string` - Null-terminated character strings
- `boolean` (or `bool`) - Boolean values (`true`/`false`)
- `file` - File handles for I/O operations
- `socket` - Network socket handles
- `dict` - Hash map dictionaries with string keys

**Comments:**
- Single line: `// comment text`
- Multi-line: `/* comment text */`

### 2. Operators

**Arithmetic:** `+`, `-`, `*`, `/`, `%`  
**Comparison:** `==`, `!=`, `<`, `>`, `<=`, `>=`  
**Logical:** `&&` (and), `||` (or)  
**Assignment:** `=`  
**String concatenation:** `+` (for strings)

### 3. Control Flow Statements

**Conditional Statements:**
```pie
if (condition) {
    // statements
} else {
    // statements
}
```

**Loops:**
```pie
// For loop
for (initialization; condition; update) {
    // statements
}

// While loop  
while (condition) {
    // statements
}
```

**Control keywords:** `break`, `continue`, `return`

### 4. Variable Declarations

**Basic declarations:**
```pie
int x;              // Declaration only
int y = 5;          // Declaration with initialization
float pi = 3.14159; // Float initialization
char grade = 'A';   // Character initialization
string name = "Alice"; // String initialization
boolean isValid = true; // Boolean initialization
```

**Global variables:**
Variables declared outside functions are global and initialized at program startup.

### 5. Arrays

**Static Arrays:**
```pie
// Declaration with size
int numbers[10];

// Declaration with initializer list (size inferred)
string names[] = {"Alice", "Bob", "Charlie"};

// Array access
numbers[0] = 42;
string first = names[0];
```

**Dynamic Arrays:**
```pie
int[] dynamicArray = {1, 2, 3, 4, 5};
// Dynamic arrays use runtime library functions for manipulation
```

### 6. User-Defined Functions

Functions can be defined with type-safe parameters and return types.

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

float calculateAverage(int total, int count) {
    if (count == 0) {
        return 0.0;
    }
    return (float)total / count;
}
```

### 7. Program Entry Point

PIE programs have flexible entry points:

- **Automatic main generation**: If you don't define a `main()` function, the compiler automatically wraps all global statements in a `main()` function that returns 0.
- **Explicit main function**: You can define your own `main()` function for more control over program structure and return values.
- **Mixed approach**: You can have both global variables/statements and a `main()` function. Global statements will be executed before `main()` is called.

**Examples:**
```pie
// Option 1: Global statements only (main auto-generated)
string name = "World";
output("Hello, ", string);
output(name, string);

// Option 2: Explicit main function
int main() {
    output("Hello, World!", string);
    return 0;
}
```

### 8. Dictionaries

PIE supports dictionaries (hash maps) with string keys.

**Syntax:**
```pie
dict myDict = dict_create();
dict_set(myDict, "name", new_string("Jules"));
dict_set(myDict, "age", new_int(30));

string name = dict_get_string(myDict, "name");
int age = dict_get_int(myDict, "age");
```

### 9. String Operations

**String concatenation:**
```pie
string firstName = "John";
string lastName = "Doe";
string fullName = firstName + " " + lastName;
output(fullName, string); // Outputs: John Doe
```

### 10. Standard Library

PIE includes a comprehensive standard library for common operations.

#### System I/O Functions
```pie
// Input functions - read values from user
input(variable, type);    // Reads input and stores in variable

// Output functions - print values to console  
output(value, type);         // Basic output
output(value, float, precision); // Float output with precision control

// Program control
exit();                      // Exit the program
```

**Example:**
```pie
int age;
string name;

output("Enter your name: ", string);
input(name, string);
output("Enter your age: ", string);  
input(age, int);

output("Hello ", string);
output(name, string);
output("! You are ", string);
output(age, int);
output(" years old.", string);
```

#### Math Library Functions
```pie
float sqrt(float x);          // Square root
float pow(float base, float exp); // Power function  
float sin(float x);           // Sine function
float cos(float x);           // Cosine function
float floor(float x);         // Floor function
float ceil(float x);          // Ceiling function
int rand();                   // Random number generator
```

**Example:**
```pie
float x = 16.0;
float result = sqrt(x);       // result = 4.0
float power = pow(2.0, 3.0);  // power = 8.0
```

#### File I/O Library
```pie
file file_open(string filename, string mode); // Open file
void file_close(file handle);                 // Close file
void file_write(file handle, string content); // Write to file
string file_read_all(file handle);           // Read entire file
string file_read_line(file handle);          // Read single line
void file_flush(file handle);                // Flush file buffer
```

**Example:**
```pie
file myFile = file_open("data.txt", "w");
file_write(myFile, "Hello, World!");
file_close(myFile);

file readFile = file_open("data.txt", "r");
string content = file_read_all(readFile);
output(content, string);
file_close(readFile);
```

#### String Utility Functions

**Basic String Functions:**
```pie
int strlen(string s);                    // Get string length
int strcmp(string s1, string s2);       // Compare strings
string strcpy(string dest, string src); // Copy string
string strcat(string dest, string src); // Concatenate strings
```

**Advanced String Utilities:** ⭐ **NEW!**
```pie
// Case conversion
string string_to_upper(string str);     // Convert to uppercase
string string_to_lower(string str);     // Convert to lowercase

// String manipulation
string string_trim(string str);         // Remove leading/trailing whitespace
string string_substring(string str, int start, int length); // Extract substring
string string_reverse(string str);      // Reverse string

// String searching
int string_index_of(string haystack, string needle); // Find substring position
int string_contains(string haystack, string needle); // Check if contains substring
int string_starts_with(string str, string prefix);   // Check if starts with prefix
int string_ends_with(string str, string suffix);     // Check if ends with suffix

// Character operations
string string_replace_char(string str, char old, char new); // Replace character
int string_count_char(string str, char ch);         // Count character occurrences
int string_is_empty(string str);                    // Check if string is empty
```

**Example:**
```pie
string text = "  Hello World  ";
string trimmed = string_trim(text);
string upper = string_to_upper(trimmed);
output(upper, string);  // Output: HELLO WORLD

string sub = string_substring(upper, 0, 5);
output(sub, string);  // Output: HELLO
```

#### Network Library
```pie
socket tcp_socket();                           // Create TCP socket
int tcp_connect(socket sock, string host, int port); // Connect to host
int tcp_send(socket sock, string data);       // Send data
int tcp_recv(socket sock, string buffer, int size);  // Receive data
void tcp_close(socket sock);                  // Close socket
```

### 11. Example Programs

#### Simple Global Program (No explicit main function needed)
```pie
// The compiler automatically wraps these statements in main()
int n;
float total = 0.0;
float avg;
char grade;

output("Enter number of scores: ", string);
input(n, int);

for (int i = 0; i < n; i = i + 1) {
    int score;
    output("Enter score: ", string);
    input(score, int);
    total = total + score;
}

avg = total / n;

if (avg >= 90.0) {
    grade = 'A';
} else if (avg >= 80.0) {
    grade = 'B'; 
} else if (avg >= 70.0) {
    grade = 'C';
} else if (avg >= 60.0) {
    grade = 'D';
} else {
    grade = 'F';
}

output("Average: ", string);
output(avg, float, 2);
output("Grade: ", string);
output(grade, char);
```

#### Traditional C-style Program with Explicit Main Function
```pie
int main() {
    string message = "Hello from PIE!";
    output(message, string);
    
    int x = 10;
    int y = 20;
    int result = x + y;
    
    output("The sum is: ", string);
    output(result, int);
    
    return 0;
}
```

#### Program with Functions and Global Variables
```pie
// Global variables
string appName = "Calculator";
int version = 1;

// Function definition
int add(int a, int b) {
    return a + b;
}

float divide(float a, float b) {
    if (b == 0.0) {
        output("Error: Division by zero!", string);
        return 0.0;
    }
    return a / b;
}

// Main program logic (executed automatically)
output("Welcome to ", string);
output(appName, string);
output(" v", string);
output(version, int);

int x = 15;
int y = 25;
int sum = add(x, y);

output("Sum of ", string);
output(x, int);
output(" and ", string); 
output(y, int);
output(" is ", string);
output(sum, int);

float result = divide(10.0, 3.0);
output("10.0 / 3.0 = ", string);
output(result, float, 3);
```


## How to Run the Compiler

### Prerequisites

- Python 3.x
- [llvmlite](https://github.com/numba/llvmlite)
- Clang and LLVM tools (`llvm-as`, `llc`)

### Steps

1. **Write your PIE program** (e.g., `test.pie`).
2. **Run the compiler:** `python3 main.py`
3. **Run your program:** `./program`
