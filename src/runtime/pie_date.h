#ifndef PIE_DATE_H
#define PIE_DATE_H

// PIE Date Module - Date and Time Parsing, Formatting, and Manipulation
// Provides comprehensive date/time functionality for PIE programs

// ============================================================================
// Current Time Functions
// ============================================================================

/**
 * Get current Unix timestamp (seconds since epoch)
 * @return Current timestamp in seconds
 */
int pie_date_now(void);

/**
 * Get current time in milliseconds since epoch
 * @return Current timestamp in milliseconds
 */
long long pie_date_now_millis(void);

// ============================================================================
// Formatting Functions
// ============================================================================

/**
 * Format a Unix timestamp using strftime format string
 * @param timestamp Unix timestamp
 * @param format strftime format string (e.g., "%Y-%m-%d %H:%M:%S")
 * @return Formatted date string (caller must free)
 */
char* pie_date_format(int timestamp, const char* format);

/**
 * Format timestamp as ISO 8601 (YYYY-MM-DDTHH:MM:SS)
 * @param timestamp Unix timestamp
 * @return ISO 8601 formatted string (caller must free)
 */
char* pie_date_format_iso(int timestamp);

/**
 * Format timestamp as date only (YYYY-MM-DD)
 * @param timestamp Unix timestamp
 * @return Date string (caller must free)
 */
char* pie_date_format_date(int timestamp);

/**
 * Format timestamp as time only (HH:MM:SS)
 * @param timestamp Unix timestamp
 * @return Time string (caller must free)
 */
char* pie_date_format_time(int timestamp);

// ============================================================================
// Parsing Functions
// ============================================================================

/**
 * Parse a date string using strptime format and return Unix timestamp
 * @param date_str Date string to parse
 * @param format strptime format string (e.g., "%Y-%m-%d %H:%M:%S")
 * @return Unix timestamp or -1 on error
 */
int pie_date_parse(const char* date_str, const char* format);

/**
 * Parse ISO 8601 date string and return Unix timestamp
 * @param iso_str ISO 8601 formatted string (e.g., "2025-11-05T14:30:00")
 * @return Unix timestamp or -1 on error
 */
int pie_date_parse_iso(const char* iso_str);

// ============================================================================
// Component Extraction Functions
// ============================================================================

/**
 * Extract year from timestamp
 * @param timestamp Unix timestamp
 * @return Year (e.g., 2025)
 */
int pie_date_get_year(int timestamp);

/**
 * Extract month (1-12) from timestamp
 * @param timestamp Unix timestamp
 * @return Month (1=January, 12=December)
 */
int pie_date_get_month(int timestamp);

/**
 * Extract day of month (1-31) from timestamp
 * @param timestamp Unix timestamp
 * @return Day of month
 */
int pie_date_get_day(int timestamp);

/**
 * Extract hour (0-23) from timestamp
 * @param timestamp Unix timestamp
 * @return Hour
 */
int pie_date_get_hour(int timestamp);

/**
 * Extract minute (0-59) from timestamp
 * @param timestamp Unix timestamp
 * @return Minute
 */
int pie_date_get_minute(int timestamp);

/**
 * Extract second (0-59) from timestamp
 * @param timestamp Unix timestamp
 * @return Second
 */
int pie_date_get_second(int timestamp);

/**
 * Get day of week (0=Sunday, 6=Saturday)
 * @param timestamp Unix timestamp
 * @return Day of week (0-6)
 */
int pie_date_get_weekday(int timestamp);

/**
 * Get weekday name (e.g., 'Monday')
 * @param timestamp Unix timestamp
 * @return Weekday name (do not free - static string)
 */
const char* pie_date_get_weekday_name(int timestamp);

/**
 * Get month name (e.g., 'January')
 * @param timestamp Unix timestamp
 * @return Month name (do not free - static string)
 */
const char* pie_date_get_month_name(int timestamp);

// ============================================================================
// Date Arithmetic Functions
// ============================================================================

/**
 * Add seconds to timestamp
 * @param timestamp Unix timestamp
 * @param seconds Number of seconds to add (can be negative)
 * @return New timestamp
 */
int pie_date_add_seconds(int timestamp, int seconds);

/**
 * Add minutes to timestamp
 * @param timestamp Unix timestamp
 * @param minutes Number of minutes to add (can be negative)
 * @return New timestamp
 */
int pie_date_add_minutes(int timestamp, int minutes);

/**
 * Add hours to timestamp
 * @param timestamp Unix timestamp
 * @param hours Number of hours to add (can be negative)
 * @return New timestamp
 */
int pie_date_add_hours(int timestamp, int hours);

/**
 * Add days to timestamp
 * @param timestamp Unix timestamp
 * @param days Number of days to add (can be negative)
 * @return New timestamp
 */
int pie_date_add_days(int timestamp, int days);

// ============================================================================
// Date Difference Functions
// ============================================================================

/**
 * Get difference in seconds between two timestamps
 * @param timestamp1 First timestamp
 * @param timestamp2 Second timestamp
 * @return Difference in seconds (timestamp1 - timestamp2)
 */
int pie_date_diff_seconds(int timestamp1, int timestamp2);

/**
 * Get difference in minutes between two timestamps
 * @param timestamp1 First timestamp
 * @param timestamp2 Second timestamp
 * @return Difference in minutes (timestamp1 - timestamp2)
 */
int pie_date_diff_minutes(int timestamp1, int timestamp2);

/**
 * Get difference in hours between two timestamps
 * @param timestamp1 First timestamp
 * @param timestamp2 Second timestamp
 * @return Difference in hours (timestamp1 - timestamp2)
 */
int pie_date_diff_hours(int timestamp1, int timestamp2);

/**
 * Get difference in days between two timestamps
 * @param timestamp1 First timestamp
 * @param timestamp2 Second timestamp
 * @return Difference in days (timestamp1 - timestamp2)
 */
int pie_date_diff_days(int timestamp1, int timestamp2);

// ============================================================================
// Date Property Functions
// ============================================================================

/**
 * Check if year is a leap year
 * @param timestamp Unix timestamp
 * @return 1 if leap year, 0 otherwise
 */
int pie_date_is_leap_year(int timestamp);

/**
 * Get number of days in the month
 * @param timestamp Unix timestamp
 * @return Number of days in month (28-31)
 */
int pie_date_days_in_month(int timestamp);

/**
 * Get timestamp for start of day (00:00:00)
 * @param timestamp Unix timestamp
 * @return Timestamp at start of same day
 */
int pie_date_start_of_day(int timestamp);

/**
 * Get timestamp for end of day (23:59:59)
 * @param timestamp Unix timestamp
 * @return Timestamp at end of same day
 */
int pie_date_end_of_day(int timestamp);

/**
 * Get timestamp for first day of month at 00:00:00
 * @param timestamp Unix timestamp
 * @return Timestamp at start of month
 */
int pie_date_start_of_month(int timestamp);

/**
 * Get timestamp for last day of month at 23:59:59
 * @param timestamp Unix timestamp
 * @return Timestamp at end of month
 */
int pie_date_end_of_month(int timestamp);

#endif // PIE_DATE_H
