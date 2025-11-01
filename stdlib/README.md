# PIE Module System

The PIE module system allows you to organize code into reusable libraries and import functionality from external modules.

## Status

🚧 **In Development** - Design phase complete, implementation in progress

## Quick Start

### Importing Modules

```pie
import http;
import json;

int main() {
    string response = http.get("https://api.example.com/data");
    json.object data = json.parse(response);
    
    string name = json.get_string(data, "name");
    output("Name: " + name, string);
    
    return 0;
}
```

### Available Modules

| Module | Status | Description |
|--------|--------|-------------|
| `http` | 📋 Designed | HTTP client and server |
| `json` | 📋 Designed | JSON parsing and serialization |
| `math` | 📋 Planned | Extended mathematical functions |
| `io` | 📋 Planned | Advanced file I/O utilities |

## Module Structure

Each module consists of:

1. **`module.json`** - Metadata and interface definition
2. **`<module>.pie`** - PIE interface file (optional)
3. **C implementation** - Runtime implementation in `runtime/`

### Example: HTTP Module

```
stdlib/http/
├── module.json       # Module metadata
└── http.pie          # PIE interface

runtime/
├── pie_http.c        # C implementation
└── pie_http.h        # C header
```

## HTTP Module

### Client Functions

```pie
import http;

// GET request
string response = http.get("https://api.example.com/users");

// POST request
dict headers;
headers["Content-Type"] = "application/json";
string body = "{\"name\":\"Alice\"}";
string response = http.post("https://api.example.com/users", body, headers);

// PUT request
string response = http.put("https://api.example.com/users/1", body, headers);

// DELETE request
string response = http.delete("https://api.example.com/users/1");
```

### Server Functions

```pie
import http;

void handle_request(http.request req, http.response res) {
    if (req.path == "/hello") {
        res.status(200);
        res.header("Content-Type", "text/plain");
        res.send("Hello from PIE!");
    } else {
        res.status(404);
        res.send("Not found");
    }
}

int main() {
    http.listen(8080, handle_request);
    return 0;
}
```

### HTTP Status Codes

```pie
http.HTTP_OK                    // 200
http.HTTP_CREATED               // 201
http.HTTP_NO_CONTENT            // 204
http.HTTP_BAD_REQUEST           // 400
http.HTTP_UNAUTHORIZED          // 401
http.HTTP_FORBIDDEN             // 403
http.HTTP_NOT_FOUND             // 404
http.HTTP_INTERNAL_ERROR        // 500
```

## JSON Module

### Parsing and Serialization

```pie
import json;

// Parse JSON string
string json_text = "{\"name\":\"Alice\",\"age\":30}";
json.object obj = json.parse(json_text);

// Access values
string name = json.get_string(obj, "name");
int age = json.get_int(obj, "age");

// Create JSON object
json.object person = json.create_object();
json.set_string(person, "name", "Bob");
json.set_int(person, "age", 25);

// Convert to string
string result = json.stringify(person);
```

### Working with Arrays

```pie
import json;

// Create array
json.array users = json.create_array();

// Add values
json.array_push_string(users, "Alice");
json.array_push_string(users, "Bob");
json.array_push_int(users, 42);

// Get array size
int count = json.array_size(users);

// Access elements
string first = json.array_get_string(users, 0);
```

### Objects and Arrays

```pie
import json;

// Create array of objects
json.array products = json.create_array();

json.object prod1 = json.create_object();
json.set_string(prod1, "name", "Laptop");
json.set_int(prod1, "price", 999);

json.array_push_object(products, prod1);

// Access object in array
json.object item = json.array_get_object(products, 0);
string name = json.get_string(item, "name");
```

## Complete Example: REST API Server

