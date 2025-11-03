#ifndef PIE_HTTP_H
#define PIE_HTTP_H

#include "dict_lib.h"

// HTTP Module - Client and Server Support
// This module provides HTTP client (via libcurl) and server (via libmicrohttpd) functionality

// Opaque types for HTTP structures
typedef void* http_request_t;
typedef void* http_response_t;

// Function pointer type for HTTP request handlers
typedef void (*http_handler_t)(http_request_t request, http_response_t response);

// ============================================================================
// HTTP Response Information Structure
// ============================================================================

typedef struct {
    char* body;
    int status_code;
    char* headers;  // Raw headers as string
} http_client_response_t;

// ============================================================================
// HTTP Client Functions
// ============================================================================

/**
 * Perform HTTP GET request
 * @param url The URL to request
 * @return Response body as string (caller must free)
 */
char* http_get(const char* url);

/**
 * Perform HTTP GET request with full response info
 * @param url The URL to request
 * @return Response structure with body, status, and headers (caller must free)
 */
http_client_response_t* http_get_full(const char* url);

/**
 * Perform HTTP GET request with custom headers
 * @param url The URL to request
 * @param headers Dictionary of HTTP headers (can be NULL)
 * @return Response body as string (caller must free)
 */
char* http_get_headers(const char* url, Dictionary* headers);

/**
 * Perform HTTP POST request
 * @param url The URL to request
 * @param body The request body
 * @param headers Dictionary of HTTP headers (can be NULL)
 * @return Response body as string (caller must free)
 */
char* http_post(const char* url, const char* body, Dictionary* headers);

/**
 * Perform HTTP POST request with full response info
 * @param url The URL to request
 * @param body The request body
 * @param headers Dictionary of HTTP headers (can be NULL)
 * @return Response structure with body, status, and headers (caller must free)
 */
http_client_response_t* http_post_full(const char* url, const char* body, Dictionary* headers);

/**
 * Perform HTTP PUT request
 * @param url The URL to request
 * @param body The request body
 * @param headers Dictionary of HTTP headers (can be NULL)
 * @return Response body as string (caller must free)
 */
char* http_put(const char* url, const char* body, Dictionary* headers);

/**
 * Perform HTTP DELETE request
 * @param url The URL to request
 * @return Response body as string (caller must free)
 */
char* http_delete(const char* url);

/**
 * Get HTTP status code from last request
 * NOTE: This is a simplified API. Use http_get_full() for better status handling
 * @return Last HTTP status code
 */
int http_get_status_code(void);

/**
 * Get HTTP response headers from last request as a Dictionary
 * NOTE: This is a simplified API. Use http_get_full() for better header handling
 * @return Dictionary with header names as keys and header values as strings (caller must free)
 */
Dictionary* http_get_response_headers(void);

/**
 * Free http_client_response_t structure
 * @param response Response structure to free
 */
void http_free_response(http_client_response_t* response);

// ============================================================================
// HTTP Server Functions
// ============================================================================

/**
 * Start HTTP server on specified port (blocking)
 * @param port Port number to listen on
 * @param handler Function to handle requests
 */
void http_listen(int port, http_handler_t handler);

/**
 * Start HTTPS server on specified port (blocking)
 * @param port Port number to listen on
 * @param cert_file Path to SSL certificate file
 * @param key_file Path to SSL private key file
 * @param handler Function to handle requests
 */
void http_listen_ssl(int port, const char* cert_file, const char* key_file, http_handler_t handler);

// ============================================================================
// HTTP Request/Response Helper Functions
// ============================================================================

/**
 * Get request method (GET, POST, etc.)
 * @param request HTTP request object
 * @return Method string (do not free)
 */
const char* http_request_get_method(http_request_t request);

/**
 * Get request path
 * @param request HTTP request object
 * @return Path string (do not free)
 */
const char* http_request_get_path(http_request_t request);

/**
 * Get request body
 * @param request HTTP request object
 * @return Body string (do not free)
 */
const char* http_request_get_body(http_request_t request);

/**
 * Get request header value
 * @param request HTTP request object
 * @param header_name Header name
 * @return Header value or NULL if not found (do not free)
 */
const char* http_request_get_header(http_request_t request, const char* header_name);

/**
 * Set response status code
 * @param response HTTP response object
 * @param status_code HTTP status code (e.g., 200, 404)
 */
void http_response_set_status(http_response_t response, int status_code);

/**
 * Set response body
 * @param response HTTP response object
 * @param body Response body content
 */
void http_response_set_body(http_response_t response, const char* body);

/**
 * Set response header
 * @param response HTTP response object
 * @param header_name Header name
 * @param header_value Header value
 */
void http_response_set_header(http_response_t response, const char* header_name, const char* header_value);

#endif // PIE_HTTP_H
