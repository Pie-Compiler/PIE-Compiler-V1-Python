# Functions

Functions are reusable blocks of code that can be defined and called in a PIE program.

## Defining a Function

A function is defined with a return type, a name, a list of parameters, and a body.

```pie
// A function that takes two integers and returns their sum
int add(int a, int b) {
    return a + b;
}

// A function with no return value
void greet(string name) {
    output("Hello, " + name, string);
}
```

## Calling a Function

A function is called by its name, followed by a list of arguments in parentheses.

```pie
int sum = add(5, 10);
greet("PIE");
```

## Built-in Functions

PIE provides a set of built-in functions for common tasks. These are documented in the [Standard Library](./standard_library.md) section.

Examples of built-in functions:

```pie
// System functions
output("Hello, World!", string);

// Array functions
int numbers[] = [1, 2, 3];
arr_push(numbers, 4);
int size = arr_size(numbers);
```
