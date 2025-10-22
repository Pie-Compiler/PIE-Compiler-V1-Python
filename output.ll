; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@x = internal global i32 10
@y = internal global i32 20
@.str0 = internal constant [13 x i8] c"Same message\00"
@message = internal global ptr @.str0
@nullable_str = internal global ptr null
@.str1 = internal constant [41 x i8] c"=== Testing Conditionals with Output ===\00"
@.str2 = internal constant [25 x i8] c"Test 1: x is less than y\00"
@.str3 = internal constant [29 x i8] c"Test 1: x is not less than y\00"
@.str4 = internal constant [28 x i8] c"Test 2: x is greater than 5\00"
@.str5 = internal constant [34 x i8] c"Test 2: y is also greater than 15\00"
@.str6 = internal constant [29 x i8] c"Test 4: Both conditions true\00"
@.str7 = internal constant [36 x i8] c"Test 4: At least one condition true\00"
@.str8 = internal constant [23 x i8] c"Test 5: String is null\00"
@.str9 = internal constant [27 x i8] c"Test 5: String is not null\00"
@.str10 = internal constant [37 x i8] c"=== All Conditional Tests Passed ===\00"

declare void @input_int(ptr)

declare void @input_float(ptr)

declare void @input_string(ptr)

declare void @input_char(ptr)

declare void @output_int(i32)

declare void @output_string(ptr)

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

declare ptr @concat_strings(ptr, ptr)

declare i32 @pie_strlen(ptr)

declare i32 @pie_strcmp(ptr, ptr)

declare ptr @pie_strcpy(ptr, ptr)

declare ptr @pie_strcat(ptr, ptr)

declare ptr @string_to_upper(ptr)

declare ptr @string_to_lower(ptr)

declare ptr @string_trim(ptr)

declare ptr @string_substring(ptr, i32, i32)

declare i32 @string_index_of(ptr, ptr)

declare ptr @string_replace_char(ptr, i8, i8)

declare ptr @string_reverse(ptr)

declare i32 @string_count_char(ptr, i8)

declare i64 @file_open(ptr, ptr)

declare void @file_close(i64)

declare void @file_write(i64, ptr)

declare ptr @file_read_all(i64)

declare ptr @file_read_line(i64)

declare ptr @dict_create()

declare void @dict_set(ptr, ptr, ptr)

declare ptr @dict_get(ptr, ptr)

declare i32 @dict_get_int(ptr, ptr)

declare double @dict_get_float(ptr, ptr)

declare ptr @dict_get_string(ptr, ptr)

declare i32 @dict_has_key(ptr, ptr)

declare i32 @dict_key_exists(ptr, ptr)

declare void @dict_delete(ptr, ptr)

declare void @dict_free(ptr)

declare ptr @dict_value_create_int(i32)

declare ptr @dict_value_create_float(double)

declare ptr @dict_value_create_string(ptr)

declare ptr @dict_value_create_null()

declare ptr @new_int(i32)

declare ptr @new_float(double)

declare ptr @new_string(ptr)

declare i32 @is_variable_defined(ptr)

declare i32 @is_variable_null(ptr)

declare i32 @string_contains(ptr, ptr)

declare i32 @string_starts_with(ptr, ptr)

declare i32 @string_ends_with(ptr, ptr)

declare i32 @string_is_empty(ptr)

declare void @d_array_int_push(ptr, i32)

declare i32 @d_array_int_pop(ptr)

declare i32 @d_array_int_size(ptr)

declare i32 @d_array_int_contains(ptr, i32)

declare i32 @d_array_int_indexof(ptr, i32)

declare ptr @d_array_int_concat(ptr, ptr)

declare double @d_array_int_avg(ptr)

declare i32 @d_array_int_get(ptr, i32)

declare void @d_array_int_set(ptr, i32, i32)

declare void @d_array_string_push(ptr, ptr)

declare ptr @d_array_string_pop(ptr)

declare i32 @d_array_string_size(ptr)

declare i32 @d_array_string_contains(ptr, ptr)

declare i32 @d_array_string_indexof(ptr, ptr)

declare ptr @d_array_string_concat(ptr, ptr)

declare ptr @d_array_string_get(ptr, i32)

declare void @d_array_string_set(ptr, i32, ptr)

declare void @d_array_float_push(ptr, double)

declare double @d_array_float_pop(ptr)

declare i32 @d_array_float_size(ptr)

declare i32 @d_array_float_contains(ptr, double)

declare i32 @d_array_float_indexof(ptr, double)

declare double @d_array_float_avg(ptr)

declare ptr @d_array_int_create()

declare ptr @d_array_string_create()

declare ptr @d_array_float_create()

declare void @d_array_int_append(ptr, i32)

declare void @d_array_string_append(ptr, ptr)

declare void @d_array_float_append(ptr, double)

declare double @d_array_float_get(ptr, i32)

declare void @d_array_float_set(ptr, i32, double)

declare void @d_array_float_free(ptr)

declare void @print_int_array(ptr)

declare void @print_string_array(ptr)

declare void @print_float_array(ptr)

