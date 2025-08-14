; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayInt = type { i32*, i64, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }

@x = internal global double 0.000000e+00
@num = internal global i32 0
@big_num = internal global double 0.000000e+00
@.str0 = internal constant [4 x i8] c"Foo\00"
@.str1 = internal constant [55 x i8] c"Enter a number (recommend < 46340 to avoid overflow): \00"
@.str2 = internal constant [11 x i8] c"Square of \00"
@.str3 = internal constant [5 x i8] c" is \00"
@.str4 = internal constant [2 x i8] c"\0A\00"
@.str5 = internal constant [45 x i8] c"Enter a large number for float calculation: \00"

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

define i32 @sqr(i32 %y) {
entry:
  %y.1 = alloca i32, align 4
  store i32 %y, i32* %y.1, align 4
  %.4 = load i32, i32* %y.1, align 4
  %.5 = load i32, i32* %y.1, align 4
  %i_tmp = mul i32 %.4, %.5
  ret i32 %i_tmp
}

define double @sqr_float(double %y) {
entry:
  %y.1 = alloca double, align 8
  store double %y, double* %y.1, align 8
  %.4 = load double, double* %y.1, align 8
  %.5 = load double, double* %y.1, align 8
  %f_tmp = fmul double %.4, %.5
  ret double %f_tmp
}

define i32 @main() {
entry:
  %.2 = sitofp i32 2 to double
  %.3 = sitofp i32 3 to double
  %call_tmp = call double @pie_pow(double %.2, double %.3)
  store double %call_tmp, double* @x, align 8
  %.5 = load double, double* @x, align 8
  call void @output_float(double %.5, i32 2)
  %.7 = load double, double* @x, align 8
  %.8 = sitofp i32 5 to double
  %f_cmp_tmp = fcmp ogt double %.7, %.8
  %.9 = load double, double* @x, align 8
  %.10 = sitofp i32 8 to double
  %f_cmp_tmp.1 = fcmp one double %.9, %.10
  %and_tmp = and i1 %f_cmp_tmp, %f_cmp_tmp.1
  br i1 %and_tmp, label %then, label %if_cont

then:                                             ; preds = %entry
  %.12 = bitcast [4 x i8]* @.str0 to i8*
  call void @output_string(i8* %.12)
  br label %if_cont

if_cont:                                          ; preds = %then, %entry
  %.15 = bitcast [55 x i8]* @.str1 to i8*
  call void @output_string(i8* %.15)
  call void @input_int(i32* @num)
  %.18 = bitcast [11 x i8]* @.str2 to i8*
  call void @output_string(i8* %.18)
  %.20 = load i32, i32* @num, align 4
  call void @output_int(i32 %.20)
  %.22 = bitcast [5 x i8]* @.str3 to i8*
  call void @output_string(i8* %.22)
  %.24 = load i32, i32* @num, align 4
  %call_tmp.1 = call i32 @sqr(i32 %.24)
  call void @output_int(i32 %call_tmp.1)
  %.26 = bitcast [2 x i8]* @.str4 to i8*
  call void @output_string(i8* %.26)
  %.28 = bitcast [45 x i8]* @.str5 to i8*
  call void @output_string(i8* %.28)
  call void @input_float(double* @big_num)
  call void @output_string(i8* %.18)
  %.32 = load double, double* @big_num, align 8
  call void @output_float(double %.32, i32 1)
  call void @output_string(i8* %.22)
  %.35 = load double, double* @big_num, align 8
  %call_tmp.2 = call double @sqr_float(double %.35)
  call void @output_float(double %call_tmp.2, i32 1)
  call void @output_string(i8* %.26)
  ret i32 0
}
