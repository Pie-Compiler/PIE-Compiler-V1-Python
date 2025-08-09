; ModuleID = "main_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

%"DArrayInt" = type {i32*, i64, i64}
%"DArrayString" = type {i8**, i64, i64}
%"DictValue" = type {i32, i64}
%"Dictionary" = type {i8**, i32, i32}
declare void @"input_int"(i32* %".1")

declare void @"input_float"(double* %".1")

declare void @"input_string"(i8* %".1")

declare void @"input_char"(i8* %".1")

declare void @"output_int"(i32 %".1")

declare void @"output_string"(i8* %".1")

declare void @"output_char"(i8 %".1")

declare void @"output_float"(double %".1", i32 %".2")

declare double @"pie_sqrt"(double %".1")

declare double @"pie_pow"(double %".1", double %".2")

declare double @"pie_sin"(double %".1")

declare double @"pie_cos"(double %".1")

declare double @"pie_floor"(double %".1")

declare double @"pie_ceil"(double %".1")

declare i32 @"pie_rand"()

declare i8* @"concat_strings"(i8* %".1", i8* %".2")

declare i32 @"pie_strlen"(i8* %".1")

declare i32 @"pie_strcmp"(i8* %".1", i8* %".2")

declare i8* @"pie_strcpy"(i8* %".1", i8* %".2")

declare i8* @"pie_strcat"(i8* %".1", i8* %".2")

declare i64 @"file_open"(i8* %".1", i8* %".2")

declare void @"file_close"(i64 %".1")

declare void @"file_write"(i64 %".1", i8* %".2")

declare void @"file_flush"(i64 %".1")

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

declare %"Dictionary"* @"dict_create"()

declare void @"dict_set"(%"Dictionary"* %".1", i8* %".2", %"DictValue"* %".3")

declare %"DictValue"* @"dict_get"(%"Dictionary"* %".1", i8* %".2")

declare i32 @"dict_get_int"(%"Dictionary"* %".1", i8* %".2")

declare double @"dict_get_float"(%"Dictionary"* %".1", i8* %".2")

declare i8* @"dict_get_string"(%"Dictionary"* %".1", i8* %".2")

declare void @"dict_delete"(%"Dictionary"* %".1", i8* %".2")

declare void @"dict_free"(%"Dictionary"* %".1")

declare %"DictValue"* @"dict_value_create_int"(i32 %".1")

declare %"DictValue"* @"dict_value_create_float"(double %".1")

declare %"DictValue"* @"dict_value_create_string"(i8* %".1")

