; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayInt = type { i32*, i64, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%Dictionary = type { i8**, i32, i32 }
%DictValue = type { i32, i64 }

@my_int = internal global i32 42
@my_float = internal global double 3.141590e+00
@my_char = internal global i8 81
@.str0 = internal constant [44 x i8] c"The quick brown fox jumps over the lazy dog\00"
@my_string = internal global i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str0, i32 0, i32 0)
@numbers = internal global %DArrayInt* null
@fibonacci = internal global %DArrayInt* null
@animals = internal global %DArrayString* null
@colors = internal global %DArrayString* null
@letters = internal global %DArrayChar* null
@vowels = internal global %DArrayChar* null
@prices = internal global %DArrayFloat* null
@coordinates = internal global %DArrayFloat* null
@person = internal global %Dictionary* null
@config = internal global %Dictionary* null
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
@hello = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str1, i32 0, i32 0)
@.str2 = internal constant [6 x i8] c"World\00"
@world = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str2, i32 0, i32 0)
@greeting = internal global i8* null
@str_length = internal global i32 0
@numbers_size = internal global i32 0
@animals_size = internal global i32 0
@letters_size = internal global i32 0
@search_index = internal global i32 0
@not_found = internal global i32 0
@more_numbers = internal global %DArrayInt* null
@combined = internal global %DArrayInt* null
@numbers_avg = internal global double 0.000000e+00
@prices_avg = internal global double 0.000000e+00
@person_name = internal global i8* null
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

declare void @input_int(i32*)

declare void @input_float(double*)

declare void @input_string(i8**)

declare void @input_char(i8*)

declare void @output_int(i32)

declare void @output_string(i8*)

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

declare i8* @concat_strings(i8*, i8*)

declare i32 @pie_strlen(i8*)

declare i32 @pie_strcmp(i8*, i8*)

declare i8* @pie_strcpy(i8*, i8*)

declare i8* @pie_strcat(i8*, i8*)

declare i8* @string_to_upper(i8*)

declare i8* @string_to_lower(i8*)

declare i8* @string_trim(i8*)

declare i8* @string_substring(i8*, i32, i32)

declare i32 @string_index_of(i8*, i8*)

declare i8* @string_replace_char(i8*, i8, i8)

declare i8* @string_reverse(i8*)

declare i32 @string_count_char(i8*, i8)

declare i64 @file_open(i8*, i8*)

declare void @file_close(i64)

declare void @file_write(i64, i8*)

declare i8* @file_read_all(i64)

declare i8* @file_read_line(i64)

declare %Dictionary* @dict_create()

declare void @dict_set(%Dictionary*, i8*, %DictValue*)

declare %DictValue* @dict_get(%Dictionary*, i8*)

declare i32 @dict_get_int(%Dictionary*, i8*)

declare double @dict_get_float(%Dictionary*, i8*)

declare i8* @dict_get_string(%Dictionary*, i8*)

declare i32 @dict_has_key(%Dictionary*, i8*)

declare i32 @dict_key_exists(%Dictionary*, i8*)

declare void @dict_delete(%Dictionary*, i8*)

declare void @dict_free(%Dictionary*)

declare %DictValue* @dict_value_create_int(i32)

declare %DictValue* @dict_value_create_float(double)

declare %DictValue* @dict_value_create_string(i8*)

declare %DictValue* @dict_value_create_null()

declare %DictValue* @new_int(i32)

declare %DictValue* @new_float(double)

declare %DictValue* @new_string(i8*)

declare i32 @is_variable_defined(i8*)

declare i32 @is_variable_null(i8*)

declare i32 @string_contains(i8*, i8*)

declare i32 @string_starts_with(i8*, i8*)

declare i32 @string_ends_with(i8*, i8*)

declare i32 @string_is_empty(i8*)

declare void @d_array_int_push(%DArrayInt*, i32)

declare i32 @d_array_int_pop(%DArrayInt*)

declare i32 @d_array_int_size(%DArrayInt*)

declare i32 @d_array_int_contains(%DArrayInt*, i32)

declare i32 @d_array_int_indexof(%DArrayInt*, i32)

declare %DArrayInt* @d_array_int_concat(%DArrayInt*, %DArrayInt*)

declare double @d_array_int_avg(%DArrayInt*)

declare i32 @d_array_int_get(%DArrayInt*, i32)

