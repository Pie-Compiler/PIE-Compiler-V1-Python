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
@name1 = internal global i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str0, i32 0, i32 0)
@name2 = internal global i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str0, i32 0, i32 0)
@.str1 = internal constant [9 x i8] c"Jane Doe\00"
@name3 = internal global i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str1, i32 0, i32 0)
@.str2 = internal constant [6 x i8] c"apple\00"
@alpha1 = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str2, i32 0, i32 0)
@.str3 = internal constant [7 x i8] c"banana\00"
@alpha2 = internal global i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str3, i32 0, i32 0)
@.str4 = internal constant [7 x i8] c"cherry\00"
@alpha3 = internal global i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str4, i32 0, i32 0)
@.str5 = internal constant [3 x i8] c"hi\00"
@short_str = internal global i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str5, i32 0, i32 0)
@.str6 = internal constant [12 x i8] c"hello world\00"
@long_str = internal global i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str6, i32 0, i32 0)
@.str7 = internal constant [24 x i8] c"Hello World Programming\00"
@text = internal global i8* getelementptr inbounds ([24 x i8], [24 x i8]* @.str7, i32 0, i32 0)
@.str8 = internal constant [6 x i8] c"World\00"
@search = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str8, i32 0, i32 0)
@.str9 = internal constant [6 x i8] c"Hello\00"
@prefix = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str9, i32 0, i32 0)
@.str10 = internal constant [12 x i8] c"Programming\00"
@suffix = internal global i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str10, i32 0, i32 0)
@.str11 = internal constant [13 x i8] c"john_doe_123\00"
@username = internal global i8* getelementptr inbounds ([13 x i8], [13 x i8]* @.str11, i32 0, i32 0)
@.str12 = internal constant [10 x i8] c"secret123\00"
@password = internal global i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str12, i32 0, i32 0)
@.str13 = internal constant [6 x i8] c"admin\00"
@user_role = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str13, i32 0, i32 0)
@.str14 = internal constant [5 x i8] c"read\00"
@access_level = internal global i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str14, i32 0, i32 0)
@first = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str9, i32 0, i32 0)
@second = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str8, i32 0, i32 0)
@combined = internal global i8* null
@.str15 = internal constant [19 x i8] c"name1 equals name2\00"
@.str16 = internal constant [27 x i8] c"name1 does not equal name2\00"
@.str17 = internal constant [19 x i8] c"name1 equals name3\00"
@.str18 = internal constant [27 x i8] c"name1 does not equal name3\00"
@.str19 = internal constant [38 x i8] c"name1 does not equal name3 (correct!)\00"
@.str20 = internal constant [32 x i8] c"name1 equals name3 (incorrect!)\00"
@.str21 = internal constant [37 x i8] c"apple comes before banana (correct!)\00"
@.str22 = internal constant [34 x i8] c"apple does not come before banana\00"
@.str23 = internal constant [36 x i8] c"banana comes after apple (correct!)\00"
@.str24 = internal constant [33 x i8] c"banana does not come after apple\00"
@.str25 = internal constant [38 x i8] c"apple is less than or equal to banana\00"
@.str26 = internal constant [42 x i8] c"apple is not less than or equal to banana\00"
@.str27 = internal constant [41 x i8] c"banana is greater than or equal to apple\00"
@.str28 = internal constant [45 x i8] c"banana is not greater than or equal to apple\00"
@.str29 = internal constant [35 x i8] c"Short string length is less than 5\00"
@.str30 = internal constant [39 x i8] c"Short string length is not less than 5\00"
@.str31 = internal constant [37 x i8] c"Long string length is greater than 5\00"
@.str32 = internal constant [41 x i8] c"Long string length is not greater than 5\00"
@.str33 = internal constant [47 x i8] c"Short string length is less than or equal to 2\00"
@.str34 = internal constant [51 x i8] c"Short string length is not less than or equal to 2\00"
@.str35 = internal constant [22 x i8] c"Text contains 'World'\00"
@.str36 = internal constant [30 x i8] c"Text does not contain 'World'\00"
@.str37 = internal constant [25 x i8] c"Text starts with 'Hello'\00"
@.str38 = internal constant [33 x i8] c"Text does not start with 'Hello'\00"
@.str39 = internal constant [29 x i8] c"Text ends with 'Programming'\00"
@.str40 = internal constant [37 x i8] c"Text does not end with 'Programming'\00"
@.str41 = internal constant [1 x i8] zeroinitializer
@.str42 = internal constant [22 x i8] c"Empty string is empty\00"
@.str43 = internal constant [26 x i8] c"Empty string is not empty\00"
@.str44 = internal constant [30 x i8] c"Non-empty string is not empty\00"
@.str45 = internal constant [26 x i8] c"Non-empty string is empty\00"
@.str46 = internal constant [5 x i8] c"john\00"
@.str47 = internal constant [28 x i8] c"Username starts with 'john'\00"
@.str48 = internal constant [36 x i8] c"Username does not start with 'john'\00"
@.str49 = internal constant [2 x i8] c"_\00"
@.str50 = internal constant [29 x i8] c"Username contains underscore\00"
@.str51 = internal constant [37 x i8] c"Username does not contain underscore\00"
@.str52 = internal constant [4 x i8] c"123\00"
@.str53 = internal constant [25 x i8] c"Username ends with '123'\00"
@.str54 = internal constant [33 x i8] c"Username does not end with '123'\00"
@.str55 = internal constant [7 x i8] c"secret\00"
@.str56 = internal constant [27 x i8] c"Password contains 'secret'\00"
@.str57 = internal constant [35 x i8] c"Password does not contain 'secret'\00"
@.str58 = internal constant [37 x i8] c"Password is longer than 8 characters\00"
@.str59 = internal constant [41 x i8] c"Password is not longer than 8 characters\00"
@.str60 = internal constant [26 x i8] c"User has admin privileges\00"
@.str61 = internal constant [21 x i8] c"Access level is read\00"
@.str62 = internal constant [6 x i8] c"write\00"
@.str63 = internal constant [22 x i8] c"Access level is write\00"
@.str64 = internal constant [21 x i8] c"Unknown access level\00"
@.str65 = internal constant [5 x i8] c"user\00"
@.str66 = internal constant [29 x i8] c"User has standard privileges\00"
@.str67 = internal constant [18 x i8] c"Unknown user role\00"
@.str68 = internal constant [11 x i8] c"HelloWorld\00"
@.str69 = internal constant [37 x i8] c"String concatenation works correctly\00"
@.str70 = internal constant [28 x i8] c"String concatenation failed\00"
@.str71 = internal constant [39 x i8] c"Combined string is longer than 'Hello'\00"
@.str72 = internal constant [43 x i8] c"Combined string is not longer than 'Hello'\00"

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
  %.2 = load i8*, i8** @first, align 8
  %.3 = load i8*, i8** @second, align 8
  %concat_tmp = call i8* @concat_strings(i8* %.2, i8* %.3)
  store i8* %concat_tmp, i8** @combined, align 8
  %.5 = load i8*, i8** @name1, align 8
  %.6 = load i8*, i8** @name2, align 8
  %strcmp_result = call i32 @pie_strcmp(i8* %.5, i8* %.6)
  %str_eq = icmp eq i32 %strcmp_result, 0
  br i1 %str_eq, label %then, label %else

