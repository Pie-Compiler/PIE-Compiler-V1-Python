; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%DArrayInt = type { i32*, i64, i64 }
%DArrayString = type { i8**, i64, i64 }
%DArrayChar = type { i8*, i64, i64 }
%DArrayFloat = type { double*, i64, i64 }

@target_num = internal global i32 42
@.str0 = internal constant [4 x i8] c"Bob\00"
@target_name = internal global i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str0, i32 0, i32 0)
@target_grade = internal global i8 66
@target_score = internal global double 8.550000e+01
@numbers = internal global %DArrayInt* null
@names = internal global %DArrayString* null
@grades = internal global %DArrayChar* null
@scores = internal global %DArrayFloat* null
@num_index = internal global i32 0
@name_index = internal global i32 0
@grade_index = internal global i32 0
@score_index = internal global i32 0
@.str1 = internal constant [6 x i8] c"David\00"
@new_name = internal global i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str1, i32 0, i32 0)
@new_number = internal global i32 50
@new_grade = internal global i8 68
@new_score = internal global double 6.700000e+01
@popped = internal global double 0.000000e+00
@.str2 = internal constant [6 x i8] c"Alice\00"
@.str3 = internal constant [8 x i8] c"Charlie\00"
@.str4 = internal constant [37 x i8] c"Testing arr_contains with variables:\00"
@.str5 = internal constant [21 x i8] c"Found target number!\00"
@.str6 = internal constant [19 x i8] c"Found target name!\00"
@.str7 = internal constant [20 x i8] c"Found target grade!\00"
@.str8 = internal constant [20 x i8] c"Found target score!\00"
@.str9 = internal constant [36 x i8] c"Testing arr_indexof with variables:\00"
@.str10 = internal constant [21 x i8] c"Target number index:\00"
@.str11 = internal constant [19 x i8] c"Target name index:\00"
@.str12 = internal constant [20 x i8] c"Target grade index:\00"
@.str13 = internal constant [20 x i8] c"Target score index:\00"
@.str14 = internal constant [25 x i8] c"After pushing variables:\00"
@.str15 = internal constant [7 x i8] c"Names:\00"
@.str16 = internal constant [9 x i8] c"Numbers:\00"
@.str17 = internal constant [8 x i8] c"Grades:\00"
@.str18 = internal constant [8 x i8] c"Scores:\00"

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
  call void @d_array_int_append(%DArrayInt* %.2, i32 10)
  call void @d_array_int_append(%DArrayInt* %.2, i32 20)
  call void @d_array_int_append(%DArrayInt* %.2, i32 42)
  call void @d_array_int_append(%DArrayInt* %.2, i32 30)
  %.8 = call %DArrayString* @d_array_string_create()
  store %DArrayString* %.8, %DArrayString** @names, align 8
  %.10 = bitcast [6 x i8]* @.str2 to i8*
  call void @d_array_string_append(%DArrayString* %.8, i8* %.10)
  call void @d_array_string_append(%DArrayString* %.8, i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str0, i32 0, i32 0))
  %.13 = bitcast [8 x i8]* @.str3 to i8*
  call void @d_array_string_append(%DArrayString* %.8, i8* %.13)
  %.15 = call %DArrayChar* @d_array_char_create()
  store %DArrayChar* %.15, %DArrayChar** @grades, align 8
  call void @d_array_char_append(%DArrayChar* %.15, i8 65)
  call void @d_array_char_append(%DArrayChar* %.15, i8 66)
  call void @d_array_char_append(%DArrayChar* %.15, i8 67)
  %.20 = call %DArrayFloat* @d_array_float_create()
  store %DArrayFloat* %.20, %DArrayFloat** @scores, align 8
  call void @d_array_float_append(%DArrayFloat* %.20, double 7.850000e+01)
  call void @d_array_float_append(%DArrayFloat* %.20, double 8.550000e+01)
  call void @d_array_float_append(%DArrayFloat* %.20, double 9.200000e+01)
  %.25 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.26 = load i32, i32* @target_num, align 4
  %.27 = call i32 @d_array_int_indexof(%DArrayInt* %.25, i32 %.26)
  store i32 %.27, i32* @num_index, align 4
  %.29 = load %DArrayString*, %DArrayString** @names, align 8
  %.30 = load i8*, i8** @target_name, align 8
  %.31 = call i32 @d_array_string_indexof(%DArrayString* %.29, i8* %.30)
  store i32 %.31, i32* @name_index, align 4
  %.33 = load %DArrayChar*, %DArrayChar** @grades, align 8
  %.34 = load i8, i8* @target_grade, align 1
  %.35 = call i32 @d_array_char_indexof(%DArrayChar* %.33, i8 %.34)
  store i32 %.35, i32* @grade_index, align 4
  %.37 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  %.38 = load double, double* @target_score, align 8
  %.39 = call i32 @d_array_float_indexof(%DArrayFloat* %.37, double %.38)
  store i32 %.39, i32* @score_index, align 4
  %.41 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  %.42 = call double @d_array_float_pop(%DArrayFloat* %.41)
  store double %.42, double* @popped, align 8
  %.44 = bitcast [37 x i8]* @.str4 to i8*
  call void @output_string(i8* %.44)
  %.46 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.47 = load i32, i32* @target_num, align 4
  %.48 = call i32 @d_array_int_contains(%DArrayInt* %.46, i32 %.47)
  %bool_cond = icmp ne i32 %.48, 0
  br i1 %bool_cond, label %then, label %if_cont

