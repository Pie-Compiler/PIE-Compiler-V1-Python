#include "pie_http.h"
#include "dict_lib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <microhttpd.h>
#include <ctype.h>

// ============================================================================
// Internal Structures and Helpers
// ============================================================================

// Structure to hold response data from curl
typedef struct {
    char* data;
    size_t size;
} http_response_buffer_t;

// Structure to hold header data from curl
typedef struct {
    char* data;
    size_t size;
} http_header_buffer_t;

// Global variables to store last response info (for simplified API)
static int last_status_code = 0;
static char* last_response_headers = NULL;

// Server context structure
typedef struct {
    http_handler_t handler;
    struct MHD_Daemon* daemon;
} server_context_t;

// Connection-specific data for accumulating POST/PUT body
typedef struct {
    char* body_data;
    size_t body_size;
} connection_data_t;

// Server request/response structures
typedef struct {
    const char* method;
    const char* url;
    const char* path;
    const char* body;
    struct MHD_Connection* connection;
} server_request_t;

typedef struct {
    int status_code;
    char* body;
    struct MHD_Response* mhd_response;
    struct {
        char** names;
        char** values;
        size_t count;
        size_t capacity;
    } headers;
} server_response_t;

// Callback function for curl to write received data
static size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t realsize = size * nmemb;
    http_response_buffer_t* mem = (http_response_buffer_t*)userp;
    
    char* ptr = realloc(mem->data, mem->size + realsize + 1);
    if (!ptr) {
        fprintf(stderr, "Not enough memory for HTTP response\n");
        return 0;
    }
    
    mem->data = ptr;
    memcpy(&(mem->data[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->data[mem->size] = 0;  // Null-terminate
    
    return realsize;
}

// Callback function for curl to write received headers
static size_t header_callback(char* buffer, size_t size, size_t nitems, void* userdata) {
    size_t realsize = size * nitems;
    http_header_buffer_t* mem = (http_header_buffer_t*)userdata;
    
    char* ptr = realloc(mem->data, mem->size + realsize + 1);
    if (!ptr) {
        fprintf(stderr, "Not enough memory for HTTP headers\n");
        return 0;
    }
    
    mem->data = ptr;
    memcpy(&(mem->data[mem->size]), buffer, realsize);
    mem->size += realsize;
    mem->data[mem->size] = 0;  // Null-terminate
    
    return realsize;
}

// ============================================================================
// HTTP Client Functions - libcurl Implementation
// ============================================================================

char* http_get(const char* url) {
    http_client_response_t* full_response = http_get_full(url);
    if (!full_response) {
        return strdup("[ERROR] Failed to perform GET request");
    }
    
    char* body = full_response->body;
    full_response->body = NULL;  // Don't free the body
    http_free_response(full_response);
    
    return body;
}

http_client_response_t* http_get_full(const char* url) {
    CURL* curl;
    CURLcode res;
    http_response_buffer_t response;
    http_header_buffer_t headers;
    long response_code;
    
    response.data = malloc(1);
    response.size = 0;
    headers.data = malloc(1);
    headers.size = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (!curl) {
        free(response.data);
        free(headers.data);
        return NULL;
    }
    
    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    // Set callback function to receive data
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);
    
    // Set callback function to receive headers
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, (void*)&headers);
    
    // Follow redirects
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    
    // Set a user agent
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "PIE-HTTP/1.0");
    
    // Perform the request
    res = curl_easy_perform(curl);
    
    // Get response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    // Store in global vars for simplified API
    last_status_code = (int)response_code;
    if (last_response_headers) {
        free(last_response_headers);
    }
    last_response_headers = strdup(headers.data);
    
    // Check for errors
    if (res != CURLE_OK) {
        char* error_msg = malloc(256);
        snprintf(error_msg, 256, "[ERROR] HTTP GET failed: %s", curl_easy_strerror(res));
        free(response.data);
        free(headers.data);
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        
        http_client_response_t* err_response = malloc(sizeof(http_client_response_t));
        err_response->body = error_msg;
        err_response->status_code = 0;
        err_response->headers = strdup("");
        return err_response;
    }
    
    // Clean up curl
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
    // Create response structure
    http_client_response_t* full_resp = malloc(sizeof(http_client_response_t));
    full_resp->body = response.data;
    full_resp->status_code = (int)response_code;
    full_resp->headers = headers.data;
    
    return full_resp;
}

