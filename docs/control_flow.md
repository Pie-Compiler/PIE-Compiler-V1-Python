# Control Flow

PIE provides a set of control flow statements that are similar to those in other C-style languages.

## `if-else` Statement

The `if-else` statement allows for conditional execution of code.

```pie
int x = 10;

if (x > 5) {
    output("x is greater than 5", string);
} else if (x < 5) {
    output("x is less than 5", string);
} else {
    output("x is equal to 5", string);
}
```

## `while` Loop

The `while` loop executes a block of code as long as a condition is true.

```pie
int i = 0;
while (i < 5) {
    output(i, int);
    i = i + 1;
}
```

## `do-while` Loop

The `do-while` loop is similar to the `while` loop, but the condition is checked at the end of the loop, so the loop body is always executed at least once.

```pie
int i = 0;
do {
    output(i, int);
    i = i + 1;
} while (i < 5);
```

## `for` Loop

The `for` loop provides a concise way to iterate over a range of values.

```pie
for (int i = 0; i < 5; i = i + 1) {
    output(i, int);
}
```

## `switch-case` Statement

The `switch-case` statement allows for selecting one of many code blocks to be executed.

```pie
int day = 3;
switch (day) {
    case 1:
        output("Monday", string);
        break;
    case 2:
        output("Tuesday", string);
        break;
    case 3:
        output("Wednesday", string);
        break;
    default:
        output("Some other day", string);
}
```

## `break` and `continue`

- `break`: Exits a loop or `switch` statement.
- `continue`: Skips the current iteration of a loop and proceeds to the next one.
