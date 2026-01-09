#ifndef PIE_SQLITE_H
#define PIE_SQLITE_H

#include "d_array.h"
#include <stdint.h>

// SQLite database handle (opaque pointer to sqlite3*)
typedef intptr_t pie_database;

// Open a SQLite database
// Returns database handle, or 0 on error
pie_database pie_sqlite_open(const char *path);

// Close a database connection
void pie_sqlite_close(pie_database db);

// Execute SQL statement (no result)
// Returns 1 on success, 0 on error
int pie_sqlite_exec(pie_database db, const char *sql);

// Execute SQL query and return results as array of dictionaries
// Each row is a dictionary with column names as keys
DArrayDict *pie_sqlite_query(pie_database db, const char *sql);

// Get the last error message for the database
const char *pie_sqlite_last_error(pie_database db);

// Transaction management
int pie_sqlite_begin(pie_database db);
int pie_sqlite_commit(pie_database db);
int pie_sqlite_rollback(pie_database db);

// Get number of rows changed by last INSERT/UPDATE/DELETE
int pie_sqlite_changes(pie_database db);

#endif // PIE_SQLITE_H
