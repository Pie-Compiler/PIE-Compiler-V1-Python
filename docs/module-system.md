# PIE Module System Guide

The PIE module system allows you to organize code into reusable components and leverage standard libraries for common tasks like HTTP requests, JSON parsing, and more.

## Table of Contents

- [Overview](#overview)
- [Importing Modules](#importing-modules)
- [Standard Library Modules](#standard-library-modules)
- [Creating User-Defined Modules](#creating-user-defined-modules)
- [Export Statement](#export-statement)
- [Module Search Path](#module-search-path)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## Overview

PIE supports two types of modules:

1. **Standard Library Modules** - Built-in modules like `http` and `json` with C implementations
2. **User-Defined Modules** - Custom `.pie` files you create with exported functions

Modules provide:
- ✅ **Code Reusability** - Write once, use everywhere
- ✅ **Namespace Isolation** - Avoid naming conflicts
- ✅ **Encapsulation** - Public exports and private implementations
- ✅ **Maintainability** - Organize large projects into logical units

---

## Importing Modules

### Basic Import Syntax

```pie
import module_name;
```

After importing, call module functions using dot notation:

```pie
import http;

string response = http.get("https://api.example.com");
```

### Import with Alias (Coming Soon)

```pie
import http as web;  // Not yet implemented

string response = web.get("https://api.example.com");
```

### Multiple Imports

Import multiple modules in your program:

```pie
import http;
import json;
import mathutils;

int main() {
    string data = http.get("https://api.example.com/data");
    json.object parsed = json.parse(data);
    int squared = mathutils.square(10);
    return 0;
}
```

---

## Standard Library Modules

PIE includes several standard library modules with powerful functionality.

### HTTP Module

The `http` module provides HTTP client and server capabilities.

**Available Functions:**
- `http.get(string url)` → `string` - Perform GET request
- `http.post(string url, string body)` → `string` - Perform POST request
- `http.put(string url, string body)` → `string` - Perform PUT request
- `http.delete(string url)` → `string` - Perform DELETE request

**Example:**
```pie
import http;

int main() {
    string response = http.get("https://jsonplaceholder.typicode.com/todos/1");
    output("Response: ", string);
    output(response, string);
    return 0;
}
```

### JSON Module

The `json` module provides JSON parsing and manipulation.

**Available Functions:**

*Parsing & Stringification:*
- `json.parse(string json_string)` → `json.object`
- `json.stringify(json.object obj)` → `string`

*Object Operations:*
- `json.create_object()` → `json.object`
- `json.get_string(json.object obj, string key)` → `string`
- `json.get_int(json.object obj, string key)` → `int`
- `json.get_float(json.object obj, string key)` → `float`
- `json.get_bool(json.object obj, string key)` → `int`
- `json.set_string(json.object obj, string key, string value)` → `void`
- `json.set_int(json.object obj, string key, int value)` → `void`
- `json.set_float(json.object obj, string key, float value)` → `void`

*Array Operations:*
- `json.create_array()` → `json.array`
- `json.array_append_string(json.array arr, string value)` → `void`
- `json.array_append_int(json.array arr, int value)` → `void`
- `json.array_get_string(json.array arr, int index)` → `string`
- `json.array_get_int(json.array arr, int index)` → `int`
- `json.array_size(json.array arr)` → `int`

**Example:**
```pie
import json;

int main() {
    // Parse JSON string
    string json_str = "{\"name\":\"Alice\",\"age\":25}";
    json.object person = json.parse(json_str);
    
    // Extract values
    string name = json.get_string(person, "name");
    int age = json.get_int(person, "age");
    
    output("Name: ", string);
    output(name, string);
    output("Age: ", string);
    output(age, int);
    
    return 0;
}
```

---

## Creating User-Defined Modules

You can create your own reusable modules by writing `.pie` files with exported functions.

### Step 1: Create a Module File

Create a file named `mathutils.pie`:

```pie
// mathutils.pie - Mathematical utility functions

// Export a function to calculate square
export int square(int x) {
    return x * x;
}

// Export a function to calculate cube
export int cube(int x) {
    return x * x * x;
}

// Export a function to check if number is even
export int is_even(int n) {
    if (n % 2 == 0) {
        return 1;
    }
    return 0;
}

// Private helper function (not exported)
int helper_add_one(int x) {
    return x + 1;
}

// Exported function that uses private helper
export int increment(int x) {
    return helper_add_one(x);
}
```

### Step 2: Import and Use the Module

Create `main.pie` in the same directory:

```pie
import mathutils;

int main() {
    int num = 5;
    
    int sq = mathutils.square(num);
    output("Square of 5: ", string);
    output(sq, int);
    
    int cb = mathutils.cube(num);
    output("Cube of 5: ", string);
    output(cb, int);
    
    int even = mathutils.is_even(num);
    if (even == 1) {
        output("5 is even", string);
    } else {
        output("5 is odd", string);
    }
    
    return 0;
}
```

### Step 3: Compile and Run

```bash
python3 src/main.py main.pie
./program
```

**Output:**
```
Square of 5: 25
Cube of 5: 125
5 is odd
```

---

## Export Statement

The `export` keyword makes functions visible to code that imports your module.

### Exported Functions

Functions marked with `export` become part of the module's public API:

```pie
// Visible to importers
export int public_function(int x) {
    return x * 2;
}

// NOT visible to importers
int private_function(int x) {
    return x + 1;
}
```

### When to Export

✅ **Export when:**
- Function is part of the module's public interface
- Other programs need to call this function
- You want to provide a utility to users

❌ **Don't export when:**
- Function is an internal helper
- Implementation detail that may change
- Only used within the module itself

### Export Benefits

1. **Encapsulation** - Hide implementation details
2. **API Control** - Define clear public interfaces
3. **Flexibility** - Change private functions without breaking users
4. **Security** - Prevent access to internal logic

---

## Module Search Path

When you import a module, the compiler searches for it in this order:

1. **Standard Library** - `stdlib/` directory (for built-in modules)
2. **Source File Directory** - Same directory as the file doing the import
3. **Current Working Directory** - Directory where compiler is run
4. **User Paths** - Additional paths (can be configured)

### Example Directory Structure

```
my_project/
├── main.pie              # Imports mathutils
├── mathutils.pie         # User-defined module
├── utils/
│   └── helpers.pie       # Another module
└── stdlib/               # Standard library (in compiler directory)
    ├── http/
    │   ├── module.json
    │   ├── http.pie
    │   └── pie_http.c
    └── json/
        ├── module.json
        ├── json.pie
        └── pie_json.c
```

---

## Best Practices

### 1. **Organize by Functionality**

Group related functions into cohesive modules:

```pie
// Good: math_utils.pie
export int square(int x) { ... }
export int cube(int x) { ... }
export int power(int base, int exp) { ... }

// Bad: mixing unrelated functions
export int square(int x) { ... }
export string format_date(int timestamp) { ... }
```

### 2. **Use Clear Names**

Module and function names should be descriptive:

```pie
// Good
import string_utils;
string result = string_utils.to_upper(text);

// Less clear
import su;
string result = su.up(text);
```

### 3. **Export Only What's Needed**

Keep internal helpers private:

```pie
// Good practice
export int factorial(int n) {
    return factorial_helper(n, 1);
}

int factorial_helper(int n, int acc) {  // Private
    if (n <= 1) return acc;
    return factorial_helper(n - 1, n * acc);
}
```

### 4. **Document Your Modules**

Add comments explaining the module's purpose:

```pie
// math_utils.pie - Mathematical utility functions
// 
// This module provides common mathematical operations
// including exponentiation, factorial, and prime checking.

export int factorial(int n) {
    // Calculate factorial of n
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

### 5. **Avoid Circular Dependencies**

Don't create modules that import each other:

```pie
// ❌ Bad: module_a.pie imports module_b.pie
// ❌ Bad: module_b.pie imports module_a.pie

// ✅ Good: Create a third module with shared code
```

---

## Examples

### Example 1: String Utilities Module

**string_utils.pie:**
```pie
export string to_upper(string str) {
    return string_to_upper(str);
}

export string to_lower(string str) {
    return string_to_lower(str);
}

export string trim(string str) {
    return string_trim(str);
}

export int length(string str) {
    return strlen(str);
}
```

**Usage:**
```pie
import string_utils;

int main() {
    string text = "  Hello World  ";
    string upper = string_utils.to_upper(text);
    string trimmed = string_utils.trim(text);
    int len = string_utils.length(trimmed);
    
    output(upper, string);
    output(len, int);
    return 0;
}
```

### Example 2: Validation Module

**validators.pie:**
```pie
export int is_valid_email(string email) {
    int at_pos = string_index_of(email, "@");
    if (at_pos < 1) {
        return 0;  // No @ symbol or at start
    }
    
    int dot_pos = string_index_of(email, ".");
    if (dot_pos < at_pos + 2) {
        return 0;  // No domain extension
    }
    
    return 1;
}

export int is_positive(int num) {
    if (num > 0) {
        return 1;
    }
    return 0;
}

export int is_in_range(int num, int min, int max) {
    if (num >= min && num <= max) {
        return 1;
    }
    return 0;
}
```

**Usage:**
```pie
import validators;

int main() {
    string email = "user@example.com";
    if (validators.is_valid_email(email) == 1) {
        output("Valid email", string);
    } else {
        output("Invalid email", string);
    }
    
    int age = 25;
    if (validators.is_in_range(age, 18, 65) == 1) {
        output("Age is valid", string);
    }
    
    return 0;
}
```

### Example 3: Using HTTP and JSON Together

**api_client.pie:**
```pie
import http;
import json;

export json.object fetch_user(int user_id) {
    // Build URL
    string base_url = "https://jsonplaceholder.typicode.com/users/";
    // Note: In real implementation, would concatenate user_id
    string url = "https://jsonplaceholder.typicode.com/users/1";
    
    // Fetch data
    string response = http.get(url);
    
    // Parse JSON
    json.object user = json.parse(response);
    
    return user;
}

export void print_user(json.object user) {
    string name = json.get_string(user, "name");
    string email = json.get_string(user, "email");
    
    output("Name: ", string);
    output(name, string);
    output("Email: ", string);
    output(email, string);
}
```

**main.pie:**
```pie
import api_client;

int main() {
    json.object user = api_client.fetch_user(1);
    api_client.print_user(user);
    return 0;
}
```

### Example 4: Mathematical Operations

**See the complete example in:**
- `examples/user_modules/mathutils.pie` - Full mathematical utilities module
- `examples/user_modules/test_mathutils.pie` - Comprehensive test program

---

## Advanced Topics

### Module Initialization

Currently, PIE modules are stateless - they only export functions. Module-level variables and initialization code are not yet supported.

**Coming Soon:**
- Module-level constants
- Initialization functions
- Module state

### Nested Modules

Nested module namespaces (e.g., `utils.string.format`) are planned for future releases.

### Package Management

A package manager for sharing and distributing PIE modules is under consideration.

---

## Troubleshooting

### Module Not Found Error

```
Error: Module 'mymodule' not found
```

**Solutions:**
1. Ensure `mymodule.pie` exists in the same directory as your source file
2. Check the filename matches exactly (case-sensitive)
3. Verify the module has a `.pie` extension

### Function Not Found Error

```
Error: Function 'mymodule.myfunction' not declared
```

**Solutions:**
1. Ensure the function is marked with `export` in the module
2. Check function name spelling
3. Verify you imported the correct module

### Circular Import Error

```
Error: Circular dependency detected
```

**Solutions:**
1. Refactor shared code into a third module
2. Reorganize module dependencies
3. Combine modules if they're tightly coupled

---

## Summary

The PIE module system provides:

✅ **Standard library modules** for HTTP, JSON, and more  
✅ **User-defined modules** with export/private distinction  
✅ **Namespace isolation** using dot notation  
✅ **Code reusability** across projects  
✅ **Clean APIs** with controlled exports  

For more examples and advanced usage, see:
- `examples/user_modules/` - User-defined module examples
- `examples/modules/` - Standard library usage examples
- `stdlib/` - Standard library source code

Happy coding with PIE modules! 🥧
