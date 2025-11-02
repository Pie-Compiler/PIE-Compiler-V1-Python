# PIE HTTP Examples

This directory contains examples demonstrating the HTTP capabilities of the PIE language.

## Prerequisites

Install required system libraries:

```bash
# Ubuntu/Debian
sudo apt-get install libcurl4-openssl-dev libmicrohttpd-dev

# Fedora/RHEL  
sudo dnf install libcurl-devel libmicrohttpd-devel

# macOS
brew install curl libmicrohttpd
```

## Example Files

### Client Examples

#### Basic GET Request
See any of the client test files in the workspace.

### Server Examples

#### 1. `test_minimal_server.pie` - Minimal Server
The simplest possible HTTP server.

**Compile and Run:**
```bash
source venv/bin/activate
python3 ./src/main.py test_minimal_server.pie
./program
```

**Test:**
```bash
curl http://localhost:9000/
# Output: Hello from PIE!
```

#### 2. `test_http_server_complete.pie` - Routing Example
Demonstrates path-based routing with different responses.

**Compile and Run:**
```bash
source venv/bin/activate
python3 ./src/main.py test_http_server_complete.pie
./program
```

**Test:**
```bash
# Root path
curl http://localhost:8080/
# Output: Welcome to PIE HTTP Server!

# Hello route
curl http://localhost:8080/hello
# Output: Hello, World!

# API endpoint
curl http://localhost:8080/api/data
# Output: {message: This is data, status: ok}

# 404 Not Found
curl http://localhost:8080/notfound
# Output: 404 - Page Not Found
```

#### 3. `test_http_showcase.pie` - Full Feature Demo
Demonstrates all HTTP server features: routing, methods, headers, status codes.

**Compile and Run:**
```bash
source venv/bin/activate
python3 ./src/main.py test_http_showcase.pie
./program
```

**Test:**
```bash
# HTML home page (200 OK)
curl http://localhost:3000/

# JSON API endpoint (200 OK with headers)
curl -v http://localhost:3000/api

# Simple hello (200 OK)
curl http://localhost:3000/hello

# Status endpoint (200 OK)
curl http://localhost:3000/status

# Method not allowed (405)
curl -X POST http://localhost:3000/api

# Not found (404)
curl http://localhost:3000/unknown
```

## API Quick Reference

### Server Functions

```pie
// Start server
void http.listen(int port, ptr handler)

// Request inspection
string http.request_get_path(ptr request)
string http.request_get_method(ptr request)
string http.request_get_body(ptr request)
string http.request_get_header(ptr request, string name)
Dictionary http.request_get_headers(ptr request)

// Response building
void http.response_set_body(ptr response, string content)
void http.response_set_header(ptr response, string name, string value)
void http.response_set_status(ptr response, int code)
```

### Creating a Handler

Handlers must have this signature:
```pie
void handler_name(ptr request, ptr response) {
    // Access request
    string path = http.request_get_path(request);
    string method = http.request_get_method(request);
    
    // Build response
    http.response_set_status(response, 200);
    http.response_set_header(response, "Content-Type", "text/plain");
    http.response_set_body(response, "Hello!");
}
```

### Starting the Server

```pie
void start() {
    http.listen(PORT, handler_name);  // Pass function name without ()
}
```

## Common Status Codes

- **200** - OK (success)
- **201** - Created (resource created)
- **400** - Bad Request (malformed request)
- **404** - Not Found (resource doesn't exist)
- **405** - Method Not Allowed (wrong HTTP method)
- **500** - Internal Server Error (server error)

## Tips

1. **No Parentheses**: Pass handler as `handler_name`, not `handler_name()`
2. **Blocking**: `http.listen()` blocks - it's the last line in `start()`
3. **Content-Type**: Always set for proper client interpretation
4. **Status Codes**: Use appropriate codes (200 for success, 404 for not found, etc.)

## Troubleshooting

### Compilation Errors

**Error**: `Module function 'http.xxx' not declared`
- Make sure you have `import http;` at the top
- Check function name spelling in `stdlib/http/module.json`

**Error**: `Type of #1 arg mismatch`
- Ensure handler signature is `void name(ptr request, ptr response)`
- Pass handler without parentheses: `http.listen(port, handler)`

### Runtime Errors

**Error**: `Address already in use`
- Port is already taken
- Change port number or kill existing process: `pkill -f "./program"`

**No response from server**
- Check if server started (should print "Server running...")
- Verify port number matches curl command
- Check firewall settings

## Documentation

For complete documentation, see:
- `docs/http-complete-implementation.md` - Full implementation details
- `docs/http-complete-guide.md` - User guide
- `docs/http-function-pointers-fix.md` - Technical compiler details
