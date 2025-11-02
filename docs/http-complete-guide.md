# PIE HTTP Module - Complete Implementation Guide

## Overview

The PIE HTTP module provides both **HTTP client** and **HTTP server** functionality, making PIE ideal for web services, REST APIs, and server applications.

### Key Features

✅ **HTTP Client with full response info**
- GET, POST, PUT, DELETE methods  
- Response status codes (200, 404, 500, etc.)
- Response headers access
- Custom request headers (coming soon)
- Built on libcurl for reliability

✅ **HTTP Server**
- Listen on any port
- Request routing and handling
- Set custom status codes and headers
- Built on libmicrohttpd for performance

✅ **Production Ready**
- Real HTTP/HTTPS support
- Follows redirects
- Error handling
- Thread-safe (via libmicrohttpd)

---

## Installation

Make sure you have the required system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install libcurl4-openssl-dev libmicrohttpd-dev

# macOS
brew install curl libmicrohttpd

# Arch Linux
sudo pacman -S curl libmicrohttpd
```

---

## HTTP Client Examples

### 1. Simple GET Request

```pie
import http;

string response = http.get("https://api.example.com/data");
output(response, string);
```

### 2. GET with Status Code Check

```pie
import http;

string response = http.get("https://httpbin.org/status/200");
int status_code = http.get_status_code();

if (status_code == 200) {
    output("Success!", string);
    output(response, string);
} else {
    output("Request failed", string);
    output(status_code, int);
}
```

### 3. Testing Different HTTP Status Codes

```pie
import http;

// Test 200 OK
string r1 = http.get("https://httpbin.org/status/200");
output("Status 200:", string);
output(http.get_status_code(), int);

// Test 404 Not Found
string r2 = http.get("https://httpbin.org/status/404");
output("Status 404:", string);
output(http.get_status_code(), int);

// Test 500 Server Error
string r3 = http.get("https://httpbin.org/status/500");
output("Status 500:", string);
output(http.get_status_code(), int);
```

### 4. Error Handling

```pie
import http;

string response = http.get("https://invalid-domain.example");
int status = http.get_status_code();

if (status == 0) {
    output("Network error or DNS failure", string);
} else if (status >= 400) {
    output("HTTP error occurred", string);
    output(status, int);
} else {
    output("Success!", string);
}
```

---

## HTTP Server Examples

### 1. Simple HTTP Server

```pie
import http;

func hello_handler(ptr request, ptr response) {
    string path = http.request_get_path(request);
    
    http.response_set_status(response, 200);
    http.response_set_header(response, "Content-Type", "text/plain");
    http.response_set_body(response, "Hello from PIE!");
}

output("Starting server on port 8080...", string);
http.listen(8080, hello_handler);
```

### 2. REST API Server

```pie
import http;

func api_handler(ptr request, ptr response) {
    string method = http.request_get_method(request);
    string path = http.request_get_path(request);
    
    output("Request:", string);
    output(method, string);
    output(path, string);
    
    // Route handling
    if (path == "/") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "text/html");
        http.response_set_body(response, "<h1>PIE API Server</h1>");
    } else if (path == "/api/status") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "application/json");
        http.response_set_body(response, "{\"status\": \"OK\", \"version\": \"1.0\"}");
    } else if (path == "/api/hello") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "application/json");
        http.response_set_body(response, "{\"message\": \"Hello from PIE!\"}");
    } else {
        http.response_set_status(response, 404);
        http.response_set_header(response, "Content-Type", "text/plain");
        http.response_set_body(response, "404 - Not Found");
    }
}

output("Starting API server on port 3000...", string);
output("Try: http://localhost:3000/", string);
output("Try: http://localhost:3000/api/status", string);
output("Try: http://localhost:3000/api/hello", string);

http.listen(3000, api_handler);
```

### 3. Echo Server

```pie
import http;

func echo_handler(ptr request, ptr response) {
    string method = http.request_get_method(request);
    string path = http.request_get_path(request);
    string body = http.request_get_body(request);
    
    // Echo back request information
    http.response_set_status(response, 200);
    http.response_set_header(response, "Content-Type", "text/plain");
    http.response_set_body(response, "Echo Server - Request received!");
    
    output("Echoed request:", string);
    output(path, string);
}