then:                                             ; preds = %entry
  %.8 = bitcast [19 x i8]* @.str15 to i8*
  call void @output_string(i8* %.8)
  br label %if_cont

else:                                             ; preds = %entry
  %.11 = bitcast [27 x i8]* @.str16 to i8*
  call void @output_string(i8* %.11)
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  %.14 = load i8*, i8** @name1, align 8
  %.15 = load i8*, i8** @name3, align 8
  %strcmp_result.1 = call i32 @pie_strcmp(i8* %.14, i8* %.15)
  %str_eq.1 = icmp eq i32 %strcmp_result.1, 0
  br i1 %str_eq.1, label %then.1, label %else.1

then.1:                                           ; preds = %if_cont
  %.17 = bitcast [19 x i8]* @.str17 to i8*
  call void @output_string(i8* %.17)
  br label %if_cont.1

else.1:                                           ; preds = %if_cont
  %.20 = bitcast [27 x i8]* @.str18 to i8*
  call void @output_string(i8* %.20)
  br label %if_cont.1

if_cont.1:                                        ; preds = %else.1, %then.1
  %.23 = load i8*, i8** @name1, align 8
  %.24 = load i8*, i8** @name3, align 8
  %strcmp_result.2 = call i32 @pie_strcmp(i8* %.23, i8* %.24)
  %str_ne = icmp ne i32 %strcmp_result.2, 0
  br i1 %str_ne, label %then.2, label %else.2

