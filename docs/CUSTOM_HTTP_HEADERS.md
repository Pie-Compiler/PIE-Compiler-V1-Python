# Custom HTTP Headers in PIE

## Overview
PIE now supports setting custom HTTP headers for GET, POST, and PUT requests using dictionaries. This allows you to add authentication tokens, custom headers, and override default headers.

## Supported Functions
- `http.get_headers(string url, dict headers)` - GET request with custom headers
- `http.post(string url, string body, dict headers)` - POST request with custom headers
- `http.post_full(string url, string body, dict headers)` - POST with full response info
- `http.put(string url, string body, dict headers)` - PUT request with custom headers
- `http.delete(string url, dict headers)` - DELETE request with custom headers

## Basic Usage

### Creating a Headers Dictionary
```pie
dict headers = {};
dict_set(headers, "Content-Type", "application/json");
dict_set(headers, "Authorization", "Bearer token123");
dict_set(headers, "X-Custom-Header", "custom-value");
```

### POST Request with Custom Headers
```pie
import http;
import json;

// Create JSON body
ptr body = json.create_object();
json.set_string(body, "name", "John Doe");
string json_body = json.stringify(body);

// Set custom headers
dict headers = {};
dict_set(headers, "Content-Type", "application/json");
dict_set(headers, "Authorization", "Bearer my-secret-token");
dict_set(headers, "X-API-Version", "v1");

// Make POST request
string response = http.post(
    "https://api.example.com/users",
    json_body,
    headers
);

output(response, string);
```

### GET Request with Custom Headers
```pie
import http;

// Set authentication headers
dict headers = {};
dict_set(headers, "Authorization", "Bearer my-access-token");
dict_set(headers, "Accept", "application/json");
dict_set(headers, "X-Request-ID", "req-12345");

// Make GET request
string response = http.get_headers(
    "https://api.example.com/data",
    headers
);

output(response, string);
```

### PUT Request with Custom Headers
```pie
import http;
import json;

// Create update data
ptr update = json.create_object();
json.set_string(update, "status", "updated");
string update_body = json.stringify(update);

// Set headers
dict headers = {};
dict_set(headers, "Content-Type", "application/json");
dict_set(headers, "If-Match", "etag-value");
dict_set(headers, "X-Updated-By", "PIE-App");

// Make PUT request
string response = http.put(
    "https://api.example.com/resource/123",
    update_body,
    headers
);

output(response, string);
```

### DELETE Request with Custom Headers
```pie
import http;

// Set authentication headers for DELETE
dict headers = {};
dict_set(headers, "Authorization", "Bearer my-access-token");
dict_set(headers, "X-Request-ID", "delete-req-001");

// Make DELETE request
string response = http.delete(
    "https://api.example.com/resource/123",
    headers
);

output(response, string);
```

## Common Headers

### Authentication Headers
```pie
// Bearer token authentication
dict_set(headers, "Authorization", "Bearer eyJhbGc...");

// Basic authentication
dict_set(headers, "Authorization", "Basic dXNlcjpwYXNz");

// API key authentication
dict_set(headers, "X-API-Key", "your-api-key");
```

### Content Type Headers
```pie
// JSON content
dict_set(headers, "Content-Type", "application/json");

// Form data
dict_set(headers, "Content-Type", "application/x-www-form-urlencoded");

// Plain text
dict_set(headers, "Content-Type", "text/plain");

// XML content
dict_set(headers, "Content-Type", "application/xml");
```

### Accept Headers
```pie
// Accept JSON response
dict_set(headers, "Accept", "application/json");

// Accept any content type
dict_set(headers, "Accept", "*/*");

// Accept specific types
dict_set(headers, "Accept", "application/json, text/html");
```

### Custom Application Headers
```pie
// Request tracking
dict_set(headers, "X-Request-ID", "unique-request-id");
dict_set(headers, "X-Correlation-ID", "correlation-id");

// API versioning
dict_set(headers, "X-API-Version", "v2");

// Client information
dict_set(headers, "X-Client-Version", "1.0.0");
dict_set(headers, "X-Device-Type", "mobile");
```

## Important Notes

1. **Header Names**: Header names are case-insensitive in HTTP but should be formatted using standard capitalization (e.g., "Content-Type" not "content-type").

2. **Automatic Headers**: PIE automatically adds:
   - `User-Agent: PIE-HTTP/1.0`
   - `Content-Type: application/json` (for POST/PUT if not provided)

3. **Overriding Default Headers**: You can override default headers by setting them explicitly in your dictionary:
   ```pie
   dict_set(headers, "Content-Type", "text/plain"); // Overrides default
   dict_set(headers, "User-Agent", "MyApp/1.0");    // Overrides default
   ```

4. **Empty Dictionary**: If you don't need custom headers, you can still pass an empty dictionary:
   ```pie
   dict headers = {};
   string response = http.post(url, body, headers);
   ```

## Implementation Details

The custom headers are implemented by:
1. Iterating through all key-value pairs in the headers dictionary
2. Converting each pair to the format `"Header-Name: header-value"`
3. Adding them to libcurl's header list
4. Sending them with the HTTP request

The implementation uses `strcasecmp()` to check for duplicate headers (case-insensitive comparison) to prevent duplicate `Content-Type` headers if explicitly provided.
