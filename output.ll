; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@n = internal global i32 0
@total = internal global double 0.000000e+00
@i = internal global i32 0
@avg = internal global double 0.000000e+00
@prompt = internal global i8* null
@grade = internal global i8 0
@valid = internal global i1 false
@d = internal global i32 5
@f = internal global i32 10
@.str0 = internal constant [33 x i8] c"Enter the number of test scores:\00"
@.str1 = internal constant [18 x i8] c"Enter test score:\00"
@.str2 = internal constant [15 x i8] c"Average Score:\00"
@.str3 = internal constant [7 x i8] c"Grade:\00"

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

define i32 @main() {
entry:
  %.2 = bitcast [33 x i8]* @.str0 to i8*
  store i8* %.2, i8** @prompt, align 8
  %.4 = load i8*, i8** @prompt, align 8
  call void @output_string(i8* %.4)
  call void @input_int(i32* @n)
  %.7 = sitofp i32 0 to double
  store double %.7, double* @total, align 8
  store i32 0, i32* @i, align 4
  br label %for_header

for_header:                                       ; preds = %for_update, %entry
  %.11 = load i32, i32* @i, align 4
  %.12 = load i32, i32* @n, align 4
  %i_cmp_tmp = icmp slt i32 %.11, %.12
  br i1 %i_cmp_tmp, label %for_body, label %for_exit

for_body:                                         ; preds = %for_header
  %score = alloca i32, align 4
  %.14 = bitcast [18 x i8]* @.str1 to i8*
  store i8* %.14, i8** @prompt, align 8
  %.16 = load i8*, i8** @prompt, align 8
  call void @output_string(i8* %.16)
  call void @input_int(i32* %score)
  %.19 = load double, double* @total, align 8
  %.20 = load i32, i32* %score, align 4
  %.21 = sitofp i32 %.20 to double
  %f_tmp = fadd double %.19, %.21
  store double %f_tmp, double* @total, align 8
  br label %for_update

for_update:                                       ; preds = %for_body
  %.24 = load i32, i32* @i, align 4
  %i_tmp = add i32 %.24, 1
  store i32 %i_tmp, i32* @i, align 4
  br label %for_header

for_exit:                                         ; preds = %for_header
  %.27 = load i32, i32* @n, align 4
  %i_cmp_tmp.1 = icmp eq i32 %.27, 0
  br i1 %i_cmp_tmp.1, label %then, label %else

then:                                             ; preds = %for_exit
  store i1 false, i1* @valid, align 1
  br label %if_cont

else:                                             ; preds = %for_exit
  store i1 true, i1* @valid, align 1
  br label %if_cont

if_cont:                                          ; preds = %else, %then
  %.33 = load i1, i1* @valid, align 1
  %i_cmp_tmp.2 = icmp eq i1 %.33, true
  br i1 %i_cmp_tmp.2, label %then.1, label %else.1

then.1:                                           ; preds = %if_cont
  %.35 = load double, double* @total, align 8
  %.36 = load i32, i32* @n, align 4
  %.37 = sitofp i32 %.36 to double
  %f_tmp.1 = fdiv double %.35, %.37
  store double %f_tmp.1, double* @avg, align 8
  br label %if_cont.1

else.1:                                           ; preds = %if_cont
  store double 0.000000e+00, double* @avg, align 8
  br label %if_cont.1

if_cont.1:                                        ; preds = %else.1, %then.1
  %.42 = load double, double* @avg, align 8
  %f_cmp_tmp = fcmp oge double %.42, 9.000000e+01
  br i1 %f_cmp_tmp, label %then.2, label %else.2

then.2:                                           ; preds = %if_cont.1
  store i8 65, i8* @grade, align 1
  br label %if_cont.2

else.2:                                           ; preds = %if_cont.1
  %.46 = load double, double* @avg, align 8
  %f_cmp_tmp.1 = fcmp oge double %.46, 8.000000e+01
  br i1 %f_cmp_tmp.1, label %then.3, label %else.3

if_cont.2:                                        ; preds = %if_cont.3, %then.2
  %.63 = bitcast [15 x i8]* @.str2 to i8*
  store i8* %.63, i8** @prompt, align 8
  %.65 = load i8*, i8** @prompt, align 8
  call void @output_string(i8* %.65)
  %.67 = load double, double* @avg, align 8
  call void @output_float(double %.67, i32 4)
  %.69 = bitcast [7 x i8]* @.str3 to i8*
  store i8* %.69, i8** @prompt, align 8
  %.71 = load i8*, i8** @prompt, align 8
  call void @output_string(i8* %.71)
  %.73 = load i8, i8* @grade, align 1
  call void @output_char(i8 %.73)
  %.75 = load i32, i32* @d, align 4
  %i_cmp_tmp.3 = icmp sgt i32 %.75, 3
  %.76 = load i32, i32* @f, align 4
  %i_cmp_tmp.4 = icmp sgt i32 %.76, 3
  %and_tmp = and i1 %i_cmp_tmp.3, %i_cmp_tmp.4
  br i1 %and_tmp, label %then.6, label %if_cont.6

then.3:                                           ; preds = %else.2
  store i8 66, i8* @grade, align 1
  br label %if_cont.3

else.3:                                           ; preds = %else.2
  %.50 = load double, double* @avg, align 8
  %f_cmp_tmp.2 = fcmp oge double %.50, 7.000000e+01
  br i1 %f_cmp_tmp.2, label %then.4, label %else.4

if_cont.3:                                        ; preds = %if_cont.4, %then.3
  br label %if_cont.2

then.4:                                           ; preds = %else.3
  store i8 67, i8* @grade, align 1
  br label %if_cont.4

else.4:                                           ; preds = %else.3
  %.54 = load double, double* @avg, align 8
  %f_cmp_tmp.3 = fcmp oge double %.54, 6.000000e+01
  br i1 %f_cmp_tmp.3, label %then.5, label %else.5

if_cont.4:                                        ; preds = %if_cont.5, %then.4
  br label %if_cont.3

then.5:                                           ; preds = %else.4
  store i8 68, i8* @grade, align 1
  br label %if_cont.5

else.5:                                           ; preds = %else.4
  store i8 70, i8* @grade, align 1
  br label %if_cont.5

if_cont.5:                                        ; preds = %else.5, %then.5
  br label %if_cont.4

then.6:                                           ; preds = %if_cont.2
  store i32 10, i32* @d, align 4
  br label %if_cont.6

if_cont.6:                                        ; preds = %then.6, %if_cont.2
  ret i32 0
}