then.2:                                           ; preds = %if_cont.1
  %.26 = bitcast [38 x i8]* @.str19 to i8*
  call void @output_string(i8* %.26)
  br label %if_cont.2

else.2:                                           ; preds = %if_cont.1
  %.29 = bitcast [32 x i8]* @.str20 to i8*
  call void @output_string(i8* %.29)
  br label %if_cont.2

if_cont.2:                                        ; preds = %else.2, %then.2
  %.32 = load i8*, i8** @alpha1, align 8
  %.33 = load i8*, i8** @alpha2, align 8
  %strcmp_result.3 = call i32 @pie_strcmp(i8* %.32, i8* %.33)
  %str_lt = icmp slt i32 %strcmp_result.3, 0
  br i1 %str_lt, label %then.3, label %else.3

then.3:                                           ; preds = %if_cont.2
  %.35 = bitcast [37 x i8]* @.str21 to i8*
  call void @output_string(i8* %.35)
  br label %if_cont.3

else.3:                                           ; preds = %if_cont.2
  %.38 = bitcast [34 x i8]* @.str22 to i8*
  call void @output_string(i8* %.38)
  br label %if_cont.3

if_cont.3:                                        ; preds = %else.3, %then.3
  %.41 = load i8*, i8** @alpha2, align 8
  %.42 = load i8*, i8** @alpha1, align 8
  %strcmp_result.4 = call i32 @pie_strcmp(i8* %.41, i8* %.42)
  %str_gt = icmp sgt i32 %strcmp_result.4, 0
  br i1 %str_gt, label %then.4, label %else.4

then.4:                                           ; preds = %if_cont.3
  %.44 = bitcast [36 x i8]* @.str23 to i8*
  call void @output_string(i8* %.44)
  br label %if_cont.4

else.4:                                           ; preds = %if_cont.3
  %.47 = bitcast [33 x i8]* @.str24 to i8*
  call void @output_string(i8* %.47)
  br label %if_cont.4

if_cont.4:                                        ; preds = %else.4, %then.4
  %.50 = load i8*, i8** @alpha1, align 8
  %.51 = load i8*, i8** @alpha2, align 8
  %strcmp_result.5 = call i32 @pie_strcmp(i8* %.50, i8* %.51)
  %str_le = icmp sle i32 %strcmp_result.5, 0
  br i1 %str_le, label %then.5, label %else.5

then.5:                                           ; preds = %if_cont.4
  %.53 = bitcast [38 x i8]* @.str25 to i8*
  call void @output_string(i8* %.53)
  br label %if_cont.5

else.5:                                           ; preds = %if_cont.4
  %.56 = bitcast [42 x i8]* @.str26 to i8*
  call void @output_string(i8* %.56)
  br label %if_cont.5

if_cont.5:                                        ; preds = %else.5, %then.5
  %.59 = load i8*, i8** @alpha2, align 8
  %.60 = load i8*, i8** @alpha1, align 8
  %strcmp_result.6 = call i32 @pie_strcmp(i8* %.59, i8* %.60)
  %str_ge = icmp sge i32 %strcmp_result.6, 0
  br i1 %str_ge, label %then.6, label %else.6

then.6:                                           ; preds = %if_cont.5
  %.62 = bitcast [41 x i8]* @.str27 to i8*
  call void @output_string(i8* %.62)
  br label %if_cont.6

else.6:                                           ; preds = %if_cont.5
  %.65 = bitcast [45 x i8]* @.str28 to i8*
  call void @output_string(i8* %.65)
  br label %if_cont.6

if_cont.6:                                        ; preds = %else.6, %then.6
  %.68 = load i8*, i8** @short_str, align 8
  %strlen_result = call i32 @pie_strlen(i8* %.68)
  %cmp_lt = icmp slt i32 %strlen_result, 5
  br i1 %cmp_lt, label %then.7, label %else.7

then.7:                                           ; preds = %if_cont.6
  %.70 = bitcast [35 x i8]* @.str29 to i8*
  call void @output_string(i8* %.70)
  br label %if_cont.7

else.7:                                           ; preds = %if_cont.6
  %.73 = bitcast [39 x i8]* @.str30 to i8*
  call void @output_string(i8* %.73)
  br label %if_cont.7