declare void @d_array_int_set(%DArrayInt*, i32, i32)

declare void @d_array_string_push(%DArrayString*, i8*)

declare i8* @d_array_string_pop(%DArrayString*)

declare i32 @d_array_string_size(%DArrayString*)

declare i32 @d_array_string_contains(%DArrayString*, i8*)

declare i32 @d_array_string_indexof(%DArrayString*, i8*)

declare %DArrayString* @d_array_string_concat(%DArrayString*, %DArrayString*)

declare i8* @d_array_string_get(%DArrayString*, i32)

declare void @d_array_string_set(%DArrayString*, i32, i8*)

declare void @d_array_float_push(%DArrayFloat*, double)

declare double @d_array_float_pop(%DArrayFloat*)

declare i32 @d_array_float_size(%DArrayFloat*)

declare i32 @d_array_float_contains(%DArrayFloat*, double)

declare i32 @d_array_float_indexof(%DArrayFloat*, double)

declare double @d_array_float_avg(%DArrayFloat*)

declare %DArrayInt* @d_array_int_create()

declare %DArrayString* @d_array_string_create()

declare %DArrayFloat* @d_array_float_create()

declare void @d_array_int_append(%DArrayInt*, i32)

declare void @d_array_string_append(%DArrayString*, i8*)

declare void @d_array_float_append(%DArrayFloat*, double)

declare double @d_array_float_get(%DArrayFloat*, i32)

declare void @d_array_float_set(%DArrayFloat*, i32, double)

declare void @d_array_float_free(%DArrayFloat*)

declare void @print_int_array(%DArrayInt*)

declare void @print_string_array(%DArrayString*)

declare void @print_float_array(%DArrayFloat*)

declare void @print_char_array(%DArrayChar*)

declare %DArrayChar* @d_array_char_create()

declare void @d_array_char_append(%DArrayChar*, i8)

declare i8 @d_array_char_get(%DArrayChar*, i32)

declare void @d_array_char_set(%DArrayChar*, i32, i8)

declare i32 @d_array_char_size(%DArrayChar*)

declare void @d_array_char_free(%DArrayChar*)

declare i8 @d_array_char_pop(%DArrayChar*)

declare i1 @d_array_char_contains(%DArrayChar*, i8)

declare i32 @d_array_char_indexof(%DArrayChar*, i8)

declare %DArrayChar* @d_array_char_concat(%DArrayChar*, %DArrayChar*)

