
# 文件输入/输出

- fopen() fclose() getc() putc() exit()
- fprintf() fscanf() fgets() fputs()
- rewind() fseek() ftell() fflush()
- fgetpos() fsetpos() feof() ferror()
- ungetc() setvbuf() fread() fwrite()

## 与文件交互

最基本的 `ls > ls.txt` 实现了向文件输出， C 语言能完成对文件更复杂的操作，打开一个文件，然后使用 IO 函数读取或者写入。

文件是磁盘上有名字的存储区，是对磁盘的一种抽象。unix 或 C 语言把文件看做一个连续字节，类似数组，每个字节都能单独读写。

文件的两种类型：文本文件和二进制文件。所有文件都是以二进制方式存储的，但是如果是二进制编码字符如 ascii 码，那这就是文本文件。如果文件中的二进制值代表机器码或者数值数据(如 bmp mp3 avi)，那就是二进制文件。

unix 和 C 都是用 \n 来表示换行。MS-DOS 使用 \r\n 表示换行，
- 以文本模式打开文件，会自动替换为 C 模式的换行
- 以二进制方式打开时，会看到所有的原始内容

事实上，这两种模式对 unix linux 来说没什么区别。

除了文件的模式，还有 IO 的级别。**底层 I/O**(low-level I/O) 使用操作系统的 api，使用系统调用操作文件。**标准高级 I/O**(standard high-level I/O) 使用 C 库里的 api。这里讨论 标准高级IO，关于底层IO参考操作系统课程。

C 程序会自动打开 3 个文件 **标准输入**、**标准输出**、**标准错误**。默认下标准输入是键盘，标准输出和错误输出时显示屏。
- 标准输入是 getchar() scanf() 等使用的文件
- 标准输出是 putchar() puts() printf() 等使用的文件

这 3 个文件都是指向 FILE 的指针，stdin stdout stderr，可以作为标准 IO 的参数，。

标准输出提供了一个逻辑上不同的地方来发送错误信息，如使用重定向把标准输出到文件，那么标准错误仍然会输出到屏幕上。

## C 库标准 I/O

与系统调用相比，C 库标准 I/O 的优势
- 封装了更好用的 I/O，如 printf 把不同形式的数据转换成屏幕上的字符
- 输入输出缓冲，一次转移一块信息(通常512Byte)，减少了进入内核态的次数

一个操作文件的例子

```c
#include <stdio.h>

int main()
{
    int ch;
    unsigned long int count = 0;

    FILE *fp = fopen("./dns.c", "r");

    while ( (ch = getc(fp)) != EOF )
    {
        putc(ch, stdout);
        count++;
    }
    fclose(fp);
    printf("%ld\n", count);
    return 0;
}
```

这里使用了 EOF 来判断文件结尾。上面的程序是读取文件循环的一个标准写法。因此在 while 条件里判断时，一定要先读取一次。不能写成下面这样

```c
while(ch != EOF)
{

}
```


### fopen()


### getc() putc() 

和 getchar() putchar() 类似，这两个函数只从标准输入读，只输出到标准输出。getc 和 putc 是这两个函数的文件读写版。

`putc(ch, stdout)` 和 `putchar(ch)` 的效果是一样的


### fclose()



## 文件 I/O 

### fprintf() fscanf()

printf 和 scanf 的文件版，第一参数为文件指针，其他的用法全都一样。

### fgets() fputs()

gets 和 puts 的文件版，

### 随机访问 fseek() ftell()

文件可以看做是一个数组，前面的 API 并没有明显的指出文件的位置。

fseek() 可以设置读取的位置。

### fgetpos() fsetpos()

## 更多的标准 IO

### fflush()

### 二进制 IO fread() fwrite()


























