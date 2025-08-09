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

declare void @"output_float"(double %".1")

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
  %"arr" = alloca %"DArrayInt"*
  %"count" = alloca i32
  %".2" = bitcast [39 x i8]* @"str_literal.-8030652404147510688" to i8*
  call void @"output_string"(i8* %".2")
  call void @"input_int"(i32* %"count")
  %"num" = alloca i32
  %"sum" = alloca i32
  store i32 0, i32* %"sum"
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"L0"
L0:
  %".8" = load i32, i32* %"i"
  %".9" = load i32, i32* %"count"
  %"t0" = icmp slt i32 %".8", %".9"
  br i1 %"t0", label %"if_true", label %"L1"
if_true:
  %".11" = bitcast [15 x i8]* @"str_literal.5811775124267156209" to i8*
  call void @"output_string"(i8* %".11")
  call void @"input_int"(i32* %"num")
  %".14" = load i32, i32* %"sum"
  %".15" = load i32, i32* %"num"
  %"t1" = add i32 %".14", %".15"
  store i32 %"t1", i32* %"sum"
  %".17" = load i32, i32* %"i"
  %"t2" = add i32 %".17", 1
  store i32 %"t2", i32* %"i"
  br label %"L0"
L1:
  %"average" = alloca double
  %".20" = load i32, i32* %"sum"
  %".21" = load i32, i32* %"count"
  %".22" = sitofp i32 %".20" to double
  %".23" = sitofp i32 %".21" to double
  %"t3" = fdiv double %".22", %".23"
  store double %"t3", double* %"average"
  %".25" = bitcast [11 x i8]* @"str_literal.3644668908010861392" to i8*
  call void @"output_string"(i8* %".25")
  %".27" = load i32, i32* %"sum"
  call void @"output_int"(i32 %".27")
  %".29" = bitcast [15 x i8]* @"str_literal.-3787800507713842230" to i8*
  call void @"output_string"(i8* %".29")
  %".31" = load double, double* %"average"
  call void @"output_float"(double %".31")
  ret i32 0
}

@"str_literal.-8030652404147510688" = internal constant [39 x i8] c"How many numbers do you want to enter?\00"
@"str_literal.5811775124267156209" = internal constant [15 x i8] c"Enter a number\00"
@"str_literal.3644668908010861392" = internal constant [11 x i8] c"The sum is\00"
@"str_literal.-3787800507713842230" = internal constant [15 x i8] c"The average is\00"