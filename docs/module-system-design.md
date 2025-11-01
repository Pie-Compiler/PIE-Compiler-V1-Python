# PIE Module System Design

**Version:** 1.0.0  
**Status:** Design Specification  
**Last Updated:** November 1, 2025

---

## 1. Overview

The PIE module system provides a way to organize code into reusable libraries and import functionality from external modules. This design supports both standard library modules (like `http` and `json`) and user-defined modules.

### Goals

- ✅ Clean, simple import syntax
- ✅ Namespace management to avoid conflicts
- ✅ Standard library modules (http, json, math, etc.)
- ✅ User-defined modules
- ✅ Efficient compilation (only compile what's used)
- ✅ C interop for performance-critical modules

---

## 2. Module Syntax

### Import Statement

```pie
// Import entire module
import http;
import json;

// Import with alias
import http as h;

// Import specific items (future enhancement)
from http import get, post;

// Import standard library
import std.math;
import std.io;
```

### Module Usage

```pie
import http;
import json;

int main() {
    // Use module functions with namespace
    string response = http.get("https://api.example.com/data");
    
    // Parse JSON response
    json.object obj = json.parse(response);
    string name = json.get_string(obj, "name");
    
    output("Name: " + name, string);
    
    return 0;
}
```

---

## 3. Directory Structure

```
PIE-Compiler-V1-Python/
├── src/
│   ├── frontend/
│   │   ├── lexer.py          # Add IMPORT, FROM keywords
│   │   ├── parser.py         # Parse import statements
│   │   ├── semanticAnalysis.py  # Module resolution
│   │   └── module_resolver.py   # NEW: Module discovery and loading
│   ├── backend/
│   │   └── llvm_generator.py # Generate module code
│   └── main.py
├── stdlib/                    # NEW: Standard library modules
│   ├── http/
│   │   ├── http.pie          # PIE interface
│   │   └── module.json       # Module metadata
│   ├── json/
│   │   ├── json.pie          # PIE interface
│   │   └── module.json       # Module metadata
│   ├── math/
│   │   ├── math.pie
│   │   └── module.json
│   └── io/
│       ├── io.pie
│       └── module.json
├── runtime/                   # Runtime C implementations
│   ├── pie_http.c            # HTTP implementation
│   ├── pie_http.h
│   ├── pie_json.c            # JSON implementation
│   ├── pie_json.h
│   ├── pie_net.c             # Network utilities
│   └── pie_net.h
└── examples/
    └── modules/
        ├── http_server.pie
        ├── json_api.pie
        └── custom_module/
            └── mymodule.pie
```

---

## 4. Module Metadata (module.json)

Each module has a `module.json` file describing its interface, dependencies, and C bindings.

### Example: http/module.json

```json
{
  "name": "http",
  "version": "1.0.0",
  "description": "HTTP client and server support",
  "author": "PIE Team",
  "requires": {
    "pie_version": ">=1.0.0",
    "modules": []
  },
  "c_bindings": {
    "headers": ["pie_http.h"],
    "sources": ["pie_http.c"],
    "libraries": ["curl", "microhttpd", "pthread", "ssl", "crypto"]
  },
  "exports": {
    "functions": [
      {"name": "get", "signature": "string(string url)"},
      {"name": "post", "signature": "string(string url, string body, dict headers)"},
      {"name": "put", "signature": "string(string url, string body, dict headers)"},
      {"name": "delete", "signature": "string(string url)"},
      {"name": "listen", "signature": "void(int port, function handler)"}
    ],
    "types": [
      {"name": "request", "type": "struct"},
      {"name": "response", "type": "struct"},
      {"name": "status", "type": "enum"}
    ]
  }
}
```

### Example: json/module.json

```json
{
  "name": "json",
  "version": "1.0.0",
  "description": "JSON parsing and serialization",
  "author": "PIE Team",
  "requires": {
    "pie_version": ">=1.0.0",
    "modules": []
  },
  "c_bindings": {
    "headers": ["pie_json.h"],
    "sources": ["pie_json.c"],
    "libraries": ["jansson"]
  },
  "exports": {
    "functions": [
      {"name": "parse", "signature": "json.object(string text)"},
      {"name": "stringify", "signature": "string(json.object obj)"},
      {"name": "get_string", "signature": "string(json.object obj, string key)"},
      {"name": "get_int", "signature": "int(json.object obj, string key)"},
      {"name": "get_float", "signature": "float(json.object obj, string key)"},
      {"name": "get_bool", "signature": "bool(json.object obj, string key)"},
      {"name": "set_string", "signature": "void(json.object obj, string key, string value)"},
      {"name": "set_int", "signature": "void(json.object obj, string key, int value)"},
      {"name": "set_float", "signature": "void(json.object obj, string key, float value)"},
      {"name": "set_bool", "signature": "void(json.object obj, string key, bool value)"},
      {"name": "create_object", "signature": "json.object()"},
      {"name": "create_array", "signature": "json.array()"}
    ],
    "types": [
      {"name": "object", "type": "opaque"},
      {"name": "array", "type": "opaque"}
    ]
  }
}
```

---

## 5. AST Additions

### Import Statement Node

```python
class ImportStatement(Statement):
    def __init__(self, module_name, alias=None, items=None):
        self.module_name = module_name  # e.g., "http" or "std.math"
        self.alias = alias               # e.g., "h" in "import http as h"
        self.items = items or []         # e.g., ["get", "post"] in "from http import get, post"
        self.resolved_path = None        # Filled by module resolver
```

---

## 6. Lexer Additions

Add new tokens:

```python
# In lexer.py
reserved = {
    # ... existing keywords ...
    'import': 'KEYWORD_IMPORT',
    'from': 'KEYWORD_FROM',
    'as': 'KEYWORD_AS',
}

tokens = [
    # ... existing tokens ...
    'DOT',  # Already exists for member access
]
```

---

## 7. Parser Additions

### Parse Import Statements

```python
# In parser.py
def parse_import_statement(self):
    """
    import_statement : KEYWORD_IMPORT module_path
                     | KEYWORD_IMPORT module_path KEYWORD_AS IDENTIFIER
                     | KEYWORD_FROM module_path KEYWORD_IMPORT import_list
    
    module_path : IDENTIFIER (DOT IDENTIFIER)*
    import_list : IDENTIFIER (COMMA IDENTIFIER)*
    """
    self.expect('KEYWORD_IMPORT')
    
    # Parse module path (e.g., http or std.math)
    module_parts = [self.current_token.value]
    self.advance()
    
    while self.current_token.type == 'DOT':
        self.advance()
        module_parts.append(self.expect('IDENTIFIER').value)
    
    module_name = '.'.join(module_parts)
    
    # Check for alias
    alias = None
    if self.current_token.type == 'KEYWORD_AS':
        self.advance()
        alias = self.expect('IDENTIFIER').value
    
    self.expect('SEMICOLON')
    
    return ImportStatement(module_name, alias)
```

---

## 8. Module Resolver

Create a new file: `src/frontend/module_resolver.py`

```python
import os
import json
from pathlib import Path

class ModuleResolver:
    def __init__(self, stdlib_path=None, user_paths=None):
        self.stdlib_path = stdlib_path or Path(__file__).parent.parent.parent / 'stdlib'
        self.user_paths = user_paths or []
        self.loaded_modules = {}  # Cache loaded modules
        
    def resolve_module(self, module_name):
        """
        Resolve a module name to its file path and metadata.
        
        Search order:
        1. Standard library (stdlib/)
        2. User-defined paths
        3. Current directory
        """
        # Check if already loaded
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        
        # Try standard library first
        module_path = self.stdlib_path / module_name
        if module_path.exists():
            return self._load_module(module_path, module_name)
        
        # Try user paths
        for user_path in self.user_paths:
            module_path = Path(user_path) / module_name
            if module_path.exists():
                return self._load_module(module_path, module_name)
        
        raise ModuleNotFoundError(f"Module '{module_name}' not found")
    
    def _load_module(self, module_path, module_name):
        """Load module metadata and PIE interface file."""
        # Load module.json
        metadata_file = module_path / 'module.json'
        if not metadata_file.exists():
            raise ModuleError(f"Module '{module_name}' missing module.json")
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Load PIE interface file
        pie_file = module_path / f'{module_name}.pie'
        if not pie_file.exists():
            raise ModuleError(f"Module '{module_name}' missing {module_name}.pie")
        
        module_info = {
            'name': module_name,
            'path': module_path,
            'pie_file': pie_file,
            'metadata': metadata
        }
        
        self.loaded_modules[module_name] = module_info
        return module_info

class ModuleNotFoundError(Exception):
    pass

class ModuleError(Exception):
    pass
```

---

## 9. Semantic Analysis Integration

Update `semantic_analyzer.py` to handle imports:

```python
# In SemanticAnalyzer class
def __init__(self, symbol_table, module_resolver=None):
    self.symbol_table = symbol_table
    self.type_checker = TypeChecker(self.symbol_table)
    self.errors = []
    self.warnings = []
    self.error_set = set()
    self.current_function = None
    self.in_switch = False
    self.module_resolver = module_resolver or ModuleResolver()
    self.imported_modules = {}  # Track imported modules
    self._register_builtin_functions()

def visit_importstatement(self, node):
    """Process import statements and register module symbols."""
    try:
        # Resolve the module
        module_info = self.module_resolver.resolve_module(node.module_name)
        node.resolved_path = module_info['pie_file']
        
        # Register module namespace
        namespace = node.alias or node.module_name
        self.imported_modules[namespace] = module_info
        
        # Register module functions in symbol table with namespace
        metadata = module_info['metadata']
        for func in metadata['exports']['functions']:
            full_name = f"{namespace}.{func['name']}"
            # Parse signature and register function
            self._register_module_function(full_name, func)
        
        # Register module types
        for type_def in metadata['exports'].get('types', []):
            type_name = f"{namespace}.{type_def['name']}"
            self.symbol_table.add_symbol(
                type_name,
                'type',
                type_kind=type_def['type']
            )
            
    except (ModuleNotFoundError, ModuleError) as e:
        self.add_error(str(e))

def _register_module_function(self, full_name, func_metadata):
    """Register a module function in the symbol table."""
    # Parse signature: "string(string url, string body, dict headers)"
    # This is simplified; full implementation would parse properly
    signature = func_metadata['signature']
    # ... parsing logic ...
    
    self.symbol_table.add_symbol(
        full_name,
        'function',
        return_type=return_type,
        params=params,
        param_types=param_types,
        is_module_function=True
    )
```

---

## 10. Code Generation

Update `llvm_generator.py` to handle module function calls:

```python
def visit_functioncall(self, node):
    # Check if this is a module function call (contains '.')
    if '.' in node.name:
        return self.visit_module_function_call(node)
    
    # ... existing code ...

def visit_module_function_call(self, node):
    """Handle calls to module functions like http.get()"""
    # Module functions are declared in the C runtime
    # They should already be declared in the LLVM module
    
    func = self.module.get_global(node.name.replace('.', '_'))
    if func is None:
        # Declare external function
        func = self._declare_module_function(node.name)
    
    # Process arguments as normal
    args = []
    for arg in node.args:
        arg_val = self.visit(arg)
        args.append(self._load_if_pointer(arg_val))
    
    return self.builder.call(func, args, 'module_call_tmp')

def _declare_module_function(self, func_name):
    """Declare an external module function."""
    # Look up function signature from symbol table
    symbol = self.symbol_table.lookup_function(func_name)
    if not symbol:
        raise Exception(f"Module function not found: {func_name}")
    
    # Create LLVM function type
    param_types = [self._pie_type_to_llvm(pt) for pt in symbol['param_types']]
    return_type = self._pie_type_to_llvm(symbol['return_type'])
    
    func_type = ir.FunctionType(return_type, param_types)
    c_name = func_name.replace('.', '_')  # http.get -> http_get
    
    return ir.Function(self.module, func_type, name=c_name)
```

---

## 11. Build System Integration

Update `main.py` to handle module compilation:

```python
def compile_with_modules(source_file):
    """Compile PIE program with module support."""
    # Parse main file
    parser = Parser(source_file)
    ast = parser.parse()
    
    # Initialize module resolver
    module_resolver = ModuleResolver()
    
    # Semantic analysis with module support
    symbol_table = SymbolTable()
    analyzer = SemanticAnalyzer(symbol_table, module_resolver)
    success, errors = analyzer.analyze(ast)
    
    if not success:
        print("Compilation failed due to semantic errors.")
        return False
    
    # Code generation
    llvm_generator = LLVMCodeGenerator(symbol_table, analyzer.imported_modules)
    llvm_module = llvm_generator.generate(ast)
    
    # Collect C sources and libraries from modules
    c_sources = []
    libraries = []
    
    for module_info in analyzer.imported_modules.values():
        metadata = module_info['metadata']
        c_bindings = metadata.get('c_bindings', {})
        
        # Add C source files
        for src in c_bindings.get('sources', []):
            c_sources.append(f"runtime/{src}")
        
        # Add libraries
        libraries.extend(c_bindings.get('libraries', []))
    
    # Build with additional sources and libraries
    build_and_link(llvm_module, c_sources, libraries)
    
    return True
```

---

## 12. Compilation Flow

```
┌─────────────────────┐
│  main.pie           │
│  import http;       │
│  import json;       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Lexer              │
│  - Tokenize imports │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Parser             │
│  - Parse imports    │
│  - Build AST        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Module Resolver    │
│  - Find modules     │
│  - Load metadata    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Semantic Analyzer  │
│  - Register symbols │
│  - Type checking    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  LLVM Generator     │
│  - Generate IR      │
│  - Link modules     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Build & Link       │
│  - Compile C files  │
│  - Link libraries   │
│  - Generate binary  │
└─────────────────────┘
```

---

## 13. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Add IMPORT, FROM, AS keywords to lexer
- [ ] Implement import statement parsing
- [ ] Create ModuleResolver class
- [ ] Update AST with ImportStatement node

### Phase 2: Module System Core (Week 3-4)
- [ ] Implement module.json parsing
- [ ] Update semantic analyzer for module support
- [ ] Add module function registration
- [ ] Test with simple module

### Phase 3: HTTP Module (Week 5-6)
- [ ] Design HTTP C API (pie_http.c/h)
- [ ] Implement HTTP client (GET, POST, PUT, DELETE)
- [ ] Implement HTTP server (basic)
- [ ] Create http.pie interface
- [ ] Write tests

### Phase 4: JSON Module (Week 7-8)
- [ ] Design JSON C API (pie_json.c/h)
- [ ] Implement JSON parsing (using jansson)
- [ ] Implement JSON serialization
- [ ] Create json.pie interface
- [ ] Write tests

### Phase 5: Integration & Testing (Week 9-10)
- [ ] Build system integration
- [ ] End-to-end testing
- [ ] Documentation
- [ ] Example programs

---

## 14. Example Programs

### HTTP Server with JSON

```pie
import http;
import json;

void handle_request(http.request req, http.response res) {
    if (req.method == "GET" && req.path == "/api/users") {
        // Create JSON response
        json.array users = json.create_array();
        
        json.object user1 = json.create_object();
        json.set_string(user1, "name", "Alice");
        json.set_int(user1, "age", 30);
        
        json.object user2 = json.create_object();
        json.set_string(user2, "name", "Bob");
        json.set_int(user2, "age", 25);
        
        // Serialize to JSON string
        string response_body = json.stringify(users);
        
        res.status(200);
        res.header("Content-Type", "application/json");
        res.send(response_body);
    } else {
        res.status(404);
        res.send("Not found");
    }
}

int main() {
    output("Starting server on port 8080...", string);
    http.listen(8080, handle_request);
    return 0;
}
```

### HTTP Client with JSON

```pie
import http;
import json;

int main() {
    // Make HTTP request
    string response = http.get("https://api.github.com/users/octocat");
    
    // Parse JSON
    json.object user = json.parse(response);
    
    // Extract data
    string name = json.get_string(user, "name");
    int followers = json.get_int(user, "followers");
    
    output("Name: " + name, string);
    output("Followers: " + followers, int);
    
    return 0;
}
```

---

## 15. Next Steps

1. Review and approve this design
2. Begin Phase 1 implementation
3. Create initial module structure
4. Implement HTTP module prototype
5. Implement JSON module prototype
6. Test and iterate

---

## Appendix: Standard Library Modules (Planned)

| Module | Description | Priority |
|--------|-------------|----------|
| `http` | HTTP client/server | High |
| `json` | JSON parsing/serialization | High |
| `io` | File I/O utilities | Medium |
| `math` | Extended math functions | Medium |
| `net` | Low-level networking | Low |
| `crypto` | Cryptographic functions | Low |
| `time` | Date/time utilities | Medium |
| `regex` | Regular expressions | Low |
| `collections` | Advanced data structures | Medium |

