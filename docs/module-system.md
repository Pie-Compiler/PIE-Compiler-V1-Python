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

The `http` module provides HTTP client capabilities powered by **libcurl**. It allows you to make HTTP requests to web APIs and servers directly from PIE programs.

**Available Functions:**

| Function | Signature | Description |
|----------|-----------|-------------|
| `get` | `string(string url)` | Perform HTTP GET request |
| `post` | `string(string url, string body, dict headers)` | Perform HTTP POST request |
| `put` | `string(string url, string body, dict headers)` | Perform HTTP PUT request |
| `delete` | `string(string url)` | Perform HTTP DELETE request |

**Implementation Details:**
- Uses libcurl for reliable HTTP communication
- Automatically follows redirects
- Custom User-Agent: "PIE-HTTP/1.0"
- Returns response body as string
- Error messages prefixed with `[ERROR]`

#### HTTP GET Example

Fetch data from a public API:

```pie
import http;

// Make a GET request to a public API
string response = http.get("https://httpbin.org/get");

output("=== HTTP GET Response ===", string);
output(response, string);

// Example output:
// {
//   "args": {},
//   "headers": {
//     "Accept": "*/*",
//     "Host": "httpbin.org",
//     "User-Agent": "PIE-HTTP/1.0"
//   },
//   "origin": "xxx.xxx.xxx.xxx",
//   "url": "https://httpbin.org/get"
// }
```

#### HTTP POST Example

Send data to an API endpoint:

```pie
import http;

// Prepare JSON body
string json_body = "{\"name\": \"PIE Lang\", \"version\": \"1.0\"}";

// Make POST request
string response = http.post(
    "https://httpbin.org/post",
    json_body,
    null  // headers parameter (optional)
);

output("POST Response: ", string);
output(response, string);
```

#### HTTP PUT Example

Update a resource:

```pie
import http;

string update_data = "{\"status\": \"updated\"}";

string response = http.put(
    "https://httpbin.org/put",
    update_data,
    null
);

output("PUT Response: ", string);
output(response, string);
```

#### HTTP DELETE Example

Delete a resource:

```pie
import http;

string response = http.delete("https://httpbin.org/delete");

output("DELETE Response: ", string);
output(response, string);
```

#### Complete HTTP Client Example

A practical example fetching and displaying API data:

```pie
import http;

output("=== Testing PIE HTTP Module ===", string);

// Test 1: GET request
output("Fetching user data...", string);
string user_response = http.get("https://jsonplaceholder.typicode.com/users/1");
output("User Data:", string);
output(user_response, string);

// Test 2: POST request
output("Creating new post...", string);
string new_post = "{\"title\": \"Hello from PIE\", \"body\": \"Testing HTTP POST\", \"userId\": 1}";
string post_response = http.post(
    "https://jsonplaceholder.typicode.com/posts",
    new_post,
    null
);
output("Created Post:", string);
output(post_response, string);

output("=== All HTTP tests complete! ===", string);
```

### JSON Module

The `json` module provides JSON parsing and manipulation capabilities powered by **libjansson**.

**Implementation Status:** ⚠️ Currently using stub implementations. Full functionality coming soon with Jansson library integration.

**Available Functions:**

| Category | Function | Signature | Description |
|----------|----------|-----------|-------------|
| **Parsing** | `parse` | `json.object(string text)` | Parse JSON string into object |
| | `stringify` | `string(json.object obj)` | Convert JSON object to string |
| **Object Creation** | `create_object` | `json.object()` | Create new empty JSON object |
| | `create_array` | `json.array()` | Create new empty JSON array |
| **Object Getters** | `get_string` | `string(json.object obj, string key)` | Get string value from object |
| | `get_int` | `int(json.object obj, string key)` | Get integer value from object |
| | `get_float` | `float(json.object obj, string key)` | Get float value from object |
| | `get_bool` | `int(json.object obj, string key)` | Get boolean value from object |
| | `get_object` | `json.object(json.object obj, string key)` | Get nested object |
| | `get_array` | `json.array(json.object obj, string key)` | Get array from object |
| **Object Setters** | `set_string` | `void(json.object obj, string key, string value)` | Set string value |
| | `set_int` | `void(json.object obj, string key, int value)` | Set integer value |
| | `set_float` | `void(json.object obj, string key, float value)` | Set float value |
| | `set_bool` | `void(json.object obj, string key, int value)` | Set boolean value |
| **Array Operations** | `array_size` | `int(json.array arr)` | Get array size |
| | `array_get_string` | `string(json.array arr, int index)` | Get string at index |
| | `array_get_int` | `int(json.array arr, int index)` | Get integer at index |
| | `array_get_object` | `json.object(json.array arr, int index)` | Get object at index |
| | `array_push_string` | `void(json.array arr, string value)` | Add string to array |
| | `array_push_int` | `void(json.array arr, int value)` | Add integer to array |
| | `array_push_object` | `void(json.array arr, json.object obj)` | Add object to array |

