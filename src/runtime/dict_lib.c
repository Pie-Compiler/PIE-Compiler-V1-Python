#include "dict_lib.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define INITIAL_CAPACITY 16

// Hash function (djb2)
static uint32_t hash_key(const char* key) {
    uint32_t hash = 5381;
    int c;
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return hash;
}

Dictionary* dict_create() {
    Dictionary* dict = (Dictionary*)malloc(sizeof(Dictionary));
    if (!dict) return NULL;
    dict->capacity = INITIAL_CAPACITY;
    dict->size = 0;
    dict->buckets = (DictNode**)calloc(dict->capacity, sizeof(DictNode*));
    if (!dict->buckets) {
        free(dict);
        return NULL;
    }
    return dict;
}

static void dict_free_value(DictValue* value) {
    if (!value) return;
    if (value->type == DICT_VALUE_STRING) {
        free(value->as.string_val);
    }
    free(value);
}

void dict_free(Dictionary* dict) {
    if (!dict) return;
    for (uint32_t i = 0; i < dict->capacity; i++) {
        DictNode* node = dict->buckets[i];
        while (node) {
            DictNode* next = node->next;
            free(node->key);
            dict_free_value(node->value);
            free(node);
            node = next;
        }
    }
    free(dict->buckets);
    free(dict);
}

// NOTE: For simplicity, this implementation doesn't handle resizing.
void dict_set(Dictionary* dict, const char* key, DictValue* value) {
    if (!dict) return;
    uint32_t index = hash_key(key) % dict->capacity;
    DictNode* node = dict->buckets[index];

    // Check if key already exists
    while (node) {
        if (strcmp(node->key, key) == 0) {
            dict_free_value(node->value);
            node->value = value;
            return;
        }
        node = node->next;
    }

    // Key doesn't exist, create a new node
    DictNode* new_node = (DictNode*)malloc(sizeof(DictNode));
    new_node->key = strdup(key);
    new_node->value = value;
    new_node->next = dict->buckets[index];
    dict->buckets[index] = new_node;
    dict->size++;
}

DictValue* dict_get(Dictionary* dict, const char* key) {
    if (!dict) return NULL;
    uint32_t index = hash_key(key) % dict->capacity;
    DictNode* node = dict->buckets[index];
    while (node) {
        if (strcmp(node->key, key) == 0) {
            return node->value;
        }
        node = node->next;
    }
    return NULL; // Not found
}

int32_t dict_get_int(Dictionary* dict, const char* key) {
    DictValue* val = dict_get(dict, key);
    if (val && val->type == DICT_VALUE_INT) {
        return val->as.int_val;
    }
    return 0; // Default value
}

double dict_get_float(Dictionary* dict, const char* key) {
    DictValue* val = dict_get(dict, key);
    if (val && val->type == DICT_VALUE_FLOAT) {
        return val->as.float_val;
    }
    return 0.0; // Default value
}

char* dict_get_string(Dictionary* dict, const char* key) {
    DictValue* val = dict_get(dict, key);
    if (val && val->type == DICT_VALUE_STRING) {
        return val->as.string_val;
    }
    return ""; // Default value
}

void dict_delete(Dictionary* dict, const char* key) {
    if (!dict) return;
    uint32_t index = hash_key(key) % dict->capacity;
    DictNode** p = &dict->buckets[index];
    while (*p) {
        DictNode* entry = *p;
        if (strcmp(entry->key, key) == 0) {
            *p = entry->next;
            free(entry->key);
            dict_free_value(entry->value);
            free(entry);
            dict->size--;
            return;
        }
        p = &(*p)->next;
    }
}

// Helper functions for creating values
DictValue* dict_value_create_int(int32_t value) {
    DictValue* dv = (DictValue*)malloc(sizeof(DictValue));
    dv->type = DICT_VALUE_INT;
    dv->as.int_val = value;
    return dv;
}

DictValue* dict_value_create_float(double value) {
    DictValue* dv = (DictValue*)malloc(sizeof(DictValue));
    dv->type = DICT_VALUE_FLOAT;
    dv->as.float_val = value;
    return dv;
}

DictValue* dict_value_create_string(const char* value) {
    DictValue* dv = (DictValue*)malloc(sizeof(DictValue));
    dv->type = DICT_VALUE_STRING;
    dv->as.string_val = strdup(value);
    return dv;
}

DictValue* dict_value_create_null() {
    DictValue* dv = (DictValue*)malloc(sizeof(DictValue));
    dv->type = DICT_VALUE_NULL;
    return dv;
}
