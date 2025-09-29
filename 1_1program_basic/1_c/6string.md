
# 字符串和字符串函数


字符串的处理，字符串是以 '\0' 结尾的 char 类型数组。因此数组和指针的操作可以应用于字符串处理。C 库也提供了许多处理字符串的函数。

## 字符串表示

```c
#define MSG "string content"
#define MAX_LENGTH 80

int main()
{
    char words[MAX_LENGTH] = "string array";
    const char *ptr = "pointer at string";
    puts(MSG);
    puts(words);
    puts(ptr);
    return 0;
}
```

`puts` 函数只用来输出字符串，并自动在末尾加上换行符 `'\n'`

字符串字面量，或者叫字符串常量，""里的内容在编译时会自动加上 \0 ，ANSI C 标准规定，字符串字面量之间没有间隔或只用空格分隔，等效于一整个字符串字面量。

```c
char txt[50] = "hello" "world";
```

字符串常量(字符串字面量)为**静态存储类型**(static) ，在整个程序的生命周期内都存在。双引号的内容视为指向字符串存储位置的指针。理解下面的操作在干什么

```c
int main()
{
    printf("%s %p %c", "hello", "world", *"test");
}
```

定义字符串数组必须要让编译器知道多少空间。关于字符串数组的初始化

```c
char txt[20] = "hello world";
```

数组的末尾全都是 \0，字符串存储在静态存储区，程序加载时字符串常量就在了，但是数组在运行到的时候才会分配内存，此时将字符串复制到数组中。程序中有两个副本，一个是在静态内存中的字符串字面量，一个是在数组中的字符串。这是初始化字符串数组不一样的地方。

初始化一个字符串指针，只把字符串的地址赋值给指针，没有拷贝内容的过程。

一个例子

```c
#include <stdio.h>
#define MSG "hello world"
int main()
{
    char txt[] = MSG;
    const char *ptr = MSG;
    printf("%p\n", "hello world");
    printf("%p\n", txt);
    printf("%p\n", ptr);
    printf("%p\n", MSG);
    printf("%p\n", "hello world");
}
```

```bash
0x61c4f23c8004
0x7ffd69e9557c
0x61c4f23c8004
0x61c4f23c8004
0x61c4f23c8004
```

两个副本，以及编译器的优化，内容一致的字符串只留了一个副本。

字符串数组的两种方式

```c
#include <stdio.h>
#define SLEN 40
#define LIM 5
int main(void)
{
    const char *mytalents[LIM] = {
        "Adding numbers swiftly",
        "Multiplying accurately", 
        "Stashing data",
        "Following instructions to the letter",
        "Understanding the C language"
    };
    char yourtalents[LIM][SLEN] = {
        "Walking in a straight line",
        "Sleeping", 
        "Watching television",
        "Mailing letters", 
        "Reading email"
    };
    int i;
    
    puts("Let's compare talents.");
    printf ("%-36s  %-25s\n", "My Talents", "Your Talents");
    for (i = 0; i < LIM; i++)
        printf("%-36s  %-25s\n", mytalents[i], yourtalents[i]);
    printf("\nsizeof mytalents: %zd, sizeof yourtalents: %zd\n",
           sizeof(mytalents), sizeof(yourtalents));
    
    return 0;
}
```

mytalents 是一个指针数组，yourtalents 是一个二维数组。

字符串会涉及到指针，绝大多数操作都是通过指针完成的。

## 字符串输入

读字符串的第一件事，分配空间。最简单的方式 `char txt[80]` ，然后可以使用 scanf gets fgets 来读取了。

### gets puts

使用 `scanf("%s", txt)` 只能读取一个单词，读取整行使用 `gets()` 更方便，此函数读取整行知道遇到 `\n` ，然后丢弃 `\n` 存储其他内容，并在末尾加 `\0`。对应的输出函数为 `puts()`。

```c
#include <stdio.h>
#define STLEN 81
int main(void)
{
    char words[STLEN];
     
    puts("Enter a string, please.");
    gets(words);  // typical use
    printf("Your string twice:\n");
    printf("%s\n", words);
    puts(words);
    puts("Done.");
    
    return 0;
}
```

```shell
Enter a string, please.
hello world
Your string twice:
hello world
hello world
Done.
```

gcc 9.5.0 编译会给一个警告信息，
```c
getsputs.c:9:5: warning: implicit declaration of function ‘gets’; did you mean ‘fgets’? [-Wimplicit-function-declaration]
    9 |     gets(words);  // typical use
      |     ^~~~
      |     fgets
/usr/bin/ld: /tmp/cci9ChCl.o: in function `main':
getsputs.c:(.text+0x34): warning: the `gets' function is dangerous and should not be used.
```

问题在于，gets 只有一个参数，导致无法检查数组是否装得下，数组名会转换为数组首元素地址来处理，gets只知道数组的开始处，不知道数据中有多少个元素。如果输入的字符过多，就会导致缓冲区溢出(buffer overflow)，

因此在 C99 标准中建议不在使用此函数，所以使用此函数编译器会给出警告。C11 标准中直接废除了此函数。

### fgets fputs

gets 的代替函数。`fgets()` 

```c
char *fgets(char *str, int n, FILE *stream);
int fputs(const char *str, FILE *stream);
```
- 参数
  - str: 指向一个字符数组的指针，用于存储读取到的字符串。这个数组必须足够大以容纳读取的数据及一个终止空字符 '\0'。
  - n: 读取的最大字符数（包括终止空字符）。fgets 会读取至多 n-1 个字符，确保最后一个位置留给终止空字符 '\0'。
  - stream: 指向 FILE 对象的指针，指定从哪个文件流中读取数据。可以是 stdin（标准输入）、文件指针等。
