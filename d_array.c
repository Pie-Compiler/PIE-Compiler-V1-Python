#include "d_array.h"
#include <stdlib.h>
#include <string.h>

DArrayInt* d_array_int_create() {
    DArrayInt* arr = (DArrayInt*)malloc(sizeof(DArrayInt));
    arr->data = (int*)malloc(sizeof(int) * 4); // Initial capacity of 4
    arr->size = 0;
    arr->capacity = 4;
    return arr;
}

void d_array_int_append(DArrayInt* arr, int value) {
    if (arr->size >= arr->capacity) {
        arr->capacity *= 2;
        arr->data = (int*)realloc(arr->data, sizeof(int) * arr->capacity);
    }
    arr->data[arr->size++] = value;
}

int d_array_int_get(DArrayInt* arr, int index) {
    if (index >= arr->size) {
        // Error handling? For now, return 0
        return 0;
    }
    return arr->data[index];
}

void d_array_int_set(DArrayInt* arr, int index, int value) {
    if (index < arr->size) {
        arr->data[index] = value;
    }
}

int d_array_int_size(DArrayInt* arr) {
    return arr->size;
}

void d_array_int_free(DArrayInt* arr) {
    if (arr) {
        free(arr->data);
        free(arr);
    }
}

DArrayString* d_array_string_create() {
    DArrayString* arr = (DArrayString*)malloc(sizeof(DArrayString));
    arr->data = (char**)malloc(sizeof(char*) * 4);
    arr->size = 0;
    arr->capacity = 4;
    return arr;
}

void d_array_string_append(DArrayString* arr, const char* value) {
    if (arr->size >= arr->capacity) {
        arr->capacity *= 2;
        arr->data = (char**)realloc(arr->data, sizeof(char*) * arr->capacity);
    }
    arr->data[arr->size++] = strdup(value);
}

char* d_array_string_get(DArrayString* arr, int index) {
    if (index >= arr->size) {
        return NULL;
    }
    return arr->data[index];
}

void d_array_string_set(DArrayString* arr, int index, const char* value) {
    if (index < arr->size) {
        free(arr->data[index]);
        arr->data[index] = strdup(value);
    }
}

int d_array_string_size(DArrayString* arr) {
    return arr->size;
}

void d_array_string_free(DArrayString* arr) {
    if (arr) {
        for (size_t i = 0; i < arr->size; i++) {
            free(arr->data[i]);
        }
        free(arr->data);
        free(arr);
    }
}