output("Echo server on port 9000", string);
http.listen(9000, echo_handler);
```

---

## API Reference

### Client Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `http.get()` | `string(string url)` | Perform HTTP GET request |
| `http.get_status_code()` | `int()` | Get status code from last request |
| `http.get_response_headers()` | `string()` | Get response headers from last request |
| `http.post()` | `string(string url, string body, ptr headers)` | Perform HTTP POST request |
| `http.put()` | `string(string url, string body, ptr headers)` | Perform HTTP PUT request |
| `http.delete()` | `string(string url)` | Perform HTTP DELETE request |

### Server Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `http.listen()` | `void(int port, ptr handler)` | Start HTTP server |
| `http.listen_ssl()` | `void(int port, string cert, string key, ptr handler)` | Start HTTPS server |

### Request Helper Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `http.request_get_method()` | `string(ptr request)` | Get HTTP method (GET, POST, etc.) |
| `http.request_get_path()` | `string(ptr request)` | Get request path/URL |
| `http.request_get_body()` | `string(ptr request)` | Get request body |
| `http.request_get_header()` | `string(ptr request, string name)` | Get specific header value |

### Response Helper Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `http.response_set_status()` | `void(ptr response, int code)` | Set response status code |
| `http.response_set_body()` | `void(ptr response, string body)` | Set response body |
| `http.response_set_header()` | `void(ptr response, string name, string value)` | Set response header |

---

## Common HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful request with no response body |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Server is down |

---

## Testing Your Server

Once your PIE HTTP server is running, test it with:

### Using curl:
```bash
# Test GET request
curl http://localhost:8080/

# Test with headers
curl -H "User-Agent: TestClient" http://localhost:8080/api/status

# Test POST request
curl -X POST -d '{"test": true}' http://localhost:8080/api/data
```

### Using a browser:
Simply navigate to `http://localhost:8080/` in your web browser.

### Using PIE client:
```pie
import http;

string response = http.get("http://localhost:8080/api/status");
output(response, string);
output(http.get_status_code(), int);
```

---

## Best Practices

1. **Always check status codes** - Don't assume requests succeed
2. **Handle errors gracefully** - Network failures happen
3. **Use appropriate status codes** - Return correct HTTP status in server responses
4. **Set Content-Type headers** - Helps clients parse responses correctly
5. **Log requests** - Use `output()` to track server activity
6. **Route requests properly** - Use path matching for clean API design

---

## Real-World Use Cases

### 1. Web Scraper
```pie
import http;

string html = http.get("https://example.com");
// Parse HTML and extract data
```

### 2. REST API Client
```pie
import http;

// GET data from API
string users = http.get("https://jsonplaceholder.typicode.com/users");
int status = http.get_status_code();

if (status == 200) {
    output("Got users:", string);
    output(users, string);
}
```

### 3. Microservice
Build a PIE microservice that responds to HTTP requests and processes data.

### 4. Webhook Receiver
Create a server that listens for webhooks from external services.

---

## Performance Notes

- **Client**: Uses libcurl with connection reuse
- **Server**: Uses libmicrohttpd with threading support
- **Concurrency**: Server can handle multiple simultaneous connections
- **Memory**: Responses are properly freed after use

---

## Troubleshooting

### Server won't start
- Check if port is already in use: `lsof -i :<port>`
- Use a different port number
- Make sure libmicrohttpd is installed

### Client requests fail
- Check internet connection
- Verify URL is correct and accessible
- Check status code for HTTP errors
- Look for `[ERROR]` prefix in response

### Headers not working
- Currently uses default headers
- Custom headers via Dictionary coming soon

---

## Coming Soon

🔜 Custom request headers via Dictionary  
🔜 WebSocket support  
🔜 HTTP/2 support  
🔜 Request/response middleware  
🔜 Connection pooling  
🔜 Async requests  

---

## Example: Complete Web Server

```pie
import http;

func router(ptr request, ptr response) {
    string method = http.request_get_method(request);
    string path = http.request_get_path(request);
    
    output("Request:", string);
    output(method, string);
    output(path, string);
    
    // Homepage
    if (path == "/") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "text/html");
        http.response_set_body(response, "<html><body><h1>PIE Web Server</h1><p>Welcome!</p></body></html>");
        return;
    }
    
    // API endpoints
    if (path == "/api/version") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "application/json");
        http.response_set_body(response, "{\"version\": \"1.0.0\", \"language\": \"PIE\"}");
        return;
    }
    
    if (path == "/api/time") {
        http.response_set_status(response, 200);
        http.response_set_header(response, "Content-Type", "application/json");
        http.response_set_body(response, "{\"timestamp\": 1234567890}");
        return;
    }
    
    // 404 for everything else
    http.response_set_status(response, 404);
    http.response_set_header(response, "Content-Type", "text/plain");
    http.response_set_body(response, "404 - Page Not Found");
}

output("=== PIE Web Server ===", string);
output("Starting on http://localhost:8000", string);
output("", string);
output("Available routes:", string);
output("  GET /", string);
output("  GET /api/version", string);
output("  GET /api/time", string);
output("", string);
output("Press Ctrl+C to stop", string);

http.listen(8000, router);
```

---

**PIE is now a powerful web-capable language!** 🎉🥧

Build REST APIs, microservices, web scrapers, and full web servers - all in PIE!
