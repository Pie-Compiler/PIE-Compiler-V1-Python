# PIE Compiler Changelog

## Recent Updates

### Bug Fixes

#### Fixed llvmlite Deprecation Warning
- **Issue**: The compiler was using the deprecated `llvmlite.initialize()` function
- **Fix**: Removed the deprecated call from `src/backend/llvm_generator.py`
- **Impact**: The quickfox.pie test file now compiles and runs without errors
- **File Modified**: `src/backend/llvm_generator.py` (line 24)

### New Features

#### Advanced String Utilities
Added 8 new string manipulation functions to enhance text processing capabilities:

1. **`string_to_upper(string str)`** - Convert string to uppercase
   - Returns a new string with all characters in uppercase
   - Example: `string_to_upper("hello")` → `"HELLO"`

2. **`string_to_lower(string str)`** - Convert string to lowercase
   - Returns a new string with all characters in lowercase
   - Example: `string_to_lower("HELLO")` → `"hello"`

3. **`string_trim(string str)`** - Remove leading/trailing whitespace
   - Returns a new string with whitespace removed from both ends
   - Example: `string_trim("  hello  ")` → `"hello"`

4. **`string_substring(string str, int start, int length)`** - Extract substring
   - Returns a substring starting at position `start` with given `length`
   - Example: `string_substring("hello world", 0, 5)` → `"hello"`

5. **`string_index_of(string haystack, string needle)`** - Find substring position
   - Returns the index of first occurrence, or -1 if not found
   - Example: `string_index_of("hello world", "world")` → `6`

6. **`string_replace_char(string str, char old_char, char new_char)`** - Replace character
   - Returns a new string with all occurrences of `old_char` replaced by `new_char`
   - Example: `string_replace_char("hello world", ' ', '_')` → `"hello_world"`

7. **`string_reverse(string str)`** - Reverse string
   - Returns a new string with characters in reverse order
   - Example: `string_reverse("PIE")` → `"EIP"`

8. **`string_count_char(string str, char ch)`** - Count character occurrences
   - Returns the number of times `ch` appears in the string
   - Example: `string_count_char("hello", 'l')` → `2`

#### Implementation Details

**Files Modified:**
- `src/runtime/string_lib.h` - Added function declarations
- `src/runtime/string_lib.c` - Implemented all 8 new functions
- `src/backend/llvm_generator.py` - Added LLVM function declarations
- `src/frontend/parser.py` - Registered functions in symbol table

**Files Created:**
- `docs/advanced_string_utilities.md` - Comprehensive documentation with examples
- `test_string_utils.pie` - Test file demonstrating all new functions

**Documentation Updates:**
- Updated `README.md` to include new string utilities
- Added examples and use cases for each function

### Testing

#### Test Files
1. **quickfox.pie** - Comprehensive test suite for all PIE features
   - Status: ✅ Passing
   - Tests: Variables, arrays, dictionaries, math functions, string operations, control flow

2. **test_string_utils.pie** - New test file for string utilities
   - Status: ✅ Passing
   - Tests: All 8 new string functions plus existing utilities

#### Test Results
All tests pass successfully:
```
=== Testing New String Utilities ===
✅ string_to_upper: "Hello World" → "HELLO WORLD"
✅ string_to_lower: "Hello World" → "hello world"
✅ string_trim: "   spaces around   " → "spaces around"
✅ string_substring: "The quick brown fox" (4, 5) → "quick"
✅ string_index_of: Found "quick" at index 4
✅ string_replace_char: "hello world" → "hello_world"
✅ string_reverse: "PIE" → "EIP"
✅ string_count_char: "hello world" has 3 'l's

=== Testing Existing String Utilities ===
✅ string_contains: Text contains 'fox'
✅ string_starts_with: Text starts with 'The'
✅ string_ends_with: Text ends with 'fox'
✅ string_is_empty: Empty string detected
```

### Performance

All string utility functions are implemented in C for optimal performance:
- **Time Complexity**: O(n) for most operations where n is string length
- **Memory Management**: Automatic memory allocation and cleanup
- **Safety**: Null pointer checks and bounds validation

### Compatibility

- **LLVM Version**: Compatible with LLVM 18
- **Python Version**: Python 3.x
- **Dependencies**: llvmlite 0.45.1, ply 3.11

### Usage Examples

#### Example 1: Text Normalization
```pie
string input = "  HELLO WORLD  ";
string normalized = string_to_lower(string_trim(input));
output(normalized, string);  // Output: "hello world"
```

#### Example 2: String Analysis
```pie
string text = "The quick brown fox";
int index = string_index_of(text, "quick");
string sub = string_substring(text, index, 5);
output(sub, string);  // Output: "quick"
```

#### Example 3: Character Replacement
```pie
string filename = "my file name.txt";
string safe_name = string_replace_char(filename, ' ', '_');
output(safe_name, string);  // Output: "my_file_name.txt"
```

### Breaking Changes

None. All changes are backward compatible.

### Known Issues

None currently identified.

### Future Enhancements

Potential additions for future releases:
- String splitting functions
- Regular expression support
- Unicode string handling
- String formatting functions
- More advanced text processing utilities

---

## Summary

This update successfully:
1. ✅ Fixed the llvmlite deprecation warning in quickfox.pie
2. ✅ Added 8 new advanced string utility functions
3. ✅ Created comprehensive documentation
4. ✅ Implemented thorough testing
5. ✅ Maintained backward compatibility

The PIE compiler now offers a robust set of string manipulation tools suitable for text processing, data parsing, and general string operations.