if_cont.7:                                        ; preds = %else.7, %then.7
  %.76 = load i8*, i8** @long_str, align 8
  %strlen_result.1 = call i32 @pie_strlen(i8* %.76)
  %cmp_gt = icmp sgt i32 %strlen_result.1, 5
  br i1 %cmp_gt, label %then.8, label %else.8

then.8:                                           ; preds = %if_cont.7
  %.78 = bitcast [37 x i8]* @.str31 to i8*
  call void @output_string(i8* %.78)
  br label %if_cont.8

else.8:                                           ; preds = %if_cont.7
  %.81 = bitcast [41 x i8]* @.str32 to i8*
  call void @output_string(i8* %.81)
  br label %if_cont.8

if_cont.8:                                        ; preds = %else.8, %then.8
  %.84 = load i8*, i8** @short_str, align 8
  %strlen_result.2 = call i32 @pie_strlen(i8* %.84)
  %cmp_le = icmp sle i32 %strlen_result.2, 2
  br i1 %cmp_le, label %then.9, label %else.9

then.9:                                           ; preds = %if_cont.8
  %.86 = bitcast [47 x i8]* @.str33 to i8*
  call void @output_string(i8* %.86)
  br label %if_cont.9

else.9:                                           ; preds = %if_cont.8
  %.89 = bitcast [51 x i8]* @.str34 to i8*
  call void @output_string(i8* %.89)
  br label %if_cont.9

if_cont.9:                                        ; preds = %else.9, %then.9
  %.92 = load i8*, i8** @text, align 8
  %.93 = load i8*, i8** @search, align 8
  %call_tmp = call i32 @string_contains(i8* %.92, i8* %.93)
  %.94 = load i8*, i8** @text, align 8
  %.95 = load i8*, i8** @search, align 8
  %call_tmp.1 = call i32 @string_contains(i8* %.94, i8* %.95)
  %.96 = load i8*, i8** @text, align 8
  %.97 = load i8*, i8** @search, align 8
  %call_tmp.2 = call i32 @string_contains(i8* %.96, i8* %.97)
  %i_cmp_tmp = icmp eq i32 %call_tmp.2, 1
  br i1 %i_cmp_tmp, label %then.10, label %else.10

then.10:                                          ; preds = %if_cont.9
  %.99 = bitcast [22 x i8]* @.str35 to i8*
  call void @output_string(i8* %.99)
  br label %if_cont.10

else.10:                                          ; preds = %if_cont.9
  %.102 = bitcast [30 x i8]* @.str36 to i8*
  call void @output_string(i8* %.102)
  br label %if_cont.10

if_cont.10:                                       ; preds = %else.10, %then.10
  %.105 = load i8*, i8** @text, align 8
  %.106 = load i8*, i8** @prefix, align 8
  %call_tmp.3 = call i32 @string_starts_with(i8* %.105, i8* %.106)
  %.107 = load i8*, i8** @text, align 8
  %.108 = load i8*, i8** @prefix, align 8
  %call_tmp.4 = call i32 @string_starts_with(i8* %.107, i8* %.108)
  %.109 = load i8*, i8** @text, align 8
  %.110 = load i8*, i8** @prefix, align 8
  %call_tmp.5 = call i32 @string_starts_with(i8* %.109, i8* %.110)
  %i_cmp_tmp.1 = icmp eq i32 %call_tmp.5, 1
  br i1 %i_cmp_tmp.1, label %then.11, label %else.11

then.11:                                          ; preds = %if_cont.10
  %.112 = bitcast [25 x i8]* @.str37 to i8*
  call void @output_string(i8* %.112)
  br label %if_cont.11

else.11:                                          ; preds = %if_cont.10
  %.115 = bitcast [33 x i8]* @.str38 to i8*
  call void @output_string(i8* %.115)
  br label %if_cont.11

if_cont.11:                                       ; preds = %else.11, %then.11
  %.118 = load i8*, i8** @text, align 8
  %.119 = load i8*, i8** @suffix, align 8
  %call_tmp.6 = call i32 @string_ends_with(i8* %.118, i8* %.119)
  %.120 = load i8*, i8** @text, align 8
  %.121 = load i8*, i8** @suffix, align 8
  %call_tmp.7 = call i32 @string_ends_with(i8* %.120, i8* %.121)
  %.122 = load i8*, i8** @text, align 8
  %.123 = load i8*, i8** @suffix, align 8
  %call_tmp.8 = call i32 @string_ends_with(i8* %.122, i8* %.123)
  %i_cmp_tmp.2 = icmp eq i32 %call_tmp.8, 1
  br i1 %i_cmp_tmp.2, label %then.12, label %else.12

