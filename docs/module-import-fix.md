# Module Import System Fix

## Problem

The PIE compiler was linking **all** C runtime files regardless of which modules were actually imported in the source code. This caused linker errors when compiling programs without module imports.

### Specific Issue

When compiling `testFiles/File_I_O.pie` (which has no imports), the compiler would:
1. Compile **all** runtime C files, including `pie_http.c`
2. Try to link `pie_http.o` without including the required libraries (`-lcurl -lmicrohttpd -lpthread`)
3. Fail with undefined reference errors:
   ```
   /usr/bin/ld: pie_http.o: undefined reference to `MHD_start_daemon'
   /usr/bin/ld: pie_http.o: undefined reference to `MHD_stop_daemon'
   ...
   ```

## Root Cause

In `src/main.py`, the `build_and_link()` function was using:

```python
# Get all C files from runtime directory
c_files = [f for f in os.listdir(runtime_path) if f.endswith('.c')]

# Compile each runtime C file
for c_file in c_files:
    # Compile everything, including module-specific files
    ...
```

This compiled **every** `.c` file in the runtime directory, regardless of whether the module was imported.

## Solution

Modified `build_and_link()` to distinguish between:

### 1. Core Runtime Files (Always Compiled)
These provide fundamental functionality needed by all PIE programs:
- `runtime.c` - Core runtime initialization
- `d_array.c` - Dynamic array implementation
- `dict_lib.c` - Dictionary/hashmap
- `string_lib.c` - String operations
- `file_lib.c` - File I/O
- `crypto_lib.c` - Cryptographic functions
- `time_lib.c` - Time/date functions
- `regex_lib.c` - Regular expressions
- `math_lib.c` - Math operations
- `net_lib.c` - Network utilities

### 2. Module-Specific Files (Only When Imported)
These are compiled **only** when their corresponding module is imported:
- `pie_http.c` - Only when `import http;` is present
- `pie_json.c` - Only when `import json;` is present

## Implementation

### Changes to `src/main.py`

**Before:**
```python
# Get all C files from runtime directory
c_files = [f for f in os.listdir(runtime_path) if f.endswith('.c')]
runtime_c_files = set(c_files)

# Compile each runtime C file
for c_file in c_files:
    obj_file = c_file.replace('.c', '.o')
    subprocess.run(
        [clang_path, "-c", "-fPIC", os.path.join(runtime_path, c_file), "-o", obj_file],
        check=True
    )
    obj_files.append(obj_file)
```

**After:**
```python
# Core runtime files (always compiled)
core_runtime_files = [
    'runtime.c',
    'd_array.c',
    'dict_lib.c',
    'string_lib.c',
    'file_lib.c',
    'crypto_lib.c',
    'time_lib.c',
    'regex_lib.c',
    'math_lib.c',
    'net_lib.c'
]

# Track which C files are being compiled
runtime_c_files = set()

# Compile core runtime files
for c_file in core_runtime_files:
    if os.path.exists(os.path.join(runtime_path, c_file)):
        obj_file = c_file.replace('.c', '.o')
        subprocess.run(
            [clang_path, "-c", "-fPIC", os.path.join(runtime_path, c_file), "-o", obj_file],
            check=True
        )
        obj_files.append(obj_file)
        runtime_c_files.add(c_file)
```

The module-specific C files are still handled by the existing module import mechanism:

```python
# Compile module-specific C sources if any (skip duplicates already in runtime/)
for c_source_path in c_sources:
    c_file = os.path.basename(c_source_path)
    # Skip if this file was already compiled from runtime directory
    if c_file in runtime_c_files:
        continue
    if os.path.exists(c_source_path):
        obj_file = c_file.replace('.c', '.o')
        print(f"Compiling module source: {c_source_path}")
        subprocess.run(
            [clang_path, "-c", "-fPIC", str(c_source_path), "-o", obj_file],
            check=True
        )
        obj_files.append(obj_file)
```

## Testing

### Test 1: File Without Imports ✅

**File:** `testFiles/File_I_O.pie` (no imports)

**Result:**
```bash
$ python3 ./src/main.py testFiles/File_I_O.pie
Build and linking successful! Executable: ./program

$ ./program
File written successfully with various expressions
File contents:
Line 1: Hello, World! 
Line 2: PIE language 
...
```

**Verification:** No HTTP-related linker errors, program runs successfully.

### Test 2: File With HTTP Import ✅

**File:** `test_minimal_server.pie` (has `import http;`)

**Result:**
```bash
$ python3 ./src/main.py test_minimal_server.pie
Imported modules: http
Module C sources: ['/home/ian/.../pie_http.c']
Module libraries: ['curl', 'microhttpd', 'pthread']
Compiling module source: .../pie_http.c
Build and linking successful! Executable: ./program

$ ./program
[PIE HTTP Server] Server running on http://localhost:9000
```

**Verification:** `pie_http.c` is compiled and linked with required libraries.

### Test 3: File With JSON Import ✅

**File:** `test_json_simple.pie` (has `import json;`)

**Result:**
```bash
$ python3 ./src/main.py test_json_simple.pie
Imported modules: json
Module C sources: ['/home/ian/.../pie_json.c']
Module libraries: ['jansson']
Compiling module source: .../pie_json.c
Build and linking successful! Executable: ./program
```

**Verification:** `pie_json.c` is compiled and linked with jansson library.

## Impact

### Before Fix
- ❌ Files without imports: **Compilation failed** (linker errors)
- ✅ Files with imports: Worked but unnecessarily slow (all C files compiled)

### After Fix
- ✅ Files without imports: **Compilation succeeds**
- ✅ Files with imports: **Compilation succeeds with correct libraries**
- ⚡ Faster compilation (only compiles needed files)

## Benefits

1. **Fixes Linker Errors**: Programs without imports now compile successfully
2. **Faster Builds**: Only compiles C files that are actually needed
3. **Correct Dependencies**: Only links required libraries for imported modules
4. **Scalable**: Easy to add new modules without affecting non-importing code
5. **Clean Separation**: Clear distinction between core runtime and optional modules

## Module System Architecture

```
PIE Source Code
    ↓
  Parser detects: import http;
    ↓
  SemanticAnalyzer tracks: imported_modules['http']
    ↓
  ModuleResolver provides:
    - C sources: ['pie_http.c']
    - Libraries: ['curl', 'microhttpd', 'pthread']
    ↓
  main.py build_and_link():
    - Compiles core runtime (always)
    - Compiles pie_http.c (because http imported)
    - Links with -lcurl -lmicrohttpd -lpthread
    ↓
  Executable: ./program
```

## Adding New Modules

To add a new module with C bindings:

1. **Create module definition**: `stdlib/module_name/module.json`
   ```json
   {
     "c_bindings": {
       "sources": ["pie_module.c"],
       "libraries": ["libname"]
     }
   }
   ```

2. **Create C implementation**: `src/runtime/pie_module.c`
   - Implement module functions
   - Must **not** be in `core_runtime_files` list

3. **Import in PIE code**: `import module_name;`
   - Compiler automatically includes C source and libraries

4. **Core runtime stays unchanged**: No need to modify `main.py`

## Future Enhancements

Potential improvements to the module system:

- [ ] Automatic detection of module dependencies
- [ ] Module caching (compile once, reuse .o files)
- [ ] Build configuration for conditional module inclusion
- [ ] Warning for unused imports
- [ ] Module versioning and compatibility checks

## Conclusion

The module import system now works correctly, compiling only the necessary C files and linking only the required libraries based on which modules are actually imported in the PIE source code. This fix was essential for making the compiler practical for real-world use.