char* http_get_headers(const char* url, Dictionary* headers) {
    CURL* curl;
    CURLcode res;
    http_response_buffer_t response;
    http_header_buffer_t resp_headers;
    struct curl_slist* header_list = NULL;
    long response_code;
    
    response.data = malloc(1);
    response.size = 0;
    resp_headers.data = malloc(1);
    resp_headers.size = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (!curl) {
        free(response.data);
        free(resp_headers.data);
        return strdup("[ERROR] Failed to initialize CURL");
    }
    
    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    // Add custom headers from dictionary
    if (headers) {
        for (uint32_t i = 0; i < headers->capacity; i++) {
            DictNode* node = headers->buckets[i];
            while (node) {
                if (node->value && node->value->type == DICT_VALUE_STRING) {
                    // Format: "Header-Name: header-value"
                    size_t header_len = strlen(node->key) + strlen(node->value->as.string_val) + 3;
                    char* header_str = malloc(header_len);
                    snprintf(header_str, header_len, "%s: %s", node->key, node->value->as.string_val);
                    header_list = curl_slist_append(header_list, header_str);
                    free(header_str);
                }
                node = node->next;
            }
        }
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header_list);
    }
    
    // Set callbacks
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, (void*)&resp_headers);
    
    // Follow redirects
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    
    // Set user agent
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "PIE-HTTP/1.0");
    
    // Perform the request
    res = curl_easy_perform(curl);
    
    // Get response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    // Store in global vars
    last_status_code = (int)response_code;
    if (last_response_headers) {
        free(last_response_headers);
    }
    last_response_headers = strdup(resp_headers.data);
    
    // Check for errors
    if (res != CURLE_OK) {
        char* error_msg = malloc(256);
        snprintf(error_msg, 256, "[ERROR] HTTP GET failed: %s", curl_easy_strerror(res));
        free(response.data);
        free(resp_headers.data);
        if (header_list) curl_slist_free_all(header_list);
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        return error_msg;
    }
    
    // Clean up
    free(resp_headers.data);
    if (header_list) curl_slist_free_all(header_list);
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
    return response.data;
}

char* http_post(const char* url, const char* body, Dictionary* headers) {
    http_client_response_t* full_response = http_post_full(url, body, headers);
    if (!full_response) {
        return strdup("[ERROR] Failed to perform POST request");
    }
    
    char* response_body = full_response->body;
    full_response->body = NULL;  // Don't free the body
    http_free_response(full_response);
    
    return response_body;
}

