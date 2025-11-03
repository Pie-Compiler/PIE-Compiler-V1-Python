#ifndef PIE_JSON_H
#define PIE_JSON_H

// JSON Module - Parsing and Serialization
// This module provides JSON support via the Jansson library

// Opaque types - internally these are json_t* from Jansson
typedef void* pie_json_object_t;
typedef void* pie_json_array_t;

// ============================================================================
// JSON Object Creation and Parsing
// ============================================================================

/**
 * Parse JSON string into object
 * @param text JSON string to parse
 * @return JSON object (caller must eventually call pie_json_free on it)
 */
pie_json_object_t pie_json_parse(const char* text);

/**
 * Convert JSON object to string
 * @param obj JSON object
 * @return JSON string (caller must free)
 */
char* pie_json_stringify(pie_json_object_t obj);

/**
 * Create new empty JSON object
 * @return New JSON object (caller must eventually call pie_json_free on it)
 */
pie_json_object_t pie_json_create_object();

/**
 * Create new empty JSON array
 * @return New JSON array (caller must eventually call pie_json_free on it)
 */
pie_json_array_t pie_json_create_array();

/**
 * Free JSON object/array
 * @param obj JSON object or array to free
 */
void pie_json_free(pie_json_object_t obj);

// ============================================================================
// JSON Object Get Functions
// ============================================================================

/**
 * Get string value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return String value or NULL if not found (do not free - owned by JSON object)
 */
const char* pie_json_get_string(pie_json_object_t obj, const char* key);

/**
 * Get integer value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Integer value (returns 0 if not found or wrong type)
 */
int pie_json_get_int(pie_json_object_t obj, const char* key);

/**
 * Get float value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Float value (returns 0.0 if not found or wrong type)
 */
double pie_json_get_float(pie_json_object_t obj, const char* key);

/**
 * Get boolean value from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Boolean value (returns 0 if not found or wrong type)
 */
int pie_json_get_bool(pie_json_object_t obj, const char* key);

/**
 * Get nested object from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return Nested JSON object or NULL if not found
 */
pie_json_object_t pie_json_get_object(pie_json_object_t obj, const char* key);

/**
 * Get array from JSON object
 * @param obj JSON object
 * @param key Key name
 * @return JSON array or NULL if not found
 */
pie_json_array_t pie_json_get_array(pie_json_object_t obj, const char* key);

// ============================================================================
// JSON Object Set Functions
// ============================================================================

/**
 * Set string value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value String value
 */
void pie_json_set_string(pie_json_object_t obj, const char* key, const char* value);

/**
 * Set integer value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Integer value
 */
void pie_json_set_int(pie_json_object_t obj, const char* key, int value);

/**
 * Set float value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Float value
 */
void pie_json_set_float(pie_json_object_t obj, const char* key, double value);

/**
 * Set boolean value in JSON object
 * @param obj JSON object
 * @param key Key name
 * @param value Boolean value
 */
void pie_json_set_bool(pie_json_object_t obj, const char* key, int value);

// ============================================================================
// JSON Array Functions
// ============================================================================

/**
 * Get size of JSON array
 * @param arr JSON array
 * @return Array size (number of elements)
 */
int pie_json_array_len(pie_json_array_t arr);

/**
 * Get string from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return String value or NULL if not found (do not free)
 */
const char* pie_json_array_get_string(pie_json_array_t arr, int index);

/**
 * Get integer from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return Integer value (returns 0 if not found or wrong type)
 */
int pie_json_array_get_int(pie_json_array_t arr, int index);

/**
 * Get object from JSON array at index
 * @param arr JSON array
 * @param index Array index
 * @return JSON object or NULL if not found
 */
pie_json_object_t pie_json_array_get_object(pie_json_array_t arr, int index);

/**
 * Add string to JSON array
 * @param arr JSON array
 * @param value String value to add
 */
void pie_json_array_push_string(pie_json_array_t arr, const char* value);

/**
 * Add integer to JSON array
 * @param arr JSON array
 * @param value Integer value to add
 */
void pie_json_array_push_int(pie_json_array_t arr, int value);

/**
 * Add object to JSON array
 * @param arr JSON array
 * @param obj JSON object to add
 */
void pie_json_array_push_object(pie_json_array_t arr, pie_json_object_t obj);

#endif // PIE_JSON_H
