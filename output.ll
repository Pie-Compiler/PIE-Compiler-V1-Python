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

@username = internal global i8* null
@.str0 = internal constant [14 x i8] c"john123adsasd\00"
@user = internal global i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str0, i32 0, i32 0)
@.str1 = internal constant [80 x i8] c"(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)+>2<21\00"
@.str2 = internal constant [15 x i8] c"Username valid\00"
@.str3 = internal constant [33 x i8] c"Username must be 3-20 characters\00"

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
  %.2 = bitcast [80 x i8]* @.str1 to i8*
  %call_tmp = call i8* @regex_compile(i8* %.2)
  store i8* %call_tmp, i8** @username, align 8
  %.4 = load i8*, i8** @username, align 8
  %.5 = load i8*, i8** @user, align 8
  %call_tmp.1 = call i32 @regex_match(i8* %.4, i8* %.5)
  %.6 = load i8*, i8** @username, align 8
  %.7 = load i8*, i8** @user, align 8
  %call_tmp.2 = call i32 @regex_match(i8* %.6, i8* %.7)
  %.8 = load i8*, i8** @username, align 8
  %.9 = load i8*, i8** @user, align 8
  %call_tmp.3 = call i32 @regex_match(i8* %.8, i8* %.9)
  %i_cmp_tmp = icmp eq i32 %call_tmp.3, 1
  br i1 %i_cmp_tmp, label %then, label %else

then:                                             ; preds = %entry
  %.11 = bitcast [15 x i8]* @.str2 to i8*
  call void @output_string(i8* %.11)
  br label %if_cont

else:                                             ; preds = %entry
  %.14 = bitcast [33 x i8]* @.str3 to i8*
  call void @output_string(i8* %.14)
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  ret i32 0
}
