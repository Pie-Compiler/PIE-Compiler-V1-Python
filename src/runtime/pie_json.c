#include "pie_json.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jansson.h>

// ============================================================================
// JSON Object Creation and Parsing
// ============================================================================

pie_json_object_t pie_json_parse(const char* text) {
    if (!text) {
        return NULL;
    }
    
    json_error_t error;
    json_t* root = json_loads(text, 0, &error);
    
    if (!root) {
        fprintf(stderr, "JSON parse error on line %d: %s\n", error.line, error.text);
        return NULL;
    }
    
    return (pie_json_object_t)root;
}

char* pie_json_stringify(pie_json_object_t obj) {
    if (!obj) {
        return strdup("null");
    }
    
    json_t* json = (json_t*)obj;
    char* result = json_dumps(json, JSON_COMPACT);
    
    if (!result) {
        return strdup("null");
    }
    
    return result;
}

pie_json_object_t pie_json_create_object() {
    return (pie_json_object_t)json_object();
}

pie_json_array_t pie_json_create_array() {
    return (pie_json_array_t)json_array();
}

void pie_json_free(pie_json_object_t obj) {
    if (obj) {
        json_decref((json_t*)obj);
    }
}

// ============================================================================
// JSON Object Get Functions
// ============================================================================

const char* pie_json_get_string(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return "";
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value || !json_is_string(value)) {
        return "";
    }
    
    const char* str = json_string_value(value);
    return str ? str : "";
}

int pie_json_get_int(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return 0;
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value) {
        return 0;
    }
    
    if (json_is_integer(value)) {
        return (int)json_integer_value(value);
    }
    
    if (json_is_real(value)) {
        return (int)json_real_value(value);
    }
    
    return 0;
}

double pie_json_get_float(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return 0.0;
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value) {
        return 0.0;
    }
    
    if (json_is_real(value)) {
        return json_real_value(value);
    }
    
    if (json_is_integer(value)) {
        return (double)json_integer_value(value);
    }
    
    return 0.0;
}

int pie_json_get_bool(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return 0;
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value) {
        return 0;
    }
    
    if (json_is_true(value)) {
        return 1;
    }
    
    if (json_is_false(value)) {
        return 0;
    }
    
    // For non-boolean values, return truthy behavior
    if (json_is_integer(value)) {
        return json_integer_value(value) != 0;
    }
    
    return 0;
}

pie_json_object_t pie_json_get_object(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return NULL;
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value || !json_is_object(value)) {
        return NULL;
    }
    
    // Increase reference count since we're returning it
    json_incref(value);
    return (pie_json_object_t)value;
}

pie_json_array_t pie_json_get_array(pie_json_object_t obj, const char* key) {
    if (!obj || !key) {
        return NULL;
    }
    
    json_t* json = (json_t*)obj;
    json_t* value = json_object_get(json, key);
    
    if (!value || !json_is_array(value)) {
        return NULL;
    }
    
    // Increase reference count since we're returning it
    json_incref(value);
    return (pie_json_array_t)value;
}

// ============================================================================
// JSON Object Set Functions
// ============================================================================

void pie_json_set_string(pie_json_object_t obj, const char* key, const char* value) {
    if (!obj || !key || !value) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_object_set_new(json, key, json_string(value));
}

void pie_json_set_int(pie_json_object_t obj, const char* key, int value) {
    if (!obj || !key) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_object_set_new(json, key, json_integer(value));
}

void pie_json_set_float(pie_json_object_t obj, const char* key, double value) {
    if (!obj || !key) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_object_set_new(json, key, json_real(value));
}

void pie_json_set_bool(pie_json_object_t obj, const char* key, int value) {
    if (!obj || !key) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_object_set_new(json, key, value ? json_true() : json_false());
}

void pie_json_set_object(pie_json_object_t obj, const char* key, pie_json_object_t value) {
    if (!obj || !key || !value) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_t* val_json = (json_t*)value;
    
    // Increase reference count since json_object_set_new steals the reference
    json_incref(val_json);
    json_object_set_new(json, key, val_json);
}

void pie_json_set_array(pie_json_object_t obj, const char* key, pie_json_array_t value) {
    if (!obj || !key || !value) {
        return;
    }
    
    json_t* json = (json_t*)obj;
    json_t* val_json = (json_t*)value;
    
    // Increase reference count since json_object_set_new steals the reference
    json_incref(val_json);
    json_object_set_new(json, key, val_json);
}

// ============================================================================
// JSON Array Functions
// ============================================================================

int pie_json_array_len(pie_json_array_t arr) {
    if (!arr) {
        return 0;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return 0;
    }
    
    return (int)json_array_size(json);
}

const char* pie_json_array_get_string(pie_json_array_t arr, int index) {
    if (!arr || index < 0) {
        return "";
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return "";
    }
    
    json_t* value = json_array_get(json, (size_t)index);
    if (!value || !json_is_string(value)) {
        return "";
    }
    
    const char* str = json_string_value(value);
    return str ? str : "";
}

int pie_json_array_get_int(pie_json_array_t arr, int index) {
    if (!arr || index < 0) {
        return 0;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return 0;
    }
    
    json_t* value = json_array_get(json, (size_t)index);
    if (!value) {
        return 0;
    }
    
    if (json_is_integer(value)) {
        return (int)json_integer_value(value);
    }
    
    if (json_is_real(value)) {
        return (int)json_real_value(value);
    }
    
    return 0;
}

pie_json_object_t pie_json_array_get_object(pie_json_array_t arr, int index) {
    if (!arr || index < 0) {
        return NULL;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return NULL;
    }
    
    json_t* value = json_array_get(json, (size_t)index);
    if (!value || !json_is_object(value)) {
        return NULL;
    }
    
    // Increase reference count since we're returning it
    json_incref(value);
    return (pie_json_object_t)value;
}

void pie_json_array_push_string(pie_json_array_t arr, const char* value) {
    if (!arr || !value) {
        return;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return;
    }
    
    json_array_append_new(json, json_string(value));
}

void pie_json_array_push_int(pie_json_array_t arr, int value) {
    if (!arr) {
        return;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return;
    }
    
    json_array_append_new(json, json_integer(value));
}

void pie_json_array_push_object(pie_json_array_t arr, pie_json_object_t obj) {
    if (!arr || !obj) {
        return;
    }
    
    json_t* json = (json_t*)arr;
    if (!json_is_array(json)) {
        return;
    }
    
    // Increase reference count since the array will hold a reference
    json_incref((json_t*)obj);
    json_array_append(json, (json_t*)obj);
}
