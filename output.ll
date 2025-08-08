; ModuleID = "main_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

%"DArrayInt" = type {i32*, i64, i64}
%"DArrayString" = type {i8**, i64, i64}
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

declare %"DArrayString"* @"file_read_lines"(i64 %".1")

declare i32 @"tcp_socket"()

declare i32 @"tcp_connect"(i32 %".1", i8* %".2", i32 %".3")

declare i32 @"tcp_send"(i32 %".1", i8* %".2")

declare i32 @"tcp_recv"(i32 %".1", i8* %".2", i32 %".3")

declare void @"tcp_close"(i32 %".1")

declare %"DArrayInt"* @"d_array_int_create"()

declare void @"d_array_int_append"(%"DArrayInt"* %".1", i32 %".2")

declare i32 @"d_array_int_get"(%"DArrayInt"* %".1", i32 %".2")

declare void @"d_array_int_set"(%"DArrayInt"* %".1", i32 %".2", i32 %".3")

declare i32 @"d_array_int_size"(%"DArrayInt"* %".1")

declare void @"d_array_int_free"(%"DArrayInt"* %".1")

declare %"DArrayString"* @"d_array_string_create"()

declare void @"d_array_string_append"(%"DArrayString"* %".1", i8* %".2")

declare i8* @"d_array_string_get"(%"DArrayString"* %".1", i32 %".2")

declare void @"d_array_string_set"(%"DArrayString"* %".1", i32 %".2", i8* %".3")

declare i32 @"d_array_string_size"(%"DArrayString"* %".1")

declare void @"d_array_string_free"(%"DArrayString"* %".1")

define i32 @"main"()
{
entry:
  %"f" = alloca i64
  %".2" = bitcast [9 x i8]* @"str_literal.-659537568429198537" to i8*
  %".3" = bitcast [2 x i8]* @"str_literal.-7801684977136661346" to i8*
  %"t0" = call i64 @"file_open"(i8* %".2", i8* %".3")
  store i64 %"t0", i64* %"f"
  %".5" = load i64, i64* %"f"
  %".6" = bitcast [8 x i8]* @"str_literal.-7776754242896332199" to i8*
  call void @"file_write"(i64 %".5", i8* %".6")
  %".7" = load i64, i64* %"f"
  %".8" = bitcast [8 x i8]* @"str_literal.-6731738979385074476" to i8*
  call void @"file_write"(i64 %".7", i8* %".8")
  %".9" = load i64, i64* %"f"
  call void @"file_close"(i64 %".9")
  %".10" = bitcast [9 x i8]* @"str_literal.-659537568429198537" to i8*
  %".11" = bitcast [2 x i8]* @"str_literal.-5261059135734759601" to i8*
  %"t4" = call i64 @"file_open"(i8* %".10", i8* %".11")
  store i64 %"t4", i64* %"f"
  %"lines" = alloca %"DArrayString"*
  %".13" = load i64, i64* %"f"
  %"t5" = call %"DArrayString"* @"file_read_lines"(i64 %".13")
  store %"DArrayString"* %"t5", %"DArrayString"** %"lines"
  %"size" = alloca i32
  %".15" = load %"DArrayString"*, %"DArrayString"** %"lines"
  %"t6" = call i32 @"d_array_string_size"(%"DArrayString"* %".15")
  store i32 %"t6", i32* %"size"
  %".17" = load i32, i32* %"size"
  call void @"output_int"(i32 %".17")
  %"s" = alloca i8*
  %".19" = load %"DArrayString"*, %"DArrayString"** %"lines"
  %"t7" = call i8* @"d_array_string_get"(%"DArrayString"* %".19", i32 0)
  store i8* %"t7", i8** %"s"
  %".21" = load i8*, i8** %"s"
  call void @"output_string"(i8* %".21")
  %".23" = load %"DArrayString"*, %"DArrayString"** %"lines"
  %"t8" = call i8* @"d_array_string_get"(%"DArrayString"* %".23", i32 1)
  store i8* %"t8", i8** %"s"
  %".25" = load i8*, i8** %"s"
  call void @"output_string"(i8* %".25")
  %".27" = load %"DArrayString"*, %"DArrayString"** %"lines"
  call void @"d_array_string_free"(%"DArrayString"* %".27")
  %".28" = load i64, i64* %"f"
  call void @"file_close"(i64 %".28")
  ret i32 0
}

@"str_literal.-659537568429198537" = internal constant [9 x i8] c"test.txt\00"
@"str_literal.-7801684977136661346" = internal constant [2 x i8] c"w\00"
@"str_literal.-7776754242896332199" = internal constant [8 x i8] c"line 1\0a\00"
@"str_literal.-6731738979385074476" = internal constant [8 x i8] c"line 2\0a\00"
@"str_literal.-5261059135734759601" = internal constant [2 x i8] c"r\00"