then:                                             ; preds = %entry
  %.50 = bitcast [21 x i8]* @.str5 to i8*
  call void @output_string(i8* %.50)
  br label %if_cont

if_cont:                                          ; preds = %then, %entry
  %.53 = load %DArrayString*, %DArrayString** @names, align 8
  %.54 = load i8*, i8** @target_name, align 8
  %.55 = call i32 @d_array_string_contains(%DArrayString* %.53, i8* %.54)
  %bool_cond.1 = icmp ne i32 %.55, 0
  br i1 %bool_cond.1, label %then.1, label %if_cont.1

then.1:                                           ; preds = %if_cont
  %.57 = bitcast [19 x i8]* @.str6 to i8*
  call void @output_string(i8* %.57)
  br label %if_cont.1

if_cont.1:                                        ; preds = %then.1, %if_cont
  %.60 = load %DArrayChar*, %DArrayChar** @grades, align 8
  %.61 = load i8, i8* @target_grade, align 1
  %.62 = call i1 @d_array_char_contains(%DArrayChar* %.60, i8 %.61)
  br i1 %.62, label %then.2, label %if_cont.2

then.2:                                           ; preds = %if_cont.1
  %.64 = bitcast [20 x i8]* @.str7 to i8*
  call void @output_string(i8* %.64)
  br label %if_cont.2

if_cont.2:                                        ; preds = %then.2, %if_cont.1
  %.67 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  %.68 = load double, double* @target_score, align 8
  %.69 = call i32 @d_array_float_contains(%DArrayFloat* %.67, double %.68)
  %bool_cond.2 = icmp ne i32 %.69, 0
  br i1 %bool_cond.2, label %then.3, label %if_cont.3

then.3:                                           ; preds = %if_cont.2
  %.71 = bitcast [20 x i8]* @.str8 to i8*
  call void @output_string(i8* %.71)
  br label %if_cont.3

if_cont.3:                                        ; preds = %then.3, %if_cont.2
  %.74 = bitcast [36 x i8]* @.str9 to i8*
  call void @output_string(i8* %.74)
  %.76 = bitcast [21 x i8]* @.str10 to i8*
  call void @output_string(i8* %.76)
  %.78 = load i32, i32* @num_index, align 4
  call void @output_int(i32 %.78)
  %.80 = bitcast [19 x i8]* @.str11 to i8*
  call void @output_string(i8* %.80)
  %.82 = load i32, i32* @name_index, align 4
  call void @output_int(i32 %.82)
  %.84 = bitcast [20 x i8]* @.str12 to i8*
  call void @output_string(i8* %.84)
  %.86 = load i32, i32* @grade_index, align 4
  call void @output_int(i32 %.86)
  %.88 = bitcast [20 x i8]* @.str13 to i8*
  call void @output_string(i8* %.88)
  %.90 = load i32, i32* @score_index, align 4
  call void @output_int(i32 %.90)
  %.92 = load %DArrayString*, %DArrayString** @names, align 8
  %.93 = load i8*, i8** @new_name, align 8
  call void @d_array_string_push(%DArrayString* %.92, i8* %.93)
  %.95 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  %.96 = load i32, i32* @new_number, align 4
  call void @d_array_int_push(%DArrayInt* %.95, i32 %.96)
  %.98 = load %DArrayChar*, %DArrayChar** @grades, align 8
  %.99 = load i8, i8* @new_grade, align 1
  call void @d_array_char_append(%DArrayChar* %.98, i8 %.99)
  %.101 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  %.102 = load double, double* @new_score, align 8
  call void @d_array_float_push(%DArrayFloat* %.101, double %.102)
  %.104 = bitcast [25 x i8]* @.str14 to i8*
  call void @output_string(i8* %.104)
  %.106 = bitcast [7 x i8]* @.str15 to i8*
  call void @output_string(i8* %.106)
  %.108 = load %DArrayString*, %DArrayString** @names, align 8
  call void @print_string_array(%DArrayString* %.108)
  %.110 = bitcast [9 x i8]* @.str16 to i8*
  call void @output_string(i8* %.110)
  %.112 = load %DArrayInt*, %DArrayInt** @numbers, align 8
  call void @print_int_array(%DArrayInt* %.112)
  %.114 = bitcast [8 x i8]* @.str17 to i8*
  call void @output_string(i8* %.114)
  %.116 = load %DArrayChar*, %DArrayChar** @grades, align 8
  call void @print_char_array(%DArrayChar* %.116)
  %.118 = bitcast [8 x i8]* @.str18 to i8*
  call void @output_string(i8* %.118)
  %.120 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  call void @print_float_array(%DArrayFloat* %.120)
  %.122 = load double, double* @popped, align 8
  call void @output_float(double %.122, i32 1)
  %.124 = load %DArrayFloat*, %DArrayFloat** @scores, align 8
  call void @print_float_array(%DArrayFloat* %.124)
  ret i32 0
}
