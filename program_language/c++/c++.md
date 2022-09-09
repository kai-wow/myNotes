# pointer & reference 指针和引用

```c++
int a[3][4] = { 0,1,2,3,4,5,6,7,8,9,10,11 };
int(*p)[4];
p = a;
// (*p)[4] = a[0] , (*p) 挨个存储 a 的每个元素的地址 
std::cout << (*p)[0] << ' ' << (*p)[1] << ' ' << (*p)[2] << ' ' << (*p)[3] << ' '<< std::endl; 
// p 存储 a 每行的首个元素的地址
std::cout << *p[0] << ' ' << *p[1] << ' ' << *p[2] << ' ' << std::endl; // 0, 4, 8
```

```c++
int arr[][3] = { 1, 2, 3, 4, 5, 6 }; 

int(*ptr)[3] = arr; // which means (*ptr)[3] = arr[0]
cout << (*ptr)[0] << " , " << (*ptr)[1] << " , " << (*ptr)[2] << endl; // 1, 2, 3
ptr++;  
cout << (*ptr)[0] << " , " << (*ptr)[1] << " , " << (*ptr)[2] << endl; // 4, 5, 6
return 0;
```

```c++
int a[5] = { 1, 2, 3, 4, 5 };
int* p1 = (int*)(&a + 1);		// refer to the address of an array after the array a
int* p2 = (int*)((int)a + 1);	// change the address of “a[0]” to an integer and add 1: undefined
int* p3 = (int*)(a + 1);		// p3 refers to a[1]

cout << p1[-1] << ' ' << p2[0] << ' ' << p3[1] << endl; // 5 33554432 3
return 0;
```



# 一些英文单词
英文      | 对应符号
---       |:---:
semicolon | ;
backslash | \
underscore| _
comma     | ,
modulus   | % 取余

# 介绍
- assembly language 汇编语言
  - 例如 vim、git，简单的英文缩写作为指令
- high-level language 高级汇编语言？，更便于阅读
  - 例如 c++、python，可以有数学公式之类的
  - 比汇编语言 更简洁，就能实现连续的工作

# c++
## 简要介绍
### 发展历史
- c 的改进版，比c 的优点是：**面向对象编程**（可重复使用，便于理解和维护）
### c++ 系统
- 程序开发环境
- 语言
- c++ standard library
  - 软件重复使用

### c++ 程序的拓展名：
1. C++程序
   - .cpp
   - .cxx
   - .cc
   - .C

2. 头文件
   - .h
   - .hpp
   - no extension
### c++程序的运行阶段
1. edit 编写程序：编写并存在disk里
2. preprocess 预处理
3. **compile 编译**：编译器将代码转为**object code**，并存在disk
4. **link 链接**：将编译过程产生的**object code**组合到一起，生成**可执行文件**，并储存在disk
（3和4同时进行，即一边编译，一边链接）
5. load 加载：put programs in memory，把程序加载到内存里
6. execute 运行：CPU 运行

### 常见 input/output function
- cin : connected to keyboard
- cout: connected to screen
- cerr

## 语法
### 语法
#### 注释
- 单行：//
- 多行：/* ... */
- preprocessor directives 预处理指令
  - 以 # 开头的，如：#include <>
  - processed by preprocessor before compile

### namespace
- 避免不同模块下相同名字冲突的一种关键字
- 两种方式
  - std:: 
  - using namespace std

### escape characters \
- 特殊字符输出时需要

escape sequence | 描述
---             | :---
\n              | 换行
\t              | tab, 8 spaces
\r              | 回到本行的行首
\\(两个)        | to print a backslash \
\"              | print a double qoute "
\a              | 响铃，系统自带的扬声器（或蜂鸣器）会发出“叮”的一声

## linkage
### 变量的 linkage
### 函数的 linkage
- 函数默认是 external linkage

## 变量
- 变量定义：a name for 存储信息的内存
- 每个变量都必须要声明
- 一旦变量声明了，就会有内存（address）
### 分类
- l-value 等式left左边的变量，都有memory
  - **所有变量都是l-value**（数字不是）
- r-value 等式right右边的值，是赋值给变量的值，可以是
  - 数字
  - 变量
  - 表达式（加减乘除等）
### 变量的几个属性
- name/ identifier
- type
- value: initial and current
- size
- address 内存地址

