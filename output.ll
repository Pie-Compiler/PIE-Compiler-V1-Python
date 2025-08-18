; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayString = type { i8**, i64, i64 }
%DArrayInt = type { i32*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }
%Dictionary = type { i8**, i32, i32 }
%DictValue = type { i32, i64 }
%DArrayFloat = type { double*, i64, i64 }

@names = internal global %DArrayString* null
@numbers = internal global %DArrayInt* null
@grades = internal global %DArrayChar* null
@search_value = internal global i32 3
@arr1 = internal global %DArrayInt* null
@arr2 = internal global %DArrayInt* null
@arr3 = internal global %DArrayInt* null
@avg_nums = internal global %DArrayInt* null
@.str0 = internal constant [6 x i8] c"Alice\00"
@.str1 = internal constant [4 x i8] c"Bob\00"
@.str2 = internal constant [8 x i8] c"Charlie\00"
@.str3 = internal constant [29 x i8] c"Numbers contains the value 3\00"
@.str4 = internal constant [6 x i8] c"David\00"

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
  %.2 = call %DArrayString* @d_array_string_create()
  store %DArrayString* %.2, %DArrayString** @names, align 8
  %.4 = bitcast [6 x i8]* @.str0 to i8*
  call void @d_array_string_append(%DArrayString* %.2, i8* %.4)
  %.6 = bitcast [4 x i8]* @.str1 to i8*
  call void @d_array_string_append(%DArrayString* %.2, i8* %.6)
  %.8 = bitcast [8 x i8]* @.str2 to i8*
  call void @d_array_string_append(%DArrayString* %.2, i8* %.8)
  %.10 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.10, %DArrayInt** @numbers, align 8
  call void @d_array_int_append(%DArrayInt* %.10, i32 1)
  call void @d_array_int_append(%DArrayInt* %.10, i32 2)
  call void @d_array_int_append(%DArrayInt* %.10, i32 3)
  %.15 = call %DArrayChar* @d_array_char_create()
  store %DArrayChar* %.15, %DArrayChar** @grades, align 8
  call void @d_array_char_append(%DArrayChar* %.15, i8 65)
  call void @d_array_char_append(%DArrayChar* %.15, i8 66)
  call void @d_array_char_append(%DArrayChar* %.15, i8 67)
  %.20 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.20, %DArrayInt** @arr1, align 8
  call void @d_array_int_append(%DArrayInt* %.20, i32 10)
  call void @d_array_int_append(%DArrayInt* %.20, i32 20)
  %.24 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.24, %DArrayInt** @arr2, align 8
  call void @d_array_int_append(%DArrayInt* %.24, i32 30)
  call void @d_array_int_append(%DArrayInt* %.24, i32 40)
  %.28 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.28, %DArrayInt** @arr3, align 8
  %.30 = load %DArrayInt*, %DArrayInt** @arr1, align 8
  %.31 = load %DArrayInt*, %DArrayInt** @arr2, align 8
  %.32 = load %DArrayInt*, %DArrayInt** @arr1, align 8
  %.33 = load %DArrayInt*, %DArrayInt** @arr2, align 8
  %concat_array_tmp = call %DArrayInt* @d_array_int_concat(%DArrayInt* %.32, %DArrayInt* %.33)
  store %DArrayInt* %concat_array_tmp, %DArrayInt** @arr3, align 8
  %.35 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.35, %DArrayInt** @avg_nums, align 8
  call void @d_array_int_append(%DArrayInt* %.35, i32 10)
  call void @d_array_int_append(%DArrayInt* %.35, i32 20)
  call void @d_array_int_append(%DArrayInt* %.35, i32 37)
  %.40 = load %DArrayChar*, %DArrayChar** @grades, align 8
  %.41 = call i32 @d_array_char_indexof(%DArrayChar* %.40, i8 82)
  call void @output_int(i32 %.41)
  %.43 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.44 = load i32, i32* @search_value, align 4
  %.45 = call i32 @d_array_int_contains(%DArrayInt* %.43, i32 %.44)
  %bool_cond = icmp ne i32 %.45, 0
  br i1 %bool_cond, label %then, label %else

then:                                             ; preds = %entry
  %.47 = bitcast [29 x i8]* @.str3 to i8*
  call void @output_string(i8* %.47)
  br label %if_cont

else:                                             ; preds = %entry
  %.50 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @print_int_array(%DArrayInt* %.50)
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  %.53 = load %DArrayString*, %DArrayString** @names, align 8
  %.54 = bitcast [6 x i8]* @.str4 to i8*
  call void @d_array_string_push(%DArrayString* %.53, i8* %.54)
  %.56 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @d_array_int_push(%DArrayInt* %.56, i32 4)
  %.58 = load %DArrayString*, %DArrayString** @names, align 8
  %.59 = call i32 @d_array_string_size(%DArrayString* %.58)
  call void @output_int(i32 %.59)
  %.61 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.62 = call i32 @d_array_int_size(%DArrayInt* %.61)
  call void @output_int(i32 %.62)
  %.64 = load %DArrayInt*, %DArrayInt** @arr3, align 8
  %.65 = call i32 @d_array_int_size(%DArrayInt* %.64)
  call void @output_int(i32 %.65)
  %.67 = load %DArrayInt*, %DArrayInt** @arr3, align 8
  %dyn_idx_tmp = call i32 @d_array_int_get(%DArrayInt* %.67, i32 0)
  call void @output_int(i32 %dyn_idx_tmp)
  %.69 = load %DArrayInt*, %DArrayInt** @arr3, align 8
  %dyn_idx_tmp.1 = call i32 @d_array_int_get(%DArrayInt* %.69, i32 3)
  call void @output_int(i32 %dyn_idx_tmp.1)
  %.71 = load %DArrayInt*, %DArrayInt** @avg_nums, align 8
  %.72 = call double @d_array_int_avg(%DArrayInt* %.71)
  call void @output_float(double %.72, i32 3)
  %.74 = load %DArrayString*, %DArrayString** @names, align 8
  call void @print_string_array(%DArrayString* %.74)
  ret i32 0
}