http_client_response_t* http_post_full(const char* url, const char* body, Dictionary* headers) {
    CURL* curl;
    CURLcode res;
    http_response_buffer_t response;
    http_header_buffer_t resp_headers;
    struct curl_slist* header_list = NULL;
    long response_code;
    
    response.data = malloc(1);
    response.size = 0;
    resp_headers.data = malloc(1);
    resp_headers.size = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (!curl) {
        free(response.data);
        free(resp_headers.data);
        return NULL;
    }
    
    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    // Set POST data
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
    
    // Add custom headers from dictionary
    int has_content_type = 0;
    if (headers) {
        for (uint32_t i = 0; i < headers->capacity; i++) {
            DictNode* node = headers->buckets[i];
            while (node) {
                if (node->value && node->value->type == DICT_VALUE_STRING) {
                    // Format: "Header-Name: header-value"
                    size_t header_len = strlen(node->key) + strlen(node->value->as.string_val) + 3;
                    char* header_str = malloc(header_len);
                    snprintf(header_str, header_len, "%s: %s", node->key, node->value->as.string_val);
                    header_list = curl_slist_append(header_list, header_str);
                    
                    // Check if Content-Type was provided
                    if (strcasecmp(node->key, "Content-Type") == 0) {
                        has_content_type = 1;
                    }
                    
                    free(header_str);
                }
                node = node->next;
            }
        }
    }
    
    // Add default Content-Type if not provided
    if (!has_content_type) {
        header_list = curl_slist_append(header_list, "Content-Type: application/json");
    }
    
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header_list);
    
    // Set callbacks
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, (void*)&resp_headers);
    
    // Set user agent
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "PIE-HTTP/1.0");
    
    // Perform the request
    res = curl_easy_perform(curl);
    
    // Get response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    // Store in global vars
    last_status_code = (int)response_code;
    if (last_response_headers) {
        free(last_response_headers);
    }
    last_response_headers = strdup(resp_headers.data);
    
    // Check for errors
    if (res != CURLE_OK) {
        char* error_msg = malloc(256);
        snprintf(error_msg, 256, "[ERROR] HTTP POST failed: %s", curl_easy_strerror(res));
        free(response.data);
        free(resp_headers.data);
        curl_slist_free_all(header_list);
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        
        http_client_response_t* err_response = malloc(sizeof(http_client_response_t));
        err_response->body = error_msg;
        err_response->status_code = 0;
        err_response->headers = strdup("");
        return err_response;
    }
    
    // Clean up
    curl_slist_free_all(header_list);
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
    // Create response structure
    http_client_response_t* full_resp = malloc(sizeof(http_client_response_t));
    full_resp->body = response.data;
    full_resp->status_code = (int)response_code;
    full_resp->headers = resp_headers.data;
    
    return full_resp;
}

char* http_put(const char* url, const char* body, Dictionary* headers) {
    CURL* curl;
    CURLcode res;
    http_response_buffer_t response;
    http_header_buffer_t resp_headers;
    struct curl_slist* header_list = NULL;
    long response_code;
    
    response.data = malloc(1);
    response.size = 0;
    resp_headers.data = malloc(1);
    resp_headers.size = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (!curl) {
        free(response.data);
        free(resp_headers.data);
        return strdup("[ERROR] Failed to initialize CURL");
    }
    
    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    // Set custom request method to PUT
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
    
    // Set PUT data
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
    
    // Add custom headers from dictionary
    int has_content_type = 0;
    if (headers) {
        for (uint32_t i = 0; i < headers->capacity; i++) {
            DictNode* node = headers->buckets[i];
            while (node) {
                if (node->value && node->value->type == DICT_VALUE_STRING) {
                    // Format: "Header-Name: header-value"
                    size_t header_len = strlen(node->key) + strlen(node->value->as.string_val) + 3;
                    char* header_str = malloc(header_len);
                    snprintf(header_str, header_len, "%s: %s", node->key, node->value->as.string_val);
                    header_list = curl_slist_append(header_list, header_str);
                    
                    // Check if Content-Type was provided
                    if (strcasecmp(node->key, "Content-Type") == 0) {
                        has_content_type = 1;
                    }
                    
                    free(header_str);
                }
                node = node->next;
            }
        }
    }
    
    // Add default Content-Type if not provided
    if (!has_content_type) {
        header_list = curl_slist_append(header_list, "Content-Type: application/json");
    }
    
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header_list);
    
    // Set callbacks
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, (void*)&resp_headers);
    
    // Set user agent
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "PIE-HTTP/1.0");
    
    // Perform the request
    res = curl_easy_perform(curl);
    
    // Get response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    // Store in global vars
    last_status_code = (int)response_code;
    if (last_response_headers) {
        free(last_response_headers);
    }
    last_response_headers = strdup(resp_headers.data);
    
    // Check for errors
    if (res != CURLE_OK) {
        char* error_msg = malloc(256);
        snprintf(error_msg, 256, "[ERROR] HTTP PUT failed: %s", curl_easy_strerror(res));
        free(response.data);
        free(resp_headers.data);
        if (header_list) curl_slist_free_all(header_list);
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        return error_msg;
    }
    
    // Clean up
    free(resp_headers.data);
    if (header_list) curl_slist_free_all(header_list);
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
    return response.data;
}

