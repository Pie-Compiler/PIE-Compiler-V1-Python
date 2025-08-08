#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

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