#### JSON Creation Example

Create and manipulate JSON objects:

```pie
import json;

// Create a new JSON object
json.object person = json.create_object();

// Set values
json.set_string(person, "name", "Alice");
json.set_int(person, "age", 25);
json.set_float(person, "height", 5.6);
json.set_bool(person, "active", 1);

// Convert to JSON string
string json_str = json.stringify(person);
output("JSON: ", string);
output(json_str, string);

// Output: {"name":"Alice","age":25,"height":5.6,"active":true}
```

#### JSON Parsing Example

Parse and extract data from JSON:

```pie
import json;

// Parse JSON string
string json_data = "{\"name\":\"Bob\",\"score\":95,\"passed\":true}";
json.object result = json.parse(json_data);

// Extract values
string name = json.get_string(result, "name");
int score = json.get_int(result, "score");
int passed = json.get_bool(result, "passed");

output("Student: ", string);
output(name, string);
output("Score: ", string);
output(score, int);
```

#### JSON Array Example

Work with JSON arrays:

```pie
import json;

// Create array
json.array colors = json.create_array();

// Add items
json.array_push_string(colors, "red");
json.array_push_string(colors, "green");
json.array_push_string(colors, "blue");

// Get array size
int size = json.array_size(colors);
output("Array size: ", string);
output(size, int);

// Access elements
string first = json.array_get_string(colors, 0);
output("First color: ", string);
output(first, string);
```

#### HTTP + JSON Combined Example

A practical example combining HTTP and JSON:

```pie
import http;
import json;

output("=== Fetching and Parsing JSON Data ===", string);

// Fetch JSON data from API
string response = http.get("https://jsonplaceholder.typicode.com/users/1");

// Note: Full JSON parsing will work once Jansson integration is complete
// For now, you can work with the raw JSON string
output("API Response:", string);
output(response, string);

// With full JSON support (coming soon):
// json.object user = json.parse(response);
// string name = json.get_string(user, "name");
// string email = json.get_string(user, "email");
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

## System Dependencies

### Required Libraries for Standard Modules

Some standard library modules require system libraries to be installed.

#### HTTP Module Dependencies

The HTTP module requires **libcurl** for HTTP client functionality:

```bash
# Ubuntu/Debian
sudo apt-get install libcurl4-openssl-dev

# macOS
brew install curl

# Arch Linux
sudo pacman -S curl
```

Optional for server functionality (not yet implemented):
```bash
# Ubuntu/Debian
sudo apt-get install libmicrohttpd-dev
```

#### JSON Module Dependencies

The JSON module will require **libjansson** once fully implemented:

```bash
# Ubuntu/Debian
sudo apt-get install libjansson-dev

# macOS
brew install jansson

# Arch Linux
sudo pacman -S jansson
```

#### Install All Dependencies

For convenience, install all dependencies at once:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libcurl4-openssl-dev libmicrohttpd-dev libjansson-dev

# macOS
brew install curl jansson

# Arch Linux
sudo pacman -S curl jansson
```

### Verifying Installation

Test your HTTP module installation:

```pie
// test_http.pie
import http;

string response = http.get("https://httpbin.org/get");
output("Response received successfully!", string);
output(response, string);
```

Compile and run:
```bash
python3 src/main.py test_http.pie
./program
```

If you see a response, the HTTP module is working correctly!

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
