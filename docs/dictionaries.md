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
// Create a dictionary
dict my_dict = dict_create();

// Set some values
dict_set(my_dict, "count", new_int(100));
dict_set(my_dict, "pi", new_float(3.14159));
dict_set(my_dict, "message", new_string("Hello, Dictionary!"));

// Get values
int count = dict_get_int(my_dict, "count");
float pi = dict_get_float(my_dict, "pi");
string msg = dict_get_string(my_dict, "message");

output(count, int);
output(pi, float);
output(msg, string);
```
