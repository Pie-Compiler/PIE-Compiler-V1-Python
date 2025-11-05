# PIE Date Module

The `date` module provides comprehensive date and time functionality for PIE programs, including parsing, formatting, arithmetic operations, and date manipulation.

## Installation

The date module is part of the PIE standard library and is located in `stdlib/date/`. It requires no external libraries beyond the standard C library.

## Usage

```pie
import date;

int main() {
    int now = date.now();
    string formatted = date.format_iso(now);
    output(formatted, string);
    return 0;
}
```

## API Reference

### Current Time Functions

#### `date.now() -> int`
Get the current Unix timestamp (seconds since epoch).

```pie
int timestamp = date.now();
output(timestamp, int);  // e.g., 1762342270
```

#### `date.now_millis() -> int`
Get the current time in milliseconds since epoch.

```pie
int ms = date.now_millis();
```

### Formatting Functions

#### `date.format(timestamp, format) -> string`
Format a Unix timestamp using strftime format string.

```pie
int now = date.now();
string custom = date.format(now, "%A, %B %d, %Y at %I:%M %p");
// Output: "Wednesday, November 05, 2025 at 02:31 PM"
```

Common format specifiers:
- `%Y` - 4-digit year (2025)
- `%m` - Month (01-12)
- `%d` - Day of month (01-31)
- `%H` - Hour 24-hour (00-23)
- `%I` - Hour 12-hour (01-12)
- `%M` - Minute (00-59)
- `%S` - Second (00-59)
- `%p` - AM/PM
- `%A` - Full weekday name
- `%B` - Full month name

#### `date.format_iso(timestamp) -> string`
Format timestamp as ISO 8601 (YYYY-MM-DDTHH:MM:SS).

```pie
string iso = date.format_iso(now);
// Output: "2025-11-05T14:31:10"
```

#### `date.format_date(timestamp) -> string`
Format timestamp as date only (YYYY-MM-DD).

```pie
string dateOnly = date.format_date(now);
// Output: "2025-11-05"
```

#### `date.format_time(timestamp) -> string`
Format timestamp as time only (HH:MM:SS).

```pie
string timeOnly = date.format_time(now);
// Output: "14:31:10"
```

### Parsing Functions

#### `date.parse(date_str, format) -> int`
Parse a date string using strptime format and return Unix timestamp. Returns -1 on error.

```pie
int parsed = date.parse("2025/12/25", "%Y/%m/%d");
```

#### `date.parse_iso(iso_str) -> int`
Parse ISO 8601 date string and return Unix timestamp. Supports formats:
- `YYYY-MM-DDTHH:MM:SS`
- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DD`

```pie
int christmas = date.parse_iso("2025-12-25T00:00:00");
```

### Component Extraction

#### `date.get_year(timestamp) -> int`
Extract year from timestamp.

```pie
int year = date.get_year(now);  // e.g., 2025
```

#### `date.get_month(timestamp) -> int`
Extract month (1-12) from timestamp.

```pie
int month = date.get_month(now);  // 1 = January, 12 = December
```

#### `date.get_day(timestamp) -> int`
Extract day of month (1-31) from timestamp.

```pie
int day = date.get_day(now);
```

#### `date.get_hour(timestamp) -> int`
Extract hour (0-23) from timestamp.

```pie
int hour = date.get_hour(now);
```

#### `date.get_minute(timestamp) -> int`
Extract minute (0-59) from timestamp.

```pie
int minute = date.get_minute(now);
```

#### `date.get_second(timestamp) -> int`
Extract second (0-59) from timestamp.

```pie
int second = date.get_second(now);
```

#### `date.get_weekday(timestamp) -> int`
Get day of week (0=Sunday, 6=Saturday).

```pie
int weekday = date.get_weekday(now);  // 0-6
```

#### `date.get_weekday_name(timestamp) -> string`
Get weekday name (e.g., 'Monday').

```pie
string dayName = date.get_weekday_name(now);  // "Wednesday"
```

#### `date.get_month_name(timestamp) -> string`
Get month name (e.g., 'January').

```pie
string monthName = date.get_month_name(now);  // "November"
```

### Date Arithmetic

#### `date.add_seconds(timestamp, seconds) -> int`
Add seconds to timestamp (can be negative to subtract).

```pie
int later = date.add_seconds(now, 3600);  // 1 hour later
int earlier = date.add_seconds(now, -3600);  // 1 hour earlier
```

#### `date.add_minutes(timestamp, minutes) -> int`
Add minutes to timestamp.

```pie
int later = date.add_minutes(now, 30);  // 30 minutes later
```

#### `date.add_hours(timestamp, hours) -> int`
Add hours to timestamp.

```pie
int tomorrow_same_time = date.add_hours(now, 24);
```

#### `date.add_days(timestamp, days) -> int`
Add days to timestamp.

```pie
int tomorrow = date.add_days(now, 1);
int yesterday = date.add_days(now, -1);
int next_week = date.add_days(now, 7);
```

### Date Differences

#### `date.diff_seconds(timestamp1, timestamp2) -> int`
Get difference in seconds between two timestamps (timestamp1 - timestamp2).

```pie
int diff = date.diff_seconds(future, now);
```

#### `date.diff_minutes(timestamp1, timestamp2) -> int`
Get difference in minutes between two timestamps.

```pie
int diffMinutes = date.diff_minutes(later, now);
```

#### `date.diff_hours(timestamp1, timestamp2) -> int`
Get difference in hours between two timestamps.

```pie
int diffHours = date.diff_hours(tomorrow, now);
```

#### `date.diff_days(timestamp1, timestamp2) -> int`
Get difference in days between two timestamps.

```pie
int daysUntil = date.diff_days(christmas, now);
```

### Date Properties

#### `date.is_leap_year(timestamp) -> int`
Check if year is a leap year (returns 1 for true, 0 for false).

```pie
int isLeap = date.is_leap_year(now);
if (isLeap == 1) {
    output("This is a leap year\n", string);
}
```

#### `date.days_in_month(timestamp) -> int`
Get number of days in the month (28-31).

```pie
int days = date.days_in_month(now);
```

#### `date.start_of_day(timestamp) -> int`
Get timestamp for start of day (00:00:00).

```pie
int startOfDay = date.start_of_day(now);
string time = date.format_time(startOfDay);  // "00:00:00"
```

#### `date.end_of_day(timestamp) -> int`
Get timestamp for end of day (23:59:59).

```pie
int endOfDay = date.end_of_day(now);
```

#### `date.start_of_month(timestamp) -> int`
Get timestamp for first day of month at 00:00:00.

```pie
int startOfMonth = date.start_of_month(now);
```

#### `date.end_of_month(timestamp) -> int`
Get timestamp for last day of month at 23:59:59.

```pie
int endOfMonth = date.end_of_month(now);
```

## Examples

### Working with JSON API Responses

```pie
import date;
import json;

