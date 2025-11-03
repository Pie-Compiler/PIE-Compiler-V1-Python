# PIE Module Import Paths Guide

This document describes the enhanced module import system that supports custom directory paths.

## Overview

The PIE compiler now supports specifying custom paths when importing modules, making it easy to organize your code in different directories and import modules from anywhere in your project.

## Import Syntax

### 1. Standard Import (Default Search Path)

```pie
import module_name;
```

The compiler searches for the module in this order:
1. Standard library (`stdlib/`)
2. Source file directory
3. Current working directory
4. User-defined paths (via `-I` flag or `PIEPATH` environment variable)

**Example:**
```pie
import http;      // Searches for http module in stdlib
import json;      // Searches for json module in stdlib
```

---

### 2. Import with Alias

```pie
import module_name as alias;
```

Import a module and give it a custom name (alias) for use in your code.

**Example:**
```pie
import http as web;

string response = web.get("https://example.com");
```

---

### 3. Import from Custom Path (New Feature!)

```pie
import module_name from "path";
```

Import a module from a specific directory path. This is useful when your modules are organized in different folders.

**Path Types:**
- **Relative paths**: Start with `./` (relative to source file) or `../` (parent directory)
- **Absolute paths**: Start with `/` (absolute filesystem path)

**Examples:**

#### Relative Path - Same Directory
```pie
import UserModule from "./";
```

#### Relative Path - Subdirectory
```pie
import util from "./Utils/";
import helpers from "./lib/helpers/";
```

#### Relative Path - Parent Directory
```pie
import shared from "../shared/";
```

#### Absolute Path
```pie
import config from "/opt/myapp/config/";
```

---

### 4. Import from Custom Path with Alias

```pie
import module_name from "path" as alias;
```

Combine custom path and alias for maximum flexibility.

**Example:**
```pie
import UserModule from "./modules/" as user;
import utilities from "./lib/utils/" as utils;

string result = user.someFunction();
int value = utils.calculate(10);
```

---

## How Module Resolution Works

When you import a module, the compiler follows this resolution process:

### Without Custom Path

1. Check **standard library** (`stdlib/module_name/`)
2. Check **source file directory** (`<source_dir>/module_name.pie`)
3. Check **user paths** (specified via `-I` flag)
4. Check **current working directory**

### With Custom Path

1. **Resolve the path** (relative paths are resolved relative to the source file)
2. **Look for the module** in the specified directory:
   - First, try directory-based module: `<path>/module_name/module.json`
   - Then, try single-file module: `<path>/module_name.pie`
3. **Load the module** if found, error otherwise

---

## Directory Structure Examples

### Example 1: Simple Project Structure

```
my_project/
├── main.pie           # Your main program
├── Utils/
│   └── util.pie       # Utility module
└── Models/
    └── User.pie       # User model module
```

**main.pie:**
```pie
import util from "./Utils/";
import User from "./Models/";

int sum = util.add(5, 10);
string username = User.getName();
```

---

### Example 2: Nested Modules

```
my_app/
├── src/
│   ├── main.pie
│   ├── controllers/
│   │   └── UserController.pie
│   ├── models/
│   │   └── User.pie
│   └── lib/
│       ├── database/
│       │   └── db.pie
│       └── validation/
│           └── validator.pie
```

**src/main.pie:**
```pie
import UserController from "./controllers/";
import User from "./models/";
import db from "./lib/database/";
import validator from "./lib/validation/";

// Use the imported modules
UserController.handleRequest();
```

---

### Example 3: Shared Modules Across Projects

```
workspace/
├── shared/
│   ├── logging.pie
│   └── config.pie
├── project1/
│   └── main.pie
└── project2/
    └── app.pie
```

**project1/main.pie:**
```pie
// Import from parent directory
import logging from "../shared/";
import config from "../shared/";

logging.info("Application started");
```

**project2/app.pie:**
```pie
// Import from parent directory
import logging from "../shared/";

logging.debug("Debug mode enabled");
```

---

## Complete Working Example

### File Structure
```
PIE-Compiler-V1-Python/
├── testFiles/
│   ├── UserModule.pie    # Module with grade remarks
│   └── Utils/
│       └── util.pie      # Module with math utilities
└── test_modules.pie      # Main program
```