```pie
import http;
import json;

json.array users;  // In-memory user storage

void init_users() {
    users = json.create_array();
    
    json.object user1 = json.create_object();
    json.set_string(user1, "name", "Alice");
    json.set_string(user1, "email", "alice@example.com");
    json.array_push_object(users, user1);
}

void handle_request(http.request req, http.response res) {
    // GET /api/users - List all users
    if (req.method == "GET" && req.path == "/api/users") {
        string response_body = json.stringify(users);
        res.status(http.HTTP_OK);
        res.header("Content-Type", "application/json");
        res.send(response_body);
    }
    // POST /api/users - Create user
    else if (req.method == "POST" && req.path == "/api/users") {
        json.object new_user = json.parse(req.body);
        
        if (new_user != null) {
            json.array_push_object(users, new_user);
            
            json.object response = json.create_object();
            json.set_string(response, "message", "User created");
            
            string response_body = json.stringify(response);
            res.status(http.HTTP_CREATED);
            res.header("Content-Type", "application/json");
            res.send(response_body);
        } else {
            res.status(http.HTTP_BAD_REQUEST);
            res.send("Invalid JSON");
        }
    }
    // 404
    else {
        res.status(http.HTTP_NOT_FOUND);
        res.send("Not found");
    }
}

int main() {
    init_users();
    
    output("Starting API server on port 8080...", string);
    http.listen(8080, handle_request);
    
    return 0;
}
```

## Implementation Status

### Phase 1: Foundation ✅
- [x] Module system design
- [x] Module metadata format (module.json)
- [x] Module resolver implementation
- [x] Directory structure
- [x] Example programs

### Phase 2: Compiler Integration 🚧
- [ ] Add IMPORT keyword to lexer
- [ ] Parse import statements
- [ ] Integrate module resolver with semantic analyzer
- [ ] Register module symbols
- [ ] Handle namespace resolution

### Phase 3: HTTP Module 📋
- [ ] Design C API for HTTP client
- [ ] Implement GET, POST, PUT, DELETE
- [ ] Design C API for HTTP server
- [ ] Implement request handling
- [ ] Test HTTP module

### Phase 4: JSON Module 📋
- [ ] Integrate jansson library
- [ ] Implement JSON parsing
- [ ] Implement JSON serialization
- [ ] Implement object/array operations
- [ ] Test JSON module

### Phase 5: Testing & Documentation 📋
- [ ] End-to-end tests
- [ ] Performance testing
- [ ] Complete documentation
- [ ] Example applications

## Building with Modules

Once implemented, modules will be compiled automatically:

```bash
# Compile program that imports http and json
python3 ./src/main.py my_server.pie

# The compiler will:
# 1. Detect import statements
# 2. Resolve modules from stdlib/
# 3. Link required C implementations
# 4. Link external libraries (libcurl, jansson, etc.)
```

## Module Search Path

Modules are searched in this order:

1. Standard library: `stdlib/`
2. User paths (via `-I` flag or `PIEPATH` environment variable)
3. Current directory

Example:
```bash
# Add custom module path
python3 ./src/main.py -I /path/to/modules my_program.pie

# Or use environment variable
export PIEPATH=/path/to/modules
python3 ./src/main.py my_program.pie
```

## Creating Custom Modules

To create a custom module:

1. Create module directory: `mymodule/`
2. Create `module.json` with metadata
3. Create `mymodule.pie` with interface
4. Optionally create C implementation
5. Place in search path or current directory

See `docs/module-system-design.md` for detailed specifications.

## Contributing

Module development is tracked in the project's issue tracker. See:
- HTTP Module: Issue #TBD
- JSON Module: Issue #TBD

## Examples

See `examples/modules/` for complete working examples:
- `http_server.pie` - HTTP server with JSON API
- `http_client.pie` - HTTP client making API calls
- `json_demo.pie` - JSON parsing and manipulation

## Documentation

- [Module System Design](docs/module-system-design.md) - Complete architecture
- [HTTP Module Specification](docs/http.md) - HTTP module details
- Module API Reference - Coming soon

## License

Part of the PIE Compiler project. See LICENSE for details.
