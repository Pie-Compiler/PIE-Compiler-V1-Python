# String Comparisons Quick Reference

## 🚀 Quick Start

```pie
string name = "Alice";
string password = "secret123";

// Basic comparisons
if(name == "Alice") { /* exact match */ }
if(name < "Bob") { /* alphabetical order */ }

// Length validation
if(password < 8) { /* too short */ }
if(name > 20) { /* too long */ }

// String utilities
if(string_contains(password, "123")) { /* weak password */ }
if(string_starts_with(name, "Al")) { /* starts with 'Al' */ }
```

## 📊 Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|---------|
| `==` | String equality | `"hello" == "hello"` | `true` |
| `!=` | String inequality | `"hello" != "world"` | `true` |
| `<` | String comes before | `"apple" < "banana"` | `true` |
| `>` | String comes after | `"zebra" > "apple"` | `true` |
| `<=` | String before or equal | `"apple" <= "apple"` | `true` |
| `>=` | String after or equal | `"zebra" >= "apple"` | `true` |

## 🔢 String-to-Integer Comparisons

**Automatic conversion to string length comparisons:**

| PIE Code | What It Does | LLVM Generated |
|----------|---------------|----------------|
| `string < 5` | Check if string length < 5 | `strlen(string) < 5` |
| `10 > string` | Check if 10 > string length | `10 > strlen(string)` |
| `string <= 20` | Check if string length ≤ 20 | `strlen(string) <= 20` |
| `15 >= string` | Check if 15 ≥ string length | `15 >= strlen(string)` |

## 🛠️ String Utility Functions

### Content Checking
```pie
string text = "Hello world";

// Check if string contains substring
if(string_contains(text, "world")) { /* found */ }

// Check if string starts with prefix
if(string_starts_with(text, "He")) { /* starts with 'He' */ }

// Check if string ends with suffix
if(string_ends_with(text, "ld")) { /* ends with 'ld' */ }

// Check if string is empty
if(string_is_empty(text)) { /* empty string */ }
```

### Length Operations
```pie
string message = "Hello";
int length = pie_strlen(message);  // Get string length

// Direct length comparison (automatic)
if(message < 10) { /* length < 10 */ }

// Manual length comparison
if(pie_strlen(message) < 10) { /* same as above */ }
```

## 📝 Common Patterns

### Input Validation
```pie
string username = "john_doe";

// Length validation
if(username < 3) {
    output("Username too short", string);
} else if(username > 20) {
    output("Username too long", string);
} else {
    output("Username length OK", string);
}
```

### Password Strength
```pie
string password = "secret123";

// Comprehensive validation
if(password < 8) {
    output("Password too short", string);
} else if(string_contains(password, "123")) {
    output("Password too weak", string);
} else if(string_contains(password, "password")) {
    output("Password too common", string);
} else {
    output("Password strength OK", string);
}
```

### File Processing
```pie
string filename = "document.pdf";

// File type checking
if(string_ends_with(filename, ".pdf")) {
    output("Processing PDF", string);
} else if(string_ends_with(filename, ".txt")) {
    output("Processing text", string);
} else {
    output("Unsupported format", string);
}

// Filename length validation
if(filename > 100) {
    output("Filename too long", string);
}
```

### String Search
```pie
string content = "The quick brown fox";

// Multiple conditions
if(string_contains(content, "fox")) {
    output("Found fox", string);
}

if(string_starts_with(content, "The")) {
    output("Starts with 'The'", string);
}

if(string_ends_with(content, "fox")) {
    output("Ends with 'fox'", string);
}
```

## ⚡ Performance Tips

### Efficient Length Checking
```pie
// Good: Automatic conversion (compiler optimized)
if(long_string < 100) { /* efficient */ }

// Avoid: Manual length calculation
int len = pie_strlen(long_string);
if(len < 100) { /* less efficient */ }
```

### Multiple String Operations
```pie
string input = "user123";

// Combine checks efficiently
if(input < 3 || input > 15) {
    output("Invalid length", string);
}

if(string_starts_with(input, "admin")) {
    output("Reserved prefix", string);
}
```

## 🚨 Common Pitfalls

### ❌ Don't Do This
```pie
// Comparing string with null using ==
if(username == null) { /* won't work as expected */ }

// Manual string length for simple comparisons
int len = pie_strlen(password);
if(len < 8) { /* use password < 8 instead */ }
```

### ✅ Do This Instead
```pie
// Use is_variable_null for null checking
if(is_variable_null(username)) { /* correct */ }

// Use automatic length conversion
if(password < 8) { /* cleaner and more efficient */ }
```

## 🔍 Debugging String Comparisons

### Check Generated LLVM Code
```bash
python3 src/main.py your_program.pie
# Look at output.ll for generated string comparison code
```

### Verify String Types
```pie
// Ensure variables are declared as string
string name = "John";  // Correct
// name = "John";      // Wrong - no type declaration
```

### Test Edge Cases
```pie
string empty = "";
string long_str = "very_long_string_that_exceeds_normal_lengths";

// Test empty strings
if(string_is_empty(empty)) { /* should trigger */ }

// Test length limits
if(long_str > 50) { /* should trigger */ }
```

## 📚 Related Documentation

- **[String Comparisons](string_comparisons.md)** - Comprehensive guide
- **[Dictionaries](dictionaries.md)** - Safe dictionary access
- **[Data Types](data_types.md)** - String type information
- **[Examples](examples.md)** - Sample programs

---

**Quick Reference v1.0** - String Comparison Features 🚀
