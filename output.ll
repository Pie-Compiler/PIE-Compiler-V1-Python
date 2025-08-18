; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%Dictionary = type { i8**, i32, i32 }
%DictValue = type { i32, i64 }
%DArrayInt = type { i32*, i64, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }

@config = internal global %Dictionary* null
@.str0 = internal constant [10 x i8] c"max_users\00"
@.str1 = internal constant [8 x i8] c"timeout\00"
@.str2 = internal constant [5 x i8] c"host\00"
@.str3 = internal constant [10 x i8] c"localhost\00"
@.str4 = internal constant [31 x i8] c"Max timeout is greater than 20\00"
@.str5 = internal constant [12 x i8] c"Max users: \00"
@.str6 = internal constant [10 x i8] c"Timeout: \00"
@.str7 = internal constant [7 x i8] c"Host: \00"

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

define void @main_logic() {
entry:
  %.2 = load %Dictionary*, %Dictionary** @config, align 8
  %.3 = bitcast [10 x i8]* @.str0 to i8*
  %call_tmp = call %DictValue* @new_int(i32 100)
  call void @dict_set(%Dictionary* %.2, i8* %.3, %DictValue* %call_tmp)
  %.4 = load %Dictionary*, %Dictionary** @config, align 8
  %.5 = bitcast [8 x i8]* @.str1 to i8*
  %.6 = sitofp i32 12 to double
  %call_tmp.2 = call %DictValue* @new_float(double %.6)
  call void @dict_set(%Dictionary* %.4, i8* %.5, %DictValue* %call_tmp.2)
  %.7 = load %Dictionary*, %Dictionary** @config, align 8
  %.8 = bitcast [5 x i8]* @.str2 to i8*
  %.9 = bitcast [10 x i8]* @.str3 to i8*
  %call_tmp.4 = call %DictValue* @new_string(i8* %.9)
  call void @dict_set(%Dictionary* %.7, i8* %.8, %DictValue* %call_tmp.4)
  %max_users = alloca i32, align 4
  %.10 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.6 = call i32 @dict_get_int(%Dictionary* %.10, i8* %.3)
  store i32 %call_tmp.6, i32* %max_users, align 4
  %timeout = alloca double, align 8
  %.12 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.7 = call double @dict_get_float(%Dictionary* %.12, i8* %.5)
  store double %call_tmp.7, double* %timeout, align 8
  %host = alloca i8*, align 8
  %.14 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.8 = call i8* @dict_get_string(%Dictionary* %.14, i8* %.8)
  store i8* %call_tmp.8, i8** %host, align 8
  %.16 = load double, double* %timeout, align 8
  %.17 = sitofp i32 20 to double
  %f_cmp_tmp = fcmp ogt double %.16, %.17
  br i1 %f_cmp_tmp, label %then, label %if_cont

then:                                             ; preds = %entry
  %.19 = bitcast [31 x i8]* @.str4 to i8*
  call void @output_string(i8* %.19)
  br label %if_cont

if_cont:                                          ; preds = %then, %entry
  %.22 = bitcast [12 x i8]* @.str5 to i8*
  call void @output_string(i8* %.22)
  %.24 = load i32, i32* %max_users, align 4
  call void @output_int(i32 %.24)
  %.26 = bitcast [10 x i8]* @.str6 to i8*
  call void @output_string(i8* %.26)
  %.28 = load double, double* %timeout, align 8
  call void @output_float(double %.28, i32 2)
  %.30 = bitcast [7 x i8]* @.str7 to i8*
  call void @output_string(i8* %.30)
  %.32 = load i8*, i8** %host, align 8
  call void @output_string(i8* %.32)
  ret void
}

define i32 @main() {
entry:
  %call_tmp = call %Dictionary* @dict_create()
  store %Dictionary* %call_tmp, %Dictionary** @config, align 8
  call void @main_logic()
  ret i32 0
}
