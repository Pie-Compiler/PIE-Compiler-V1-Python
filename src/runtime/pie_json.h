#ifndef PIE_JSON_H
#define PIE_JSON_H

// JSON Module - Parsing and Serialization
// This module provides JSON support via the Jansson library

// Opaque types - internally these are json_t* from Jansson
typedef void* json_object_t;
typedef void* json_array_t;

// ============================================================================
// JSON Object Creation and Parsing
// ============================================================================

/**
 * Parse JSON string into object
 * @param text JSON string to parse
 * @return JSON object (caller must eventually call json_free on it)
 */
json_object_t json_parse(const char* text);

/**
 * Convert JSON object to string
 * @param obj JSON object
 * @return JSON string (caller must free)
 */
char* json_stringify(json_object_t obj);

/**
 * Create new empty JSON object
 * @return New JSON object (caller must eventually call json_free on it)
 */
json_object_t json_create_object();

/**
 * Create new empty JSON array
 * @return New JSON array (caller must eventually call json_free on it)
 */
json_array_t json_create_array();

/**
 * Free JSON object/array
 * @param obj JSON object or array to free
 */
void json_free(json_object_t obj);

// ============================================================================
// JSON Object Get Functions
// ============================================================================

/**
 * Get string value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return String value or NULL if not found (do not free - owned by JSON object)
 */
const char* json_get_string(json_object_t obj, const char* key);

/**
 * Get integer value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Integer value (returns 0 if not found or wrong type)
 */
int json_get_int(json_object_t obj, const char* key);

/**
 * Get float value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Float value (returns 0.0 if not found or wrong type)
 */
double json_get_float(json_object_t obj, const char* key);

/**
 * Get boolean value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Boolean value (returns 0 if not found or wrong type)
 */
int json_get_bool(json_object_t obj, const char* key);

/**
 * Get nested object from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Nested JSON object or NULL if not found
 */
json_object_t json_get_object(json_object_t obj, const char* key);

/**
 * Get array from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return JSON array or NULL if not found
 */
json_array_t json_get_array(json_object_t obj, const char* key);

// ============================================================================
// JSON Object Set Functions
// ============================================================================

/**
 * Set string value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value String value
 */
void json_set_string(json_object_t obj, const char* key, const char* value);

/**
 * Set integer value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Integer value
 */
void json_set_int(json_object_t obj, const char* key, int value);

/**
 * Set float value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Float value
 */
void json_set_float(json_object_t obj, const char* key, double value);

/**
 * Set boolean value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Boolean value
 */
void json_set_bool(json_object_t obj, const char* key, int value);

// ============================================================================
// JSON Array Functions
// ============================================================================

/**
 * Get size of JSON array
 * @param arr JSON array
 * @return Array size (number of elements)
 */
int json_array_size(json_array_t arr);

/**
 * Get string from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return String value or NULL if not found (do not free)
 */
const char* json_array_get_string(json_array_t arr, int index);

/**
 * Get integer from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return Integer value (returns 0 if not found or wrong type)
 */
int json_array_get_int(json_array_t arr, int index);

/**
 * Get object from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return JSON object or NULL if not found
 */
json_object_t json_array_get_object(json_array_t arr, int index);

/**
 * Add string to JSON array
 * @param arr JSON array
 * @param value String value to add
 */
void json_array_push_string(json_array_t arr, const char* value);

/**
 * Add integer to JSON array
 * @param arr JSON array
 * @param value Integer value to add
 */
void json_array_push_int(json_array_t arr, int value);

/**
 * Add object to JSON array
 * @param arr JSON array
 * @param obj JSON object to add
 */
void json_array_push_object(json_array_t arr, json_object_t obj);

#endif // PIE_JSON_H
