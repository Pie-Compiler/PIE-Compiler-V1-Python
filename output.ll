; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@my_int = internal global i32 42
@my_float = internal global double 3.141590e+00
@my_char = internal global i8 81
@.str0 = internal constant [44 x i8] c"The quick brown fox jumps over the lazy dog\00"
@my_string = internal global ptr @.str0
@numbers = internal global ptr null
@fibonacci = internal global ptr null
@animals = internal global ptr null
@colors = internal global ptr null
@letters = internal global ptr null
@vowels = internal global ptr null
@prices = internal global ptr null
@coordinates = internal global ptr null
@person = internal global ptr null
@config = internal global ptr null
@sum_result = internal global i32 15
@diff_result = internal global i32 7
@mult_result = internal global i32 42
@div_result = internal global double 5.000000e+00
@mod_result = internal global i32 2
@float_sum = internal global double 1.280000e+01
@float_div = internal global double 0x4009249249249249
@pi_value = internal global double 0.000000e+00
@e_value = internal global double 0.000000e+00
@angle = internal global double 0.000000e+00
@sin_45 = internal global double 0.000000e+00
@cos_45 = internal global double 0.000000e+00
@tan_45 = internal global double 0.000000e+00
@power_result = internal global double 0.000000e+00
@sqrt_result = internal global double 0.000000e+00
@round_up = internal global double 0.000000e+00
@round_down = internal global double 0.000000e+00
@floor_result = internal global double 0.000000e+00
@ceil_result = internal global double 0.000000e+00
@abs_result = internal global double 0.000000e+00
@abs_int_result = internal global i32 0
@min_result = internal global double 0.000000e+00
@max_result = internal global double 0.000000e+00
@min_int_result = internal global i32 0
@max_int_result = internal global i32 0
@.str1 = internal constant [6 x i8] c"Hello\00"
@hello = internal global ptr @.str1
@.str2 = internal constant [6 x i8] c"World\00"
@world = internal global ptr @.str2
@greeting = internal global ptr null
@str_length = internal global i32 0
@numbers_size = internal global i32 0
@animals_size = internal global i32 0
@letters_size = internal global i32 0
@search_index = internal global i32 0
@not_found = internal global i32 0
@more_numbers = internal global ptr null
@combined = internal global ptr null
@numbers_avg = internal global double 0.000000e+00
@prices_avg = internal global double 0.000000e+00
@person_name = internal global ptr null
@person_age = internal global i32 0
@person_height = internal global double 0.000000e+00
@cmp_result = internal global i32 0
@a = internal global i32 10
@b = internal global i32 20
@.str3 = internal constant [4 x i8] c"fox\00"
@.str4 = internal constant [4 x i8] c"dog\00"
@.str5 = internal constant [4 x i8] c"cat\00"
@.str6 = internal constant [5 x i8] c"bird\00"
@.str7 = internal constant [4 x i8] c"red\00"
@.str8 = internal constant [6 x i8] c"green\00"
@.str9 = internal constant [5 x i8] c"blue\00"
@.str10 = internal constant [5 x i8] c"name\00"
@.str11 = internal constant [9 x i8] c"John Fox\00"
@.str12 = internal constant [4 x i8] c"age\00"
@.str13 = internal constant [7 x i8] c"height\00"
@.str14 = internal constant [6 x i8] c"debug\00"
@.str15 = internal constant [8 x i8] c"timeout\00"
@.str16 = internal constant [5 x i8] c"host\00"
@.str17 = internal constant [10 x i8] c"localhost\00"
@.str18 = internal constant [6 x i8] c"zebra\00"
@.str19 = internal constant [6 x i8] c"apple\00"
@.str20 = internal constant [7 x i8] c"banana\00"
@.str21 = internal constant [29 x i8] c"=== Basic Variable Tests ===\00"
@.str22 = internal constant [9 x i8] c"Integer:\00"
@.str23 = internal constant [7 x i8] c"Float:\00"
@.str24 = internal constant [11 x i8] c"Character:\00"
@.str25 = internal constant [65 x i8] c"================================================================\00"
@.str26 = internal constant [38 x i8] c"PIE COMPILER COMPREHENSIVE TEST SUITE\00"
@.str27 = internal constant [36 x i8] c"Testing all major language features\00"
@.str28 = internal constant [9 x i8] c"elephant\00"
@.str29 = internal constant [23 x i8] c"=== Variable Tests ===\00"
@.str30 = internal constant [15 x i8] c"String length:\00"
@.str31 = internal constant [28 x i8] c"=== Math Function Tests ===\00"
@.str32 = internal constant [10 x i8] c"Pi value:\00"
@.str33 = internal constant [9 x i8] c"E value:\00"
@.str34 = internal constant [17 x i8] c"Sin(45 degrees):\00"
@.str35 = internal constant [17 x i8] c"Cos(45 degrees):\00"
@.str36 = internal constant [6 x i8] c"2^3 =\00"
@.str37 = internal constant [20 x i8] c"Square root of 16 =\00"
@.str38 = internal constant [12 x i8] c"Round(3.7):\00"
@.str39 = internal constant [12 x i8] c"Floor(3.9):\00"
@.str40 = internal constant [11 x i8] c"Ceil(3.1):\00"
@.str41 = internal constant [11 x i8] c"Abs(-5.5):\00"
@.str42 = internal constant [15 x i8] c"Min(3.5, 7.2):\00"
@.str43 = internal constant [12 x i8] c"Max(15, 8):\00"
@.str44 = internal constant [30 x i8] c"=== Array Operations Test ===\00"
@.str45 = internal constant [25 x i8] c"Numbers array contains 3\00"
@.str46 = internal constant [27 x i8] c"Animals array contains fox\00"
@.str47 = internal constant [20 x i8] c"Numbers array size:\00"
@.str48 = internal constant [20 x i8] c"Animals array size:\00"
@.str49 = internal constant [17 x i8] c"Numbers average:\00"
@.str50 = internal constant [16 x i8] c"Prices average:\00"
@.str51 = internal constant [14 x i8] c"First number:\00"
@.str52 = internal constant [14 x i8] c"First animal:\00"
@.str53 = internal constant [14 x i8] c"First letter:\00"
@.str54 = internal constant [35 x i8] c"=== Dictionary Operations Test ===\00"
@.str55 = internal constant [13 x i8] c"Person name:\00"
@.str56 = internal constant [12 x i8] c"Person age:\00"
@.str57 = internal constant [15 x i8] c"Person height:\00"
@.str58 = internal constant [30 x i8] c"=== String Functions Test ===\00"
@.str59 = internal constant [23 x i8] c"Concatenated greeting:\00"
@.str60 = internal constant [33 x i8] c"strcmp result (apple vs banana):\00"
@.str61 = internal constant [34 x i8] c"=== Comparison Operators Test ===\00"
@.str62 = internal constant [21 x i8] c"Equality test passed\00"
@.str63 = internal constant [23 x i8] c"Inequality test passed\00"
@.str64 = internal constant [22 x i8] c"Less than test passed\00"
@.str65 = internal constant [25 x i8] c"Greater than test passed\00"
@.str66 = internal constant [31 x i8] c"Less than or equal test passed\00"
@.str67 = internal constant [34 x i8] c"Greater than or equal test passed\00"
@.str68 = internal constant [23 x i8] c"=== Array Contents ===\00"
@.str69 = internal constant [15 x i8] c"Numbers array:\00"
@.str70 = internal constant [15 x i8] c"Animals array:\00"
@.str71 = internal constant [15 x i8] c"Letters array:\00"
@.str72 = internal constant [14 x i8] c"Prices array:\00"
@.str73 = internal constant [16 x i8] c"Combined array:\00"
@.str74 = internal constant [21 x i8] c"=== Test Summary ===\00"
@.str75 = internal constant [49 x i8] c"Primitive types tested: int, float, char, string\00"
@.str76 = internal constant [53 x i8] c"Array types tested: int[], string[], char[], float[]\00"
@.str77 = internal constant [63 x i8] c"Dictionary operations tested: static initialization and access\00"
@.str78 = internal constant [54 x i8] c"Math functions tested: trigonometry, powers, rounding\00"
@.str79 = internal constant [60 x i8] c"String operations tested: concatenation, length, comparison\00"
@.str80 = internal constant [50 x i8] c"Control flow tested: conditionals and comparisons\00"
@.str81 = internal constant [59 x i8] c"Array functions tested: push, size, contains, indexof, avg\00"
@.str82 = internal constant [30 x i8] c"Total variables created: ~50+\00"
@.str83 = internal constant [29 x i8] c"Total functions called: ~20+\00"
@.str84 = internal constant [34 x i8] c"PIE Compiler Test Suite: COMPLETE\00"
@.str85 = internal constant [34 x i8] c"All tests completed successfully!\00"
@.str86 = internal constant [50 x i8] c"The quick brown fox has tested every PIE feature!\00"

