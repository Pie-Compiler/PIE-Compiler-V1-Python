; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

declare void @input_int(i32*)

declare void @input_float(double*)

declare void @input_string(i8*)

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

define i32 @add(i32 %a, i32 %b) {
entry:
  %a.1 = alloca i32, align 4
  store i32 %a, i32* %a.1, align 4
  %b.1 = alloca i32, align 4
  store i32 %b, i32* %b.1, align 4
  %.6 = load i32, i32* %a.1, align 4
  %.7 = load i32, i32* %b.1, align 4
  %i_tmp = add i32 %.6, %.7
  ret i32 %i_tmp
}

define i32 @main() {
entry:
  %x = alloca i32, align 4
  %y = alloca i32, align 4
  store i32 10, i32* %x, align 4
  store i32 20, i32* %y, align 4
  %z = alloca i32, align 4
  %.4 = load i32, i32* %x, align 4
  %.5 = load i32, i32* %y, align 4
  %call_tmp = call i32 @add(i32 %.4, i32 %.5)
  store i32 %call_tmp, i32* %z, align 4
  %.7 = load i32, i32* %z, align 4
  call void @output_int(i32 %.7)
  ret i32 0
}
