#include "string_lib.h"
#include <string.h>

int pie_strlen(const char* s) {
    return strlen(s);
}

int pie_strcmp(const char* s1, const char* s2) {
    return strcmp(s1, s2);
}

char* pie_strcpy(char* dest, const char* src) {
    return strcpy(dest, src);
}

char* pie_strcat(char* dest, const char* src) {
    return strcat(dest, src);
}