declare void @input_int(ptr)

declare void @input_float(ptr)

declare void @input_string(ptr)

declare void @input_char(ptr)

declare void @output_int(i32)

declare void @output_string(ptr)

declare void @output_char(i8)

declare void @output_float(double, i32)

declare void @pie_exit()

declare double @pie_sqrt(double)

declare double @pie_pow(double, double)

declare double @pie_sin(double)

declare double @pie_cos(double)

declare double @pie_tan(double)

declare double @pie_asin(double)

declare double @pie_acos(double)

declare double @pie_atan(double)

declare double @pie_log(double)

declare double @pie_log10(double)

declare double @pie_exp(double)

declare double @pie_floor(double)

declare double @pie_ceil(double)

declare double @pie_round(double)

declare double @pie_abs(double)

declare i32 @pie_abs_int(i32)

declare double @pie_min(double, double)

declare double @pie_max(double, double)

declare i32 @pie_min_int(i32, i32)

declare i32 @pie_max_int(i32, i32)

declare i32 @pie_rand()

declare void @pie_srand(i32)

declare i32 @pie_rand_range(i32, i32)

declare double @pie_pi()

declare double @pie_e()

declare i32 @pie_time()

declare ptr @concat_strings(ptr, ptr)

declare i32 @pie_strlen(ptr)

