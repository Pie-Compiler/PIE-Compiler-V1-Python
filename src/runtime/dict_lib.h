#ifndef DICT_LIB_H
#define DICT_LIB_H

#include <stdint.h>

// Type tags for dictionary values
typedef enum {
    DICT_VALUE_INT,
    DICT_VALUE_FLOAT,
    DICT_VALUE_STRING,
    DICT_VALUE_NULL
} DictValueType;

// A union to hold different value types
typedef struct {
    DictValueType type;
    union {
        int32_t int_val;
        double float_val;
        char* string_val;
    } as;
} DictValue;

// A key-value pair
typedef struct DictNode {
    char* key;
    DictValue* value;
    struct DictNode* next;
} DictNode;

// The dictionary itself (a hash table)
typedef struct {
    DictNode** buckets;
    uint32_t capacity;
    uint32_t size;
} Dictionary;

// Public API
Dictionary* dict_create();
void dict_set(Dictionary* dict, const char* key, DictValue* value);
DictValue* dict_get(Dictionary* dict, const char* key);
int32_t dict_get_int(Dictionary* dict, const char* key);
double dict_get_float(Dictionary* dict, const char* key);
char* dict_get_string(Dictionary* dict, const char* key);
int32_t dict_has_key(Dictionary* dict, const char* key);  // New function to check key existence
void dict_delete(Dictionary* dict, const char* key);
void dict_free(Dictionary* dict);

// Helper functions for creating values
DictValue* dict_value_create_int(int32_t value);
DictValue* dict_value_create_float(double value);
DictValue* dict_value_create_string(const char* value);
DictValue* dict_value_create_null();

// PIE language wrapper functions (as documented)
DictValue* new_int(int32_t value);
DictValue* new_float(double value);
DictValue* new_string(const char* value);
int32_t dict_key_exists(Dictionary* dict, const char* key);  // Check if key exists

// Variable validation functions
int32_t is_variable_defined(void* variable);
int32_t is_variable_null(void* variable);

// String utility functions
int32_t string_contains(const char* haystack, const char* needle);
int32_t string_starts_with(const char* str, const char* prefix);
int32_t string_ends_with(const char* str, const char* suffix);
int32_t string_is_empty(const char* str);

#endif // DICT_LIB_H
