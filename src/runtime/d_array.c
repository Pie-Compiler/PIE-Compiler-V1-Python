#include "d_array.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// --- Core Generic Functions ---

DArray* d_array_create(size_t element_size, size_t initial_capacity) {
    DArray* arr = (DArray*)malloc(sizeof(DArray));
    if (!arr) return NULL;
    arr->element_size = element_size;
    arr->size = 0;
    arr->capacity = (initial_capacity > 0) ? initial_capacity : 4; // Default capacity 4
    arr->data = malloc(arr->capacity * arr->element_size);
    if (!arr->data) {
        free(arr);
        return NULL;
    }
    return arr;
}

void d_array_free(DArray* arr) {
    if (arr) {
        // If it's an array of strings, the strings themselves must be freed
        if (arr->element_size == sizeof(char*)) {
            for (size_t i = 0; i < arr->size; i++) {
                char* str = *(char**)((char*)arr->data + i * arr->element_size);
                if (str) {
                    free(str);
                }
            }
        }
        free(arr->data);
        free(arr);
    }
}

static void d_array_resize(DArray* arr) {
    if (arr->size >= arr->capacity) {
        arr->capacity *= 2;
        void* new_data = realloc(arr->data, arr->capacity * arr->element_size);
        if (!new_data) {
            // Handle realloc failure, though it's rare on modern systems
            // For simplicity, we'll exit. A real-world app might do more.
            fprintf(stderr, "Failed to resize dynamic array.\n");
            exit(EXIT_FAILURE);
        }
        arr->data = new_data;
    }
}

void d_array_push(DArray* arr, const void* value) {
    d_array_resize(arr);
    void* dest = (char*)arr->data + arr->size * arr->element_size;
    memcpy(dest, value, arr->element_size);
    arr->size++;
}

void d_array_pop(DArray* arr, void* out_value) {
    if (arr->size == 0) return;
    arr->size--;
    void* src = (char*)arr->data + arr->size * arr->element_size;
    if (out_value) {
        memcpy(out_value, src, arr->element_size);
    }
}

void d_array_get(DArray* arr, int index, void* out_value) {
    if (index < 0 || index >= arr->size) return;
    void* src = (char*)arr->data + index * arr->element_size;
    memcpy(out_value, src, arr->element_size);
}

void d_array_set(DArray* arr, int index, const void* value) {
    if (index < 0) return;

    // Grow array if index is out of bounds
    while (index >= arr->capacity) {
        arr->capacity *= 2;
    }
    void* new_data = realloc(arr->data, arr->capacity * arr->element_size);
    if (!new_data) {
        fprintf(stderr, "Failed to resize dynamic array for set.\n");
        exit(EXIT_FAILURE);
    }
    arr->data = new_data;

    // Zero out new memory if we expanded the size
    if (index >= arr->size) {
        void* start = (char*)arr->data + arr->size * arr->element_size;
        size_t count = index - arr->size;
        memset(start, 0, count * arr->element_size);
        arr->size = index + 1;
    }

    void* dest = (char*)arr->data + index * arr->element_size;
    memcpy(dest, value, arr->element_size);
}


int d_array_size(DArray* arr) {
    return arr ? arr->size : 0;
}

DArray* d_array_concat(const DArray* arr1, const DArray* arr2) {
    if (!arr1 || !arr2 || arr1->element_size != arr2->element_size) {
        return NULL;
    }
    DArray* new_arr = d_array_create(arr1->element_size, arr1->size + arr2->size);
    if (!new_arr) return NULL;

    // Copy from first array
    memcpy(new_arr->data, arr1->data, arr1->size * arr1->element_size);

    // Copy from second array
    void* dest_start = (char*)new_arr->data + arr1->size * arr1->element_size;
    memcpy(dest_start, arr2->data, arr2->size * arr2->element_size);

    new_arr->size = arr1->size + arr2->size;
    return new_arr;
}


// --- Comparison and Searching ---

// Pre-defined comparison functions for basic types
int compare_int(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int compare_float(const void* a, const void* b) {
    double diff = *(double*)a - *(double*)b;
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
}

int compare_char(const void* a, const void* b) {
    return (*(char*)a - *(char*)b);
}

int compare_string(const void* a, const void* b) {
    const char* s1 = *(const char**)a;
    const char* s2 = *(const char**)b;
    return strcmp(s1, s2);
}

int d_array_contains(DArray* arr, const void* value, compare_func cmp) {
    for (size_t i = 0; i < arr->size; i++) {
        void* element = (char*)arr->data + i * arr->element_size;
        if (cmp(element, value) == 0) {
            return 1; // true
        }
    }
    return 0; // false
}

int d_array_indexof(DArray* arr, const void* value, compare_func cmp) {
    for (size_t i = 0; i < arr->size; i++) {
        void* element = (char*)arr->data + i * arr->element_size;
        if (cmp(element, value) == 0) {
            return i;
        }
    }
    return -1;
}


// --- Type-Specific Helper Functions ---

double d_array_avg_int(DArray* arr) {
    if (!arr || arr->size == 0 || arr->element_size != sizeof(int)) {
        return 0.0;
    }
    long long sum = 0;
    for (size_t i = 0; i < arr->size; i++) {
        sum += ((int*)arr->data)[i];
    }
    return (double)sum / arr->size;
}

double d_array_avg_float(DArray* arr) {
    if (!arr || arr->size == 0 || arr->element_size != sizeof(double)) {
        return 0.0;
    }
    double sum = 0.0;
    for (size_t i = 0; i < arr->size; i++) {
        sum += ((double*)arr->data)[i];
    }
    return sum / arr->size;
}


// --- Printing Functions ---

void print_int_array(DArray* arr) {
    if (!arr || arr->element_size != sizeof(int)) return;
    printf("[");
    for (size_t i = 0; i < arr->size; i++) {
        printf("%d", ((int*)arr->data)[i]);
        if (i < arr->size - 1) printf(", ");
    }
    printf("]\n");
}

void print_string_array(DArray* arr) {
    if (!arr || arr->element_size != sizeof(char*)) return;
    printf("[");
    for (size_t i = 0; i < arr->size; i++) {
        printf("\"%s\"", ((char**)arr->data)[i]);
        if (i < arr->size - 1) printf(", ");
    }
    printf("]\n");
}

void print_float_array(DArray* arr) {
    if (!arr || arr->element_size != sizeof(double)) return;
    printf("[");
    for (size_t i = 0; i < arr->size; i++) {
        printf("%.2f", ((double*)arr->data)[i]);
        if (i < arr->size - 1) printf(", ");
    }
    printf("]\n");
}

void print_char_array(DArray* arr) {
    if (!arr || arr->element_size != sizeof(char)) return;
    printf("[");
    for (size_t i = 0; i < arr->size; i++) {
        printf("'%c'", ((char*)arr->data)[i]);
        if (i < arr->size - 1) printf(", ");
    }
    printf("]\n");
}