then.12:                                          ; preds = %if_cont.11
  %.125 = bitcast [29 x i8]* @.str39 to i8*
  call void @output_string(i8* %.125)
  br label %if_cont.12

else.12:                                          ; preds = %if_cont.11
  %.128 = bitcast [37 x i8]* @.str40 to i8*
  call void @output_string(i8* %.128)
  br label %if_cont.12

if_cont.12:                                       ; preds = %else.12, %then.12
  %.131 = bitcast [1 x i8]* @.str41 to i8*
  %call_tmp.9 = call i32 @string_is_empty(i8* %.131)
  %.132 = bitcast [1 x i8]* @.str41 to i8*
  %call_tmp.10 = call i32 @string_is_empty(i8* %.132)
  %.133 = bitcast [1 x i8]* @.str41 to i8*
  %call_tmp.11 = call i32 @string_is_empty(i8* %.133)
  %i_cmp_tmp.3 = icmp eq i32 %call_tmp.11, 1
  br i1 %i_cmp_tmp.3, label %then.13, label %else.13

then.13:                                          ; preds = %if_cont.12
  %.135 = bitcast [22 x i8]* @.str42 to i8*
  call void @output_string(i8* %.135)
  br label %if_cont.13

else.13:                                          ; preds = %if_cont.12
  %.138 = bitcast [26 x i8]* @.str43 to i8*
  call void @output_string(i8* %.138)
  br label %if_cont.13

if_cont.13:                                       ; preds = %else.13, %then.13
  %.141 = load i8*, i8** @text, align 8
  %call_tmp.12 = call i32 @string_is_empty(i8* %.141)
  %.142 = load i8*, i8** @text, align 8
  %call_tmp.13 = call i32 @string_is_empty(i8* %.142)
  %.143 = load i8*, i8** @text, align 8
  %call_tmp.14 = call i32 @string_is_empty(i8* %.143)
  %i_cmp_tmp.4 = icmp eq i32 %call_tmp.14, 0
  br i1 %i_cmp_tmp.4, label %then.14, label %else.14

then.14:                                          ; preds = %if_cont.13
  %.145 = bitcast [30 x i8]* @.str44 to i8*
  call void @output_string(i8* %.145)
  br label %if_cont.14

else.14:                                          ; preds = %if_cont.13
  %.148 = bitcast [26 x i8]* @.str45 to i8*
  call void @output_string(i8* %.148)
  br label %if_cont.14

if_cont.14:                                       ; preds = %else.14, %then.14
  %.151 = load i8*, i8** @username, align 8
  %.152 = bitcast [5 x i8]* @.str46 to i8*
  %call_tmp.15 = call i32 @string_starts_with(i8* %.151, i8* %.152)
  %.153 = load i8*, i8** @username, align 8
  %.154 = bitcast [5 x i8]* @.str46 to i8*
  %call_tmp.16 = call i32 @string_starts_with(i8* %.153, i8* %.154)
  %.155 = load i8*, i8** @username, align 8
  %.156 = bitcast [5 x i8]* @.str46 to i8*
  %call_tmp.17 = call i32 @string_starts_with(i8* %.155, i8* %.156)
  %i_cmp_tmp.5 = icmp eq i32 %call_tmp.17, 1
  br i1 %i_cmp_tmp.5, label %then.15, label %else.15

then.15:                                          ; preds = %if_cont.14
  %.158 = bitcast [28 x i8]* @.str47 to i8*
  call void @output_string(i8* %.158)
  br label %if_cont.15

else.15:                                          ; preds = %if_cont.14
  %.161 = bitcast [36 x i8]* @.str48 to i8*
  call void @output_string(i8* %.161)
  br label %if_cont.15

if_cont.15:                                       ; preds = %else.15, %then.15
  %.164 = load i8*, i8** @username, align 8
  %.165 = bitcast [2 x i8]* @.str49 to i8*
  %call_tmp.18 = call i32 @string_contains(i8* %.164, i8* %.165)
  %.166 = load i8*, i8** @username, align 8
  %.167 = bitcast [2 x i8]* @.str49 to i8*
  %call_tmp.19 = call i32 @string_contains(i8* %.166, i8* %.167)
  %.168 = load i8*, i8** @username, align 8
  %.169 = bitcast [2 x i8]* @.str49 to i8*
  %call_tmp.20 = call i32 @string_contains(i8* %.168, i8* %.169)
  %i_cmp_tmp.6 = icmp eq i32 %call_tmp.20, 1
  br i1 %i_cmp_tmp.6, label %then.16, label %else.16