declare i32 @pie_strcmp(ptr, ptr)

declare ptr @pie_strcpy(ptr, ptr)

declare ptr @pie_strcat(ptr, ptr)

declare ptr @string_to_upper(ptr)

declare ptr @string_to_lower(ptr)

declare ptr @string_trim(ptr)

declare ptr @string_substring(ptr, i32, i32)

declare i32 @string_index_of(ptr, ptr)

declare ptr @string_replace_char(ptr, i8, i8)

declare ptr @string_reverse(ptr)

declare i32 @string_count_char(ptr, i8)

declare i64 @file_open(ptr, ptr)

declare void @file_close(i64)

declare void @file_write(i64, ptr)

declare ptr @file_read_all(i64)

declare ptr @file_read_line(i64)

declare ptr @dict_create()

declare void @dict_set(ptr, ptr, ptr)

declare ptr @dict_get(ptr, ptr)

declare i32 @dict_get_int(ptr, ptr)

declare double @dict_get_float(ptr, ptr)

declare ptr @dict_get_string(ptr, ptr)

declare i32 @dict_has_key(ptr, ptr)

declare i32 @dict_key_exists(ptr, ptr)

declare void @dict_delete(ptr, ptr)

declare void @dict_free(ptr)

declare ptr @dict_value_create_int(i32)

declare ptr @dict_value_create_float(double)

declare ptr @dict_value_create_string(ptr)

declare ptr @dict_value_create_null()

declare ptr @new_int(i32)

declare ptr @new_float(double)

declare ptr @new_string(ptr)

declare i32 @is_variable_defined(ptr)

declare i32 @is_variable_null(ptr)

declare i32 @string_contains(ptr, ptr)

declare i32 @string_starts_with(ptr, ptr)

declare i32 @string_ends_with(ptr, ptr)

declare i32 @string_is_empty(ptr)

declare void @d_array_int_push(ptr, i32)

declare i32 @d_array_int_pop(ptr)

declare i32 @d_array_int_size(ptr)

declare i32 @d_array_int_contains(ptr, i32)

declare i32 @d_array_int_indexof(ptr, i32)

declare ptr @d_array_int_concat(ptr, ptr)

declare double @d_array_int_avg(ptr)

declare i32 @d_array_int_get(ptr, i32)

declare void @d_array_int_set(ptr, i32, i32)

declare void @d_array_string_push(ptr, ptr)

declare ptr @d_array_string_pop(ptr)

declare i32 @d_array_string_size(ptr)

declare i32 @d_array_string_contains(ptr, ptr)

declare i32 @d_array_string_indexof(ptr, ptr)

declare ptr @d_array_string_concat(ptr, ptr)

declare ptr @d_array_string_get(ptr, i32)

declare void @d_array_string_set(ptr, i32, ptr)

declare void @d_array_float_push(ptr, double)

declare double @d_array_float_pop(ptr)

declare i32 @d_array_float_size(ptr)

declare i32 @d_array_float_contains(ptr, double)

declare i32 @d_array_float_indexof(ptr, double)

declare double @d_array_float_avg(ptr)

declare ptr @d_array_int_create()

declare ptr @d_array_string_create()

declare ptr @d_array_float_create()

declare void @d_array_int_append(ptr, i32)

declare void @d_array_string_append(ptr, ptr)

declare void @d_array_float_append(ptr, double)

declare double @d_array_float_get(ptr, i32)

declare void @d_array_float_set(ptr, i32, double)

declare void @d_array_float_free(ptr)

declare void @print_int_array(ptr)

declare void @print_string_array(ptr)

declare void @print_float_array(ptr)

declare void @print_char_array(ptr)

declare ptr @d_array_char_create()

declare void @d_array_char_append(ptr, i8)

declare i8 @d_array_char_get(ptr, i32)

declare void @d_array_char_set(ptr, i32, i8)

declare i32 @d_array_char_size(ptr)

declare void @d_array_char_free(ptr)

declare i8 @d_array_char_pop(ptr)

declare i1 @d_array_char_contains(ptr, i8)

declare i32 @d_array_char_indexof(ptr, i8)

declare ptr @d_array_char_concat(ptr, ptr)

