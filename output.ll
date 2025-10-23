; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayInt = type { i32*, i64, i64 }
%Dictionary = type { i8**, i32, i32 }
%DictValue = type { i32, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }

@.str0 = internal constant [6 x i8] c"Alice\00"
@name = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str0, i32 0, i32 0)
@age = internal global i32 30
@height = internal global double 5.900000e+00
@arr = internal global %DArrayInt* null
@last = internal global i32 0
@.str1 = internal constant [9 x i8] c"Test 1: \00"
@.str2 = internal constant [8 x i8] c"Age is \00"
@.str3 = internal constant [11 x i8] c"Height is \00"
@.str4 = internal constant [5 x i8] c" is \00"
@.str5 = internal constant [16 x i8] c" years old and \00"
@.str6 = internal constant [11 x i8] c" feet tall\00"
@.str7 = internal constant [18 x i8] c"Array before pop:\00"
@.str8 = internal constant [9 x i8] c"Popped: \00"
@.str9 = internal constant [17 x i8] c"Array after pop:\00"
@.str10 = internal constant [18 x i8] c"All tests passed!\00"

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

declare i8* @int_to_string(i32)

declare i8* @float_to_string(double)

declare i8* @char_to_string(i8)

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

declare i8* @regex_compile(i8*)

declare i32 @regex_match(i8*, i8*)

declare void @regex_free(i8*)

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
  store %DArrayInt* %.2, %DArrayInt** @arr, align 8
  call void @d_array_int_append(%DArrayInt* %.2, i32 1)
  call void @d_array_int_append(%DArrayInt* %.2, i32 2)
  call void @d_array_int_append(%DArrayInt* %.2, i32 3)
  call void @d_array_int_append(%DArrayInt* %.2, i32 4)
  call void @d_array_int_append(%DArrayInt* %.2, i32 5)
  %.9 = bitcast [9 x i8]* @.str1 to i8*
  %.10 = load i8*, i8** @name, align 8
  %concat_tmp = call i8* @concat_strings(i8* %.9, i8* %.10)
  call void @output_string(i8* %concat_tmp)
  %.12 = bitcast [8 x i8]* @.str2 to i8*
  %.13 = load i32, i32* @age, align 4
  %int_to_str = call i8* @int_to_string(i32 %.13)
  %concat_tmp.1 = call i8* @concat_strings(i8* %.12, i8* %int_to_str)
  call void @output_string(i8* %concat_tmp.1)
  %.15 = bitcast [11 x i8]* @.str3 to i8*
  %.16 = load double, double* @height, align 8
  %float_to_str = call i8* @float_to_string(double %.16)
  %concat_tmp.2 = call i8* @concat_strings(i8* %.15, i8* %float_to_str)
  call void @output_string(i8* %concat_tmp.2)
  %.18 = load i8*, i8** @name, align 8
  %.19 = bitcast [5 x i8]* @.str4 to i8*
  %concat_tmp.3 = call i8* @concat_strings(i8* %.18, i8* %.19)
  %.20 = load i32, i32* @age, align 4
  %int_to_str.1 = call i8* @int_to_string(i32 %.20)
  %concat_tmp.4 = call i8* @concat_strings(i8* %concat_tmp.3, i8* %int_to_str.1)
  %.21 = bitcast [16 x i8]* @.str5 to i8*
  %concat_tmp.5 = call i8* @concat_strings(i8* %concat_tmp.4, i8* %.21)
  %.22 = load double, double* @height, align 8
  %float_to_str.1 = call i8* @float_to_string(double %.22)
  %concat_tmp.6 = call i8* @concat_strings(i8* %concat_tmp.5, i8* %float_to_str.1)
  %.23 = bitcast [11 x i8]* @.str6 to i8*
  %concat_tmp.7 = call i8* @concat_strings(i8* %concat_tmp.6, i8* %.23)
  call void @output_string(i8* %concat_tmp.7)
  %.25 = bitcast [18 x i8]* @.str7 to i8*
  call void @output_string(i8* %.25)
  %.27 = load %DArrayInt*, %DArrayInt** @arr, align 8
  call void @print_int_array(%DArrayInt* %.27)
  %.29 = load %DArrayInt*, %DArrayInt** @arr, align 8
  %.30 = call i32 @d_array_int_pop(%DArrayInt* %.29)
  store i32 %.30, i32* @last, align 4
  %.32 = bitcast [9 x i8]* @.str8 to i8*
  %.33 = load i32, i32* @last, align 4
  %int_to_str.2 = call i8* @int_to_string(i32 %.33)
  %concat_tmp.8 = call i8* @concat_strings(i8* %.32, i8* %int_to_str.2)
  call void @output_string(i8* %concat_tmp.8)
  %.35 = bitcast [17 x i8]* @.str9 to i8*
  call void @output_string(i8* %.35)
  %.37 = load %DArrayInt*, %DArrayInt** @arr, align 8
  call void @print_int_array(%DArrayInt* %.37)
  %.39 = bitcast [18 x i8]* @.str10 to i8*
  call void @output_string(i8* %.39)
  ret i32 0
}
