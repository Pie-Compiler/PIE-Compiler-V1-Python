; ModuleID = "main_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"input_int"()

declare double @"input_float"()

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

declare i32 @"tcp_socket"()

declare i32 @"tcp_connect"(i32 %".1", i8* %".2", i32 %".3")

declare i32 @"tcp_send"(i32 %".1", i8* %".2")

declare i32 @"tcp_recv"(i32 %".1", i8* %".2", i32 %".3")

declare void @"tcp_close"(i32 %".1")

define i32 @"main"()
{
entry:
  %"sock" = alloca i32
  %"t0" = call i32 @"tcp_socket"()
  store i32 %"t0", i32* %"sock"
  %"result" = alloca i32
  %".3" = load i32, i32* %"sock"
  %".4" = bitcast [10 x i8]* @"str_literal.-1099183792774921535" to i8*
  %"t1" = call i32 @"tcp_connect"(i32 %".3", i8* %".4", i32 12345)
  store i32 %"t1", i32* %"result"
  %".6" = load i32, i32* %"result"
  call void @"output_int"(i32 %".6")
  %".8" = load i32, i32* %"result"
  %"t2" = icmp eq i32 %".8", 0
  br i1 %"t2", label %"if_true", label %"L0"
if_true:
  %".10" = load i32, i32* %"sock"
  %".11" = bitcast [21 x i8]* @"str_literal.-8430177797559898463" to i8*
  %"t3" = call i32 @"tcp_send"(i32 %".10", i8* %".11")
  %".12" = load i32, i32* %"sock"
  call void @"tcp_close"(i32 %".12")
  br label %"L1"
L0:
  %"error" = alloca i8*
  %".14" = bitcast [22 x i8]* @"str_literal.-1298646941824887973" to i8*
  store i8* %".14", i8** %"error"
  %".16" = load i8*, i8** %"error"
  call void @"output_string"(i8* %".16")
  br label %"L1"
L1:
  ret i32 0
}

@"str_literal.-1099183792774921535" = internal constant [10 x i8] c"127.0.0.1\00"
@"str_literal.-8430177797559898463" = internal constant [21 x i8] c"hello from pie net!\0a\00"
@"str_literal.-1298646941824887973" = internal constant [22 x i8] c"Error sending request\00"