char* http_delete(const char* url, Dictionary* headers) {
    CURL* curl;
    CURLcode res;
    http_response_buffer_t response;
    http_header_buffer_t resp_headers;
    struct curl_slist* header_list = NULL;
    long response_code;
    
    response.data = malloc(1);
    response.size = 0;
    resp_headers.data = malloc(1);
    resp_headers.size = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (!curl) {
        free(response.data);
        free(resp_headers.data);
        return strdup("[ERROR] Failed to initialize CURL");
    }
    
    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    // Set custom request method to DELETE
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
    
    // Add custom headers from dictionary
    if (headers) {
        for (uint32_t i = 0; i < headers->capacity; i++) {
            DictNode* node = headers->buckets[i];
            while (node) {
                if (node->value && node->value->type == DICT_VALUE_STRING) {
                    // Format: "Header-Name: header-value"
                    size_t header_len = strlen(node->key) + strlen(node->value->as.string_val) + 3;
                    char* header_str = malloc(header_len);
                    snprintf(header_str, header_len, "%s: %s", node->key, node->value->as.string_val);
                    header_list = curl_slist_append(header_list, header_str);
                    free(header_str);
                }
                node = node->next;
            }
        }
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header_list);
    }
    
    // Set callbacks
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, (void*)&resp_headers);
    
    // Set user agent
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "PIE-HTTP/1.0");
    
    // Perform the request
    res = curl_easy_perform(curl);
    
    // Get response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    // Store in global vars
    last_status_code = (int)response_code;
    if (last_response_headers) {
        free(last_response_headers);
    }
    last_response_headers = strdup(resp_headers.data);
    
    // Check for errors
    if (res != CURLE_OK) {
        char* error_msg = malloc(256);
        snprintf(error_msg, 256, "[ERROR] HTTP DELETE failed: %s", curl_easy_strerror(res));
        free(response.data);
        free(resp_headers.data);
        if (header_list) curl_slist_free_all(header_list);
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        return error_msg;
    }
    
    // Clean up
    free(resp_headers.data);
    if (header_list) curl_slist_free_all(header_list);
    curl_easy_cleanup(curl);
    curl_global_cleanup();
    
    return response.data;
}

int http_get_status_code(void) {
    return last_status_code;
}

Dictionary* http_get_response_headers(void) {
    Dictionary* headers_dict = dict_create();
    
    if (!last_response_headers || strlen(last_response_headers) == 0) {
        return headers_dict;
    }
    
    // Parse the raw headers string into key-value pairs
    // Headers are formatted as "Name: Value\r\n" or "Name: Value\n"
    char* headers_copy = strdup(last_response_headers);
    char* line = strtok(headers_copy, "\r\n");
    
    while (line != NULL) {
        // Skip empty lines and status line (starts with HTTP/)
        if (strlen(line) > 0 && strncmp(line, "HTTP/", 5) != 0) {
            // Find the colon separator
            char* colon = strchr(line, ':');
            if (colon != NULL) {
                // Extract header name (before colon)
                size_t name_len = colon - line;
                char* name = malloc(name_len + 1);
                strncpy(name, line, name_len);
                name[name_len] = '\0';
                
                // Trim trailing whitespace from name
                while (name_len > 0 && isspace(name[name_len - 1])) {
                    name[--name_len] = '\0';
                }
                
                // Extract header value (after colon and any leading whitespace)
                char* value = colon + 1;
                while (*value && isspace(*value)) {
                    value++;
                }
                
                // Trim trailing whitespace from value
                size_t value_len = strlen(value);
                char* value_copy = strdup(value);
                while (value_len > 0 && isspace(value_copy[value_len - 1])) {
                    value_copy[--value_len] = '\0';
                }
                
                // Add to dictionary
                DictValue* dict_val = dict_value_create_string(value_copy);
                dict_set(headers_dict, name, dict_val);
                
                free(name);
                free(value_copy);
            }
        }
        
        line = strtok(NULL, "\r\n");
    }
    
    free(headers_copy);
    return headers_dict;
}

void http_free_response(http_client_response_t* response) {
    if (response) {
        if (response->body) free(response->body);
        if (response->headers) free(response->headers);
        free(response);
    }
}

// ============================================================================
// HTTP Server Functions - libmicrohttpd Implementation
// ============================================================================

