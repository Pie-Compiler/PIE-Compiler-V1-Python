; ModuleID = "main_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"input_int"(i32* %".1")

declare void @"input_float"(double* %".1")

declare void @"input_string"(i8* %".1")

declare void @"input_char"(i8* %".1")

declare void @"output_int"(i32 %".1")

declare void @"output_float"(double %".1", i32 %".2")

declare void @"output_string"(i8* %".1")

declare void @"output_char"(i8 %".1")

declare void @"exit_program"()

declare double @"pie_sqrt"(double %".1")

declare double @"pie_pow"(double %".1", double %".2")

declare double @"pie_sin"(double %".1")

declare double @"pie_cos"(double %".1")

declare i8* @"concat_strings"(i8* %".1", i8* %".2")

declare i64 @"file_open"(i8* %".1", i8* %".2")

declare void @"file_close"(i64 %".1")

declare void @"file_write"(i64 %".1", i8* %".2")

declare void @"file_read"(i64 %".1", i8* %".2", i32 %".3")

declare i8* @"file_read_all"(i64 %".1")

declare i32 @"tcp_socket"()

declare i32 @"tcp_connect"(i32 %".1", i8* %".2", i32 %".3")

declare i32 @"tcp_send"(i32 %".1", i8* %".2")

declare i32 @"tcp_recv"(i32 %".1", i8* %".2", i32 %".3")

declare void @"tcp_close"(i32 %".1")

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 2, i32* %"x"
  %".3" = load i32, i32* %"x"
  switch i32 %".3", label %"L3" [i32 1, label %"L1" i32 2, label %"L2"]
L3:
  call void @"output_int"(i32 3)
  br label %"L0"
L1:
  call void @"output_int"(i32 1)
  br label %"L0"
L2:
  call void @"output_int"(i32 2)
  br label %"L0"
L0:
  ret i32 0
}
