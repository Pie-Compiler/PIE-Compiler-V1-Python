; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayInt = type { i32*, i64, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }

@state = internal global i32 0
@numbers = internal global %DArrayInt* null
@num = internal global i32 0
@sum = internal global i32 0
@arrsize = internal global i32 0
@average = internal global double 0.000000e+00
@.str0 = internal constant [22 x i8] c"Please enter a number\00"
@.str1 = internal constant [25 x i8] c"Continue? \0A 0:Yes \0A 1:No\00"
@.str2 = internal constant [27 x i8] c"The sum of the numbers is \00"

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
  %.2 = call %DArrayInt* @d_array_int_create()
  store %DArrayInt* %.2, %DArrayInt** @numbers, align 8
  br label %loop_header

loop_header:                                      ; preds = %loop_body, %entry
  %.5 = load i32, i32* @state, align 4
  %i_cmp_tmp = icmp ne i32 %.5, 1
  br i1 %i_cmp_tmp, label %loop_body, label %loop_exit

loop_body:                                        ; preds = %loop_header
  %.7 = bitcast [22 x i8]* @.str0 to i8*
  call void @output_string(i8* %.7)
  call void @input_int(i32* @num)
  %.10 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.11 = load i32, i32* @num, align 4
  call void @d_array_int_push(%DArrayInt* %.10, i32 %.11)
  %.13 = bitcast [25 x i8]* @.str1 to i8*
  call void @output_string(i8* %.13)
  call void @input_int(i32* @state)
  br label %loop_header

loop_exit:                                        ; preds = %loop_header
  %.17 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.18 = call i32 @d_array_int_size(%DArrayInt* %.17)
  store i32 %.18, i32* @arrsize, align 4
  %i = alloca i32, align 4
  store i32 0, i32* %i, align 4
  br label %for_header

for_header:                                       ; preds = %for_update, %loop_exit
  %.22 = load i32, i32* %i, align 4
  %.23 = load i32, i32* @arrsize, align 4
  %i_cmp_tmp.1 = icmp slt i32 %.22, %.23
  br i1 %i_cmp_tmp.1, label %for_body, label %for_exit

for_body:                                         ; preds = %for_header
  %.25 = load i32, i32* @sum, align 4
  %.26 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.27 = load i32, i32* %i, align 4
  %dyn_idx_tmp = call i32 @d_array_int_get(%DArrayInt* %.26, i32 %.27)
  %i_tmp = add i32 %.25, %dyn_idx_tmp
  store i32 %i_tmp, i32* @sum, align 4
  br label %for_update

for_update:                                       ; preds = %for_body
  %.30 = load i32, i32* %i, align 4
  %i_tmp.1 = add i32 %.30, 1
  store i32 %i_tmp.1, i32* %i, align 4
  br label %for_header

for_exit:                                         ; preds = %for_header
  %.33 = bitcast [27 x i8]* @.str2 to i8*
  call void @output_string(i8* %.33)
  %.35 = load i32, i32* @sum, align 4
  call void @output_int(i32 %.35)
  %.37 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @print_int_array(%DArrayInt* %.37)
  %.39 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.40 = call double @d_array_int_avg(%DArrayInt* %.39)
  store double %.40, double* @average, align 8
  %.42 = load double, double* @average, align 8
  call void @output_float(double %.42, i32 2)
  ret i32 0
}