// Helper to create server response structure
static server_response_t* create_server_response(void) {
    server_response_t* resp = malloc(sizeof(server_response_t));
    resp->status_code = 200;  // Default OK
    resp->body = NULL;
    resp->mhd_response = NULL;
    resp->headers.names = malloc(sizeof(char*) * 10);
    resp->headers.values = malloc(sizeof(char*) * 10);
    resp->headers.count = 0;
    resp->headers.capacity = 10;
    return resp;
}

// Helper to free server response
static void free_server_response(server_response_t* resp) {
    if (resp) {
        if (resp->body) free(resp->body);
        for (size_t i = 0; i < resp->headers.count; i++) {
            free(resp->headers.names[i]);
            free(resp->headers.values[i]);
        }
        free(resp->headers.names);
        free(resp->headers.values);
        free(resp);
    }
}

// MHD callback for handling requests
static enum MHD_Result handle_request(void* cls,
                                     struct MHD_Connection* connection,
                                     const char* url,
                                     const char* method,
                                     const char* version,
                                     const char* upload_data,
                                     size_t* upload_data_size,
                                     void** con_cls) {
    server_context_t* ctx = (server_context_t*)cls;
    connection_data_t* con_data = (connection_data_t*)*con_cls;
    
    // First call - initialize connection data
    if (con_data == NULL) {
        con_data = malloc(sizeof(connection_data_t));
        con_data->body_data = NULL;
        con_data->body_size = 0;
        *con_cls = con_data;
        return MHD_YES;
    }
    
    // Accumulate POST/PUT body data
    if (*upload_data_size != 0) {
        // Allocate or expand buffer for body data
        char* new_body = realloc(con_data->body_data, con_data->body_size + *upload_data_size + 1);
        if (!new_body) {
            fprintf(stderr, "Failed to allocate memory for request body\n");
            *upload_data_size = 0;
            return MHD_NO;
        }
        
        con_data->body_data = new_body;
        memcpy(con_data->body_data + con_data->body_size, upload_data, *upload_data_size);
        con_data->body_size += *upload_data_size;
        con_data->body_data[con_data->body_size] = '\0';  // Null-terminate
        
        *upload_data_size = 0;  // Signal that we've processed this chunk
        return MHD_YES;
    }
    
    // Final call - all data received, process request
    // Create request structure
    server_request_t request;
    request.method = method;
    request.url = url;
    request.path = url;
    request.body = con_data->body_data ? con_data->body_data : "";
    request.connection = connection;
    
    // Create response structure
    server_response_t* response = create_server_response();
    
    // Call user handler
    if (ctx->handler) {
        ctx->handler((http_request_t)&request, (http_response_t)response);
    }
    
    // Default response if handler didn't set body
    if (response->body == NULL) {
        response->body = strdup("OK");
    }
    
    // Create MHD response
    struct MHD_Response* mhd_resp = MHD_create_response_from_buffer(
        strlen(response->body),
        (void*)response->body,
        MHD_RESPMEM_MUST_COPY
    );
    
    // Add custom headers
    for (size_t i = 0; i < response->headers.count; i++) {
        MHD_add_response_header(mhd_resp, 
                               response->headers.names[i],
                               response->headers.values[i]);
    }
    
    // Queue response
    enum MHD_Result ret = MHD_queue_response(connection, response->status_code, mhd_resp);
    
    // Cleanup
    MHD_destroy_response(mhd_resp);
    free_server_response(response);
    
    // Note: con_data cleanup is handled by request_completed_callback
    
    return ret;
}

// Callback for cleaning up connection data when request is completed/aborted
static void request_completed_callback(void* cls,
                                       struct MHD_Connection* connection,
                                       void** con_cls,
                                       enum MHD_RequestTerminationCode toe) {
    connection_data_t* con_data = (connection_data_t*)*con_cls;
    
    if (con_data != NULL) {
        if (con_data->body_data) {
            free(con_data->body_data);
        }
        free(con_data);
        *con_cls = NULL;
    }
}

