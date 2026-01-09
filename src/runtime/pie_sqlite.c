#include "pie_sqlite.h"
#include "dict_lib.h"
#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Open a SQLite database
pie_database pie_sqlite_open(const char *path) {
  sqlite3 *db = NULL;
  int rc = sqlite3_open(path, &db);
  if (rc != SQLITE_OK) {
    if (db) {
      sqlite3_close(db);
    }
    return 0;
  }
  return (pie_database)db;
}

// Close a database connection
void pie_sqlite_close(pie_database db) {
  if (db) {
    sqlite3_close((sqlite3 *)db);
  }
}

// Execute SQL statement (no result)
int pie_sqlite_exec(pie_database db, const char *sql) {
  if (!db || !sql)
    return 0;

  char *err_msg = NULL;
  int rc = sqlite3_exec((sqlite3 *)db, sql, NULL, NULL, &err_msg);

  if (err_msg) {
    // Error message is stored internally by SQLite, we can retrieve it via
    // last_error
    sqlite3_free(err_msg);
  }

  return (rc == SQLITE_OK) ? 1 : 0;
}

// Callback data for query
typedef struct {
  DArrayDict *results;
  char **column_names;
  int column_count;
} QueryCallbackData;

// Callback function for sqlite3_exec that builds dict array
static int query_callback(void *data, int argc, char **argv, char **col_names) {
  QueryCallbackData *cb_data = (QueryCallbackData *)data;

  // Create a dictionary for this row
  Dictionary *row = dict_create();

  for (int i = 0; i < argc; i++) {
    if (argv[i] != NULL) {
      // Try to detect type: if it looks like a number, store as int or float
      char *endptr;
      long int_val = strtol(argv[i], &endptr, 10);

      if (*endptr == '\0' && strlen(argv[i]) > 0) {
        // Successfully parsed as integer
        DictValue *val = dict_value_create_int((int)int_val);
        dict_set(row, col_names[i], val);
      } else {
        // Check if it's a float
        double float_val = strtod(argv[i], &endptr);
        if (*endptr == '\0' && strlen(argv[i]) > 0 &&
            strchr(argv[i], '.') != NULL) {
          // Successfully parsed as float
          DictValue *val = dict_value_create_float(float_val);
          dict_set(row, col_names[i], val);
        } else {
          // Store as string
          DictValue *val = dict_value_create_string(argv[i]);
          dict_set(row, col_names[i], val);
        }
      }
    } else {
      // NULL value - store as empty string for now
      DictValue *val = dict_value_create_string("");
      dict_set(row, col_names[i], val);
    }
  }

  d_array_dict_append(cb_data->results, row);
  return 0;
}

// Execute SQL query and return results as array of dictionaries
DArrayDict *pie_sqlite_query(pie_database db, const char *sql) {
  if (!db || !sql)
    return d_array_dict_create();

  DArrayDict *results = d_array_dict_create();
  QueryCallbackData cb_data = {results, NULL, 0};

  char *err_msg = NULL;
  int rc = sqlite3_exec((sqlite3 *)db, sql, query_callback, &cb_data, &err_msg);

  if (err_msg) {
    sqlite3_free(err_msg);
  }

  // Return results even if there was an error (may be partial)
  return results;
}

// Get the last error message for the database
const char *pie_sqlite_last_error(pie_database db) {
  if (!db)
    return "Invalid database handle";
  return sqlite3_errmsg((sqlite3 *)db);
}

// Begin a transaction
int pie_sqlite_begin(pie_database db) {
  return pie_sqlite_exec(db, "BEGIN TRANSACTION");
}

// Commit a transaction
int pie_sqlite_commit(pie_database db) { return pie_sqlite_exec(db, "COMMIT"); }

// Rollback a transaction
int pie_sqlite_rollback(pie_database db) {
  return pie_sqlite_exec(db, "ROLLBACK");
}

// Get number of rows changed by last INSERT/UPDATE/DELETE
int pie_sqlite_changes(pie_database db) {
  if (!db)
    return 0;
  return sqlite3_changes((sqlite3 *)db);
}