define i32 @main() {
entry:
  %.2 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.2, %DArrayInt** @numbers, align 8
  call void @d_array_int_append(%DArrayInt* %.2, i32 1)
  call void @d_array_int_append(%DArrayInt* %.2, i32 2)
  call void @d_array_int_append(%DArrayInt* %.2, i32 3)
  call void @d_array_int_append(%DArrayInt* %.2, i32 4)
  call void @d_array_int_append(%DArrayInt* %.2, i32 5)
  %.9 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.9, %DArrayInt** @fibonacci, align 8
  call void @d_array_int_append(%DArrayInt* %.9, i32 1)
  call void @d_array_int_append(%DArrayInt* %.9, i32 1)
  call void @d_array_int_append(%DArrayInt* %.9, i32 2)
  call void @d_array_int_append(%DArrayInt* %.9, i32 3)
  call void @d_array_int_append(%DArrayInt* %.9, i32 5)
  call void @d_array_int_append(%DArrayInt* %.9, i32 8)
  call void @d_array_int_append(%DArrayInt* %.9, i32 13)
  %.18 = call %DArrayString* @d_array_string_create()
  store %DArrayString* %.18, %DArrayString** @animals, align 8
  %.20 = bitcast [4 x i8]* @.str3 to i8*
  call void @d_array_string_append(%DArrayString* %.18, i8* %.20)
  %.22 = bitcast [4 x i8]* @.str4 to i8*
  call void @d_array_string_append(%DArrayString* %.18, i8* %.22)
  %.24 = bitcast [4 x i8]* @.str5 to i8*
  call void @d_array_string_append(%DArrayString* %.18, i8* %.24)
  %.26 = bitcast [5 x i8]* @.str6 to i8*
  call void @d_array_string_append(%DArrayString* %.18, i8* %.26)
  %.28 = call %DArrayString* @d_array_string_create()
  store %DArrayString* %.28, %DArrayString** @colors, align 8
  %.30 = bitcast [4 x i8]* @.str7 to i8*
  call void @d_array_string_append(%DArrayString* %.28, i8* %.30)
  %.32 = bitcast [6 x i8]* @.str8 to i8*
  call void @d_array_string_append(%DArrayString* %.28, i8* %.32)
  %.34 = bitcast [5 x i8]* @.str9 to i8*
  call void @d_array_string_append(%DArrayString* %.28, i8* %.34)
  %.36 = call %DArrayChar* @d_array_char_create()
  store %DArrayChar* %.36, %DArrayChar** @letters, align 8
  call void @d_array_char_append(%DArrayChar* %.36, i8 65)
  call void @d_array_char_append(%DArrayChar* %.36, i8 66)
  call void @d_array_char_append(%DArrayChar* %.36, i8 67)
  call void @d_array_char_append(%DArrayChar* %.36, i8 68)
  %.42 = call %DArrayChar* @d_array_char_create()
  store %DArrayChar* %.42, %DArrayChar** @vowels, align 8
  call void @d_array_char_append(%DArrayChar* %.42, i8 97)
  call void @d_array_char_append(%DArrayChar* %.42, i8 101)
  call void @d_array_char_append(%DArrayChar* %.42, i8 105)
  call void @d_array_char_append(%DArrayChar* %.42, i8 111)
  call void @d_array_char_append(%DArrayChar* %.42, i8 117)
  %.49 = call %DArrayFloat* @d_array_float_create()
  store %DArrayFloat* %.49, %DArrayFloat** @prices, align 8
  call void @d_array_float_append(%DArrayFloat* %.49, double 1.999000e+01)
  call void @d_array_float_append(%DArrayFloat* %.49, double 2.999000e+01)
  call void @d_array_float_append(%DArrayFloat* %.49, double 3.999000e+01)
  %.54 = call %DArrayFloat* @d_array_float_create()
  store %DArrayFloat* %.54, %DArrayFloat** @coordinates, align 8
  call void @d_array_float_append(%DArrayFloat* %.54, double 1.500000e+00)
  call void @d_array_float_append(%DArrayFloat* %.54, double 2.700000e+00)
  call void @d_array_float_append(%DArrayFloat* %.54, double 3.800000e+00)
  call void @d_array_float_append(%DArrayFloat* %.54, double 4.200000e+00)
  %.60 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.60, %DArrayInt** @more_numbers, align 8
  call void @d_array_int_append(%DArrayInt* %.60, i32 7)
  call void @d_array_int_append(%DArrayInt* %.60, i32 8)
  call void @d_array_int_append(%DArrayInt* %.60, i32 9)
  %.65 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.65, %DArrayInt** @combined, align 8
  %.67 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.68 = load %DArrayInt*, %DArrayInt** @more_numbers, align 8
  %.69 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.70 = load %DArrayInt*, %DArrayInt** @more_numbers, align 8
  %concat_array_tmp = call %DArrayInt* @d_array_int_concat(%DArrayInt* %.69, %DArrayInt* %.70)
  store %DArrayInt* %concat_array_tmp, %DArrayInt** @combined, align 8
  %.72 = call %Dictionary* @dict_create()
  %.73 = bitcast [5 x i8]* @.str10 to i8*
  %.74 = bitcast [9 x i8]* @.str11 to i8*
  %.75 = call %DictValue* @new_string(i8* %.74)
  call void @dict_set(%Dictionary* %.72, i8* %.73, %DictValue* %.75)
  %.77 = bitcast [4 x i8]* @.str12 to i8*
  %.78 = call %DictValue* @new_int(i32 30)
  call void @dict_set(%Dictionary* %.72, i8* %.77, %DictValue* %.78)
  %.80 = bitcast [7 x i8]* @.str13 to i8*
  %.81 = call %DictValue* @new_float(double 5.900000e+00)
  call void @dict_set(%Dictionary* %.72, i8* %.80, %DictValue* %.81)
  store %Dictionary* %.72, %Dictionary** @person, align 8
  %.84 = call %Dictionary* @dict_create()
  %.85 = bitcast [6 x i8]* @.str14 to i8*
  %.86 = call %DictValue* @new_int(i32 1)
  call void @dict_set(%Dictionary* %.84, i8* %.85, %DictValue* %.86)
  %.88 = bitcast [8 x i8]* @.str15 to i8*
  %.89 = call %DictValue* @new_float(double 3.050000e+01)
  call void @dict_set(%Dictionary* %.84, i8* %.88, %DictValue* %.89)
  %.91 = bitcast [5 x i8]* @.str16 to i8*
  %.92 = bitcast [10 x i8]* @.str17 to i8*
  %.93 = call %DictValue* @new_string(i8* %.92)
  call void @dict_set(%Dictionary* %.84, i8* %.91, %DictValue* %.93)
  store %Dictionary* %.84, %Dictionary** @config, align 8
  %call_tmp = call double @pie_pi()
  store double %call_tmp, double* @pi_value, align 8
  %call_tmp.1 = call double @pie_e()
  store double %call_tmp.1, double* @e_value, align 8
  %.98 = load double, double* @pi_value, align 8
  %f_tmp = fdiv double %.98, 4.000000e+00
  store double %f_tmp, double* @angle, align 8
  %.100 = load double, double* @angle, align 8
  %call_tmp.2 = call double @pie_sin(double %.100)
  store double %call_tmp.2, double* @sin_45, align 8
  %.102 = load double, double* @angle, align 8
  %call_tmp.3 = call double @pie_cos(double %.102)
  store double %call_tmp.3, double* @cos_45, align 8
  %.104 = load double, double* @angle, align 8
  %call_tmp.4 = call double @pie_tan(double %.104)
  store double %call_tmp.4, double* @tan_45, align 8
  %call_tmp.5 = call double @pie_pow(double 2.000000e+00, double 3.000000e+00)
  store double %call_tmp.5, double* @power_result, align 8
  %call_tmp.6 = call double @pie_sqrt(double 1.600000e+01)
  store double %call_tmp.6, double* @sqrt_result, align 8
  %call_tmp.7 = call double @pie_round(double 3.700000e+00)
  store double %call_tmp.7, double* @round_up, align 8
  %call_tmp.8 = call double @pie_round(double 3.200000e+00)
  store double %call_tmp.8, double* @round_down, align 8
  %call_tmp.9 = call double @pie_floor(double 3.900000e+00)
  store double %call_tmp.9, double* @floor_result, align 8
  %call_tmp.10 = call double @pie_ceil(double 3.100000e+00)
  store double %call_tmp.10, double* @ceil_result, align 8
  %f_neg_tmp = fsub double 0.000000e+00, 5.500000e+00
  %call_tmp.11 = call double @pie_abs(double %f_neg_tmp)
  store double %call_tmp.11, double* @abs_result, align 8
  %i_neg_tmp = sub i32 0, 10
  %call_tmp.12 = call i32 @pie_abs_int(i32 %i_neg_tmp)
  store i32 %call_tmp.12, i32* @abs_int_result, align 4
  %call_tmp.13 = call double @pie_min(double 3.500000e+00, double 7.200000e+00)
  store double %call_tmp.13, double* @min_result, align 8
  %call_tmp.14 = call double @pie_max(double 3.500000e+00, double 7.200000e+00)
  store double %call_tmp.14, double* @max_result, align 8
  %call_tmp.15 = call i32 @pie_min_int(i32 15, i32 8)
  store i32 %call_tmp.15, i32* @min_int_result, align 4
  %call_tmp.16 = call i32 @pie_max_int(i32 15, i32 8)
  store i32 %call_tmp.16, i32* @max_int_result, align 4
  %.118 = load i8*, i8** @hello, align 8
  %.119 = load i8*, i8** @world, align 8
  %call_tmp.17 = call i8* @concat_strings(i8* %.118, i8* %.119)
  store i8* %call_tmp.17, i8** @greeting, align 8
  %.121 = load i8*, i8** @my_string, align 8
  %call_tmp.18 = call i32 @pie_strlen(i8* %.121)
  store i32 %call_tmp.18, i32* @str_length, align 4
  %.123 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.124 = call i32 @d_array_int_size(%DArrayInt* %.123)
  store i32 %.124, i32* @numbers_size, align 4
  %.126 = load %DArrayString*, %DArrayString** @animals, align 8
  %.127 = call i32 @d_array_string_size(%DArrayString* %.126)
  store i32 %.127, i32* @animals_size, align 4
  %.129 = load %DArrayChar*, %DArrayChar** @letters, align 8
  %.130 = call i32 @d_array_char_size(%DArrayChar* %.129)
  store i32 %.130, i32* @letters_size, align 4
  %.132 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.133 = call i32 @d_array_int_indexof(%DArrayInt* %.132, i32 3)
  store i32 %.133, i32* @search_index, align 4
  %.135 = load %DArrayString*, %DArrayString** @animals, align 8
  %.136 = bitcast [6 x i8]* @.str18 to i8*
  %.137 = call i32 @d_array_string_indexof(%DArrayString* %.135, i8* %.136)
  store i32 %.137, i32* @not_found, align 4
  %.139 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.140 = call double @d_array_int_avg(%DArrayInt* %.139)
  store double %.140, double* @numbers_avg, align 8
  %.142 = load %DArrayFloat*, %DArrayFloat** @prices, align 8
  %.143 = call double @d_array_float_avg(%DArrayFloat* %.142)
  store double %.143, double* @prices_avg, align 8
  %.145 = load %Dictionary*, %Dictionary** @person, align 8
  %call_tmp.19 = call i8* @dict_get_string(%Dictionary* %.145, i8* %.73)
  store i8* %call_tmp.19, i8** @person_name, align 8
  %.147 = load %Dictionary*, %Dictionary** @person, align 8
  %call_tmp.20 = call i32 @dict_get_int(%Dictionary* %.147, i8* %.77)
  store i32 %call_tmp.20, i32* @person_age, align 4
  %.149 = load %Dictionary*, %Dictionary** @person, align 8
  %call_tmp.21 = call double @dict_get_float(%Dictionary* %.149, i8* %.80)
  store double %call_tmp.21, double* @person_height, align 8
  %.151 = bitcast [6 x i8]* @.str19 to i8*
  %.152 = bitcast [7 x i8]* @.str20 to i8*
  %call_tmp.22 = call i32 @pie_strcmp(i8* %.151, i8* %.152)
  store i32 %call_tmp.22, i32* @cmp_result, align 4
  %.154 = bitcast [29 x i8]* @.str21 to i8*
  call void @output_string(i8* %.154)
  %.156 = bitcast [9 x i8]* @.str22 to i8*
  call void @output_string(i8* %.156)
  %.158 = load i32, i32* @my_int, align 4
  call void @output_int(i32 %.158)
  %.160 = bitcast [7 x i8]* @.str23 to i8*
  call void @output_string(i8* %.160)
  %.162 = load double, double* @my_float, align 8
  call void @output_float(double %.162, i32 5)
  %.164 = bitcast [11 x i8]* @.str24 to i8*
  call void @output_string(i8* %.164)
  %.166 = load i8, i8* @my_char, align 1
  call void @output_char(i8 %.166)
  %.168 = bitcast [65 x i8]* @.str25 to i8*
  call void @output_string(i8* %.168)
  %.170 = bitcast [38 x i8]* @.str26 to i8*
  call void @output_string(i8* %.170)
  %.172 = bitcast [36 x i8]* @.str27 to i8*
  call void @output_string(i8* %.172)
  call void @output_string(i8* %.168)
  %.175 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @d_array_int_push(%DArrayInt* %.175, i32 6)
  %.177 = load %DArrayString*, %DArrayString** @animals, align 8
  %.178 = bitcast [9 x i8]* @.str28 to i8*
  call void @d_array_string_push(%DArrayString* %.177, i8* %.178)
  %.180 = load %DArrayChar*, %DArrayChar** @letters, align 8
  call void @d_array_char_append(%DArrayChar* %.180, i8 90)
  %.182 = load %DArrayFloat*, %DArrayFloat** @prices, align 8
  call void @d_array_float_push(%DArrayFloat* %.182, double 4.999000e+01)
  %.184 = bitcast [23 x i8]* @.str29 to i8*
  call void @output_string(i8* %.184)
  call void @output_string(i8* %.156)
  %.187 = load i32, i32* @my_int, align 4
  call void @output_int(i32 %.187)
  call void @output_string(i8* %.160)
  %.190 = load double, double* @my_float, align 8
  call void @output_float(double %.190, i32 5)
  call void @output_string(i8* %.164)
  %.193 = load i8, i8* @my_char, align 1
  call void @output_char(i8 %.193)
  %.195 = bitcast [15 x i8]* @.str30 to i8*
  call void @output_string(i8* %.195)
  %.197 = load i32, i32* @str_length, align 4
  call void @output_int(i32 %.197)
  %.199 = bitcast [28 x i8]* @.str31 to i8*
  call void @output_string(i8* %.199)
  %.201 = bitcast [10 x i8]* @.str32 to i8*
  call void @output_string(i8* %.201)
  %.203 = load double, double* @pi_value, align 8
  call void @output_float(double %.203, i32 5)
  %.205 = bitcast [9 x i8]* @.str33 to i8*
  call void @output_string(i8* %.205)
  %.207 = load double, double* @e_value, align 8
  call void @output_float(double %.207, i32 5)
  %.209 = bitcast [17 x i8]* @.str34 to i8*
  call void @output_string(i8* %.209)
  %.211 = load double, double* @sin_45, align 8
  call void @output_float(double %.211, i32 3)
  %.213 = bitcast [17 x i8]* @.str35 to i8*
  call void @output_string(i8* %.213)
  %.215 = load double, double* @cos_45, align 8
  call void @output_float(double %.215, i32 3)
  %.217 = bitcast [6 x i8]* @.str36 to i8*
  call void @output_string(i8* %.217)
  %.219 = load double, double* @power_result, align 8
  call void @output_float(double %.219, i32 1)
  %.221 = bitcast [20 x i8]* @.str37 to i8*
  call void @output_string(i8* %.221)
  %.223 = load double, double* @sqrt_result, align 8
  call void @output_float(double %.223, i32 1)
  %.225 = bitcast [12 x i8]* @.str38 to i8*
  call void @output_string(i8* %.225)
  %.227 = load double, double* @round_up, align 8
  call void @output_float(double %.227, i32 1)
  %.229 = bitcast [12 x i8]* @.str39 to i8*
  call void @output_string(i8* %.229)
  %.231 = load double, double* @floor_result, align 8
  call void @output_float(double %.231, i32 1)
  %.233 = bitcast [11 x i8]* @.str40 to i8*
  call void @output_string(i8* %.233)
  %.235 = load double, double* @ceil_result, align 8
  call void @output_float(double %.235, i32 1)
  %.237 = bitcast [11 x i8]* @.str41 to i8*
  call void @output_string(i8* %.237)
  %.239 = load double, double* @abs_result, align 8
  call void @output_float(double %.239, i32 1)
  %.241 = bitcast [15 x i8]* @.str42 to i8*
  call void @output_string(i8* %.241)
  %.243 = load double, double* @min_result, align 8
  call void @output_float(double %.243, i32 1)
  %.245 = bitcast [12 x i8]* @.str43 to i8*
  call void @output_string(i8* %.245)
  %.247 = load i32, i32* @max_int_result, align 4
  call void @output_int(i32 %.247)
  %.249 = bitcast [30 x i8]* @.str44 to i8*
  call void @output_string(i8* %.249)
  %.251 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.252 = call i32 @d_array_int_contains(%DArrayInt* %.251, i32 3)
  %bool_cond = icmp ne i32 %.252, 0
  br i1 %bool_cond, label %then, label %if_cont

then:                                             ; preds = %entry
  %.254 = bitcast [25 x i8]* @.str45 to i8*
  call void @output_string(i8* %.254)
  br label %if_cont

if_cont:                                          ; preds = %then, %entry
  %.257 = load %DArrayString*, %DArrayString** @animals, align 8
  %.258 = call i32 @d_array_string_contains(%DArrayString* %.257, i8* %.20)
  %bool_cond.1 = icmp ne i32 %.258, 0
  br i1 %bool_cond.1, label %then.1, label %if_cont.1

then.1:                                           ; preds = %if_cont
  %.260 = bitcast [27 x i8]* @.str46 to i8*
  call void @output_string(i8* %.260)
  br label %if_cont.1

if_cont.1:                                        ; preds = %then.1, %if_cont
  %.263 = bitcast [20 x i8]* @.str47 to i8*
  call void @output_string(i8* %.263)
  %.265 = load i32, i32* @numbers_size, align 4
  call void @output_int(i32 %.265)
  %.267 = bitcast [20 x i8]* @.str48 to i8*
  call void @output_string(i8* %.267)
  %.269 = load i32, i32* @animals_size, align 4
  call void @output_int(i32 %.269)
  %.271 = bitcast [17 x i8]* @.str49 to i8*
  call void @output_string(i8* %.271)
  %.273 = load double, double* @numbers_avg, align 8
  call void @output_float(double %.273, i32 2)
  %.275 = bitcast [16 x i8]* @.str50 to i8*
  call void @output_string(i8* %.275)
  %.277 = load double, double* @prices_avg, align 8
  call void @output_float(double %.277, i32 2)
  %.279 = bitcast [14 x i8]* @.str51 to i8*
  call void @output_string(i8* %.279)
  %.281 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %dyn_idx_tmp = call i32 @d_array_int_get(%DArrayInt* %.281, i32 0)
  call void @output_int(i32 %dyn_idx_tmp)
  %.283 = bitcast [14 x i8]* @.str52 to i8*
  call void @output_string(i8* %.283)
  %.285 = load %DArrayString*, %DArrayString** @animals, align 8
  %dyn_idx_tmp.1 = call i8* @d_array_string_get(%DArrayString* %.285, i32 0)
  call void @output_string(i8* %dyn_idx_tmp.1)
  %.287 = bitcast [14 x i8]* @.str53 to i8*
  call void @output_string(i8* %.287)
  %.289 = load %DArrayChar*, %DArrayChar** @letters, align 8
  %dyn_idx_tmp.2 = call i8 @d_array_char_get(%DArrayChar* %.289, i32 0)
  call void @output_char(i8 %dyn_idx_tmp.2)
  %.291 = bitcast [35 x i8]* @.str54 to i8*
  call void @output_string(i8* %.291)
  %.293 = bitcast [13 x i8]* @.str55 to i8*
  call void @output_string(i8* %.293)
  %.295 = load i8*, i8** @person_name, align 8
  call void @output_string(i8* %.295)
  %.297 = bitcast [12 x i8]* @.str56 to i8*
  call void @output_string(i8* %.297)
  %.299 = load i32, i32* @person_age, align 4
  call void @output_int(i32 %.299)
  %.301 = bitcast [15 x i8]* @.str57 to i8*
  call void @output_string(i8* %.301)
  %.303 = load double, double* @person_height, align 8
  call void @output_float(double %.303, i32 1)
  %.305 = bitcast [30 x i8]* @.str58 to i8*
  call void @output_string(i8* %.305)
  %.307 = bitcast [23 x i8]* @.str59 to i8*
  call void @output_string(i8* %.307)
  %.309 = load i8*, i8** @greeting, align 8
  call void @output_string(i8* %.309)
  %.311 = bitcast [33 x i8]* @.str60 to i8*
  call void @output_string(i8* %.311)
  %.313 = load i32, i32* @cmp_result, align 4
  call void @output_int(i32 %.313)
  %.315 = bitcast [34 x i8]* @.str61 to i8*
  call void @output_string(i8* %.315)
  %.317 = load i32, i32* @a, align 4
  %i_cmp_tmp = icmp eq i32 %.317, 10
  br i1 %i_cmp_tmp, label %then.2, label %if_cont.2

then.2:                                           ; preds = %if_cont.1
  %.319 = bitcast [21 x i8]* @.str62 to i8*
  call void @output_string(i8* %.319)
  br label %if_cont.2

if_cont.2:                                        ; preds = %then.2, %if_cont.1
  %.322 = load i32, i32* @a, align 4
  %.323 = load i32, i32* @b, align 4
  %i_cmp_tmp.1 = icmp ne i32 %.322, %.323
  br i1 %i_cmp_tmp.1, label %then.3, label %if_cont.3

then.3:                                           ; preds = %if_cont.2
  %.325 = bitcast [23 x i8]* @.str63 to i8*
  call void @output_string(i8* %.325)
  br label %if_cont.3

if_cont.3:                                        ; preds = %then.3, %if_cont.2
  %.328 = load i32, i32* @a, align 4
  %.329 = load i32, i32* @b, align 4
  %i_cmp_tmp.2 = icmp slt i32 %.328, %.329
  br i1 %i_cmp_tmp.2, label %then.4, label %if_cont.4

then.4:                                           ; preds = %if_cont.3
  %.331 = bitcast [22 x i8]* @.str64 to i8*
  call void @output_string(i8* %.331)
  br label %if_cont.4

if_cont.4:                                        ; preds = %then.4, %if_cont.3
  %.334 = load i32, i32* @b, align 4
  %.335 = load i32, i32* @a, align 4
  %i_cmp_tmp.3 = icmp sgt i32 %.334, %.335
  br i1 %i_cmp_tmp.3, label %then.5, label %if_cont.5

then.5:                                           ; preds = %if_cont.4
  %.337 = bitcast [25 x i8]* @.str65 to i8*
  call void @output_string(i8* %.337)
  br label %if_cont.5

if_cont.5:                                        ; preds = %then.5, %if_cont.4
  %.340 = load i32, i32* @a, align 4
  %i_cmp_tmp.4 = icmp sle i32 %.340, 10
  br i1 %i_cmp_tmp.4, label %then.6, label %if_cont.6

then.6:                                           ; preds = %if_cont.5
  %.342 = bitcast [31 x i8]* @.str66 to i8*
  call void @output_string(i8* %.342)
  br label %if_cont.6

if_cont.6:                                        ; preds = %then.6, %if_cont.5
  %.345 = load i32, i32* @b, align 4
  %i_cmp_tmp.5 = icmp sge i32 %.345, 20
  br i1 %i_cmp_tmp.5, label %then.7, label %if_cont.7

then.7:                                           ; preds = %if_cont.6
  %.347 = bitcast [34 x i8]* @.str67 to i8*
  call void @output_string(i8* %.347)
  br label %if_cont.7

if_cont.7:                                        ; preds = %then.7, %if_cont.6
  %.350 = bitcast [23 x i8]* @.str68 to i8*
  call void @output_string(i8* %.350)
  %.352 = bitcast [15 x i8]* @.str69 to i8*
  call void @output_string(i8* %.352)
  %.354 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @print_int_array(%DArrayInt* %.354)
  %.356 = bitcast [15 x i8]* @.str70 to i8*
  call void @output_string(i8* %.356)
  %.358 = load %DArrayString*, %DArrayString** @animals, align 8
  call void @print_string_array(%DArrayString* %.358)
  %.360 = bitcast [15 x i8]* @.str71 to i8*
  call void @output_string(i8* %.360)
  %.362 = load %DArrayChar*, %DArrayChar** @letters, align 8
  call void @print_char_array(%DArrayChar* %.362)
  %.364 = bitcast [14 x i8]* @.str72 to i8*
  call void @output_string(i8* %.364)
  %.366 = load %DArrayFloat*, %DArrayFloat** @prices, align 8
  call void @print_float_array(%DArrayFloat* %.366)
  %.368 = bitcast [16 x i8]* @.str73 to i8*
  call void @output_string(i8* %.368)
  %.370 = load %DArrayInt*, %DArrayInt** @combined, align 8
  call void @print_int_array(%DArrayInt* %.370)
  %.372 = bitcast [21 x i8]* @.str74 to i8*
  call void @output_string(i8* %.372)
  %.374 = bitcast [49 x i8]* @.str75 to i8*
  call void @output_string(i8* %.374)
  %.376 = bitcast [53 x i8]* @.str76 to i8*
  call void @output_string(i8* %.376)
  %.378 = bitcast [63 x i8]* @.str77 to i8*
  call void @output_string(i8* %.378)
  %.380 = bitcast [54 x i8]* @.str78 to i8*
  call void @output_string(i8* %.380)
  %.382 = bitcast [60 x i8]* @.str79 to i8*
  call void @output_string(i8* %.382)
  %.384 = bitcast [50 x i8]* @.str80 to i8*
  call void @output_string(i8* %.384)
  %.386 = bitcast [59 x i8]* @.str81 to i8*
  call void @output_string(i8* %.386)
  %.388 = bitcast [30 x i8]* @.str82 to i8*
  call void @output_string(i8* %.388)
  %.390 = bitcast [29 x i8]* @.str83 to i8*
  call void @output_string(i8* %.390)
  %.392 = bitcast [34 x i8]* @.str84 to i8*
  call void @output_string(i8* %.392)
  call void @output_string(i8* %.168)
  %.395 = bitcast [34 x i8]* @.str85 to i8*
  call void @output_string(i8* %.395)
  %.397 = bitcast [50 x i8]* @.str86 to i8*
  call void @output_string(i8* %.397)
  call void @output_string(i8* %.168)
  ret i32 0
}
