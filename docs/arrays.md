# Arrays

PIE provides built-in support for dynamic arrays, which can hold elements of type `int`, `float`, `char`, or `string`.

## Declaring Arrays

Arrays are declared with the element type, followed by the variable name, and then `[]`. They can be initialized with a list of values.

```pie
// An array of integers
int numbers[] = [10, 20, 30];

// An array of strings
string fruits[] = ["apple", "banana", "cherry"];

// An empty array of floats
float prices[] = [];
```

## Accessing Elements

Array elements are accessed using zero-based indexing.

```pie
int firstNumber = numbers[0]; // 10
string secondFruit = fruits[1]; // "banana"
```

## Modifying Elements

Elements of an array can be modified by assigning a new value to a specific index.

```pie
numbers[0] = 100;
fruits[1] = "blueberry";
```

## Array Functions

PIE provides a set of built-in functions for working with arrays.

| Function            | Description                                         |
|---------------------|-----------------------------------------------------|
| `arr_push(arr, val)`| Appends a value to the end of the array.            |
| `arr_pop(arr)`      | Removes and returns the last element of the array.  |
| `arr_size(arr)`     | Returns the number of elements in the array.        |
| `arr_contains(arr, val)`| Returns `true` if the array contains the value. |
| `arr_indexof(arr, val)` | Returns the index of the first occurrence of the value, or -1 if not found. |
| `arr_avg(arr)`      | Returns the average of the elements in a numeric array. |

**Note:** The `arr_*` functions are generic. The actual function names in the runtime are specific to the array type (e.g., `d_array_int_push`, `d_array_string_size`). The compiler maps the generic `arr_*` calls to the correct type-specific function.
