// Test HTTP server from C directly
#include "src/runtime/pie_http.h"
#include <stdio.h>

void test_handler(http_request_t request, http_response_t response) {
    const char* path = http_request_get_path(request);
    printf("Handling request to: %s\n", path);
    
    http_response_set_status(response, 200);
    http_response_set_header(response, "Content-Type", "text/plain");
    http_response_set_body(response, "Hello from C HTTP Server!");
}

int main() {
    printf("Starting HTTP server on port 8080...\n");
    printf("Visit http://localhost:8080 in your browser\n");
    printf("Press Enter to start (then Ctrl+C to stop)\n");
    getchar();
    
    http_listen(8080, test_handler);
    
    return 0;
}