define i32 @main() {
entry:
  %.2 = call ptr @d_array_int_create()
  store ptr %.2, ptr @numbers, align 8
  call void @d_array_int_append(ptr %.2, i32 1)
  call void @d_array_int_append(ptr %.2, i32 2)
  call void @d_array_int_append(ptr %.2, i32 3)
  call void @d_array_int_append(ptr %.2, i32 4)
  call void @d_array_int_append(ptr %.2, i32 5)
  %.9 = call ptr @d_array_int_create()
  store ptr %.9, ptr @fibonacci, align 8
  call void @d_array_int_append(ptr %.9, i32 1)
  call void @d_array_int_append(ptr %.9, i32 1)
  call void @d_array_int_append(ptr %.9, i32 2)
  call void @d_array_int_append(ptr %.9, i32 3)
  call void @d_array_int_append(ptr %.9, i32 5)
  call void @d_array_int_append(ptr %.9, i32 8)
  call void @d_array_int_append(ptr %.9, i32 13)
  %.18 = call ptr @d_array_string_create()
  store ptr %.18, ptr @animals, align 8
  %.20 = bitcast ptr @.str3 to ptr
  call void @d_array_string_append(ptr %.18, ptr %.20)
  %.22 = bitcast ptr @.str4 to ptr
  call void @d_array_string_append(ptr %.18, ptr %.22)
  %.24 = bitcast ptr @.str5 to ptr
  call void @d_array_string_append(ptr %.18, ptr %.24)
  %.26 = bitcast ptr @.str6 to ptr
  call void @d_array_string_append(ptr %.18, ptr %.26)
  %.28 = call ptr @d_array_string_create()
  store ptr %.28, ptr @colors, align 8
  %.30 = bitcast ptr @.str7 to ptr
  call void @d_array_string_append(ptr %.28, ptr %.30)
  %.32 = bitcast ptr @.str8 to ptr
  call void @d_array_string_append(ptr %.28, ptr %.32)
  %.34 = bitcast ptr @.str9 to ptr
  call void @d_array_string_append(ptr %.28, ptr %.34)
  %.36 = call ptr @d_array_char_create()
  store ptr %.36, ptr @letters, align 8
  call void @d_array_char_append(ptr %.36, i8 65)
  call void @d_array_char_append(ptr %.36, i8 66)
  call void @d_array_char_append(ptr %.36, i8 67)
  call void @d_array_char_append(ptr %.36, i8 68)
  %.42 = call ptr @d_array_char_create()
  store ptr %.42, ptr @vowels, align 8
  call void @d_array_char_append(ptr %.42, i8 97)
  call void @d_array_char_append(ptr %.42, i8 101)
  call void @d_array_char_append(ptr %.42, i8 105)
  call void @d_array_char_append(ptr %.42, i8 111)
  call void @d_array_char_append(ptr %.42, i8 117)
  %.49 = call ptr @d_array_float_create()
  store ptr %.49, ptr @prices, align 8
  call void @d_array_float_append(ptr %.49, double 1.999000e+01)
  call void @d_array_float_append(ptr %.49, double 2.999000e+01)
  call void @d_array_float_append(ptr %.49, double 3.999000e+01)
  %.54 = call ptr @d_array_float_create()
  store ptr %.54, ptr @coordinates, align 8
  call void @d_array_float_append(ptr %.54, double 1.500000e+00)
  call void @d_array_float_append(ptr %.54, double 2.700000e+00)
  call void @d_array_float_append(ptr %.54, double 3.800000e+00)
  call void @d_array_float_append(ptr %.54, double 4.200000e+00)
  %.60 = call ptr @d_array_int_create()
  store ptr %.60, ptr @more_numbers, align 8
  call void @d_array_int_append(ptr %.60, i32 7)
  call void @d_array_int_append(ptr %.60, i32 8)
  call void @d_array_int_append(ptr %.60, i32 9)
  %.65 = call ptr @d_array_int_create()
  store ptr %.65, ptr @combined, align 8
  %.67 = load ptr, ptr @numbers, align 8
  %.68 = load ptr, ptr @more_numbers, align 8
  %.69 = load ptr, ptr @numbers, align 8
  %.70 = load ptr, ptr @more_numbers, align 8
  %concat_array_tmp = call ptr @d_array_int_concat(ptr %.69, ptr %.70)
  store ptr %concat_array_tmp, ptr @combined, align 8
  %.72 = call ptr @dict_create()
  %.73 = bitcast ptr @.str10 to ptr
  %.74 = bitcast ptr @.str11 to ptr
  %.75 = call ptr @new_string(ptr %.74)
  call void @dict_set(ptr %.72, ptr %.73, ptr %.75)
  %.77 = bitcast ptr @.str12 to ptr
  %.78 = call ptr @new_int(i32 30)
  call void @dict_set(ptr %.72, ptr %.77, ptr %.78)
  %.80 = bitcast ptr @.str13 to ptr
  %.81 = call ptr @new_float(double 5.900000e+00)
  call void @dict_set(ptr %.72, ptr %.80, ptr %.81)
  store ptr %.72, ptr @person, align 8
  %.84 = call ptr @dict_create()
  %.85 = bitcast ptr @.str14 to ptr
  %.86 = call ptr @new_int(i32 1)
  call void @dict_set(ptr %.84, ptr %.85, ptr %.86)
  %.88 = bitcast ptr @.str15 to ptr
  %.89 = call ptr @new_float(double 3.050000e+01)
  call void @dict_set(ptr %.84, ptr %.88, ptr %.89)
  %.91 = bitcast ptr @.str16 to ptr
  %.92 = bitcast ptr @.str17 to ptr
  %.93 = call ptr @new_string(ptr %.92)
  call void @dict_set(ptr %.84, ptr %.91, ptr %.93)
  store ptr %.84, ptr @config, align 8
  %call_tmp = call double @pie_pi()
  store double %call_tmp, ptr @pi_value, align 8
  %call_tmp.1 = call double @pie_e()
  store double %call_tmp.1, ptr @e_value, align 8
  %.98 = load double, ptr @pi_value, align 8
  %f_tmp = fdiv double %.98, 4.000000e+00
  store double %f_tmp, ptr @angle, align 8
  %.100 = load double, ptr @angle, align 8
  %call_tmp.2 = call double @pie_sin(double %.100)
  store double %call_tmp.2, ptr @sin_45, align 8
  %.102 = load double, ptr @angle, align 8
  %call_tmp.3 = call double @pie_cos(double %.102)
  store double %call_tmp.3, ptr @cos_45, align 8
  %.104 = load double, ptr @angle, align 8
  %call_tmp.4 = call double @pie_tan(double %.104)
  store double %call_tmp.4, ptr @tan_45, align 8
  %call_tmp.5 = call double @pie_pow(double 2.000000e+00, double 3.000000e+00)
  store double %call_tmp.5, ptr @power_result, align 8
  %call_tmp.6 = call double @pie_sqrt(double 1.600000e+01)
  store double %call_tmp.6, ptr @sqrt_result, align 8
  %call_tmp.7 = call double @pie_round(double 3.700000e+00)
  store double %call_tmp.7, ptr @round_up, align 8
  %call_tmp.8 = call double @pie_round(double 3.200000e+00)
  store double %call_tmp.8, ptr @round_down, align 8
  %call_tmp.9 = call double @pie_floor(double 3.900000e+00)
  store double %call_tmp.9, ptr @floor_result, align 8
  %call_tmp.10 = call double @pie_ceil(double 3.100000e+00)
  store double %call_tmp.10, ptr @ceil_result, align 8
  %f_neg_tmp = fsub double 0.000000e+00, 5.500000e+00
  %call_tmp.11 = call double @pie_abs(double %f_neg_tmp)
  store double %call_tmp.11, ptr @abs_result, align 8
  %i_neg_tmp = sub i32 0, 10
  %call_tmp.12 = call i32 @pie_abs_int(i32 %i_neg_tmp)
  store i32 %call_tmp.12, ptr @abs_int_result, align 4
  %call_tmp.13 = call double @pie_min(double 3.500000e+00, double 7.200000e+00)
  store double %call_tmp.13, ptr @min_result, align 8
  %call_tmp.14 = call double @pie_max(double 3.500000e+00, double 7.200000e+00)
  store double %call_tmp.14, ptr @max_result, align 8
  %call_tmp.15 = call i32 @pie_min_int(i32 15, i32 8)
  store i32 %call_tmp.15, ptr @min_int_result, align 4
  %call_tmp.16 = call i32 @pie_max_int(i32 15, i32 8)
  store i32 %call_tmp.16, ptr @max_int_result, align 4
  %.118 = load ptr, ptr @hello, align 8
  %.119 = load ptr, ptr @world, align 8
  %call_tmp.17 = call ptr @concat_strings(ptr %.118, ptr %.119)
  store ptr %call_tmp.17, ptr @greeting, align 8
  %.121 = load ptr, ptr @my_string, align 8
  %call_tmp.18 = call i32 @pie_strlen(ptr %.121)
  store i32 %call_tmp.18, ptr @str_length, align 4
  %.123 = load ptr, ptr @numbers, align 8
  %.124 = call i32 @d_array_int_size(ptr %.123)
  store i32 %.124, ptr @numbers_size, align 4
  %.126 = load ptr, ptr @animals, align 8
  %.127 = call i32 @d_array_string_size(ptr %.126)
  store i32 %.127, ptr @animals_size, align 4
  %.129 = load ptr, ptr @letters, align 8
  %.130 = call i32 @d_array_char_size(ptr %.129)
  store i32 %.130, ptr @letters_size, align 4
  %.132 = load ptr, ptr @numbers, align 8
  %.133 = call i32 @d_array_int_indexof(ptr %.132, i32 3)
  store i32 %.133, ptr @search_index, align 4
  %.135 = load ptr, ptr @animals, align 8
  %.136 = bitcast ptr @.str18 to ptr
  %.137 = call i32 @d_array_string_indexof(ptr %.135, ptr %.136)
  store i32 %.137, ptr @not_found, align 4
  %.139 = load ptr, ptr @numbers, align 8
  %.140 = call double @d_array_int_avg(ptr %.139)
  store double %.140, ptr @numbers_avg, align 8
  %.142 = load ptr, ptr @prices, align 8
  %.143 = call double @d_array_float_avg(ptr %.142)
  store double %.143, ptr @prices_avg, align 8
  %.145 = load ptr, ptr @person, align 8
  %call_tmp.19 = call ptr @dict_get_string(ptr %.145, ptr %.73)
  store ptr %call_tmp.19, ptr @person_name, align 8
  %.147 = load ptr, ptr @person, align 8
  %call_tmp.20 = call i32 @dict_get_int(ptr %.147, ptr %.77)
  store i32 %call_tmp.20, ptr @person_age, align 4
  %.149 = load ptr, ptr @person, align 8
  %call_tmp.21 = call double @dict_get_float(ptr %.149, ptr %.80)
  store double %call_tmp.21, ptr @person_height, align 8
  %.151 = bitcast ptr @.str19 to ptr
  %.152 = bitcast ptr @.str20 to ptr
  %call_tmp.22 = call i32 @pie_strcmp(ptr %.151, ptr %.152)
  store i32 %call_tmp.22, ptr @cmp_result, align 4
  %.154 = bitcast ptr @.str21 to ptr
  call void @output_string(ptr %.154)
  %.156 = bitcast ptr @.str22 to ptr
  call void @output_string(ptr %.156)
  %.158 = load i32, ptr @my_int, align 4
  call void @output_int(i32 %.158)
  %.160 = bitcast ptr @.str23 to ptr
  call void @output_string(ptr %.160)
  %.162 = load double, ptr @my_float, align 8
  call void @output_float(double %.162, i32 5)
  %.164 = bitcast ptr @.str24 to ptr
  call void @output_string(ptr %.164)
  %.166 = load i8, ptr @my_char, align 1
  call void @output_char(i8 %.166)
  %.168 = bitcast ptr @.str25 to ptr
  call void @output_string(ptr %.168)
  %.170 = bitcast ptr @.str26 to ptr
  call void @output_string(ptr %.170)
  %.172 = bitcast ptr @.str27 to ptr
  call void @output_string(ptr %.172)
  call void @output_string(ptr %.168)
  %.175 = load ptr, ptr @numbers, align 8
  call void @d_array_int_push(ptr %.175, i32 6)
  %.177 = load ptr, ptr @animals, align 8
  %.178 = bitcast ptr @.str28 to ptr
  call void @d_array_string_push(ptr %.177, ptr %.178)
  %.180 = load ptr, ptr @letters, align 8
  call void @d_array_char_append(ptr %.180, i8 90)
  %.182 = load ptr, ptr @prices, align 8
  call void @d_array_float_push(ptr %.182, double 4.999000e+01)
  %.184 = bitcast ptr @.str29 to ptr
  call void @output_string(ptr %.184)
  call void @output_string(ptr %.156)
  %.187 = load i32, ptr @my_int, align 4
  call void @output_int(i32 %.187)
  call void @output_string(ptr %.160)
  %.190 = load double, ptr @my_float, align 8
  call void @output_float(double %.190, i32 5)
  call void @output_string(ptr %.164)
  %.193 = load i8, ptr @my_char, align 1
  call void @output_char(i8 %.193)
  %.195 = bitcast ptr @.str30 to ptr
  call void @output_string(ptr %.195)
  %.197 = load i32, ptr @str_length, align 4
  call void @output_int(i32 %.197)
  %.199 = bitcast ptr @.str31 to ptr
  call void @output_string(ptr %.199)
  %.201 = bitcast ptr @.str32 to ptr
  call void @output_string(ptr %.201)
  %.203 = load double, ptr @pi_value, align 8
  call void @output_float(double %.203, i32 5)
  %.205 = bitcast ptr @.str33 to ptr
  call void @output_string(ptr %.205)
  %.207 = load double, ptr @e_value, align 8
  call void @output_float(double %.207, i32 5)
  %.209 = bitcast ptr @.str34 to ptr
  call void @output_string(ptr %.209)
  %.211 = load double, ptr @sin_45, align 8
  call void @output_float(double %.211, i32 3)
  %.213 = bitcast ptr @.str35 to ptr
  call void @output_string(ptr %.213)
  %.215 = load double, ptr @cos_45, align 8
  call void @output_float(double %.215, i32 3)
  %.217 = bitcast ptr @.str36 to ptr
  call void @output_string(ptr %.217)
  %.219 = load double, ptr @power_result, align 8
  call void @output_float(double %.219, i32 1)
  %.221 = bitcast ptr @.str37 to ptr
  call void @output_string(ptr %.221)
  %.223 = load double, ptr @sqrt_result, align 8
  call void @output_float(double %.223, i32 1)
  %.225 = bitcast ptr @.str38 to ptr
  call void @output_string(ptr %.225)
  %.227 = load double, ptr @round_up, align 8
  call void @output_float(double %.227, i32 1)
  %.229 = bitcast ptr @.str39 to ptr
  call void @output_string(ptr %.229)
  %.231 = load double, ptr @floor_result, align 8
  call void @output_float(double %.231, i32 1)
  %.233 = bitcast ptr @.str40 to ptr
  call void @output_string(ptr %.233)
  %.235 = load double, ptr @ceil_result, align 8
  call void @output_float(double %.235, i32 1)
  %.237 = bitcast ptr @.str41 to ptr
  call void @output_string(ptr %.237)
  %.239 = load double, ptr @abs_result, align 8
  call void @output_float(double %.239, i32 1)
  %.241 = bitcast ptr @.str42 to ptr
  call void @output_string(ptr %.241)
  %.243 = load double, ptr @min_result, align 8
  call void @output_float(double %.243, i32 1)
  %.245 = bitcast ptr @.str43 to ptr
  call void @output_string(ptr %.245)
  %.247 = load i32, ptr @max_int_result, align 4
  call void @output_int(i32 %.247)
  %.249 = bitcast ptr @.str44 to ptr
  call void @output_string(ptr %.249)
  %.251 = load ptr, ptr @numbers, align 8
  %.252 = call i32 @d_array_int_contains(ptr %.251, i32 3)
  %bool_cond = icmp ne i32 %.252, 0
  br i1 %bool_cond, label %then, label %if_cont

then:                                             ; preds = %entry
  %.254 = bitcast ptr @.str45 to ptr
  call void @output_string(ptr %.254)
  br label %if_cont

if_cont:                                          ; preds = %then, %entry
  %.257 = load ptr, ptr @animals, align 8
  %.258 = call i32 @d_array_string_contains(ptr %.257, ptr %.20)
  %bool_cond.1 = icmp ne i32 %.258, 0
  br i1 %bool_cond.1, label %then.1, label %if_cont.1

then.1:                                           ; preds = %if_cont
  %.260 = bitcast ptr @.str46 to ptr
  call void @output_string(ptr %.260)
  br label %if_cont.1

if_cont.1:                                        ; preds = %then.1, %if_cont
  %.263 = bitcast ptr @.str47 to ptr
  call void @output_string(ptr %.263)
  %.265 = load i32, ptr @numbers_size, align 4
  call void @output_int(i32 %.265)
  %.267 = bitcast ptr @.str48 to ptr
  call void @output_string(ptr %.267)
  %.269 = load i32, ptr @animals_size, align 4
  call void @output_int(i32 %.269)
  %.271 = bitcast ptr @.str49 to ptr
  call void @output_string(ptr %.271)
  %.273 = load double, ptr @numbers_avg, align 8
  call void @output_float(double %.273, i32 2)
  %.275 = bitcast ptr @.str50 to ptr
  call void @output_string(ptr %.275)
  %.277 = load double, ptr @prices_avg, align 8
  call void @output_float(double %.277, i32 2)
  %.279 = bitcast ptr @.str51 to ptr
  call void @output_string(ptr %.279)
  %.281 = load ptr, ptr @numbers, align 8
  %dyn_idx_tmp = call i32 @d_array_int_get(ptr %.281, i32 0)
  call void @output_int(i32 %dyn_idx_tmp)
  %.283 = bitcast ptr @.str52 to ptr
  call void @output_string(ptr %.283)
  %.285 = load ptr, ptr @animals, align 8
  %dyn_idx_tmp.1 = call ptr @d_array_string_get(ptr %.285, i32 0)
  call void @output_string(ptr %dyn_idx_tmp.1)
  %.287 = bitcast ptr @.str53 to ptr
  call void @output_string(ptr %.287)
  %.289 = load ptr, ptr @letters, align 8
  %dyn_idx_tmp.2 = call i8 @d_array_char_get(ptr %.289, i32 0)
  call void @output_char(i8 %dyn_idx_tmp.2)
  %.291 = bitcast ptr @.str54 to ptr
  call void @output_string(ptr %.291)
  %.293 = bitcast ptr @.str55 to ptr
  call void @output_string(ptr %.293)
  %.295 = load ptr, ptr @person_name, align 8
  call void @output_string(ptr %.295)
  %.297 = bitcast ptr @.str56 to ptr
  call void @output_string(ptr %.297)
  %.299 = load i32, ptr @person_age, align 4
  call void @output_int(i32 %.299)
  %.301 = bitcast ptr @.str57 to ptr
  call void @output_string(ptr %.301)
  %.303 = load double, ptr @person_height, align 8
  call void @output_float(double %.303, i32 1)
  %.305 = bitcast ptr @.str58 to ptr
  call void @output_string(ptr %.305)
  %.307 = bitcast ptr @.str59 to ptr
  call void @output_string(ptr %.307)
  %.309 = load ptr, ptr @greeting, align 8
  call void @output_string(ptr %.309)
  %.311 = bitcast ptr @.str60 to ptr
  call void @output_string(ptr %.311)
  %.313 = load i32, ptr @cmp_result, align 4
  call void @output_int(i32 %.313)
  %.315 = bitcast ptr @.str61 to ptr
  call void @output_string(ptr %.315)
  %.317 = load i32, ptr @a, align 4
  %i_cmp_tmp = icmp eq i32 %.317, 10
  br i1 %i_cmp_tmp, label %then.2, label %if_cont.2

then.2:                                           ; preds = %if_cont.1
  %.319 = bitcast ptr @.str62 to ptr
  call void @output_string(ptr %.319)
  br label %if_cont.2

if_cont.2:                                        ; preds = %then.2, %if_cont.1
  %.322 = load i32, ptr @a, align 4
  %.323 = load i32, ptr @b, align 4
  %i_cmp_tmp.1 = icmp ne i32 %.322, %.323
  br i1 %i_cmp_tmp.1, label %then.3, label %if_cont.3

then.3:                                           ; preds = %if_cont.2
  %.325 = bitcast ptr @.str63 to ptr
  call void @output_string(ptr %.325)
  br label %if_cont.3

if_cont.3:                                        ; preds = %then.3, %if_cont.2
  %.328 = load i32, ptr @a, align 4
  %.329 = load i32, ptr @b, align 4
  %i_cmp_tmp.2 = icmp slt i32 %.328, %.329
  br i1 %i_cmp_tmp.2, label %then.4, label %if_cont.4

then.4:                                           ; preds = %if_cont.3
  %.331 = bitcast ptr @.str64 to ptr
  call void @output_string(ptr %.331)
  br label %if_cont.4

if_cont.4:                                        ; preds = %then.4, %if_cont.3
  %.334 = load i32, ptr @b, align 4
  %.335 = load i32, ptr @a, align 4
  %i_cmp_tmp.3 = icmp sgt i32 %.334, %.335
  br i1 %i_cmp_tmp.3, label %then.5, label %if_cont.5

then.5:                                           ; preds = %if_cont.4
  %.337 = bitcast ptr @.str65 to ptr
  call void @output_string(ptr %.337)
  br label %if_cont.5

if_cont.5:                                        ; preds = %then.5, %if_cont.4
  %.340 = load i32, ptr @a, align 4
  %i_cmp_tmp.4 = icmp sle i32 %.340, 10
  br i1 %i_cmp_tmp.4, label %then.6, label %if_cont.6

then.6:                                           ; preds = %if_cont.5
  %.342 = bitcast ptr @.str66 to ptr
  call void @output_string(ptr %.342)
  br label %if_cont.6

if_cont.6:                                        ; preds = %then.6, %if_cont.5
  %.345 = load i32, ptr @b, align 4
  %i_cmp_tmp.5 = icmp sge i32 %.345, 20
  br i1 %i_cmp_tmp.5, label %then.7, label %if_cont.7

then.7:                                           ; preds = %if_cont.6
  %.347 = bitcast ptr @.str67 to ptr
  call void @output_string(ptr %.347)
  br label %if_cont.7

if_cont.7:                                        ; preds = %then.7, %if_cont.6
  %.350 = bitcast ptr @.str68 to ptr
  call void @output_string(ptr %.350)
  %.352 = bitcast ptr @.str69 to ptr
  call void @output_string(ptr %.352)
  %.354 = load ptr, ptr @numbers, align 8
  call void @print_int_array(ptr %.354)
  %.356 = bitcast ptr @.str70 to ptr
  call void @output_string(ptr %.356)
  %.358 = load ptr, ptr @animals, align 8
  call void @print_string_array(ptr %.358)
  %.360 = bitcast ptr @.str71 to ptr
  call void @output_string(ptr %.360)
  %.362 = load ptr, ptr @letters, align 8
  call void @print_char_array(ptr %.362)
  %.364 = bitcast ptr @.str72 to ptr
  call void @output_string(ptr %.364)
  %.366 = load ptr, ptr @prices, align 8
  call void @print_float_array(ptr %.366)
  %.368 = bitcast ptr @.str73 to ptr
  call void @output_string(ptr %.368)
  %.370 = load ptr, ptr @combined, align 8
  call void @print_int_array(ptr %.370)
  %.372 = bitcast ptr @.str74 to ptr
  call void @output_string(ptr %.372)
  %.374 = bitcast ptr @.str75 to ptr
  call void @output_string(ptr %.374)
  %.376 = bitcast ptr @.str76 to ptr
  call void @output_string(ptr %.376)
  %.378 = bitcast ptr @.str77 to ptr
  call void @output_string(ptr %.378)
  %.380 = bitcast ptr @.str78 to ptr
  call void @output_string(ptr %.380)
  %.382 = bitcast ptr @.str79 to ptr
  call void @output_string(ptr %.382)
  %.384 = bitcast ptr @.str80 to ptr
  call void @output_string(ptr %.384)
  %.386 = bitcast ptr @.str81 to ptr
  call void @output_string(ptr %.386)
  %.388 = bitcast ptr @.str82 to ptr
  call void @output_string(ptr %.388)
  %.390 = bitcast ptr @.str83 to ptr
  call void @output_string(ptr %.390)
  %.392 = bitcast ptr @.str84 to ptr
  call void @output_string(ptr %.392)
  call void @output_string(ptr %.168)
  %.395 = bitcast ptr @.str85 to ptr
  call void @output_string(ptr %.395)
  %.397 = bitcast ptr @.str86 to ptr
  call void @output_string(ptr %.397)
  call void @output_string(ptr %.168)
  ret i32 0
}
