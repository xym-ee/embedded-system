
# C 预处理器和 C 库

- #define #include #ifdef #else #endif #ifndef #if #elif #line #error #pragma
- _Generic _Noreturn _Static_assert
- sqrt() atan() atan2() exit() atexit() assert() memcpy() memmove() va_start() va_arg() va_copy() va_end()
- C 预处理器的更多功能
- 通用选择表达式
- 内联函数
- C 库概述，一些函数

C 标准不仅描述 C 语言关键字、表达式、语句以及使用它们的规则，还描述输入执行 C 预处理器、C 标准库中的函数，以及这些函数的工作原理。

这部分看 C 预处理和 C 库。

在生成可执行文件的过程中，C 预处理器是第一个介入的程序，预处理器的工作是把一类文件替换为另一类文本。


## 预处理前的准备

- 1.扩展字符映射，如 %:include <stdio.h> 总的 %: 映射为 #
- 2.`\\n` 处理为一行，即删除 `\` 和 `\n`，删除源码中的 enter，而且字符 `\n`
  - `printf("hello \`
  - `world")`
- 3.把文本划分为预处理记号序列、空白序列、注释序列

然后就可以进行预处理了，下面来看一些预处理指令

## `#deifne`

### 基本用法

#define 可以出现在文件任何地方，其定义从指令出现的地方到文件末尾都有效。

最简单的用法，定义一个符号常量(明示常量)

```c
#define PI 3.1416f
#define HELLO  "hello world"
```


从技术角度来看，宏的替换可以看作是记号型字符串。

### 带参数的

在 #define 中是可以使用参数的，类函数宏。一个例子

```c
#define SQUARE(x)   x*x

z = SQUARE(2);
```

看起来和函数很像，但是其行为和函数不同。

写一个宏函数，一些陷阱和要注意的点。

### `#` 宏参数创建字符串

可以使用带参宏创建字符串

```c
#define PRINT_SQUARE(X) printf("X = %d \n", X*X)
PRINT_SQUARE(8);
```
输出为 X = 64，即双引号内的没有被替换。如果想要字符串中也被参数替换，可以使用 `#`，直接把记号转换成字符串。如 x 是一个宏形参，那么 #x 就转换为字符串 "x" 了。

```c
#define PRINT_SQUARE(X) printf(#X "*" #X " = %d \n", X*X)
PRINT_SQUARE(8);
```
这时候输出就是 8*8 = 64 了。

### `##` 预处理粘合

把两个记号组合成一个记号

```c
#define XNAME(n) x ## n

#define PRINT_XN(n) printf("x" #n " = %d\n", n);

int main()
{
    int XNAME(1) = 1;
    int XNAME(2) = 2;

    PRINT_XN(1);
    PRINT_XN(2);
}
```

### 变参宏 ... 和 __VA_ARGS__

一些函数如 printf 可以接收数量可变的参数。C99 对宏也提供了这样的工具。

把宏参数的最后一个参数写为 ... 然后在预定义宏中使用 __VA_ARGS__


```c
#define my_print(fmt, ...) printf(fmt, __VA_ARGS__)

int main() {
    my_print("Hello, %s! You are %d years old.\n", "John", 30);
    return 0;
}
```

__VA_ARGS__ 这个东西并不定义在头文件中，__VA_ARGS__ 是 C/C++ 编译器**预处理器**的内置特性，而不是像普通的宏那样由特定文件定义的。因此，代码编辑器（包括 VS Code）不会像对待普通函数或变量那样为它提供自动提示功能。

### 关于宏和函数

宏会比函数复杂一些，有时甚至会有副作用。宏的优点，不用考虑变量类型。C99 也提供了替换方法：内联函数。

在实际工程中，对于简单的函数，通常会使用宏，比如

```c
#define MAX(X, Y)   ((X)>(Y) ? (X) : (Y))
#define ABS(X)      ((X)<0? -(X) : (X))
```

## `#include` 

预处理器发现 #include 以后，会查看后面的文件名，然后把文件内容直接替换 #include 这行。两种形式
```c
#include <stdio.h>  
#include "main.h"
```

<> 为先查找系统目录，""为先查找当前目录。

C 语言习惯使用 .h 来表示头文件。但是实际上任意文件都可以被 include 进去。

通常头文件会放的东西
- 明示常量 如 stdio.h 中的 EOF NULL
- 宏函数 如 getchar() 的实现通常用 getc(stdin)
- 函数声明 
- 结构模板
- 类型定义 typedef 

有些时候也会在头文件声明一个外部变量用来在不同文件之间共享。如 `int status = 0;` 只有文件作用域，在此源文件相关的头文件中可以声明 `extern int status;` ，然后其他文件中就可以包含该头文件来使用此变量了。

## `#undef`

取消已定义的 `define` 指令。

已定义的宏可以是对象宏，包括空宏、函数宏。比如
```c
#define LIMIT 100
#define GOOD
#define A(X)   (X)*(X)
```

宏的作用域从声明处开始，到文件尾结束或者 #undef 结束。如果宏通过 #include 引入，那么取决于 #include 的位置。

有一些预定义宏如 __DATE__ __FILE__ ，这些是一定定义的而且不能被取消。

## 条件编译

### `#if` `#else` `#endif` 指令

### `#ifndef` 指令

### `#if` `#elif` 指令


## 预定义宏

### `#line` 和 `#error`


### `#pragma`


## 内联函数

函数调用会有一些开销。使用宏可以避免开销，C99 提供了另一种方法：**内联函数 inline function**。


## C 库

最初并没有官方的 C 库，后来 C 语言应用范围变大，在 C 标准中也有了关于 C 库的内容。


### 数学库 math.h


### 通用工具


### 断言


### string 库

memcpy 和 memmove 

### 可变参数 stdargs.h

















