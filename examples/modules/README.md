# PIE Module System Examples

This directory contains examples demonstrating the PIE module system.

## Quick Reference

### Importing Modules

```pie
import http;
import json;
import mathutils;  // User-defined module
```

### Using Standard Library Modules

```pie
import http;

int main() {
    string response = http.get("https://api.example.com");
    output(response, string);
    return 0;
}
```

### Creating Your Own Module

**mymath.pie:**
```pie
export int add(int a, int b) {
    return a + b;
}

export int multiply(int a, int b) {
    return a * b;
}

// Private helper (not exported)
int validate(int x) {
    if (x < 0) return 0;
    return 1;
}
```

**main.pie:**
```pie
import mymath;

int main() {
    int sum = mymath.add(5, 3);
    int product = mymath.multiply(4, 7);
    
    output("Sum: ", string);
    output(sum, int);
    output("Product: ", string);
    output(product, int);
    
    return 0;
}
```

## Available Examples

### HTTP Module Examples

- `http_client.pie` - Making HTTP GET/POST requests
- `http_server.pie` - Creating a simple HTTP server (planned)

### JSON Module Examples

- `json_demo.pie` - Parsing and creating JSON objects
- `json_array_demo.pie` - Working with JSON arrays (planned)

### User-Defined Module Examples

See `../user_modules/` directory:
- `mathutils.pie` - Mathematical utility functions
- `test_mathutils.pie` - Comprehensive test of mathutils

## Module System Features

✅ **Import standard library modules** (`http`, `json`)  
✅ **Create user-defined modules** with `.pie` files  
✅ **Export public functions** using `export` keyword  
✅ **Private functions** (no export) for internal use  
✅ **Namespace isolation** with dot notation (`module.function()`)  
✅ **Recursive functions** in modules  
✅ **Intra-module calls** (module functions calling each other)  

## Standard Library Modules

### HTTP Module

**Functions:**
- `http.get(string url)` - GET request
- `http.post(string url, string body)` - POST request
- `http.put(string url, string body)` - PUT request
- `http.delete(string url)` - DELETE request
- `http.listen(int port)` - Start HTTP server (planned)

### JSON Module

**Parsing:**
- `json.parse(string json)` - Parse JSON string
- `json.stringify(json.object obj)` - Convert to JSON string

**Object Operations:**
- `json.create_object()` - Create new object
- `json.get_string(json.object obj, string key)` - Get string value
- `json.get_int(json.object obj, string key)` - Get integer value
- `json.get_float(json.object obj, string key)` - Get float value
- `json.set_string(json.object obj, string key, string value)` - Set string
- `json.set_int(json.object obj, string key, int value)` - Set integer

**Array Operations:**
- `json.create_array()` - Create new array
- `json.array_append_string(json.array arr, string val)` - Append string
- `json.array_get_string(json.array arr, int index)` - Get string at index
- `json.array_size(json.array arr)` - Get array size

## Compilation

### Compiling with User-Defined Modules

Make sure the module file is in the same directory as your main program:

```bash
# Directory structure:
# my_project/
# ├── main.pie
# └── mymodule.pie

cd my_project
python3 ../src/main.py main.pie
./program
```

### Compiling with Standard Library Modules

Standard library modules are automatically found:

```bash
python3 src/main.py examples/modules/http_client.pie
./program
```

## Best Practices

1. **One module per file** - Keep modules focused and cohesive
2. **Export only public API** - Hide implementation details
3. **Use clear names** - Make module and function names descriptive
4. **Document exports** - Add comments to exported functions
5. **Avoid circular dependencies** - Don't have modules import each other

## Learn More

- **[Module System Guide](../../docs/module-system.md)** - Complete documentation
- **[Language Reference](../../docs/language-reference.md)** - Module syntax reference
- **[User Modules Examples](../user_modules/)** - More complex examples

Happy coding with PIE modules! 🥧
