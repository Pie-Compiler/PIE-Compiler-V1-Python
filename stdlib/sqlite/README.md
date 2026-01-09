# SQLite Module for PIE

The `sqlite` module provides an interface to the SQLite3 database engine, allowing PIE programs to create, query, and manage local databases.

## Usage

Import the module at the top of your PIE file:

```pie
import sqlite;
```

## Types

### `database`
A handle to an open SQLite database connection.
- Internally represented as a 64-bit integer (pointer).
- Can be compared to `null` (or `0`) to check validity.

## API Reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `open` | `database(string path)` | Opens a database file. Returns a `database` handle or `null` on error. |
| `close` | `void(database db)` | Closes the database connection. |
| `exec` | `int(database db, string sql)` | Executes a SQL statement (e.g., CREATE, INSERT). Returns `1` on success, `0` on error. |
| `query` | `dict[](database db, string sql)` | Executes a SQL query (SELECT) and returns an array of dictionaries representing rows. |
| `last_error` | `string(database db)` | Returns the error message from the last failed operation. |
| `begin` | `int(database db)` | Begins a new transaction. Returns `1` on success. |
| `commit` | `int(database db)` | Commits the current transaction. Returns `1` on success. |
| `rollback` | `int(database db)` | Rolls back the current transaction. Returns `1` on success. |
| `changes` | `int(database db)` | Returns the number of rows modified by the last INSERT, UPDATE, or DELETE. |

## Example

```pie
import sqlite;

void main() {
    database db = sqlite.open("./data.db");
    
    if (db != null) {
        // Create a table
        if (sqlite.exec(db, "CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT)") == 0) {
            output("Error creating table: " + sqlite.last_error(db), string);
            return;
        }
        
        // Insert data
        sqlite.exec(db, "INSERT INTO items VALUES (1, 'Widget')");
        
        // Query data
        dict results[] = sqlite.query(db, "SELECT * FROM items");
        
        output("Found items: ", string);
        for (int i = 0; i < arr_size(results); i++) {
            dict row = results[i];
            string name = dict_get_string(row, "name");
            output(name, string);
        }
        
        sqlite.close(db);
    } else {
        output("Failed to open database", string);
    }
}
```

## Error Handling

Most functions accept a `database` handle. If an error occurs:
1. `open` returns `null`.
2. `exec` and transaction functions return `0`.
3. Use `sqlite.last_error(db)` to retrieve the specific error message.

## Dependencies
This module requires the `sqlite3` library to be installed on the system and linked during compilation.
