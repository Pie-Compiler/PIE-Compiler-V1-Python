; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayString = type { i8**, i64, i64 }
%DArrayInt = type { i32*, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }

@static_num = internal global [3 x i32] [i32 1, i32 2, i32 3]
@names = internal global %DArrayString* null
@numbers = internal global %DArrayInt* null
@avgs = internal global %DArrayFloat* null
@grades = internal global %DArrayChar* null
@.str0 = internal constant [6 x i8] c"Alice\00"
@.str1 = internal constant [4 x i8] c"Bob\00"
@.str2 = internal constant [8 x i8] c"Charlie\00"

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

declare double @pie_floor(double)

declare double @pie_ceil(double)

declare i32 @pie_rand()

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
  %.15 = call %DArrayFloat* @d_array_float_create()
  store %DArrayFloat* %.15, %DArrayFloat** @avgs, align 8
  call void @d_array_float_append(%DArrayFloat* %.15, double 4.200000e+00)
  call void @d_array_float_append(%DArrayFloat* %.15, double 2.400000e+00)
  %.19 = call %DArrayChar* @d_array_char_create()
  store %DArrayChar* %.19, %DArrayChar** @grades, align 8
  call void @d_array_char_append(%DArrayChar* %.19, i8 65)
  call void @d_array_char_append(%DArrayChar* %.19, i8 66)
  call void @d_array_char_append(%DArrayChar* %.19, i8 67)
  call void @d_array_char_append(%DArrayChar* %.19, i8 68)
  ret i32 0
}
