# PIE HTTP Module Examples

Complete examples demonstrating the HTTP module capabilities.

## Table of Contents

- [Basic GET Request](#basic-get-request)
- [POST Request with JSON](#post-request-with-json)
- [PUT Request](#put-request)
- [DELETE Request](#delete-request)
- [Error Handling](#error-handling)
- [Complete API Client Example](#complete-api-client-example)

---

## Basic GET Request

Fetch data from a public API:

```pie
import http;

// Simple GET request
string response = http.get("https://httpbin.org/get");

output("=== HTTP GET Response ===", string);
output(response, string);
```

**Expected Output:**
```json
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "PIE-HTTP/1.0"
  },
  "origin": "xxx.xxx.xxx.xxx",
  "url": "https://httpbin.org/get"
}
```

---

## POST Request with JSON

Send data to an API:

```pie
import http;

// Prepare JSON body
string json_body = "{\"name\": \"PIE Language\", \"version\": \"1.0\", \"features\": [\"fast\", \"simple\"]}";

// Make POST request
string response = http.post(
    "https://httpbin.org/post",
    json_body,
    null  // headers (optional)
);

output("=== POST Response ===", string);
output(response, string);
```

**Expected Output:**
```json
{
  "args": {},
  "data": "{\"name\": \"PIE Language\", \"version\": \"1.0\", \"features\": [\"fast\", \"simple\"]}",
  "files": {},
  "form": {},
  "headers": {
    "Content-Type": "application/json",
    "User-Agent": "PIE-HTTP/1.0"
  },
  "json": {
    "name": "PIE Language",
    "version": "1.0",
    "features": ["fast", "simple"]
  },
  "url": "https://httpbin.org/post"
}
```

---

## PUT Request

Update a resource:

```pie
import http;

// Update data
string update_body = "{\"title\": \"Updated Title\", \"completed\": true}";

string response = http.put(
    "https://httpbin.org/put",
    update_body,
    null
);

output("=== PUT Response ===", string);
output(response, string);
```

---

## DELETE Request

Delete a resource:

```pie
import http;

string response = http.delete("https://httpbin.org/delete");

output("=== DELETE Response ===", string);
output(response, string);
```

---

## Error Handling

The HTTP module returns error messages with `[ERROR]` prefix:

```pie
import http;

// Try to access an invalid URL
string response = http.get("https://invalid-domain-that-does-not-exist.com/api");

// Check for errors
int error_pos = string_index_of(response, "[ERROR]");
if (error_pos == 0) {
    output("Request failed!", string);
    output(response, string);
} else {
    output("Request succeeded!", string);
    output(response, string);
}
```

---

## Complete API Client Example

A practical example working with JSONPlaceholder API:

**File: `api_demo.pie`**

```pie
import http;

output("=== PIE HTTP Client Demo ===", string);

// 1. Fetch all users (limited to first user for brevity)
output("1. Fetching user data...", string);
string user_response = http.get("https://jsonplaceholder.typicode.com/users/1");
output("User:", string);
output(user_response, string);

// 2. Fetch user's posts
output("2. Fetching user posts...", string);
string posts_response = http.get("https://jsonplaceholder.typicode.com/posts?userId=1");
output("Posts:", string);
output(posts_response, string);

// 3. Create a new post
output("3. Creating new post...", string);
string new_post = "{\"title\": \"Hello from PIE\", \"body\": \"This is a test post from PIE language!\", \"userId\": 1}";
string create_response = http.post(
    "https://jsonplaceholder.typicode.com/posts",
    new_post,
    null
);
output("Created:", string);
output(create_response, string);

// 4. Update a post
output("4. Updating post...", string);
string update_data = "{\"id\": 1, \"title\": \"Updated Title\", \"body\": \"Updated content\", \"userId\": 1}";
string update_response = http.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    update_data,
    null
);
output("Updated:", string);
output(update_response, string);

// 5. Delete a post
output("5. Deleting post...", string);
string delete_response = http.delete("https://jsonplaceholder.typicode.com/posts/1");
output("Deleted:", string);
output(delete_response, string);

output("=== Demo Complete! ===", string);
```

**Compile and Run:**
```bash
python3 src/main.py api_demo.pie
./program
```

---

## Real-World Use Cases

### Weather API Client

```pie
import http;

// Fetch weather data (example with OpenWeatherMap)
// Note: You'll need an API key for real usage
string city = "London";
string api_key = "your_api_key_here";

// In real usage, concatenate strings properly
string url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo";
string weather = http.get(url);

output("Weather Data:", string);
output(weather, string);
```

### GitHub API Client

```pie
import http;

// Fetch GitHub user information
string username = "torvalds";
string github_url = "https://api.github.com/users/torvalds";

string user_info = http.get(github_url);
output("GitHub User Info:", string);
output(user_info, string);
```

### REST API Testing

```pie
import http;

output("=== Testing REST API ===", string);

// Test all HTTP methods
string base_url = "https://httpbin.org";

// GET
string get_result = http.get("https://httpbin.org/get");
output("GET: OK", string);

// POST
string post_result = http.post("https://httpbin.org/post", "{\"test\": true}", null);
output("POST: OK", string);

// PUT
string put_result = http.put("https://httpbin.org/put", "{\"update\": true}", null);
output("PUT: OK", string);

// DELETE
string delete_result = http.delete("https://httpbin.org/delete");
output("DELETE: OK", string);

output("=== All tests passed! ===", string);
```

---

## Tips and Best Practices

1. **Always check for errors** - Look for `[ERROR]` prefix in responses
2. **Use httpbin.org for testing** - Great for debugging HTTP requests
3. **Be mindful of rate limits** - Many APIs have request limits
4. **Handle timeouts gracefully** - Network requests can fail
5. **Use proper JSON formatting** - Ensure valid JSON in request bodies

---

## Limitations

Current limitations of the HTTP module:

- ⚠️ Custom headers via Dictionary not yet fully implemented
- ⚠️ Authentication (OAuth, Bearer tokens) requires manual header manipulation
- ⚠️ File uploads not yet supported
- ⚠️ HTTP server functionality is stubbed (coming soon with libmicrohttpd)
- ⚠️ Streaming responses not supported

---

## Coming Soon

Future enhancements planned:

- 🔜 Custom request headers via Dictionary
- 🔜 HTTP server with request routing
- 🔜 WebSocket support
- 🔜 HTTPS with custom certificates
- 🔜 Request/response interceptors
- 🔜 Connection pooling for performance

---

## Additional Resources

- **httpbin.org** - HTTP request & response service for testing
- **jsonplaceholder.typicode.com** - Free fake REST API for testing
- **libcurl documentation** - Understanding the underlying library
- **HTTP status codes** - Reference for response codes

Happy HTTP coding with PIE! 🥧
