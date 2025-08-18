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

@.str0 = internal constant [9 x i8] c"John Doe\00"
@username = internal global i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str0, i32 0, i32 0)
@age = internal global i32 0
@config = internal global %Dictionary* null
@name = internal global i8* null
@.str1 = internal constant [7 x i8] c"server\00"
@.str2 = internal constant [10 x i8] c"localhost\00"
@.str3 = internal constant [17 x i8] c"Username is null\00"
@.str4 = internal constant [23 x i8] c"Username is not null: \00"
@.str5 = internal constant [22 x i8] c"Age is null/undefined\00"
@.str6 = internal constant [17 x i8] c"Age is defined: \00"
@.str7 = internal constant [22 x i8] c"Server not configured\00"
@.str8 = internal constant [5 x i8] c"null\00"
@.str9 = internal constant [9 x i8] c"not null\00"

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
  %.2 = call %Dictionary* @dict_create()
  %.3 = bitcast [7 x i8]* @.str1 to i8*
  %.4 = bitcast [10 x i8]* @.str2 to i8*
  %.5 = call %DictValue* @new_string(i8* %.4)
  call void @dict_set(%Dictionary* %.2, i8* %.3, %DictValue* %.5)
  store %Dictionary* %.2, %Dictionary** @config, align 8
  %.8 = load i8*, i8** @username, align 8
  %null_check = icmp eq i8* %.8, null
  br i1 %null_check, label %then, label %else

then:                                             ; preds = %entry
  %.10 = bitcast [17 x i8]* @.str3 to i8*
  call void @output_string(i8* %.10)
  br label %if_cont

else:                                             ; preds = %entry
  %.13 = bitcast [23 x i8]* @.str4 to i8*
  call void @output_string(i8* %.13)
  %.15 = load i8*, i8** @username, align 8
  call void @output_string(i8* %.15)
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  %.18 = load i32, i32* @age, align 4
  br i1 false, label %then.1, label %else.1

then.1:                                           ; preds = %if_cont
  %.20 = bitcast [22 x i8]* @.str5 to i8*
  call void @output_string(i8* %.20)
  br label %if_cont.1

else.1:                                           ; preds = %if_cont
  %.23 = bitcast [17 x i8]* @.str6 to i8*
  call void @output_string(i8* %.23)
  %.25 = load i32, i32* @age, align 4
  call void @output_int(i32 %.25)
  br label %if_cont.1

if_cont.1:                                        ; preds = %else.1, %then.1
  %.28 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp = call i32 @dict_key_exists(%Dictionary* %.28, i8* %.3)
  %.29 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.1 = call i32 @dict_key_exists(%Dictionary* %.29, i8* %.3)
  %.30 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.2 = call i32 @dict_key_exists(%Dictionary* %.30, i8* %.3)
  %i_cmp_tmp = icmp eq i32 %call_tmp.2, 1
  br i1 %i_cmp_tmp, label %then.2, label %else.2

then.2:                                           ; preds = %if_cont.1
  %server = alloca i8*, align 8
  %.32 = load %Dictionary*, %Dictionary** @config, align 8
  %call_tmp.3 = call i8* @dict_get_string(%Dictionary* %.32, i8* %.3)
  store i8* %call_tmp.3, i8** %server, align 8
  %.34 = load i8*, i8** %server, align 8
  call void @output_string(i8* %.34)
  br label %if_cont.2

else.2:                                           ; preds = %if_cont.1
  %.37 = bitcast [22 x i8]* @.str7 to i8*
  call void @output_string(i8* %.37)
  br label %if_cont.2

if_cont.2:                                        ; preds = %else.2, %then.2
  %.40 = load i8*, i8** @name, align 8
  %null_check.1 = icmp eq i8* %.40, null
  br i1 %null_check.1, label %then.3, label %else.3

then.3:                                           ; preds = %if_cont.2
  %.42 = bitcast [5 x i8]* @.str8 to i8*
  call void @output_string(i8* %.42)
  br label %if_cont.3

else.3:                                           ; preds = %if_cont.2
  %.45 = bitcast [9 x i8]* @.str9 to i8*
  call void @output_string(i8* %.45)
  br label %if_cont.3

if_cont.3:                                        ; preds = %else.3, %then.3
  ret i32 0
}