int main() {
    string response = "{\"created_at\":\"2025-11-05T10:30:00\"}";
    ptr data = json.parse(response);
    string createdStr = json.get_string(data, "created_at");
    
    int createdAt = date.parse_iso(createdStr);
    output("Created: ", string);
    output(date.format(createdAt, "%A, %B %d at %I:%M %p"), string);
    
    return 0;
}
```

### Event Countdown

```pie
import date;

int main() {
    int now = date.now();
    int christmas = date.parse_iso("2025-12-25T00:00:00");
    
    int daysUntil = date.diff_days(christmas, now);
    output("Days until Christmas: ", string);
    output(daysUntil, int);
    output("\n", string);
    
    return 0;
}
```

### Billing Period Calculation

```pie
import date;

int main() {
    int now = date.now();
    int billingStart = date.start_of_month(now);
    int billingEnd = date.end_of_month(now);
    
    int daysInPeriod = date.days_in_month(now);
    int daysElapsed = date.diff_days(now, billingStart);
    int daysRemaining = date.diff_days(billingEnd, now);
    
    output("Billing period: ", string);
    output(date.format_date(billingStart), string);
    output(" to ", string);
    output(date.format_date(billingEnd), string);
    output("\n", string);
    
    output("Days elapsed: ", string);
    output(daysElapsed, int);
    output(" / ", string);
    output(daysInPeriod, int);
    output("\n", string);
    
    return 0;
}
```

### Logging with Timestamps

```pie
import date;

int main() {
    int now = date.now();
    
    output("[", string);
    output(date.format(now, "%Y-%m-%d %H:%M:%S"), string);
    output("] INFO: System started\n", string);
    
    int later = date.add_minutes(now, 5);
    output("[", string);
    output(date.format(later, "%Y-%m-%d %H:%M:%S"), string);
    output("] INFO: User logged in\n", string);
    
    return 0;
}
```

## Implementation Details

The date module is implemented in C (`pie_date.c`) using the standard C library's time functions:
- `time()` for current timestamp
- `gettimeofday()` for millisecond precision
- `localtime()` for breaking down timestamps
- `mktime()` for composing timestamps
- `strftime()` for formatting
- `strptime()` for parsing

All timestamps are Unix timestamps (seconds since January 1, 1970, 00:00:00 UTC), which makes them easy to store, compare, and manipulate.

## Thread Safety

The current implementation uses `localtime()` which is not thread-safe. In a multi-threaded environment, consider using `localtime_r()` instead.

## Time Zones

All date functions use the local time zone of the system. For UTC operations, the underlying C functions could be modified to use `gmtime()` instead of `localtime()`.