declare void @print_char_array(ptr)

declare ptr @d_array_char_create()

declare void @d_array_char_append(ptr, i8)

declare i8 @d_array_char_get(ptr, i32)

declare void @d_array_char_set(ptr, i32, i8)

declare i32 @d_array_char_size(ptr)

declare void @d_array_char_free(ptr)

declare i8 @d_array_char_pop(ptr)

declare i1 @d_array_char_contains(ptr, i8)

declare i32 @d_array_char_indexof(ptr, i8)

declare ptr @d_array_char_concat(ptr, ptr)

define i32 @main() {
entry:
  %.2 = bitcast ptr @.str1 to ptr
  call void @output_string(ptr %.2)
  %.4 = load i32, ptr @x, align 4
  %.5 = load i32, ptr @y, align 4
  %i_cmp_tmp = icmp slt i32 %.4, %.5
  br i1 %i_cmp_tmp, label %then, label %else

then:                                             ; preds = %entry
  %.7 = bitcast ptr @.str2 to ptr
  call void @output_string(ptr %.7)
  br label %if_cont

else:                                             ; preds = %entry
  %.10 = bitcast ptr @.str3 to ptr
  call void @output_string(ptr %.10)
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  %.13 = load i32, ptr @x, align 4
  %i_cmp_tmp.1 = icmp sgt i32 %.13, 5
  br i1 %i_cmp_tmp.1, label %then.1, label %if_cont.1

then.1:                                           ; preds = %if_cont
  %.15 = bitcast ptr @.str4 to ptr
  call void @output_string(ptr %.15)
  %.17 = load i32, ptr @y, align 4
  %i_cmp_tmp.2 = icmp sgt i32 %.17, 15
  br i1 %i_cmp_tmp.2, label %then.2, label %if_cont.2

if_cont.1:                                        ; preds = %if_cont.2, %if_cont
  %.23 = load i32, ptr @x, align 4
  %i_cmp_tmp.3 = icmp eq i32 %.23, 10
  br i1 %i_cmp_tmp.3, label %then.3, label %if_cont.3

then.2:                                           ; preds = %then.1
  %.19 = bitcast ptr @.str5 to ptr
  call void @output_string(ptr %.19)
  br label %if_cont.2

if_cont.2:                                        ; preds = %then.2, %then.1
  br label %if_cont.1

then.3:                                           ; preds = %if_cont.1
  %.25 = load ptr, ptr @message, align 8
  call void @output_string(ptr %.25)
  br label %if_cont.3

if_cont.3:                                        ; preds = %then.3, %if_cont.1
  %.28 = load i32, ptr @y, align 4
  %i_cmp_tmp.4 = icmp eq i32 %.28, 20
  br i1 %i_cmp_tmp.4, label %then.4, label %if_cont.4

then.4:                                           ; preds = %if_cont.3
  %.30 = load ptr, ptr @message, align 8
  call void @output_string(ptr %.30)
  br label %if_cont.4

if_cont.4:                                        ; preds = %then.4, %if_cont.3
  %.33 = load i32, ptr @x, align 4
  %i_cmp_tmp.5 = icmp sgt i32 %.33, 5
  %.34 = load i32, ptr @y, align 4
  %i_cmp_tmp.6 = icmp slt i32 %.34, 30
  %and_tmp = and i1 %i_cmp_tmp.5, %i_cmp_tmp.6
  br i1 %and_tmp, label %then.5, label %if_cont.5

then.5:                                           ; preds = %if_cont.4
  %.36 = bitcast ptr @.str6 to ptr
  call void @output_string(ptr %.36)
  br label %if_cont.5

if_cont.5:                                        ; preds = %then.5, %if_cont.4
  %.39 = load i32, ptr @x, align 4
  %i_cmp_tmp.7 = icmp slt i32 %.39, 5
  %.40 = load i32, ptr @y, align 4
  %i_cmp_tmp.8 = icmp sgt i32 %.40, 15
  %or_tmp = or i1 %i_cmp_tmp.7, %i_cmp_tmp.8
  br i1 %or_tmp, label %then.6, label %if_cont.6

then.6:                                           ; preds = %if_cont.5
  %.42 = bitcast ptr @.str7 to ptr
  call void @output_string(ptr %.42)
  br label %if_cont.6

if_cont.6:                                        ; preds = %then.6, %if_cont.5
  %.45 = load ptr, ptr @nullable_str, align 8
  %null_check = icmp eq ptr %.45, null
  br i1 %null_check, label %then.7, label %else.1

then.7:                                           ; preds = %if_cont.6
  %.47 = bitcast ptr @.str8 to ptr
  call void @output_string(ptr %.47)
  br label %if_cont.7

else.1:                                           ; preds = %if_cont.6
  %.50 = bitcast ptr @.str9 to ptr
  call void @output_string(ptr %.50)
  br label %if_cont.7

if_cont.7:                                        ; preds = %else.1, %then.7
  %.53 = bitcast ptr @.str10 to ptr
  call void @output_string(ptr %.53)
  ret i32 0
}