then.16:                                          ; preds = %if_cont.15
  %.171 = bitcast [29 x i8]* @.str50 to i8*
  call void @output_string(i8* %.171)
  br label %if_cont.16

else.16:                                          ; preds = %if_cont.15
  %.174 = bitcast [37 x i8]* @.str51 to i8*
  call void @output_string(i8* %.174)
  br label %if_cont.16

if_cont.16:                                       ; preds = %else.16, %then.16
  %.177 = load i8*, i8** @username, align 8
  %.178 = bitcast [4 x i8]* @.str52 to i8*
  %call_tmp.21 = call i32 @string_ends_with(i8* %.177, i8* %.178)
  %.179 = load i8*, i8** @username, align 8
  %.180 = bitcast [4 x i8]* @.str52 to i8*
  %call_tmp.22 = call i32 @string_ends_with(i8* %.179, i8* %.180)
  %.181 = load i8*, i8** @username, align 8
  %.182 = bitcast [4 x i8]* @.str52 to i8*
  %call_tmp.23 = call i32 @string_ends_with(i8* %.181, i8* %.182)
  %i_cmp_tmp.7 = icmp eq i32 %call_tmp.23, 1
  br i1 %i_cmp_tmp.7, label %then.17, label %else.17

then.17:                                          ; preds = %if_cont.16
  %.184 = bitcast [25 x i8]* @.str53 to i8*
  call void @output_string(i8* %.184)
  br label %if_cont.17

else.17:                                          ; preds = %if_cont.16
  %.187 = bitcast [33 x i8]* @.str54 to i8*
  call void @output_string(i8* %.187)
  br label %if_cont.17

if_cont.17:                                       ; preds = %else.17, %then.17
  %.190 = load i8*, i8** @password, align 8
  %.191 = bitcast [7 x i8]* @.str55 to i8*
  %call_tmp.24 = call i32 @string_contains(i8* %.190, i8* %.191)
  %.192 = load i8*, i8** @password, align 8
  %.193 = bitcast [7 x i8]* @.str55 to i8*
  %call_tmp.25 = call i32 @string_contains(i8* %.192, i8* %.193)
  %.194 = load i8*, i8** @password, align 8
  %.195 = bitcast [7 x i8]* @.str55 to i8*
  %call_tmp.26 = call i32 @string_contains(i8* %.194, i8* %.195)
  %i_cmp_tmp.8 = icmp eq i32 %call_tmp.26, 1
  br i1 %i_cmp_tmp.8, label %then.18, label %else.18

then.18:                                          ; preds = %if_cont.17
  %.197 = bitcast [27 x i8]* @.str56 to i8*
  call void @output_string(i8* %.197)
  br label %if_cont.18

else.18:                                          ; preds = %if_cont.17
  %.200 = bitcast [35 x i8]* @.str57 to i8*
  call void @output_string(i8* %.200)
  br label %if_cont.18

if_cont.18:                                       ; preds = %else.18, %then.18
  %.203 = load i8*, i8** @password, align 8
  %strlen_result.3 = call i32 @pie_strlen(i8* %.203)
  %cmp_gt.1 = icmp sgt i32 %strlen_result.3, 8
  br i1 %cmp_gt.1, label %then.19, label %else.19

then.19:                                          ; preds = %if_cont.18
  %.205 = bitcast [37 x i8]* @.str58 to i8*
  call void @output_string(i8* %.205)
  br label %if_cont.19

else.19:                                          ; preds = %if_cont.18
  %.208 = bitcast [41 x i8]* @.str59 to i8*
  call void @output_string(i8* %.208)
  br label %if_cont.19

if_cont.19:                                       ; preds = %else.19, %then.19
  %.211 = load i8*, i8** @user_role, align 8
  %strcmp_result.7 = call i32 @pie_strcmp(i8* %.211, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str13, i32 0, i32 0))
  %str_eq.2 = icmp eq i32 %strcmp_result.7, 0
  br i1 %str_eq.2, label %then.20, label %else.20

