# User-Defined Modules Example

This directory demonstrates how to create and use user-defined modules in PIE.

## Files

- **mathutils.pie** - A user-defined module with mathematical utility functions
- **test_mathutils.pie** - A program that imports and uses the mathutils module

## Creating a User-Defined Module

To create your own module:

1. **Create a .pie file** with your functions
2. **Use the `export` keyword** before functions you want to make available to other modules
3. **Functions without `export`** remain private to the module

### Example:

```pie
// mymodule.pie

// Exported function - visible to importers
export int public_function(int x) {
    return x * 2;
}

// Private function - only usable within this module
int helper_function(int x) {
    return x + 1;
}

export int another_public_function() {
    // Can use private functions internally
    return helper_function(10);
}
```

## Using a User-Defined Module

To use a module in your program:

1. **Import the module** using the `import` statement
2. **Call exported functions** using dot notation: `modulename.function()`

### Example:

```pie
// main.pie

import mymodule;

int main() {
    int result = mymodule.public_function(5);
    output(result, int);
    return 0;
}
```

## Module Search Path

The compiler looks for modules in the following locations:

1. **Standard library** - `stdlib/` directory (for built-in modules like `http`, `json`)
2. **Current directory** - Same directory as the source file being compiled
3. **User modules directory** - Custom paths (can be configured)

## Exported vs Private Functions

- **Exported functions** (`export` keyword):
  - Visible to code that imports the module
  - Part of the module's public API
  - Can be called using `modulename.functionname()` syntax

- **Private functions** (no `export` keyword):
  - Only usable within the module itself
  - Not accessible to importers
  - Useful for internal helper functions

## Example: mathutils Module

The `mathutils.pie` module demonstrates various mathematical utilities:

### Exported Functions:
- `square(x)` - Calculate x²
- `cube(x)` - Calculate x³
- `is_even(n)` - Check if number is even
- `factorial(n)` - Calculate factorial
- `max(a, b)` - Find maximum of two numbers
- `min(a, b)` - Find minimum of two numbers
- `increment(x)` - Increment a number (uses private helper)
- `power(base, exp)` - Calculate base^exponent
- `is_prime(n)` - Check if number is prime
- `gcd(a, b)` - Calculate Greatest Common Divisor

### Private Functions:
- `helper_function(x)` - Internal helper (not accessible to importers)

## Running the Example

```bash
# Compile and run the test program
python3 src/main.py examples/user_modules/test_mathutils.pie
./program
```

## Best Practices

1. **Export only what's needed** - Keep internal implementation details private
2. **Use descriptive names** - Module and function names should be clear and descriptive
3. **Document your modules** - Add comments explaining what exported functions do
4. **Organize by functionality** - Group related functions into cohesive modules
5. **Avoid circular imports** - Module A shouldn't import Module B if Module B imports Module A

## Future Enhancements

- Module metadata files for user modules (similar to stdlib modules)
- Module versioning
- Package management
- Nested module namespaces