- **scope**, 活动的范围
  - local scope/block scope: local variable, function parameter
  - global scope/file scope: global variable
- **duration**, 活动的时间
  - automatic duration: normal local variable
  - static duration   : global variable, static duration local variable
  - dynamic duration  : 
- linkage

- alias : reference

#### local/global variable
- local variable: 在{}里定义的，只要遇上了 } 就会被 destory
  - automatic duration
  - static duration local variable: 在{}里面 `static int g_x;`, 静态变量的声明只会被执行一次（只能定义和初始化一次）
- global variable: 在所有函数前面，include 后面的变量。 ::为global scope operator
  - internal variable ：常量的**全局变量**, **static的全局变量、函数** 默认为 internal
    - `static int g_x; // g_x 只能在本文件里使用`
  - external variable ：非常量的**全局变量**默认为 external
    - `extern int g_x; // g_x 本文件和其他文件都能用`
    - 在其他文件调用时，需要 forward declaration:  `extern int g_x; `
变量              | scope                     | duration            | linkage
---               |:---                      |:---                  |:---
local variable    |local scope/block scope   | automatic duration   |
global variable   |global scope/file scope   | static duration 静态 |
internal variable |                          |                      | internal linkage, 只能在本文件里使用
external variable |                          |                      | external linkage, 本文件和其他文件都能用


### 初始化和赋值
- c++ 不会给未初始化变量 自动赋值

### keywords 和 命名 identifiers
#### 关键词
- c++ 有73 words for its own use, which are called keywords
- keywords 不能用作变量名
#### identifiers
- 变量、函数、class、以及其他对象的名字 叫做 identifiers
- 命名规范：
  - 不能是 keyword
  - 只能包含 字母、数字、下划线underscore character
  - 字母或下划线开头
  - 大小写有区别
  
  - 变量命名
    - 小写字母开头

  - 函数命名
    - **通常** 小写字母开头

  - structure, class 命名
    - 大写字母开头

### 基础数据类型

类别            | 类型  | 含义
---             |:---:  |:---
boolean         |bool   | True、false
**character**   |char   | **a single ASCII charactor**
floating point  |float, double, long double| 带小数的数字
integer         |short, int, long, long long|
void            |no type| void 无数值 n/a

#### integer
- 只能存储整数
##### 五种 integer types
- 五种 integer types:(主要区别在于 size 不同)
  - **character:char**
  - integer:    short, int, long, long long
  ***char 是特殊情况，他既可以是 character类型，也可能是 integer 类型***
- 整型的定义：
  `char n;`
  `short n;`
  `short int n;//也可以这样定义`
  - n bits 的变量可以存储 $2^n$ 个不同的值（再看看）

##### range 和 integer的符号
- range: 数据类型可以存储的所有值的集合
  - 两个决定因素：
    - 1. size 
    - 2. sign 符号：signed integer 可以同时储存正值和负值
      - **signed integer** 
        `signed int i; `
        - 1 byte signed integer 取值范围 range：-128~127 
          - 1 byte = 8 bits, 其中符号占 1 bit，数字7个，$2^7=128$)
          - 10000000 = -128；01111111 = 127
      - **unsigned integer** :只存储正值
        `unsigned int i;`
        - 1 byte unsigned integer 取值范围 range：0~255 ($2^8=256$)
          - 00000000 = 0；11111111 = 255

  integer 类型      | 取值范围 range
  ---               | :---
  n-bit signed      |$-2^{n-1}$ ~ $2^{n-1}-1$
  n-bit unsigned    |$0$ ~ $2^{n}-1$

- 如未声明，默认为 signed integer

##### overflow 溢出 
  - overflow: occurs when bits are lost because a variable has **not been allocated enough memory to store** them
  - 若溢出，只会存储最右边的n个bits的数值，最左边的直接lost
##### 整除：两个整型相除，只会得到结果的整数部分

#### 浮点数
- 四种类型的浮点数： float, double, long double
- **默认为 double**，float类型要在最后面加上 f作为后缀
`double a(5.0);`
`float a(5.0f);`
- 默认精度为 6: 只能存储6个数字，包括小数点前/后的非零数字
  - 可以拓展精度，用 std::setprecision() 函数

