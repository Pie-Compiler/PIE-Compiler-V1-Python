#ifndef D_ARRAY_H
#define D_ARRAY_H

#include <stddef.h>

// Generic Dynamic Array Structure
typedef struct {
    void* data;          // Pointer to the data
    size_t size;         // Current number of elements
    size_t capacity;     // Total capacity of the array
    size_t element_size; // Size of each element
} DArray;

// Generic DArray Functions
DArray* d_array_create(size_t element_size, size_t initial_capacity);
void d_array_free(DArray* arr);

void d_array_push(DArray* arr, const void* value);
void d_array_pop(DArray* arr, void* out_value);

void d_array_get(DArray* arr, int index, void* out_value);
void d_array_set(DArray* arr, int index, const void* value);

int d_array_size(DArray* arr);

// Type-specific comparison function pointer
typedef int (*compare_func)(const void*, const void*);

int d_array_contains(DArray* arr, const void* value, compare_func cmp);
int d_array_indexof(DArray* arr, const void* value, compare_func cmp);

DArray* d_array_concat(const DArray* arr1, const DArray* arr2);

// Type-specific helper functions (to be called from the compiler)
double d_array_avg_int(DArray* arr);
double d_array_avg_float(DArray* arr);

// Functions for printing (useful for debugging)
void print_int_array(DArray* arr);
void print_string_array(DArray* arr);
void print_float_array(DArray* arr);
void print_char_array(DArray* arr);

#endif // D_ARRAY_H
