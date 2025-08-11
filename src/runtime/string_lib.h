#ifndef STRING_LIB_H
#define STRING_LIB_H

#include <stddef.h>

int pie_strlen(const char* s);
int pie_strcmp(const char* s1, const char* s2);
char* pie_strcpy(char* dest, const char* src);
char* pie_strcat(char* dest, const char* src);

#endif // STRING_LIB_H
