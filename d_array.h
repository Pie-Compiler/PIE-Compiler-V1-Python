#ifndef D_ARRAY_H
#define D_ARRAY_H

#include <stddef.h>

typedef struct {
    int* data;
    size_t size;
    size_t capacity;
} DArrayInt;

DArrayInt* d_array_int_create();
void d_array_int_append(DArrayInt* arr, int value);
int d_array_int_get(DArrayInt* arr, int index);
void d_array_int_set(DArrayInt* arr, int index, int value);
int d_array_int_size(DArrayInt* arr);
void d_array_int_free(DArrayInt* arr);

typedef struct {
    char** data;
    size_t size;
    size_t capacity;
} DArrayString;

DArrayString* d_array_string_create();
void d_array_string_append(DArrayString* arr, const char* value);
char* d_array_string_get(DArrayString* arr, int index);
void d_array_string_set(DArrayString* arr, int index, const char* value);
int d_array_string_size(DArrayString* arr);
void d_array_string_free(DArrayString* arr);

#endif // D_ARRAY_H
