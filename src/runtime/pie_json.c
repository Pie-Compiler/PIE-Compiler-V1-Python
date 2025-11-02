#include "pie_json.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ============================================================================
// STUB IMPLEMENTATIONS - Replace with real Jansson library code
// ============================================================================

// Stub structure for JSON objects (in real implementation, this would be json_t*)
typedef struct {
    int is_array;
    int stub_marker;
} stub_json_t;

json_object_t json_parse(const char* text) {
    // STUB: Return a dummy object
    stub_json_t* obj = malloc(sizeof(stub_json_t));
    obj->is_array = 0;
    obj->stub_marker = 0xDEADBEEF;
    printf("[STUB] Parsing JSON: %s\n", text);
    return obj;
}

char* json_stringify(json_object_t obj) {
    // STUB: Return placeholder JSON string
    char* result = malloc(256);
    strcpy(result, "{\"stub\": \"This is a stub JSON response\"}");
    return result;
}

json_object_t json_create_object() {
    // STUB: Return a dummy object
    stub_json_t* obj = malloc(sizeof(stub_json_t));
    obj->is_array = 0;
    obj->stub_marker = 0xDEADBEEF;
    return obj;
}

json_array_t json_create_array() {
    // STUB: Return a dummy array
    stub_json_t* arr = malloc(sizeof(stub_json_t));
    arr->is_array = 1;
    arr->stub_marker = 0xDEADBEEF;
    return arr;
}

void json_free(json_object_t obj) {
    // STUB: Free the dummy object
    if (obj) {
        free(obj);
    }
}

// ============================================================================
// Get Functions (Stubs)
// ============================================================================

const char* json_get_string(json_object_t obj, const char* key) {
    return "[STUB] string value";
}

int json_get_int(json_object_t obj, const char* key) {
    return 42; // STUB value
}

double json_get_float(json_object_t obj, const char* key) {
    return 3.14; // STUB value
}

int json_get_bool(json_object_t obj, const char* key) {
    return 1; // STUB: always true
}

json_object_t json_get_object(json_object_t obj, const char* key) {
    return json_create_object(); // STUB: return new empty object
}

json_array_t json_get_array(json_object_t obj, const char* key) {
    return json_create_array(); // STUB: return new empty array
}

// ============================================================================
// Set Functions (Stubs)
// ============================================================================

void json_set_string(json_object_t obj, const char* key, const char* value) {
    // STUB: Do nothing
    printf("[STUB] Setting %s = \"%s\"\n", key, value);
}

void json_set_int(json_object_t obj, const char* key, int value) {
    // STUB: Do nothing
    printf("[STUB] Setting %s = %d\n", key, value);
}

void json_set_float(json_object_t obj, const char* key, double value) {
    // STUB: Do nothing
    printf("[STUB] Setting %s = %f\n", key, value);
}

void json_set_bool(json_object_t obj, const char* key, int value) {
    // STUB: Do nothing
    printf("[STUB] Setting %s = %s\n", key, value ? "true" : "false");
}

// ============================================================================
// Array Functions (Stubs)
// ============================================================================

int json_array_size(json_array_t arr) {
    return 0; // STUB: empty array
}

const char* json_array_get_string(json_array_t arr, int index) {
    return "[STUB] array string";
}

int json_array_get_int(json_array_t arr, int index) {
    return 42; // STUB value
}

json_object_t json_array_get_object(json_array_t arr, int index) {
    return json_create_object(); // STUB: return new empty object
}

void json_array_push_string(json_array_t arr, const char* value) {
    // STUB: Do nothing
    printf("[STUB] Pushing string to array: \"%s\"\n", value);
}

void json_array_push_int(json_array_t arr, int value) {
    // STUB: Do nothing
    printf("[STUB] Pushing int to array: %d\n", value);
}

void json_array_push_object(json_array_t arr, json_object_t obj) {
    // STUB: Do nothing
    printf("[STUB] Pushing object to array\n");
}
