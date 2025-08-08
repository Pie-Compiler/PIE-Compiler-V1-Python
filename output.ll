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
  %"filename" = alloca i8*
  %".2" = bitcast [15 x i8]* @"str_literal.-1959383206911544472" to i8*
  store i8* %".2", i8** %"filename"
  %"entriesFile" = alloca i64
  %".4" = load i8*, i8** %"filename"
  %".5" = bitcast [2 x i8]* @"str_literal.-1277787442202164103" to i8*
  %"t0" = call i64 @"file_open"(i8* %".4", i8* %".5")
  store i64 %"t0", i64* %"entriesFile"
  %"prompt" = alloca i8*
  %".7" = bitcast [16 x i8]* @"str_literal.3324229588093334085" to i8*
  store i8* %".7", i8** %"prompt"
  %"prompt2" = alloca i8*
  %".9" = bitcast [23 x i8]* @"str_literal.6550093605949987392" to i8*
  store i8* %".9", i8** %"prompt2"
  %"state" = alloca i32
  store i32 0, i32* %"state"
  %"readingFile" = alloca i64
  %".12" = load i8*, i8** %"filename"
  %".13" = bitcast [2 x i8]* @"str_literal.6225869764800647149" to i8*
  %"t1" = call i64 @"file_open"(i8* %".12", i8* %".13")
  store i64 %"t1", i64* %"readingFile"
  br label %"L0"
L0:
  %".16" = load i32, i32* %"state"
  %"t2" = icmp eq i32 %".16", 0
  br i1 %"t2", label %"if_true", label %"L1"
if_true:
  %".18" = load i8*, i8** %"prompt"
  call void @"output_string"(i8* %".18")
  %"userInput" = alloca i8*
  %".20" = alloca [256 x i8]
  %".21" = getelementptr [256 x i8], [256 x i8]* %".20", i32 0, i32 0
  store i8* %".21", i8** %"userInput"
  call void @"input_string"(i8* %".21")
  %".24" = load i8*, i8** %"userInput"
  call void @"output_string"(i8* %".24")
  %".26" = load i8*, i8** %"userInput"
  %".27" = bitcast [2 x i8]* @"str_literal.-4646666681103889553" to i8*
  %"t3" = call i8* @"concat_strings"(i8* %".26", i8* %".27")
  %".28" = load i64, i64* %"entriesFile"
  call void @"file_write"(i64 %".28", i8* %"t3")
  %"fileContents" = alloca i8*
  %".29" = load i64, i64* %"readingFile"
  %"t5" = call i8* @"file_read_all"(i64 %".29")
  store i8* %"t5", i8** %"fileContents"
  %".31" = load i8*, i8** %"fileContents"
  call void @"output_string"(i8* %".31")
  %".33" = load i8*, i8** %"prompt2"
  call void @"output_string"(i8* %".33")
  %"userChoice" = alloca i32
  call void @"input_int"(i32* %"userChoice")
  %"stop" = alloca i32
  store i32 0, i32* %"stop"
  %".37" = load i32, i32* %"userChoice"
  %".38" = load i32, i32* %"stop"
  %"t6" = icmp eq i32 %".37", %".38"
  br i1 %"t6", label %"if_true.1", label %"L3"
L1:
  %".44" = load i64, i64* %"entriesFile"
  call void @"file_close"(i64 %".44")
  %".45" = bitcast [17 x i8]* @"str_literal.-8377212011927257488" to i8*
  call void @"output_string"(i8* %".45")
  ret i32 0
if_true.1:
  %".40" = load i32, i32* %"state"
  %"t7" = add i32 %".40", 1
  store i32 %"t7", i32* %"state"
  br label %"L3"
L3:
  br label %"L0"
}

@"str_literal.-1959383206911544472" = internal constant [15 x i8] c"my_entries.txt\00"
@"str_literal.-1277787442202164103" = internal constant [2 x i8] c"a\00"
@"str_literal.3324229588093334085" = internal constant [16 x i8] c"Enter something\00"
@"str_literal.6550093605949987392" = internal constant [23 x i8] c"Continue ? (y->1/n->0)\00"
@"str_literal.6225869764800647149" = internal constant [2 x i8] c"r\00"
@"str_literal.-4646666681103889553" = internal constant [2 x i8] c"\0a\00"
@"str_literal.-8377212011927257488" = internal constant [17 x i8] c"Program complete\00"