then.20:                                          ; preds = %if_cont.19
  %.213 = bitcast [26 x i8]* @.str60 to i8*
  call void @output_string(i8* %.213)
  %.215 = load i8*, i8** @access_level, align 8
  %strcmp_result.8 = call i32 @pie_strcmp(i8* %.215, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str14, i32 0, i32 0))
  %str_eq.3 = icmp eq i32 %strcmp_result.8, 0
  br i1 %str_eq.3, label %then.21, label %else.21

else.20:                                          ; preds = %if_cont.19
  %.232 = bitcast [5 x i8]* @.str65 to i8*
  %.233 = bitcast [5 x i8]* @.str65 to i8*
  %.234 = load i8*, i8** @user_role, align 8
  %strcmp_result.10 = call i32 @pie_strcmp(i8* %.234, i8* %.233)
  %str_eq.5 = icmp eq i32 %strcmp_result.10, 0
  br i1 %str_eq.5, label %then.23, label %else.23

if_cont.20:                                       ; preds = %if_cont.23, %if_cont.21
  %.243 = bitcast [11 x i8]* @.str68 to i8*
  %.244 = bitcast [11 x i8]* @.str68 to i8*
  %.245 = load i8*, i8** @combined, align 8
  %strcmp_result.11 = call i32 @pie_strcmp(i8* %.245, i8* %.244)
  %str_eq.6 = icmp eq i32 %strcmp_result.11, 0
  br i1 %str_eq.6, label %then.24, label %else.24

then.21:                                          ; preds = %then.20
  %.217 = bitcast [21 x i8]* @.str61 to i8*
  call void @output_string(i8* %.217)
  br label %if_cont.21

else.21:                                          ; preds = %then.20
  %.220 = bitcast [6 x i8]* @.str62 to i8*
  %.221 = bitcast [6 x i8]* @.str62 to i8*
  %.222 = load i8*, i8** @access_level, align 8
  %strcmp_result.9 = call i32 @pie_strcmp(i8* %.222, i8* %.221)
  %str_eq.4 = icmp eq i32 %strcmp_result.9, 0
  br i1 %str_eq.4, label %then.22, label %else.22

if_cont.21:                                       ; preds = %if_cont.22, %then.21
  br label %if_cont.20

then.22:                                          ; preds = %else.21
  %.224 = bitcast [22 x i8]* @.str63 to i8*
  call void @output_string(i8* %.224)
  br label %if_cont.22

else.22:                                          ; preds = %else.21
  %.227 = bitcast [21 x i8]* @.str64 to i8*
  call void @output_string(i8* %.227)
  br label %if_cont.22

if_cont.22:                                       ; preds = %else.22, %then.22
  br label %if_cont.21

then.23:                                          ; preds = %else.20
  %.236 = bitcast [29 x i8]* @.str66 to i8*
  call void @output_string(i8* %.236)
  br label %if_cont.23

else.23:                                          ; preds = %else.20
  %.239 = bitcast [18 x i8]* @.str67 to i8*
  call void @output_string(i8* %.239)
  br label %if_cont.23

if_cont.23:                                       ; preds = %else.23, %then.23
  br label %if_cont.20

then.24:                                          ; preds = %if_cont.20
  %.247 = bitcast [37 x i8]* @.str69 to i8*
  call void @output_string(i8* %.247)
  br label %if_cont.24

else.24:                                          ; preds = %if_cont.20
  %.250 = bitcast [28 x i8]* @.str70 to i8*
  call void @output_string(i8* %.250)
  br label %if_cont.24

if_cont.24:                                       ; preds = %else.24, %then.24
  %.253 = load i8*, i8** @combined, align 8
  %strcmp_result.12 = call i32 @pie_strcmp(i8* %.253, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str9, i32 0, i32 0))
  %str_gt.1 = icmp sgt i32 %strcmp_result.12, 0
  br i1 %str_gt.1, label %then.25, label %else.25

then.25:                                          ; preds = %if_cont.24
  %.255 = bitcast [39 x i8]* @.str71 to i8*
  call void @output_string(i8* %.255)
  br label %if_cont.25

else.25:                                          ; preds = %if_cont.24
  %.258 = bitcast [43 x i8]* @.str72 to i8*
  call void @output_string(i8* %.258)
  br label %if_cont.25

if_cont.25:                                       ; preds = %else.25, %then.25
  ret i32 0
}