### UserModule.pie
```pie
//A sample User Module in PIE

export string remarks(float grade){
    if(grade>=90){
        return "Excellent";
    }else if(grade>=80){
        return "Good";
    }else{
        return "Pass";
    }
}
```

### Utils/util.pie
```pie
export int add(int a, int b) {
    return a + b;
}

export int multiply(int a, int b) {
    return a * b;
}

export string greet(string name) {
    return "Hello, " + name + "!";
}
```

### test_modules.pie
```pie
// Import from subdirectory with custom path
import UserModule from "./testFiles/";
import util from "./testFiles/Utils/";

output("=== Testing Module Import ===", string);

// Use UserModule
float grade = 92.5;
string remark = UserModule.remarks(grade);
output("Grade: ", string);
output(grade, float, 1);
output("Remark: " + remark, string);

// Use util module
int sum = util.add(15, 27);
output("Sum: ", string);
output(sum, int);

string greeting = util.greet("PIE Developer");
output(greeting, string);
```

### Compilation
```bash
python3 ./src/main.py test_modules.pie
./program
```

### Output
```
=== Testing Module Import ===
Grade: 
92.5
Remark: Excellent
Sum: 
42
Hello, PIE Developer!
```

---

## Error Handling

### Module Not Found Error

If the module cannot be found at the specified path:

```pie
import MyModule from "./wrong_path/";
```

**Error:**
```
Module 'MyModule' not found in custom path './wrong_path/' (resolved to: /absolute/path)
  - Tried directory module: /absolute/path/MyModule
  - Tried .pie file: /absolute/path/MyModule.pie
```

### Invalid Path Error

If you use a relative path without a source file context:

```
Cannot resolve relative import path './modules/' without source file directory
```

---

## Best Practices

### 1. Use Relative Paths for Project Modules

Always use relative paths (`./` or `../`) for modules within your project:

```pie
// Good
import utils from "./lib/";

// Avoid absolute paths unless necessary
// import utils from "/home/user/project/lib/";  // Not portable
```

### 2. Organize Modules by Function

Group related functionality into modules:

```
project/
├── controllers/
├── models/
├── views/
├── utils/
└── config/
```

### 3. Use Descriptive Module Names

```pie
// Good
import UserController from "./controllers/";
import DatabaseHelper from "./utils/database/";

// Less clear
import uc from "./c/";
import dh from "./u/d/";
```

### 4. Document Module Dependencies

At the top of your main file, document which modules are required:

```pie
// Required modules:
// - UserModule: Handles user authentication
// - util: Math and string utilities
// - config: Application configuration

import UserModule from "./modules/";
import util from "./lib/";
import config from "./config/";
```

### 5. Keep Module Paths Short

Avoid deeply nested directory structures where possible:

```pie
// Try to avoid
import helper from "./very/deeply/nested/path/to/helper/";

// Better
import helper from "./helpers/";
```

---

## Compatibility

### Backward Compatibility

The standard import syntax without custom paths still works:

```pie
import http;        // Still searches default paths
import json;        // Still searches default paths
```

### Migration Guide

If you have existing code using the default search path, no changes are needed. To use custom paths:

**Before:**
```pie
// Module must be in stdlib or current directory
import MyModule;
```

**After:**
```pie
// Module can be anywhere
import MyModule from "./any/path/";
```

---

## Technical Details

### Path Resolution Algorithm

1. **Parse import path** from string literal
2. **Determine if absolute or relative**:
   - Absolute: Starts with `/`
   - Relative: Starts with `./` or `../`
3. **Resolve relative paths**:
   - Relative to source file's directory
   - Convert to absolute path
4. **Search for module**:
   - Check for directory module: `<path>/module_name/module.json`
   - Check for file module: `<path>/module_name.pie`
5. **Load and cache module** for reuse

### Module Caching

Modules are cached after first load to improve performance:
- Each unique module is loaded only once
- Transitive dependencies are automatically resolved
- Circular dependencies are detected and prevented

---

## Summary

The enhanced module import system provides:

✅ **Flexible import paths** - Import modules from any directory
✅ **Relative and absolute paths** - Use what makes sense for your project
✅ **Backward compatible** - Existing code continues to work
✅ **Better organization** - Structure your project however you want
✅ **Clear error messages** - Know exactly what went wrong
✅ **Alias support** - Rename modules for clarity

This makes PIE suitable for larger projects with complex module hierarchies!