define i32 @"main"()
{
entry:
  %"f" = alloca double
  store double 0x40091eb851eb851f, double* %"f"
  %".3" = load double, double* %"f"
  %"t0" = call double @"pie_floor"(double %".3")
  call void @"output_float"(double %"t0", i32 2)
  %".5" = load double, double* %"f"
  %"t1" = call double @"pie_ceil"(double %".5")
  call void @"output_float"(double %"t1", i32 2)
  %"t2" = call i32 @"pie_rand"()
  call void @"output_int"(i32 %"t2")
  %"fhandle" = alloca i64
  %".8" = bitcast [15 x i8]* @"str_literal.5758048304646385660" to i8*
  %".9" = bitcast [2 x i8]* @"str_literal.4737790829888832400" to i8*
  %"t3" = call i64 @"file_open"(i8* %".8", i8* %".9")
  store i64 %"t3", i64* %"fhandle"
  %".11" = load i64, i64* %"fhandle"
  %".12" = bitcast [6 x i8]* @"str_literal.5050700449521556306" to i8*
  call void @"file_write"(i64 %".11", i8* %".12")
  %".13" = load i64, i64* %"fhandle"
  call void @"file_flush"(i64 %".13")
  %"arr" = alloca %"DArrayInt"*
  %"t6" = call %"DArrayInt"* @"d_array_int_create"()
  store %"DArrayInt"* %"t6", %"DArrayInt"** %"arr"
  %".15" = load %"DArrayInt"*, %"DArrayInt"** %"arr"
  call void @"d_array_int_append"(%"DArrayInt"* %".15", i32 1)
  %".16" = load %"DArrayInt"*, %"DArrayInt"** %"arr"
  call void @"d_array_int_append"(%"DArrayInt"* %".16", i32 2)
  %".17" = load %"DArrayInt"*, %"DArrayInt"** %"arr"
  call void @"d_array_int_append"(%"DArrayInt"* %".17", i32 3)
  %"d" = alloca %"Dictionary"*
  %"t10" = call %"Dictionary"* @"dict_create"()
  store %"Dictionary"* %"t10", %"Dictionary"** %"d"
  %".19" = bitcast [6 x i8]* @"str_literal.8807644223339669450" to i8*
  %"t11" = call %"DictValue"* @"dict_value_create_string"(i8* %".19")
  %".20" = load %"Dictionary"*, %"Dictionary"** %"d"
  %".21" = bitcast [5 x i8]* @"str_literal.-5816524308287420896" to i8*
  call void @"dict_set"(%"Dictionary"* %".20", i8* %".21", %"DictValue"* %"t11")
  %"t13" = call %"DictValue"* @"dict_value_create_int"(i32 30)
  %".22" = load %"Dictionary"*, %"Dictionary"** %"d"
  %".23" = bitcast [4 x i8]* @"str_literal.3013550875645087931" to i8*
  call void @"dict_set"(%"Dictionary"* %".22", i8* %".23", %"DictValue"* %"t13")
  %"name" = alloca i8*
  %".24" = load %"Dictionary"*, %"Dictionary"** %"d"
  %".25" = bitcast [5 x i8]* @"str_literal.-5816524308287420896" to i8*
  %"t15" = call i8* @"dict_get_string"(%"Dictionary"* %".24", i8* %".25")
  store i8* %"t15", i8** %"name"
  %"age" = alloca i32
  %".27" = load %"Dictionary"*, %"Dictionary"** %"d"
  %".28" = bitcast [4 x i8]* @"str_literal.3013550875645087931" to i8*
  %"t16" = call i32 @"dict_get_int"(%"Dictionary"* %".27", i8* %".28")
  store i32 %"t16", i32* %"age"
  %".30" = load i8*, i8** %"name"
  call void @"output_string"(i8* %".30")
  %".32" = load i32, i32* %"age"
  call void @"output_int"(i32 %".32")
  %"s1" = alloca i8*
  %".34" = bitcast [6 x i8]* @"str_literal.5050700449521556306" to i8*
  store i8* %".34", i8** %"s1"
  %"s2" = alloca i8*
  %".36" = bitcast [6 x i8]* @"str_literal.4421839943897807581" to i8*
  store i8* %".36", i8** %"s2"
  %".38" = load i8*, i8** %"s1"
  %"t17" = call i32 @"pie_strlen"(i8* %".38")
  call void @"output_int"(i32 %"t17")
  %".40" = load i8*, i8** %"s1"
  %".41" = load i8*, i8** %"s2"
  %"t18" = call i32 @"pie_strcmp"(i8* %".40", i8* %".41")
  call void @"output_int"(i32 %"t18")
  ret i32 0
}

@"str_literal.5758048304646385660" = internal constant [15 x i8] c"test_flush.txt\00"
@"str_literal.4737790829888832400" = internal constant [2 x i8] c"w\00"
@"str_literal.5050700449521556306" = internal constant [6 x i8] c"hello\00"
@"str_literal.8807644223339669450" = internal constant [6 x i8] c"Jules\00"
@"str_literal.-5816524308287420896" = internal constant [5 x i8] c"name\00"
@"str_literal.3013550875645087931" = internal constant [4 x i8] c"age\00"
@"str_literal.4421839943897807581" = internal constant [6 x i8] c"world\00"