##### rounding error
```c++
double d(0.1);
cout << setprecision(17);
cout << d; // 出现 0.10000000000000001
```
- 出现原因: 由于 double 的 limiting memory（有些数用二进制表达不出来）

- 比较两个数值的正确方式：
**$d1 - d2 < 1e-10$**

##### 特殊的浮点数:NaN & inf
- NaN: not a number
- inf: infinity

#### bool
- 赋值: true/false
`bool b1 = True;`
- 储存为整数 1/0
- 打印的结果为数值
##### 逻辑非 (!)
`bool b1 = !True;`

#### chars
- 一个 char 变量存有一个 **1-byte integer: 0-127**
- char 不会编译为整数，而是通过 ASCII 将改整数编译为一个 字符
- 初始化: 用整型，或字符都可以
```c++
char ch1(97);
char ch1('a');
char ch2(5);
char ch2('5');//char ch2(53)
```
##### ASCII: 表示英文字母，简单的符号
- 0-127 的数字中
  - 0-31  : unprintable, 如 tab 等
  - 32-127: printable,
    - 先是**符号**，再**数字0-9**，再**符号**，再**大写字母**，再**符号**，再**小写字母**，再**符号**

##### 通过 type casting 将char打印成int
- 用 static_cast() 函数，会把转化好的值存在temp中而不改变原ch变量的值
```c++
char ch1(97);
cout << static_cast<int>(ch); // 将 char 转化为 int
```
- static_cast 的时候可能会 overflow
##### cin 输入 chars
- 只有最先输入（最左边）的 存储在 char，其余的在缓冲区input buffer of cin, 后续可以迭代读取

##### 单引号和双引号
- chars 总是用**单引号**
- 一个char 只能代表一个 symbol
- **双引号**储存 string 字符串，字符串是一系列char的组合

#### literal constants 
- 可以用后缀 定义其类型
- **八进制和十六进制** 的常量
  - octal 八进制： 前缀为 0
  - hexadecimal 十六进制： 前缀为 0x
  ```c++
  int x = 012; // 10
  int x = 0xF; // 15
  ```

#### const 常量
- const keyword (更推荐)
```c++
const double g = 9.8; // prefered
int const x = 4; 
```
- **Macros 宏指令**——另一种定义常量的形式
  - 语法: #define 命名 值
  ```c++
  #define MAX_STUDENT_PER_CLASS 30
  int max_students = num_class * MAX_STUDENT_PER_CLASS; // 15
  ```

#### void
- 变量不能被定义为 void 类型
- void 的用法：
  1. 函数的返回类型
  2. pointers 指针

### 变量初始化的两种方法
- 单个变量初始化
  1. copy initialization 更常用
  `int n = 5;`
  2. direct initialization
  `int n(5);`
- 多个变量初始化
  `int a = 5, b = 6;`
  `int c(7), d(8);`
  **错误方式**：(再看看)
  `int a = 5, int b = 6;`
  `int a, int b;`
  `int a, b = 6;`




### 变量的 size
bit < byte < KB < MB < GB < TB (再看看)
- 8 bit = 1 byte
- 1024 byte = 1 KB
- 1024 KB = 1 MB
- 1024 MB = 1 GB
- 1024 GB = 1 TB

### variable size
- **sizeof** operator, 输入type或者变量，返回size（in bytes）


## string
### 1. c-style string
`char mystring[] = "string";`
- \0 空值结尾
- 一些函数
  - cin.getline()
    - 除了 普通的cin外，还可以用函数 cin.getline() , 可以读取254个字符
    - `std::cin.getline(name, 255); // 255为限制的长度`
  - strcpy()
    - `strcpy(new, old);`
  - strncpy()
    - `strcpy(new, old, length);`
  - strlen(): 字符串的长度，即有多少字符（不含null）
### 2. std::string
`std::string mystring{"Alex"};`
- 一些函数
  - std::getinline()
    - 除了 普通的cin外，还可以用函数 cin.getline() , 可以读取254个字符
    - `std::getinline(std::cin, name)`
  - 拓展字符串: +
  - .length() : 返回字符串长度（不含null）

## 指针 pointer
`int *ptr = &value;`

## 动态数组

## reference
`int &ref = value`
- reference 可看作是常量，只能定义和初始化一次，无法重新赋值