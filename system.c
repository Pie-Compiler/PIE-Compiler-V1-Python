#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Input function for float
void input_float(float *ptr) {
    // Clear any pending input
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
    
    // Get the float input
    if (scanf("%f", ptr) != 1) {
        fprintf(stderr, "Error reading float input\n");
        *ptr = 0.0f;
    }
}

// Input function for int
void input_int(int *ptr) {
    // Clear any pending input
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
    
    // Get the integer input
    if (scanf("%d", ptr) != 1) {
        fprintf(stderr, "Error reading integer input\n");
        *ptr = 0;
    }
}

// Input function for string
void input_string(char *ptr) {
    // Clear any pending input
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
    
    // Read a line of input (up to 255 characters)
    if (fgets(ptr, 255, stdin) != NULL) {
        // Remove the trailing newline if present
        size_t len = strlen(ptr);
        if (len > 0 && ptr[len-1] == '\n') {
            ptr[len-1] = '\0';
        }
    } else {
        // Error or EOF, set to empty string
        ptr[0] = '\0';
    }
}

// Input function for char
void input_char(char *ptr) {
    // Clear any pending input
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
    
    // Get the character input
    *ptr = getchar();
}

// Output function for float
void output_float(float value) {
    printf("%f\n", value);
}

// Output function for int
void output_int(int value) {
    printf("%d\n", value);
}

// Output function for string
void output_string(const char *value) {
    if (value) {
        printf("%s\n", value);
    } else {
        printf("(null)\n");
    }
}

// Output function for char
void output_char(char value) {
    printf("%c\n", value);
}

// Exit function
void exit_program() {
    exit(0);
}