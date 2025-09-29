
# 结构和复杂数据形式

- struct union typedef
- 运算符 `.` `->`
- 结构体，结构模板和结构变量
- 结构体处理函数


程序设计的另一个要点，数据的表示方法，简单变量或是数组不够用，C 中提供了**结构变量**(structure varibale)，提供了一种创造新数据的方式。

## 基本操作

结构声明(structure declaration)描述了一个结构体的布局，类似
```c
struct book {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
};

struct book library;
```

结构声明并未创建对象，创建结构变量时才会真正分配内存空间。

`struct book library;` 是下面这个表达的简化
```c
struct book {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
} library;
```

所以 `book` 也不是必须的，可以这么创建结构变量
```c
struct {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
} library;
```

初始化
```c
/* 定义时初始化 */
struct book c_premier_plus = {
    "C Premier Plus(6th Edition)",
    "Stephen PrataStephen Prata",
    89.00
};
```

C99 标准，可以指定初始化
```c
/* 定义时初始化 */
struct book c_premier_plus = {
    .title = "C Premier Plus(6th Edition)",
    .author = "Stephen PrataStephen Prata",
    .value = 89.00
};
```


结构体数组的使用，

`struct book library[MAXBOOKS];` 


`library[4].title`


结构体的嵌套

```c
struct name{
    char first[LEN];
    char last[LEN];
};

struct gay{
    struct name handle;
    char job[LEN];
};
```

printf("name: %s", fellow.gay.name);

## 结构体指针

实际工程中的代码几乎都是通过指针阿里操作结构体的，几个原因
- 指向结构体的指针比结构体本身更容易操作
- 早期的 C 实现，结构不能作为参数传递给函数，但可以传递指向结构的指针
- 即使能传递结构，但是通过传递指针也更有效率
- 一些表示数据的结构中有指向其他结构的指针

结构指针的声明
```c
struct gay * him;
him = &barney;      /* barney 是一个 struct gay 类型结构 */
```

两种访问结构成员的方法
```c
printf("name: %s", (*him).name.first);
printf("name: %s", him->name.first);
```
使用 -> 是最常用的方法，但是从 him 是一个指针，解引用的方式也是可以的。而且必须要使用括号，. 的优先级高于 *


## 函数和结构


函数的参数把值传递给函数内部，这个值可以是 int。float，ascii，地址。结构比单独的值复杂，所以早期的 C 实现无法把整个结构作为参数传递给函数。

传递结构中的值和传递一个 int 没有区别，如果要修改结构中的值，那么就要传递结构成员的地址。这和传递一个变量是一样的。

更常见的是传递结构指针到一个函数中。

当然也可以向传递变量一个把整个结构体都传递到函数内。

现在的 C 还可以把整个结构体赋值给另一个结构体，这在思维上也是符合直觉的。

一些结构的例子

```c
#include <stdio.h>

#define MAX 20

struct book
{
    char name[MAX];
    char auth[MAX];
    float price;
};

void print_book(struct book b)
{
    printf("%s \n%s \n%f\n", b.name, b.auth, b.price);
}

void print_book_by_ptr(struct book *b)
{
    printf("%s \n%s \n%f\n", b->name, b->auth, b->price);
}

void print_book_name(const char* name)
{
    printf("%s \n", name);
}

int main(int argc, char const *argv[])
{
    struct book c_premier = {
        .name = "C Premier Plus",
        .auth = "unkonw",
        .price = 88.0
    };

    struct book cc = c_premier;

    print_book(c_premier);
    printf("%s \n%s \n%f\n", cc.name, cc.auth, cc.price);
    printf("%s \n%s \n%f\n", (struct book){"C Premier Plus", "unkonw", 88.0}.name, (struct book){"C Premier Plus", "unkonw", 88.0}.auth, (struct book){"C Premier Plus", "unkonw", 88.0}.price);

    return 0;
}
```

### 结构体中的指针

前面的例子都用字符数组来存放字符串，如果使用字符串指针，要特别注意。

```c
struct book
{
    char *name;
    char *auth;
    float price;
};

int main(int argc, char const *argv[])
{
    struct book c_premier;
    c_premier = (struct book){"C Premier Plus", "unkonw", 88.0};    /* 不必须做类型转换 */
    print_book_by_ptr(&c_premier);
    
    return 0;
}
```

代码是没问题的，但是要考虑字符串常来那个被存储的位置。字符串字面量存放在静态数据区，使用指针指向时，将字符串地址赋值给该指针。如果使用字面量初始化字符串数组，那么字符串是存放在结构内部的，并且有两个备份。

在使用指针时要特别小心。

通常，在结构体有指针的情况下，会配合 malloc 和 free 来手动分配或释放需要保存数据的内存。


### 结构字面量

前面已经用过了，但是注意字面量也可以使用指定初始化器，比如

```c
(struct book){
    .name = "C Premier Plus",
    .auth = "unkonw",
    .price = 88.0,
};
```

在所有函数外部的结构字面量具有静态存储期，在块中的字面量有自动存储期。


### 伸缩型数组成员

C99 新特性

```c
#include <stdio.h>
#include <stdlib.h>

struct flex
{
    size_t count;
    double average;
    double scores [];   /* 伸缩型数组成员 */
};

int main(int argc, char const *argv[])
{
    struct flex * pf = NULL;

    pf = malloc(sizeof(struct flex) + 5 * sizeof(double));

    pf->count = 5;
    pf->scores[4] = 20.0;
    return 0;
}
```