- 返回值
  - 如果成功，fgets 返回 str（即存储读取数据的字符数组的指针）。
  - 如果发生错误或到达文件末尾且没有读取到任何字符，fgets 返回 NULL。

fgets 读到换行符 \n 也会存储到字符串中，所以输出使用配套的 fputs ，此函数不会在末尾再添加换行。

关于 fgets 和 fputs 的使用
```c
/*  fgets1.c  -- using fgets() and fputs() */
#include <stdio.h>
#define STLEN 14
int main(void)
{
    char words[STLEN];
    
    puts("Enter a string, please.");
    fgets(words, STLEN, stdin);
    printf("Your string twice (puts(), then fputs()):\n");
    puts(words);
    fputs(words, stdout);
    puts("Enter another string, please.");
    fgets(words, STLEN, stdin);
    printf("Your string twice (puts(), then fputs()):\n");
    puts(words);
    fputs(words, stdout);
    puts("Done.");
    
    return 0;
}
```

一个有意思的例子
```c
#include <stdio.h>
#define STLEN 10
int main(void)
{
    char words[STLEN];
    
    puts("Enter strings (empty line to quit):");
    while (fgets(words, STLEN, stdin) != NULL && words[0] != '\n')
        fputs(words, stdout);
    puts("Done.");
    
    return 0;
}
```

虽然 words 的长度很短，但是也正确的处理所所有的内容。linux 系统使用缓冲的 IO，按下 enter 之前，输入在缓冲区中，按下 enter 后，换行符也送入缓冲区同属吧整行发给 fgets，输出时，fputs 把字符发送给另一个缓冲区，直到遇到换行符，缓冲区的内容出现在屏幕上。


此外还有一个代替函数是 gets_s()，
```c
errno_t gets_s(char *str, rsize_t num);
```

在读取长度小于给定参数时，此函数用起来和 gets 一模一样。


### scanf

scanf 只读到空格，更像是获取单词的函数。此函数返回读取的单词数或者 EOF。例子

```c
/* scan_str.c -- using scanf() */
#include <stdio.h>
int main(void)
{
    char name1[11], name2[11];
    int count;
    
    printf("Please enter 2 names.\n");
    count = scanf("%5s %10s",name1, name2);
    printf("I read the %d names %s and %s.\n",
           count, name1, name2);
    
    return 0;
}
```

## 字符串输出

### puts()

非常好用，puts 在遇到 \0 就停止输出，然后在自动输出一个 \n。所以一定要确保有空字符。

gets() 丢弃换行符，puts自动补上换行符。

### fputs()

puts 向文件输出的版本。

```c
int fputs(const char *str, FILE *stream);
```

参数 stream 指明要输出的文件。如果要输出到显示器上则为 stdout。此函数不会自动添加 \n

fgets() 保留换行符，fputs() 不添加换行符。

### printf()

printf 不会为字符串结尾自动换行，因此需要指定
```c
printf("%s\n", txt);
```

### 自己的输入输出函数

如果 C 库函数满足不了要求，那么完全可以使用 getchar() 和 putchar() 的基础上实现自己的函数。

比如实习一个不自动换行的 puts

```c
void putstr(const char *str)
{
    while (*str != '\0')
        putchar(*(str++));
}
```

## 字符串函数

C 库 string.h 提供的库函数

### strlen()

strlen 用于计算字符串的长度（不包括终止的空字符 '\0'）。

```c
size_t strlen(const char *str);
```

- str: 指向要计算长度的以 '\0' 结尾的字符串的指针。
- 返回字符串的长度（不包括终止空字符 '\0'），类型为 size_t。

一个例子改变字符串的长度

```c
/* test_fit.c -- try the string-shrinking function */
#include <stdio.h>
#include <string.h> /* contains string function prototypes */
void fit(char *, unsigned int);

int main(void)
{
    char mesg[] = "Things should be as simple as possible,"
    " but not simpler.";
    
    puts(mesg);
    fit(mesg,38);
    puts(mesg);
    puts("Let's look at some more of the string.");
    puts(mesg + 39);
    
    return 0;
}

void fit(char *string, unsigned int size)
{
    if (strlen(string) > size)
        string[size] = '\0';
}
```

### strcat()

字符串拼接函数，把第 2 个字符串附加在第 1 个后面。

```c
char *strcat(char *dest, const char *src);
```

通过参数能看出来，此函数只修改 dest，

此函数不检查第一个数组是否能容纳第二个字符串，也会有溢出问题。和 gets 的问题类似

### strncat()

更安全的拼接

```c
char *strncat(char *dest, const char *src, size_t n);
```

- 参数说明
  - dest: 指向目标字符串的指针，该字符串必须已经以 '\0' 结尾，并且有足够的空间容纳 src 的 n 个字符以及终止的空字符 '\0'。
  - src: 指向源字符串的指针，这个字符串的前 n 个字符将被追加到 dest 的末尾。src 字符串必须以 '\0' 结尾。
  - n: 要追加的字符数，最多为 src 字符串的长度。如果 n 大于 src 的长度，strncat 只追加 src 中实际存在的字符。
- 返回值
  - 返回指向目标字符串 dest 的指针。

但是 C11 标准没有废除 strcat，来自于 C 语言相信程序员。gets 的输入来自用户，而 strcat 的问题在于程序员没有做好检查。因此写代码的人有义务确保 strcat 的安全。

### strcmp()


### strncmp

### strcpy strncpy

### sprintf


## 命令行参数的传递

## 字符串转换为数字







