#define _XOPEN_SOURCE 700
#include "pie_date.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

// Static arrays for weekday and month names
static const char* WEEKDAY_NAMES[] = {
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
};

static const char* MONTH_NAMES[] = {
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
};

// ============================================================================
// Current Time Functions
// ============================================================================

int pie_date_now(void) {
    return (int)time(NULL);
}

long long pie_date_now_millis(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (long long)(tv.tv_sec) * 1000 + (long long)(tv.tv_usec) / 1000;
}

// ============================================================================
// Formatting Functions
// ============================================================================

char* pie_date_format(int timestamp, const char* format) {
    if (!format) {
        return strdup("");
    }
    
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    
    if (!tm_info) {
        return strdup("");
    }
    
    // Allocate buffer for formatted string (256 should be enough for most formats)
    char* buffer = (char*)malloc(256);
    if (!buffer) {
        return strdup("");
    }
    
    size_t result = strftime(buffer, 256, format, tm_info);
    if (result == 0) {
        free(buffer);
        return strdup("");
    }
    
    return buffer;
}

char* pie_date_format_iso(int timestamp) {
    return pie_date_format(timestamp, "%Y-%m-%dT%H:%M:%S");
}

char* pie_date_format_date(int timestamp) {
    return pie_date_format(timestamp, "%Y-%m-%d");
}

char* pie_date_format_time(int timestamp) {
    return pie_date_format(timestamp, "%H:%M:%S");
}

// ============================================================================
// Parsing Functions
// ============================================================================

int pie_date_parse(const char* date_str, const char* format) {
    if (!date_str || !format) {
        return -1;
    }
    
    struct tm tm_info;
    memset(&tm_info, 0, sizeof(struct tm));
    
    char* result = strptime(date_str, format, &tm_info);
    if (!result) {
        return -1;
    }
    
    time_t timestamp = mktime(&tm_info);
    if (timestamp == -1) {
        return -1;
    }
    
    return (int)timestamp;
}

int pie_date_parse_iso(const char* iso_str) {
    if (!iso_str) {
        return -1;
    }
    
    // Try to parse ISO 8601 format: YYYY-MM-DDTHH:MM:SS
    struct tm tm_info;
    memset(&tm_info, 0, sizeof(struct tm));
    
    // Try with T separator first
    char* result = strptime(iso_str, "%Y-%m-%dT%H:%M:%S", &tm_info);
    
    // If that fails, try with space separator
    if (!result) {
        result = strptime(iso_str, "%Y-%m-%d %H:%M:%S", &tm_info);
    }
    
    // If that fails, try date only
    if (!result) {
        result = strptime(iso_str, "%Y-%m-%d", &tm_info);
    }
    
    if (!result) {
        return -1;
    }
    
    time_t timestamp = mktime(&tm_info);
    if (timestamp == -1) {
        return -1;
    }
    
    return (int)timestamp;
}

// ============================================================================
// Component Extraction Functions
// ============================================================================

int pie_date_get_year(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_year + 1900;
}

int pie_date_get_month(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_mon + 1;  // tm_mon is 0-11, we return 1-12
}

int pie_date_get_day(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_mday;
}

int pie_date_get_hour(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_hour;
}

int pie_date_get_minute(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_min;
}

int pie_date_get_second(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_sec;
}

int pie_date_get_weekday(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    if (!tm_info) return 0;
    return tm_info->tm_wday;  // 0 = Sunday, 6 = Saturday
}

const char* pie_date_get_weekday_name(int timestamp) {
    int weekday = pie_date_get_weekday(timestamp);
    if (weekday < 0 || weekday > 6) {
        return "";
    }
    return WEEKDAY_NAMES[weekday];
}

const char* pie_date_get_month_name(int timestamp) {
    int month = pie_date_get_month(timestamp);
    if (month < 1 || month > 12) {
        return "";
    }
    return MONTH_NAMES[month - 1];
}

// ============================================================================
// Date Arithmetic Functions
// ============================================================================

int pie_date_add_seconds(int timestamp, int seconds) {
    return timestamp + seconds;
}

int pie_date_add_minutes(int timestamp, int minutes) {
    return timestamp + (minutes * 60);
}

int pie_date_add_hours(int timestamp, int hours) {
    return timestamp + (hours * 3600);
}

int pie_date_add_days(int timestamp, int days) {
    return timestamp + (days * 86400);
}

// ============================================================================
// Date Difference Functions
// ============================================================================

int pie_date_diff_seconds(int timestamp1, int timestamp2) {
    return timestamp1 - timestamp2;
}

int pie_date_diff_minutes(int timestamp1, int timestamp2) {
    return (timestamp1 - timestamp2) / 60;
}

int pie_date_diff_hours(int timestamp1, int timestamp2) {
    return (timestamp1 - timestamp2) / 3600;
}

int pie_date_diff_days(int timestamp1, int timestamp2) {
    return (timestamp1 - timestamp2) / 86400;
}

// ============================================================================
// Date Property Functions
// ============================================================================

int pie_date_is_leap_year(int timestamp) {
    int year = pie_date_get_year(timestamp);
    
    // Leap year rules:
    // 1. Divisible by 4
    // 2. If divisible by 100, must also be divisible by 400
    if (year % 4 != 0) {
        return 0;
    } else if (year % 100 != 0) {
        return 1;
    } else if (year % 400 != 0) {
        return 0;
    } else {
        return 1;
    }
}

int pie_date_days_in_month(int timestamp) {
    int month = pie_date_get_month(timestamp);
    int year = pie_date_get_year(timestamp);
    
    // Days in each month
    static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    
    if (month < 1 || month > 12) {
        return 0;
    }
    
    int result = days[month - 1];
    
    // Check for leap year in February
    if (month == 2 && pie_date_is_leap_year(timestamp)) {
        result = 29;
    }
    
    return result;
}

int pie_date_start_of_day(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    
    if (!tm_info) {
        return timestamp;
    }
    
    // Set time to 00:00:00
    tm_info->tm_hour = 0;
    tm_info->tm_min = 0;
    tm_info->tm_sec = 0;
    
    return (int)mktime(tm_info);
}

int pie_date_end_of_day(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    
    if (!tm_info) {
        return timestamp;
    }
    
    // Set time to 23:59:59
    tm_info->tm_hour = 23;
    tm_info->tm_min = 59;
    tm_info->tm_sec = 59;
    
    return (int)mktime(tm_info);
}

int pie_date_start_of_month(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    
    if (!tm_info) {
        return timestamp;
    }
    
    // Set to first day of month at 00:00:00
    tm_info->tm_mday = 1;
    tm_info->tm_hour = 0;
    tm_info->tm_min = 0;
    tm_info->tm_sec = 0;
    
    return (int)mktime(tm_info);
}

int pie_date_end_of_month(int timestamp) {
    time_t time_val = (time_t)timestamp;
    struct tm* tm_info = localtime(&time_val);
    
    if (!tm_info) {
        return timestamp;
    }
    
    // Get days in this month
    int days = pie_date_days_in_month(timestamp);
    
    // Set to last day of month at 23:59:59
    tm_info->tm_mday = days;
    tm_info->tm_hour = 23;
    tm_info->tm_min = 59;
    tm_info->tm_sec = 59;
    
    return (int)mktime(tm_info);
}