void http_listen(int port, http_handler_t handler) {
    printf("[PIE HTTP Server] Starting on port %d...\n", port);
    
    server_context_t* ctx = malloc(sizeof(server_context_t));
    ctx->handler = handler;
    
    // Start the server
    ctx->daemon = MHD_start_daemon(
        MHD_USE_INTERNAL_POLLING_THREAD,
        port,
        NULL, NULL,
        &handle_request, ctx,
        MHD_OPTION_NOTIFY_COMPLETED, &request_completed_callback, NULL,
        MHD_OPTION_END
    );
    
    if (ctx->daemon == NULL) {
        fprintf(stderr, "[ERROR] Failed to start HTTP server on port %d\n", port);
        free(ctx);
        return;
    }
    
    printf("[PIE HTTP Server] Server running on http://localhost:%d\n", port);
    printf("[PIE HTTP Server] Press Ctrl+C to stop...\n");
    
    // Keep server running (in a real implementation, this would be non-blocking)
    // For now, we'll just pause
    getchar();
    
    // Cleanup
    MHD_stop_daemon(ctx->daemon);
    free(ctx);
    printf("[PIE HTTP Server] Server stopped.\n");
}

void http_listen_ssl(int port, const char* cert_file, const char* key_file, http_handler_t handler) {
    printf("[PIE HTTPS Server] Starting on port %d...\n", port);
    printf("[PIE HTTPS Server] Certificate: %s\n", cert_file);
    printf("[PIE HTTPS Server] Key: %s\n", key_file);
    
    // TODO: Implement SSL support
    // For now, fall back to regular HTTP
    printf("[WARNING] SSL not yet fully implemented, falling back to HTTP\n");
    http_listen(port, handler);
}

// ============================================================================
// Request/Response Helpers (for server handlers)
// ============================================================================

const char* http_request_get_method(http_request_t request) {
    server_request_t* req = (server_request_t*)request;
    return req->method;
}

const char* http_request_get_path(http_request_t request) {
    server_request_t* req = (server_request_t*)request;
    return req->path;
}

const char* http_request_get_body(http_request_t request) {
    server_request_t* req = (server_request_t*)request;
    return req->body ? req->body : "";
}

const char* http_request_get_header(http_request_t request, const char* header_name) {
    server_request_t* req = (server_request_t*)request;
    return MHD_lookup_connection_value(req->connection, MHD_HEADER_KIND, header_name);
}

// Helper callback for MHD_get_connection_values to collect headers into a dictionary
static enum MHD_Result header_iterator(void* cls, enum MHD_ValueKind kind,
                                       const char* key, const char* value) {
    Dictionary* headers_dict = (Dictionary*)cls;
    
    // Add header to dictionary
    DictValue* dict_val = dict_value_create_string(value);
    dict_set(headers_dict, key, dict_val);
    
    return MHD_YES;  // Continue iteration
}

Dictionary* http_request_get_headers(http_request_t request) {
    server_request_t* req = (server_request_t*)request;
    Dictionary* headers_dict = dict_create();
    
    // Iterate through all headers and add them to the dictionary
    MHD_get_connection_values(req->connection, MHD_HEADER_KIND, 
                              &header_iterator, headers_dict);
    
    return headers_dict;
}

void http_response_set_status(http_response_t response, int status_code) {
    server_response_t* resp = (server_response_t*)response;
    resp->status_code = status_code;
}

void http_response_set_body(http_response_t response, const char* body) {
    server_response_t* resp = (server_response_t*)response;
    if (resp->body) {
        free(resp->body);
    }
    resp->body = strdup(body);
}

void http_response_set_header(http_response_t response, const char* header_name, const char* header_value) {
    server_response_t* resp = (server_response_t*)response;
    
    // Expand arrays if needed
    if (resp->headers.count >= resp->headers.capacity) {
        resp->headers.capacity *= 2;
        resp->headers.names = realloc(resp->headers.names, sizeof(char*) * resp->headers.capacity);
        resp->headers.values = realloc(resp->headers.values, sizeof(char*) * resp->headers.capacity);
    }
    
    // Add header
    resp->headers.names[resp->headers.count] = strdup(header_name);
    resp->headers.values[resp->headers.count] = strdup(header_value);
    resp->headers.count++;
}
