# JSON Module Documentation

The JSON module provides full JSON parsing and serialization capabilities for PIE using the Jansson library.

## Features

- ✅ Parse JSON strings into objects
- ✅ Stringify objects to JSON
- ✅ Create empty objects and arrays
- ✅ Get/set values (string, int, float, bool)
- ✅ Nested objects and arrays
- ✅ Array operations (size, get, push)

## Installation

The JSON module requires the Jansson library (`libjansson`):

```bash
# Debian/Ubuntu
sudo apt-get install libjansson-dev

# Fedora/RHEL
sudo dnf install jansson-devel

# macOS
brew install jansson
```

## Basic Usage

```pie
import json;

// Create a JSON object
ptr user = json.create_object();
json.set_string(user, "name", "Alice");
json.set_int(user, "age", 30);
json.set_bool(user, "active", 1);

// Get values
string name = json.get_string(user, "name");
int age = json.get_int(user, "age");

// Stringify
string json_str = json.stringify(user);
output(json_str, string);  // {"name":"Alice","age":30,"active":true}

// Parse
ptr parsed = json.parse(json_str);
```

## API Reference

### Object Creation

#### `create_object() -> ptr`
Creates a new empty JSON object.

```pie
ptr obj = json.create_object();
```

#### `create_array() -> ptr`
Creates a new empty JSON array.

```pie
ptr arr = json.create_array();
```

### Parsing and Serialization

#### `parse(string text) -> ptr`
Parses a JSON string and returns a JSON object/array.

```pie
ptr data = json.parse('{"name":"Bob","age":25}');
```

#### `stringify(ptr obj) -> string`
Converts a JSON object/array to a JSON string.

```pie
string json_str = json.stringify(obj);
```

### Getting Values

#### `get_string(ptr obj, string key) -> string`
Gets a string value from the object.

```pie
string name = json.get_string(user, "name");
```

#### `get_int(ptr obj, string key) -> int`
Gets an integer value from the object.

```pie
int age = json.get_int(user, "age");
```

#### `get_float(ptr obj, string key) -> float`
Gets a float value from the object.

```pie
float score = json.get_float(user, "score");
```

#### `get_bool(ptr obj, string key) -> int`
Gets a boolean value from the object (returns 1 for true, 0 for false).

```pie
int active = json.get_bool(user, "active");
```

#### `get_object(ptr obj, string key) -> ptr`
Gets a nested object from the object.

```pie
ptr address = json.get_object(user, "address");
```

#### `get_array(ptr obj, string key) -> ptr`
Gets an array from the object.

```pie
ptr friends = json.get_array(user, "friends");
```

### Setting Values

#### `set_string(ptr obj, string key, string value)`
Sets a string value in the object.

```pie
json.set_string(user, "name", "Alice");
```

#### `set_int(ptr obj, string key, int value)`
Sets an integer value in the object.

```pie
json.set_int(user, "age", 30);
```

#### `set_float(ptr obj, string key, float value)`
Sets a float value in the object.

```pie
json.set_float(user, "score", 95.5);
```

#### `set_bool(ptr obj, string key, int value)`
Sets a boolean value in the object.

```pie
json.set_bool(user, "active", 1);  // 1 = true, 0 = false
```

### Array Operations

#### `array_size(ptr arr) -> int`
Gets the number of elements in an array.

```pie
int count = json.array_size(users);
```

#### `array_get_string(ptr arr, int index) -> string`
Gets a string from an array at the given index.

```pie
string name = json.array_get_string(names, 0);
```

#### `array_get_int(ptr arr, int index) -> int`
Gets an integer from an array at the given index.

```pie
int score = json.array_get_int(scores, 0);
```

#### `array_get_object(ptr arr, int index) -> ptr`
Gets an object from an array at the given index.

```pie
ptr user = json.array_get_object(users, 0);
```

#### `array_push_string(ptr arr, string value)`
Adds a string to the end of an array.

```pie
json.array_push_string(names, "Alice");
```

#### `array_push_int(ptr arr, int value)`
Adds an integer to the end of an array.

```pie
json.array_push_int(scores, 95);
```

#### `array_push_object(ptr arr, ptr obj)`
Adds an object to the end of an array.

```pie
json.array_push_object(users, user);
```

## Complete Example

```pie
import json;

// Create user object
ptr user = json.create_object();
json.set_string(user, "name", "Alice");
json.set_int(user, "age", 30);
json.set_bool(user, "active", 1);

// Create hobbies array
ptr hobbies = json.create_array();
json.array_push_string(hobbies, "reading");
json.array_push_string(hobbies, "coding");
json.array_push_string(hobbies, "gaming");

// Convert to JSON string
string json_str = json.stringify(user);
output("User JSON: ", string);
output(json_str, string);

// Parse JSON
string json_input = '{"name":"Bob","age":25,"score":95.5}';
ptr parsed = json.parse(json_input);

// Access parsed values
string name = json.get_string(parsed, "name");
int age = json.get_int(parsed, "age");
float score = json.get_float(parsed, "score");

output("Parsed name: ", string);
output(name, string);
output("Parsed age: ", string);
output(age, int);
output("Parsed score: ", string);
output(score, float);
```

## Implementation Details

The JSON module uses the Jansson C library (libjansson) for all JSON operations. All JSON objects and arrays are represented as opaque pointers (`ptr` type in PIE), which internally point to `json_t*` structures from Jansson.

### C Bindings

All PIE JSON functions are prefixed with `pie_json_` in the C implementation to avoid naming conflicts with Jansson's own functions. The mapping is handled automatically by the module system using the `c_name` field in `module.json`.

### Memory Management

Jansson uses reference counting for memory management. The PIE JSON module currently does not expose explicit free functions, as Jansson handles cleanup automatically when references are decremented. Future versions may add explicit memory management functions if needed.

## Testing

The JSON module has been tested with:
- ✅ Object creation and manipulation
- ✅ String values
- ✅ Integer values
- ✅ Nested structures
- ✅ JSON parsing
- ✅ JSON stringification

See `test_json_simple.pie` for a working example.
