; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@.str0 = internal constant [16 x i8] c"Hello from PIE!\00"
@.str1 = internal constant [13 x i8] c"The sum is: \00"

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
  %message = alloca i8*, align 8
  %.2 = bitcast [16 x i8]* @.str0 to i8*
  store i8* %.2, i8** %message, align 8
  %.4 = load i8*, i8** %message, align 8
  call void @output_string(i8* %.4)
  %x = alloca i32, align 4
  store i32 10, i32* %x, align 4
  %y = alloca i32, align 4
  store i32 20, i32* %y, align 4
  %result = alloca i32, align 4
  %.8 = load i32, i32* %x, align 4
  %.9 = load i32, i32* %y, align 4
  %i_tmp = add i32 %.8, %.9
  store i32 %i_tmp, i32* %result, align 4
  %.11 = bitcast [13 x i8]* @.str1 to i8*
  call void @output_string(i8* %.11)
  %.13 = load i32, i32* %result, align 4
  call void @output_int(i32 %.13)
  ret i32 0
}