- 伸缩型数组成员必须为最后一个成员
- 数组括号是空的

C99 的地图声明一个指向 `struct flex` 的指针，然后用 malloc 分配足够的空间。这个称为 struct hack，大小为 0 的数组，针对 gcc 编译器，不属于 C 标准，但是这种伸缩型数组成员方法是标准认可的编程技巧。

### C11 匿名结构体

在嵌套联合中有用。

### 结构体数组

## 结构体内容的保存

结构体可以保存不同类型的信息，所以是构建数据库的重要工具。这些数据最重要保存到文件中，并且能被再次查询。存储在一个结构中的整套信息称为**记录**(record)，单独的项称为**字段**(field)

首先，存储记录效率最差的方法是使用 fprintf() ，如果结构成员很多，这个函数用起来就很复杂，此外在检索时也不方便，尽管可以使用固定宽度来对齐，但是仍然不好用。

更好的方案是使用 fread() 和 fwrite() 来读写结构大小的单元。比如

```c
fwrite(&c_primer_plus, sizeof(struct book), 1, pbooks);
```

把 c_primer_plus 结构大小的数据写入 pbooks，此函数一次读写一个记录，而非一个字段。

## 更多的数据结构

计算机工程中用来解决特定文件的数据结构：队列、二叉树、堆、哈希表、图标

许多这样的形式都是链式结构(linked structure)，通常一个结构包含一些数据项和一两个指向其他同类结构的指针。

## 联合

联合(union) 在同一个内存空间中存储不同的数据类型。

典型用法：设计一种表来存储一个事先不知道类型的的数据。

```c
union hold {
    int digit;
    double gitfl;
    char letter;
};

union hold fit;
fit.digit = 23; /* 存储 23 */
fit.gitfl = 2.0; /* 清除 23 存储 2.0 */
```

`.` 运算符表示正在使用哪种数据类型。用指针访问联合时也要用 -> 运算符。

用一个联合的成员把值存储，用另一个成员查看有时候很有用。

匿名联合也是 C11 的新特性，用法和匿名结构体一样。


## 枚举类型

枚举类型为了提高程序的可读性。语法和结构相同。

从技术层面看 enum 常量是 int 类型的，在声明中，可以指定枚举常用的整数值。

关于名称空间，结构、联合、枚举共享名称空间，普通变量是另一个空间

```c
struct point {double x; double y;};
float point;
```

这样是可以的，

## typedef 和复杂类型

常用于高级数据的定义，和 #define 有一点点像
- typedef 只用于类型，不用于值
- typedef 由编译器解释，不是预处理器

作用域取决于 typedef 的位置，在函数中，那么就只有函数作用域，在文件中，那么就有文件作用域。

typedef 可以设计来提高程序的可移植性，如 sizeof 的返回类型 size_t 

最重要的，常用来给复杂类型命名，大大增加程序的可读性。

```c
typedef void (*sighandler_t)(int);

sighandler_t signal(int signum, sighandler_t handler);
```

来分析一下复杂形式的类型定义。在复杂形式中，常见符号的含义
- `*` 表示一个指针
- `()` 表示一个函数
- `[]` 表示一个数组

在定义类型之前，先看看优先级 `[]` 和 `()` 的优先级相同，高于 `*` 举例说明 
- 如 `int * risks[10]` 是一个数组，数组里为指向 int 的指针
- 如 `int (* rusks)[10]` 优先级相同，从左往右，rusks 是一个指针，指向数组，数组含有 10 个 int 元素
- 如 `int goods[12][50]` 是一个含有 12 个元素的数组，每个元素是一个含有 50 个 int 元素的数组
- 如 `int *oof[3][4]` 是一个二维数组，每个元素为 int 类型的指针
- 如 `int (*uuf)[3][4]` 从左往右看，是一个指针，指向一个二维数组，每个元素都是 int 型

一个帮助理解的例子
```c
typedef int arr5_t[5];    /* arr5 是个新类型名 */
typedef arr5_t * arr5p_t;
typedef arr5p_t arrp_t[10];
arrp_t arr;
```

函数指针在一些编程中是常用的。比如 C 库函数中 qsort
```c
void qsort(void *base, size_t num, size_t size, int (*compar)(const void *, const void *));
```

最后一个参数，分析一下，这是个指针，指向一个函数，这个函数有两个参数，返回一个整数值。

C 库中的 qsort 可以处理任意类型的数组，但是要告诉此函数使用那个函数来比较元素的大小，然后 qsort 使用用户提供的函数来进行单个元素的比较，无论数组中是整数、字符串还是结构。

声明函数指针的一个方法，先声明一个函数

```c
int compare(const void *, const void *);        /* 先声明一个函数 */
int (*compare)(const void *, const void *);     /* 替换函数名 */
```

使用函数指针访问函数的方式，有两种逻辑上不一致的语法

```c
(*compare)(&num1, &num2);
compare(&num1, &num2);
```

*compare 相当于解引用，但是函数名本身就是地址，那么指针和函数名时可以互换使用的，因此世界使用 compare 是可以的。

函数指针作为函数参数的用法是很常见的，比如下面这个例子，这在 linux 里是真实存在的

```c
void (*ret)signal(int signum, void (*handler)(int))(int);
```

使用 typedef 来提高一下可读性
```c
typedef void (*sighandler_t)(int);

sighandler_t signal(int signum, sighandler_t handler);
```








