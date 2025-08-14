# Examples

This section provides some example PIE programs to help you get started.

## Hello, World!

A classic "Hello, World!" program in PIE.

```pie
// A simple "Hello, World!" program
output("Hello, World!", string);
```

## User Input and Output

This example demonstrates how to take user input and display it.

```pie
string name;
output("Enter your name: ", string);
input(name, string);
output("Hello, " + name + "!", string);
```

## Factorial Function

This example shows how to define and use a recursive function to calculate the factorial of a number.

```pie
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int num = 5;
int result = factorial(num);

output("The factorial of ", string);
output(num, int);
output(" is ", string);
output(result, int);
output("\n", string);
```

## Working with Arrays

This example demonstrates creating an array, adding elements to it, and iterating over it.

```pie
// Create an array of integers
int numbers[] = [1, 2, 3];

// Add some more numbers
arr_push(numbers, 4);
arr_push(numbers, 5);

// Print the size of the array
output("Array size: ", string);
output(arr_size(numbers), int);
output("\n", string);

// Print the elements of the array
for (int i = 0; i < arr_size(numbers); i = i + 1) {
    output(numbers[i], int);
    output(" ", string);
}
output("\n", string);
```

## File I/O

This example shows how to write to a file and then read from it.

```pie
// Write to a file
file f = file_open("test.txt", "w");
file_write(f, "Hello from PIE!\n");
file_write(f, "This is a new line.\n");
file_close(f);

// Read from the file
f = file_open("test.txt", "r");
string content = file_read_all(f);
file_close(f);

output("File content:\n", string);
output(content, string);
```
