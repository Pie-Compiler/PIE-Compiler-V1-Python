#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include "d_array.h"

intptr_t file_open(const char* filename, const char* mode) {
    FILE* file = fopen(filename, mode);
    return (intptr_t)file;
}

void file_close(intptr_t file_handle) {
    FILE* file = (FILE*)file_handle;
    if (file) {
        fclose(file);
    }
}

// For simplicity, file_write will write a null-terminated string.
void file_write(intptr_t file_handle, const char* content) {
    FILE* file = (FILE*)file_handle;
    if (file) {
        fputs(content, file);
    }
}

void file_flush(intptr_t file_handle) {
    FILE* file = (FILE*)file_handle;
    if (file) {
        fflush(file);
    }
}

// file_read is more complex. For now, let's assume it reads a line.
// The buffer needs to be allocated by the caller.
void file_read(intptr_t file_handle, char* buffer, int size) {
    FILE* file = (FILE*)file_handle;
    if (file && buffer) {
        if (fgets(buffer, size, file) == NULL) {
            buffer[0] = '\0'; // End of file or error
        }
    }
}

char* file_read_all(intptr_t file_handle) {
    FILE* file = (FILE*)file_handle;
    if (!file) return NULL;

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* buffer = (char*)malloc(length + 1);
    if (!buffer) return NULL;

    fread(buffer, 1, length, file);
    buffer[length] = '\0';

    return buffer;
}

DArrayString* file_read_lines(intptr_t file_handle, int start_line, int end_line) {
    FILE* file = (FILE*)file_handle;
    if (!file) return NULL;

    // Default values: if start_line is -1, read from beginning
    // if end_line is -1, read until end of file
    int use_start = (start_line >= 0);
    int use_end = (end_line >= 0);
    
    DArrayString* arr = d_array_string_create();
    char* line = NULL;
    size_t len = 0;
    ssize_t read;
    int current_line = 0;

    while ((read = getline(&line, &len, file)) != -1) {
        // Check if we're in the range we want
        if (use_start && current_line < start_line) {
            current_line++;
            continue;
        }
        
        if (use_end && current_line > end_line) {
            break;
        }
        
        // Remove trailing newline
        if (read > 0 && line[read - 1] == '\n') {
            line[read - 1] = '\0';
        }
        
        // Duplicate the line before appending (getline reuses the buffer)
        char* line_copy = strdup(line);
        d_array_string_append(arr, line_copy);
        
        current_line++;
    }

    free(line);
    return arr;
}
