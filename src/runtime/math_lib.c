#include <math.h>
#include <stdlib.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef M_E
#define M_E 2.71828182845904523536
#endif

double pie_floor(double x) {
    return floor(x);
}

double pie_ceil(double x) {
    return ceil(x);
}

int pie_rand() {
    return rand();
}

void pie_srand(int seed) {
    srand(seed);
}

int pie_rand_range(int min, int max) {
    return min + rand() % (max - min + 1);
}

double pie_sqrt(double x) {
    return sqrt(x);
}

double pie_pow(double base, double exp) {
    return pow(base, exp);
}

double pie_sin(double x) {
    return sin(x);
}

double pie_cos(double x) {
    return cos(x);
}

double pie_tan(double x) {
    return tan(x);
}

double pie_asin(double x) {
    return asin(x);
}

double pie_acos(double x) {
    return acos(x);
}

double pie_atan(double x) {
    return atan(x);
}

double pie_log(double x) {
    return log(x);
}

double pie_log10(double x) {
    return log10(x);
}

double pie_exp(double x) {
    return exp(x);
}

double pie_abs(double x) {
    return fabs(x);
}

int pie_abs_int(int x) {
    return abs(x);
}

double pie_round(double x) {
    return round(x);
}

double pie_min(double a, double b) {
    return (a < b) ? a : b;
}

double pie_max(double a, double b) {
    return (a > b) ? a : b;
}

int pie_min_int(int a, int b) {
    return (a < b) ? a : b;
}

int pie_max_int(int a, int b) {
    return (a > b) ? a : b;
}

double pie_pi() {
    return M_PI;
}

double pie_e() {
    return M_E;
}

int pie_time() {
    return (int)time(NULL);
}
