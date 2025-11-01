# file_write() Expression Support

## Overview

The `file_write()` function in PIE already supports **any expression that evaluates to a string** as its second parameter, not just string literals. This includes:

- String literals
- String variables
- String concatenation with `+` operator
- Automatic type conversion (int, float → string in expressions)
- Function calls that return strings
- Complex arithmetic expressions (auto-converted to string)

## Syntax

```pie
void file_write(file f, string expression)
```

**Parameters:**
- `f` - File pointer obtained from `file_open()`
- `expression` - Any expression that evaluates to a string

## How It Works

The PIE compiler automatically converts non-string types to strings when they appear in concatenation expressions. This is handled by:

1. **Semantic Analysis** - The type checker validates that expressions can be converted to strings
2. **Code Generation** - The LLVM generator inserts calls to `int_to_string()` and `float_to_string()` runtime functions when needed
3. **Runtime** - C runtime functions perform the actual conversion

## Examples

### Basic Usage

```pie
file f = file_open("output.txt", "w");

// String literal
file_write(f, "Hello World\n");

// String variable
string message = "PIE Language";
file_write(f, message + "\n");

file_close(f);
```

### Integer Expressions

```pie
file f = file_open("numbers.txt", "w");

int count = 42;
file_write(f, "Count: " + count + "\n");

// Arithmetic expressions
int x = 10;
int y = 20;
file_write(f, "Sum: " + (x + y) + "\n");

file_close(f);
```

### Float Expressions

```pie
file f = file_open("data.txt", "w");

float pi = 3.14159;
file_write(f, "Value of PI: " + pi + "\n");

float result = 95.5;
file_write(f, "Progress: " + result + "%\n");

file_close(f);
```

### Function Calls

```pie
file f = file_open("log.txt", "w");

// Function that returns string
int timestamp = time_now();
string timeStr = time_to_local(timestamp);
file_write(f, "[" + timeStr + "] Log entry\n");

file_close(f);
```

### Complex Expressions

```pie
file f = file_open("report.txt", "w");

string name = "Alice";
int score = 95;
float average = 87.3;

// Multiple concatenations with mixed types
file_write(f, "Student: " + name + ", Score: " + score + ", Average: " + average + "\n");

file_close(f);
```

## Implementation Details

### Type Conversion in Expressions

When you write:
```pie
file_write(f, "Count: " + count + "\n");
```

The compiler:

1. Detects that `count` (int) is being concatenated with strings
2. Generates LLVM IR to call `int_to_string(count)`
3. Concatenates the resulting strings using `concat_strings()`
4. Passes the final concatenated string to `file_write()`

### LLVM IR Example

For the PIE code:
```pie
int count = 42;
file_write(f, "Count: " + count + "\n");
```

The generated LLVM IR includes:
```llvm
%count = alloca i32
store i32 42, i32* %count
%loaded_count = load i32, i32* %count
%int_to_str = call i8* @int_to_string(i32 %loaded_count)
%concat1 = call i8* @concat_strings(i8* getelementptr([8 x i8], [8 x i8]* @.str1, i32 0, i32 0), i8* %int_to_str)
%concat2 = call i8* @concat_strings(i8* %concat1, i8* getelementptr([2 x i8], [2 x i8]* @.str2, i32 0, i32 0))
call void @file_write(i64 %file_ptr, i8* %concat2)
```

### Runtime Functions

The following C runtime functions support automatic conversion:

- `int_to_string(int value)` - Converts integers to strings
- `float_to_string(double value)` - Converts floats to strings
- `concat_strings(char* s1, char* s2)` - Concatenates two strings

## Best Practices

### ✅ Good Practices

```pie
// Clear and readable
file_write(f, "User: " + username + ", Age: " + age + "\n");

// Separate complex logic
string logEntry = "[" + timestamp + "] " + message;
file_write(f, logEntry);
```

### ⚠️ Less Optimal (but still works)

```pie
// Overly complex expression
file_write(f, "Result: " + ((x + y) * 2) + " from " + x + " and " + y + "\n");
// Better to break it down:
int result = (x + y) * 2;
file_write(f, "Result: " + result + " from " + x + " and " + y + "\n");
```

## Common Use Cases

### Logging with Timestamps

```pie
void writeLog(string message) {
    file logFile = file_open("app.log", "a");
    if (logFile != null) {
        int timestamp = time_now();
        string timeStr = time_to_local(timestamp);
        file_write(logFile, "[" + timeStr + "] " + message + "\n");
        file_close(logFile);
    }
}
```

### Data Export

```pie
void exportData(string[] names, float[] scores) {
    file f = file_open("data.csv", "w");
    if (f != null) {
        file_write(f, "Name,Score\n");
        for (int i = 0; i < arr_size(names); i++) {
            file_write(f, names[i] + "," + scores[i] + "\n");
        }
        file_close(f);
    }
}
```

### Configuration Files

```pie
file config = file_open("settings.conf", "w");
if (config != null) {
    int port = 8080;
    string host = "localhost";
    
    file_write(config, "host=" + host + "\n");
    file_write(config, "port=" + port + "\n");
    file_close(config);
}
```

## Performance Considerations

Each concatenation operation allocates memory for the resulting string. For very large numbers of concatenations, consider:

1. Building strings incrementally when possible
2. Pre-calculating values before concatenation
3. Using appropriate buffer sizes in the runtime

## Testing

The enhanced test file `testFiles/File_I_O.pie` demonstrates all expression types:

```bash
# Compile and run the test
python3 ./src/main.py testFiles/File_I_O.pie
./program

# Check the output
cat output.txt
```

Expected output shows successful writing of:
- String literals
- String variables
- Integer expressions
- Float expressions
- Arithmetic calculations
- Function call results

## Summary

The `file_write()` function's expression support makes file I/O in PIE natural and intuitive. You can write data to files without manually converting types or building strings in separate steps - the compiler handles it automatically!
