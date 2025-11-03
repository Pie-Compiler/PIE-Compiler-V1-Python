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

#### `set_object(ptr obj, string key, ptr value)`
Sets a nested object in the object.

```pie
ptr address = json.create_object();
json.set_string(address, "city", "NYC");
json.set_object(user, "address", address);
```

#### `set_array(ptr obj, string key, ptr value)`
Sets an array in the object.

```pie
ptr hobbies = json.create_array();
json.array_push_string(hobbies, "reading");
json.set_array(user, "hobbies", hobbies);
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

## Working with Nested Objects

You can programmatically create nested objects using `set_object()`:

```pie
import json;

// Create user object
ptr user = json.create_object();
json.set_string(user, "name", "Alice");
json.set_int(user, "age", 30);

// Create nested address object
ptr address = json.create_object();
json.set_string(address, "street", "123 Main St");
json.set_string(address, "city", "Springfield");
json.set_string(address, "zip", "12345");

// Nest the address inside the user
json.set_object(user, "address", address);

// Convert to JSON
string json_str = json.stringify(user);
// Output: {"name":"Alice","age":30,"address":{"street":"123 Main St","city":"Springfield","zip":"12345"}}
```

You can also parse and access nested objects:

```pie
// Parse JSON with nested object
string user_json = '{"name":"Alice","age":30,"address":{"street":"123 Main St","city":"Springfield","zip":"12345"}}';
ptr user = json.parse(user_json);

// Access top-level fields
string name = json.get_string(user, "name");
int age = json.get_int(user, "age");

// Access nested object
ptr address = json.get_object(user, "address");
string street = json.get_string(address, "street");
string city = json.get_string(address, "city");
string zip = json.get_string(address, "zip");

output("Name: ", string);
output(name, string);
output("Street: ", string);
output(street, string);
output("City: ", string);
output(city, string);
```

## Working with Nested Arrays

You can programmatically create objects with nested arrays using `set_array()`:

```pie
import json;

// Create user object
ptr user = json.create_object();
json.set_string(user, "name", "Bob");
json.set_int(user, "age", 25);

// Create hobbies array
ptr hobbies = json.create_array();
json.array_push_string(hobbies, "reading");
json.array_push_string(hobbies, "coding");
json.array_push_string(hobbies, "gaming");

// Nest the array in the user object
json.set_array(user, "hobbies", hobbies);

// Convert to JSON
string json_str = json.stringify(user);
// Output: {"name":"Bob","age":25,"hobbies":["reading","coding","gaming"]}
```

You can also access nested arrays from parsed JSON:

```pie
// Parse JSON with array
string json_str = '{"name":"Bob","age":25,"hobbies":["reading","coding","gaming"]}';
ptr user = json.parse(json_str);

// Access the array
ptr hobbies = json.get_array(user, "hobbies");

// Get array length
int hobby_count = json.array_size(hobbies);
output("Number of hobbies: ", string);
output(hobby_count, int);

// Access individual elements
string hobby0 = json.array_get_string(hobbies, 0);
string hobby1 = json.array_get_string(hobbies, 1);
string hobby2 = json.array_get_string(hobbies, 2);

output("Hobbies: ", string);
output(hobby0, string);
output(", ", string);
output(hobby1, string);
output(", ", string);
output(hobby2, string);
```

## Working with Arrays of Objects

You can handle arrays containing objects using `array_get_object()`:

```pie
import json;

// Parse JSON with array of objects (e.g., server response)
string json_str = '{"users":[{"name":"Alice","age":30},{"name":"Bob","age":25}]}';
ptr data = json.parse(json_str);

// Get the users array
ptr users = json.get_array(data, "users");
int user_count = json.array_size(users);

// Access first user
ptr user0 = json.array_get_object(users, 0);
string name0 = json.get_string(user0, "name");
int age0 = json.get_int(user0, "age");

// Access second user
ptr user1 = json.array_get_object(users, 1);
string name1 = json.get_string(user1, "name");
int age1 = json.get_int(user1, "age");

output("User 0: ", string);
output(name0, string);
output(" (", string);
output(age0, int);
output(" years old)", string);
```

## Complex Nested Structures

The JSON module supports arbitrarily complex nesting of objects and arrays:

```pie
import json;

// Parse company data with employees containing skills
string company_json = '{"name":"TechCorp","employees":[{"name":"Alice","role":"Engineer","skills":["Python","C++"]},{"name":"Bob","role":"Designer","skills":["Figma","Photoshop"]}]}';
ptr company = json.parse(company_json);

// Get company name
string company_name = json.get_string(company, "name");

// Get employees array
ptr employees = json.get_array(company, "employees");
int emp_count = json.array_size(employees);

// Access first employee
ptr emp0 = json.array_get_object(employees, 0);
string emp0_name = json.get_string(emp0, "name");
string emp0_role = json.get_string(emp0, "role");

// Access skills array of first employee
ptr emp0_skills = json.get_array(emp0, "skills");
string skill0 = json.array_get_string(emp0_skills, 0);
string skill1 = json.array_get_string(emp0_skills, 1);

output("Company: ", string);
output(company_name, string);
output("Employee: ", string);
output(emp0_name, string);
output("Role: ", string);
output(emp0_role, string);
output("Skills: ", string);
output(skill0, string);
output(", ", string);
output(skill1, string);
```

## Complete Basic Example

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

The JSON module has been fully tested with:
- ✅ Object creation and manipulation
- ✅ String values
- ✅ Integer values  
- ✅ Float values
- ✅ Boolean values
- ✅ Nested objects (multi-level)
- ✅ Nested arrays
- ✅ Arrays of objects
- ✅ Complex nested structures (objects with arrays of objects with arrays)
- ✅ JSON parsing
- ✅ JSON stringification
- ✅ Array size and element access

See test files:
- `testFiles/Json.pie` - Comprehensive nested structures example
- `test_json_simple.pie` - Basic JSON operations
