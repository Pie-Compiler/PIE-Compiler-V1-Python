# String Comparisons and Operations in PIE

The PIE compiler now supports comprehensive string comparison and manipulation capabilities, making it easy to work with text data in your programs.

## Table of Contents

1. [String Comparison Operators](#string-comparison-operators)
2. [String-to-Integer Comparisons](#string-to-integer-comparisons)
3. [String Utility Functions](#string-utility-functions)
4. [Examples](#examples)
5. [Best Practices](#best-practices)

## String Comparison Operators

PIE supports all standard comparison operators for strings:

### Equality Comparisons
- `==` - String equality (case-sensitive)
- `!=` - String inequality (case-sensitive)

### Ordering Comparisons
- `<` - String comes before (lexicographic order)
- `>` - String comes after (lexicographic order)
- `<=` - String comes before or equals
- `>=` - String comes after or equals

### How It Works
String comparisons use the `pie_strcmp` function internally, which returns:
- `-1` if the first string comes before the second
- `0` if the strings are equal
- `1` if the first string comes after the second

**Example:**
```pie
string name1 = "Alice";
string name2 = "Bob";

if(name1 < name2){
    output("Alice comes before Bob alphabetically", string);
}

if(name1 == name2){
    output("Names are equal", string);
} else {
    output("Names are different", string);
}
```

## String-to-Integer Comparisons

One of the most powerful features is automatic string-to-integer comparison using string length. When you compare a string with an integer, PIE automatically converts it to a string length comparison.

### Automatic Conversion
- `string < int` → `strlen(string) < int`
- `int < string` → `int < strlen(string)`
- `string <= int` → `strlen(string) <= int`
- `int >= string` → `int >= strlen(string)`

### Use Cases
This feature is perfect for:
- **Input validation**: Checking if user input meets length requirements
- **Password policies**: Ensuring passwords are long enough
- **Filename validation**: Checking if filenames are within acceptable length limits
- **Data processing**: Filtering strings based on length criteria

**Examples:**
```pie
string password = "secret123";

// Check if password is too short
if(password < 8){
    output("Password must be at least 8 characters", string);
}

// Check if filename is reasonable length
string filename = "very_long_filename_that_might_be_too_long.txt";
if(filename > 50){
    output("Filename is too long", string);
}

// Validate input length
string user_input = "hello";
if(user_input <= 3){
    output("Input is too short", string);
}

if(20 >= user_input){
    output("Input length is acceptable", string);
}
```

## String Utility Functions

PIE provides several built-in string utility functions for common string operations:

### String Content Functions

#### `string_contains(haystack, needle)`
Checks if one string contains another as a substring.
- **Returns**: `1` if found, `0` if not found
- **Parameters**: 
  - `haystack`: The string to search in
  - `needle`: The string to search for

```pie
string text = "Hello world";
if(string_contains(text, "world")){
    output("Text contains 'world'", string);
}
```

#### `string_starts_with(str, prefix)`
Checks if a string starts with a specific prefix.
- **Returns**: `1` if true, `0` if false
- **Parameters**:
  - `str`: The string to check
  - `prefix`: The prefix to look for

```pie
string filename = "document.pdf";
if(string_starts_with(filename, "doc")){
    output("Filename starts with 'doc'", string);
}
```

#### `string_ends_with(str, suffix)`
Checks if a string ends with a specific suffix.
- **Returns**: `1` if true, `0` if false
- **Parameters**:
  - `str`: The string to check
  - `suffix`: The suffix to look for

```pie
string filename = "document.pdf";
if(string_ends_with(filename, ".pdf")){
    output("File is a PDF", string);
}
```

#### `string_is_empty(str)`
Checks if a string is empty (has length 0).
- **Returns**: `1` if empty, `0` if not empty
- **Parameters**:
  - `str`: The string to check

```pie
string user_input = "";
if(string_is_empty(user_input)){
    output("Please enter some text", string);
}
```

### String Length Function

#### `pie_strlen(str)`
Returns the length of a string (number of characters).
- **Returns**: Integer representing string length
- **Parameters**:
  - `str`: The string to measure

```pie
string message = "Hello";
int length = pie_strlen(message);
output("Message length: ", string);
output(length, int);
```

## Examples

### Complete Input Validation Example
```pie
string username = "john_doe";
string password = "secret";

// Check username length
if(username < 3){
    output("Username too short", string);
} else if(username > 20){
    output("Username too long", string);
} else {
    output("Username length OK", string);
}

// Check password strength
if(password < 8){
    output("Password too weak", string);
} else if(string_contains(password, "123")){
    output("Password contains common pattern", string);
} else {
    output("Password strength OK", string);
}
```

### File Processing Example
```pie
string filename = "report_2024.pdf";

// Check file type
if(string_ends_with(filename, ".pdf")){
    output("Processing PDF file", string);
} else if(string_ends_with(filename, ".txt")){
    output("Processing text file", string);
} else {
    output("Unsupported file type", string);
}

// Check filename length
if(filename > 50){
    output("Filename too long for system", string);
}
```

### String Search Example
```pie
string content = "The quick brown fox jumps over the lazy dog";

// Search for specific words
if(string_contains(content, "fox")){
    output("Found 'fox' in content", string);
}

if(string_starts_with(content, "The")){
    output("Content starts with 'The'", string);
}

if(string_ends_with(content, "dog")){
    output("Content ends with 'dog'", string);
}
```

## Best Practices

### 1. Use String Length Comparisons for Validation
```pie
// Good: Clear and intuitive
if(password < 8){
    output("Password too short", string);
}

// Avoid: Manual length checking
int pass_len = pie_strlen(password);
if(pass_len < 8){
    output("Password too short", string);
}
```

### 2. Combine Multiple Checks
```pie
string input = "user123";

// Check multiple conditions
if(input < 3 || input > 15){
    output("Input length must be between 3 and 15 characters", string);
}

if(string_starts_with(input, "admin")){
    output("Username cannot start with 'admin'", string);
}
```

### 3. Handle Empty Strings
```pie
string user_input = "";

// Always check for empty strings before processing
if(string_is_empty(user_input)){
    output("Please provide input", string);
} else if(user_input < 5){
    output("Input too short", string);
} else {
    // Process valid input
    output("Processing: ", string);
    output(user_input, string);
}
```

### 4. Use Appropriate Comparison Operators
```pie
string filename = "document.txt";

// For exact matches
if(filename == "document.txt"){
    output("Exact filename match", string);
}

// For pattern matching
if(string_ends_with(filename, ".txt")){
    output("Text file detected", string);
}

// For length validation
if(filename > 100){
    output("Filename too long", string);
}
```

## Performance Considerations

- **String comparisons** are O(n) where n is the length of the shorter string
- **String length comparisons** are O(n) where n is the string length
- **String utility functions** are O(n) for most operations
- For large-scale string processing, consider caching string lengths if used multiple times

## Error Handling

All string functions handle edge cases gracefully:
- **NULL pointers**: Functions return safe default values
- **Empty strings**: Properly detected and handled
- **Invalid inputs**: No crashes or undefined behavior

## Summary

The string comparison system in PIE provides:
- ✅ **Intuitive syntax** for string operations
- ✅ **Automatic type conversion** for string-to-integer comparisons
- ✅ **Comprehensive utility functions** for common string tasks
- ✅ **Robust error handling** for edge cases
- ✅ **Performance optimization** through built-in functions

This makes PIE an excellent choice for text processing, input validation, and string manipulation tasks.
