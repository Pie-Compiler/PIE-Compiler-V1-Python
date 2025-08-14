# Data Types

PIE is a statically typed language. The following data types are supported:

## Primitive Types

| Type      | Description                  | Example                               |
|-----------|------------------------------|---------------------------------------|
| `int`     | 32-bit signed integer        | `int x = 10;`                         |
| `float`   | 64-bit floating-point number | `float y = 3.14;`                     |
| `char`    | A single character           | `char c = 'a';`                       |
| `string`  | A sequence of characters     | `string s = "Hello";`                 |
| `bool`    | Boolean value (`true`/`false`) | `bool b = true;`                      |
| `void`    | Represents the absence of a value, used as a function return type | `void myFunction() { ... }` |

`boolean` is an alias for `bool`.

## Composite Types

### Arrays

Arrays are ordered collections of elements of the same type. They are dynamic and can grow or shrink in size.

```pie
// Declare an array of integers
int numbers[] = [1, 2, 3, 4, 5];

// Declare an empty array of strings
string names[] = [];
```

See the [Arrays](./arrays.md) documentation for more details.

### Dictionaries

Dictionaries are collections of key-value pairs. Keys are strings, and values can be of type `int`, `float`, or `string`.

```pie
// Declare a dictionary
dict person = {"name": "John", "age": 30};
```

See the [Dictionaries](./dictionaries.md) documentation for more details.

## Special Types

| Type     | Description                                       |
|----------|---------------------------------------------------|
| `file`   | Represents a file handle for file I/O operations. |
| `socket` | Represents a network socket for network communication. |
| `null`   | Represents a null or empty value.                 |
