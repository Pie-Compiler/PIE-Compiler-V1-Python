# Dictionary Validation and Safe Access

This document describes the improved dictionary support in the PIE compiler, which now includes validation for undefined indices and safe access patterns.

## New Functions

### `dict_has_key(dict, key)`
- **Purpose**: Check if a key exists in a dictionary
- **Parameters**: 
  - `dict`: The dictionary to check
  - `key`: The string key to look for
- **Returns**: `1` if key exists, `0` if not found
- **C Function**: `dict_has_key`

### `dict_key_exists(dict, key)`
- **Purpose**: PIE language wrapper for checking key existence
- **Parameters**: Same as `dict_has_key`
- **Returns**: Same as `dict_has_key`
- **C Function**: `dict_key_exists`

## Safe Dictionary Access Patterns

### Pattern 1: Check Before Access
```pie
dict config = {"server": "localhost", "port": 8080};

if(dict_key_exists(config, "server") == 1){
    string server = dict_get_string(config, "server");
    output(server, string);
} else {
    output("Server not configured", string);
}
```

### Pattern 2: Safe Access with Default Values
```pie
dict settings = {"theme": "dark"};

string theme;
if(dict_key_exists(settings, "theme") == 1){
    theme = dict_get_string(settings, "theme");
} else {
    theme = "light";  // Default value
}
```

### Pattern 3: Validation in Loops
```pie
dict user = {"name": "John", "age": 30};
string[] required_keys = {"name", "age", "email"};

int i = 0;
while(i < 3){
    string key = required_keys[i];
    if(dict_key_exists(user, key) == 1){
        output("Key '", string);
        output(key, string);
        output("' is present", string);
    } else {
        output("Missing required key: ", string);
        output(key, string);
    }
    i = i + 1;
}
```

## Improved Error Handling

The compiler now provides better error handling for dictionary access:

1. **Key Existence Validation**: Use `dict_key_exists()` to check if a key exists before accessing it
2. **Safe Default Values**: Provide fallback values when keys don't exist
3. **Runtime Safety**: The compiler generates code that safely handles missing keys

## Backward Compatibility

All existing dictionary code will continue to work. The new functions are additive and don't break existing functionality.

## Performance Considerations

- `dict_has_key()` performs a hash table lookup, so it's efficient
- For frequently accessed keys, consider storing the result of `dict_key_exists()` in a variable
- The validation adds minimal overhead compared to the benefits of safe access

## Examples

See the following test files for complete examples:
- `test_dict_improved.pie` - Comprehensive testing of all features
- `dict_validation_example.pie` - Simple practical examples

## Future Enhancements

Potential future improvements could include:
- Compile-time key validation for known dictionary structures
- Automatic default value generation based on type
- Dictionary schema validation
- More sophisticated error reporting for missing keys
