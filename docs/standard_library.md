# Standard Library

PIE includes a standard library with a rich set of built-in functions for various tasks.

## System Functions

| Function                  | Description                               |
|---------------------------|-------------------------------------------|
| `output(val, type, ...)`  | Prints a value to the console. The type of the value must be specified. For floats, an optional precision can be provided. |
| `input(var, type)`        | Reads a value from the console and stores it in the given variable. The type must be specified. |
| `exit()`                  | Exits the program.                        |

## Math Functions

| Function          | Description                               |
|-------------------|-------------------------------------------|
| `sqrt(x)`         | Returns the square root of `x`.           |
| `pow(base, exp)`  | Returns `base` raised to the power of `exp`. |
| `sin(x)`          | Returns the sine of `x`.                  |
| `cos(x)`          | Returns the cosine of `x`.                |
| `floor(x)`        | Returns the largest integer less than or equal to `x`. |
| `ceil(x)`         | Returns the smallest integer greater than or equal to `x`. |
| `rand()`          | Returns a random integer.                 |

## String Functions

| Function            | Description                               |
|---------------------|-------------------------------------------|
| `strlen(s)`         | Returns the length of the string `s`.     |
| `strcmp(s1, s2)`    | Compares two strings.                     |
| `strcpy(dest, src)` | Copies the string `src` to `dest`.        |
| `strcat(dest, src)` | Concatenates the string `src` onto the end of `dest`. |

## File I/O Functions

| Function                      | Description                               |
|-------------------------------|-------------------------------------------|
| `file_open(filename, mode)`   | Opens a file and returns a file handle.   |
| `file_close(file_handle)`     | Closes an open file.                      |
| `file_write(file_handle, content)` | Writes content to a file.            |
| `file_flush(file_handle)`     | Flushes the output buffer of a file.      |
| `file_read(file_handle, buffer, size)` | Reads `size` bytes from a file into a buffer. |
| `file_read_all(file_handle)`  | Reads the entire content of a file and returns it as a string. |
| `file_read_lines(file_handle)`| Reads all lines from a file and returns them as an array of strings. |

## Network Functions

| Function                      | Description                               |
|-------------------------------|-------------------------------------------|
| `tcp_socket()`                | Creates a new TCP socket.                 |
| `tcp_connect(sockfd, host, port)` | Connects a socket to a host and port. |
| `tcp_send(sockfd, data)`      | Sends data over a socket.                 |
| `tcp_recv(sockfd, buffer, size)` | Receives data from a socket.         |
| `tcp_close(sockfd)`           | Closes a socket.                          |

## Array and Dictionary Functions

See the [Arrays](./arrays.md) and [Dictionaries](./dictionaries.md) documentation for details on their respective functions.
