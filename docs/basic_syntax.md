# Basic Syntax

This section covers the basic syntax of the PIE programming language.

## Variables

Variables are declared with their type, followed by the variable name. They can be optionally initialized at the time of declaration.

```pie
// Declare an integer variable
int x;

// Declare and initialize a float variable
float y = 3.14;

// Declare a string variable
string message = "Hello, PIE!";
```

## Semicolons

Each statement in PIE must be terminated with a semicolon (`;`).

```pie
int a = 5;
int b = 10;
int c = a + b;
```

## Comments

PIE supports two types of comments:

- **Single-line comments:** These start with `//` and continue to the end of the line.
- **Multi-line comments:** These start with `/*` and end with `*/`.

```pie
// This is a single-line comment.
int x = 10; // This is also a single-line comment.

/*
This is a multi-line comment.
It can span multiple lines.
*/
int y = 20;
```

## No `main` Function Required

PIE programs can be written as a sequence of statements without needing a `main` function. The statements in the global scope are executed in the order they appear.

```pie
// This is a valid PIE program.
string name = "World";
output("Hello, " + name, string);
```

However, you can still define and use functions, including a `main` function if you prefer to structure your code that way.
