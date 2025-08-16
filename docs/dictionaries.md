# Dictionaries

Dictionaries are collections of key-value pairs. In PIE, dictionary keys are always strings, and values can be of type `int`, `float`, or `string`.

## Declaring Dictionaries

Dictionaries are declared using the `dict` keyword and can be initialized with a list of key-value pairs.

```pie
// A dictionary representing a person
dict person = {"name": "John Doe", "age": 30};

// An empty dictionary
dict config = {};
```

## Accessing Values

Dictionary values are accessed using the key.

**Note:** Direct key-based access syntax (e.g., `person["name"]`) is not yet supported in the parser. You must use the `dict_get_*` functions.

## Important: Variable Initialization Order

When declaring global variables with dictionary operations, it's important to understand PIE's initialization order:

### ✅ Correct Usage

```pie
// Dictionary literals are initialized immediately
dict person = {"name": "Alice", "age": 25};

// These work because the dictionary is already initialized
string name = dict_get_string(person, "name");
int age = dict_get_int(person, "age");
```

### ❌ Problematic Usage

```pie
// This creates an empty dictionary
dict config = dict_create();

// These will retrieve from an EMPTY dictionary because
// dict_set operations happen AFTER global variable initialization
int max_users = dict_get_int(config, "max_users");  // Returns 0!
string host = dict_get_string(config, "host");      // Returns ""!

// These dict_set calls happen later in the main execution
dict_set(config, "max_users", new_int(100));
dict_set(config, "host", new_string("localhost"));
```

### 💡 Solution: Use Functions

```pie
dict config = dict_create();

void setup_config() {
    dict_set(config, "max_users", new_int(100));
    dict_set(config, "timeout", new_float(30.5));
    dict_set(config, "host", new_string("localhost"));
}

void use_config() {
    int max_users = dict_get_int(config, "max_users");
    float timeout = dict_get_float(config, "timeout");
    string host = dict_get_string(config, "host");
    
    output("Max users: ", string);
    output(max_users, int);
}

// Call functions in the correct order
setup_config();
use_config();
```

**Why This Happens:** PIE follows a two-phase initialization:
1. **Static Phase**: Dictionary literals and simple constants are initialized
2. **Dynamic Phase**: Function calls like `dict_set()` are executed in the main program

This ensures runtime functions have a proper execution context and prevents initialization-order bugs.

## Dictionary Functions

PIE provides a set of built-in functions for working with dictionaries.

| Function                          | Description                               |
|-----------------------------------|-------------------------------------------|
| `dict_create()`                   | Creates and returns a new, empty dictionary. |
| `dict_set(d, key, val)`           | Sets the value for a key in the dictionary. `val` must be created with `new_int`, `new_float`, or `new_string`. |
| `dict_get_int(d, key)`            | Retrieves an integer value for a key.     |
| `dict_get_float(d, key)`          | Retrieves a float value for a key.        |
| `dict_get_string(d, key)`         | Retrieves a string value for a key.       |
| `dict_delete(d, key)`             | Deletes a key-value pair from the dictionary. |

### Helper functions for creating values:

| Function            | Description                               |
|---------------------|-------------------------------------------|
| `new_int(val)`      | Creates a new integer value for a dictionary. |
| `new_float(val)`    | Creates a new float value for a dictionary.   |
| `new_string(val)`   | Creates a new string value for a dictionary.  |

### Example

```pie
// Method 1: Using dictionary literals (recommended for static data)
dict person = {"name": "John Doe", "age": 30, "score": 95.5};

string name = dict_get_string(person, "name");
int age = dict_get_int(person, "age");
float score = dict_get_float(person, "score");

output("Name: ", string);
output(name, string);
output("Age: ", string);
output(age, int);

// Method 2: Using function-based approach (for dynamic data)
dict config = dict_create();

void setup() {
    dict_set(config, "count", new_int(100));
    dict_set(config, "pi", new_float(3.14159));
    dict_set(config, "message", new_string("Hello, Dictionary!"));
}

void display() {
    int count = dict_get_int(config, "count");
    float pi = dict_get_float(config, "pi");
    string msg = dict_get_string(config, "message");

    output(count, int);
    output(pi, float);
    output(msg, string);
}

// Execute in correct order
setup();
display();
```
