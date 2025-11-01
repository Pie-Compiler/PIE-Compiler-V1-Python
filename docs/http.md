# 🧩 PIE HTTP Module Design Specification

**Version:** 1.0.0
**Target Audience:** PIE language developers and system-level programmers
**Purpose:** Provide native HTTP client and server support within PIE using synchronous operations and C interop for performance and simplicity.

---

## 1. 🏗️ Architectural Overview

The HTTP module will be implemented as:

* A **standard library** written partly in **PIE**, backed by **C code**.
* Compiles to C and links with **libcurl** (for client) and **libmicrohttpd** (for server).
* Thread-based concurrency for server connections (using C’s `pthread` or PIE’s internal thread abstraction).

### Structure

```
/stdlib
  http.pi        → High-level PIE interface
/src/native
  pie_http.c     → C implementation (HTTP client + server)
  pie_http.h     → Header definitions
```

---

## 2. 🌐 HTTP Module Goals

| Capability        | Description                                     | PIE 1.0.0 Support          |
| ----------------- | ----------------------------------------------- | -------------------------- |
| HTTP Client       | GET, POST, PUT, DELETE, HEAD                    | ✅                          |
| HTTP Headers      | Set and retrieve request/response headers       | ✅                          |
| HTTP Server       | Listen on port, handle incoming requests        | ✅                          |
| Response Builder  | Set status codes, headers, and body             | ✅                          |
| HTTPS             | Support via libcurl and libmicrohttpd + OpenSSL | ✅                          |
| Chunked Transfer  | Optional for later versions                     | ⬜ Future                   |
| Asynchronous I/O  | Event loop, futures, coroutines                 | ❌ Deferred                 |
| Low-level sockets | TCP/UDP socket control for custom protocols     | ⬜ Planned for `net` module |

---

## 3. 🧠 Data Type Additions

To make HTTP expressive and practical, PIE may introduce **compound data types** and **type aliases**:

| Type                 | Description                                | Internal C Representation  |
| -------------------- | ------------------------------------------ | -------------------------- |
| `map<string,string>` | Key–value pairs (headers, query params)    | `struct pie_map`           |
| `bytearray`          | Binary-safe string type                    | `uint8_t *` + length       |
| `http_request`       | Incoming request struct                    | `struct pie_http_request`  |
| `http_response`      | Outgoing response struct                   | `struct pie_http_response` |
| `http_status`        | Enum of common codes (OK, NOT_FOUND, etc.) | `enum pie_http_status`     |

---

## 4. 📦 HTTP Client API (libcurl backend)

### Example Usage (PIE)

```pie
import http;

function main() {
    map<string,string> headers;
    headers["Content-Type"] = "application/json";

    string data = "{\"user\": \"ian\"}";

    string response = http.post("https://api.example.com/register", data, headers);

    output(response, string);
}
```

### Function Signatures

```pie
namespace http {
    function get(string url) -> string;
    function post(string url, string body, map<string,string> headers) -> string;
    function put(string url, string body, map<string,string> headers) -> string;
    function delete(string url) -> string;
}
```

### C Mapping Example

```c
char* pie_http_post(const char* url, const char* body, struct pie_map* headers);
```

---

## 5. 🛰️ HTTP Server API (libmicrohttpd backend)

### Example Usage (PIE)

```pie
import http;

function handle(req, res) {
    string path = req.path;
    if (path == "/hello") {
        res.status(200);
        res.header("Content-Type", "text/plain");
        res.send("Hello from PIE!");
    } else {
        res.status(404);
        res.send("Not found");
    }
}

function main() {
    http.listen(8080, handle);
}
```

### Function Signatures

```pie
namespace http {
    function listen(int port, function handler(http_request, http_response)) -> void;
}
```

### `http_request` Struct

```pie
struct http_request {
    string method;
    string path;
    string query;
    map<string,string> headers;
    string body;
}
```

### `http_response` Struct

```pie
struct http_response {
    function status(int code) -> void;
    function header(string key, string value) -> void;
    function send(string body) -> void;
}
```

### C Mapping Example

```c
struct pie_http_request {
    char* method;
    char* path;
    char* query;
    struct pie_map* headers;
    char* body;
};

struct pie_http_response {
    int status;
    struct pie_map* headers;
    char* body;
};

void pie_http_listen(int port, void (*handler)(struct pie_http_request*, struct pie_http_response*));
```

---

## 6. 🧵 Concurrency Model (Server-Side)

### Design:

* Each connection spawns a **new thread** using `pthread_create`.
* The handler function (from PIE) runs in that thread.
* The runtime ensures safe memory cleanup post-response.

### Advantages:

* Simplifies logic—no async runtime needed.
* Works naturally with PIE’s C-level execution model.
* Allows for PIE-native “thread pools” later.

### Example (PIE)

```pie
thread t = thread_start(http.listen, 8080, handler);
thread_join(t);
```

---

## 7. 🔐 Security and HTTPS

* **libcurl** handles SSL verification automatically.
* **libmicrohttpd** supports HTTPS if OpenSSL is linked.
* PIE config flags:

  ```bash
  piec main.pi --with-ssl
  ```
* PIE-level API:

  ```pie
  http.listen_ssl(443, "cert.pem", "key.pem", handler);
  ```

---

## 8. ⚙️ Compiler & Build Integration

During PIE → C compilation:

* The compiler adds include paths:

  ```c
  #include "pie_http.h"
  ```
* And links:

  ```bash
  -lcurl -lmicrohttpd -lpthread -lssl -lcrypto
  ```
* PIE modules like `http` are resolved in the stdlib directory.

---

## 9. 🧩 Future Extensions (Post-1.0)

| Feature               | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| **Async HTTP**        | Integrate with a future PIE async runtime using `libuv`.     |
| **WebSocket API**     | Event-based bidirectional sockets using `libwebsockets`.     |
| **Streaming APIs**    | Chunked upload/download.                                     |
| **Native JSON type**  | Structured JSON data type for easier HTTP response handling. |
| **Integrated router** | Express-like syntax: `http.route("/api", handler)`           |

---

