---
sort: 2
---
# shell 基础


## shell 是啥

shell 和 windows 图形界面时一个层次的东西。图形界面和shell并非操作系统内核。

Shell 本身并不是内核的一部分，它是一个应用程序，开机自动启动，并呈现在用户面前；用户通过 Shell 来使用 Linux，不启动 Shell 的话，用户就没办法使用 Linux。

对于windows，没有图形界面的话，普通用户就无法使用计算机。

- 编程语言
- 解释shell语言的解析器


## shell 如何使用

shell 接收用户输入的字符串，解析处理后显示结果（输出到显示屏，写入文件）。

运行一个命令，shell会调用内核的**接口**，这就是用户使用内核的方式。shell并不接触底层如文件系统之类的，shell只是使用接口。

shell 有内部命令和外部命令。使用`type <cmd>`来查看命令类型。

命令是程序。在shell启动时，会加载命令所在的目录，即环境变量，`echo $PATH`输出的目录里就是所有可用的命令。

可以写一个helloworld程序，编译后把可执行程序的目录添加到环境变量里，就相当于自己搞了个外部命令。

Shell 本身支持的命令并不多，功能也有限，但是 Shell 可以调用其他的程序，每个程序就是一个命令，这使得 Shell 命令的数量可以无限扩展。

Shell 还可以让多个外部程序发生连接，在它们之间很方便地传递数据，也就是把一个程序的输出结果传递给另一个程序作为输入。

所以 Shell 的强大，是它擅长使用和组织其他的程序。

## shell是编程语言

编译型语言，解释型语言。shell和python差不多。

## 常用的 shell

- bash
  - linux的默认shell
- zsh
  - 具好用的现代shell

查看当前系统安装的shell`cat etc/shells`

上古时期，使用linux的唯一方式就是shell，现在都有图形化桌面了。

当然现代linux的发行版也保留了进入控制台的方法。现代 Linux 系统在启动时会自动创建几个虚拟控制台（Virtual Console），其中一个供图形桌面程序使用，其他的保留原生控制台的样子。虚拟控制台其实就是 Linux 系统内存中运行的虚拟终端（Virtual Terminal）。

从图形界面模式进入控制台按下Ctrl + Alt + Fn(n=1,2,3,4,5...)快捷键就能够来回切换。

图形界面也是程序，会占用资源，因此装有linux的服务器在安装调试完毕后，运行在控制台模式下可以节省资源。

学习时更常用的，是发行版里桌面环境的终端。即Terminal。ubuntu的图形界面程序是GNOME。

## shell 命令

```shell
# command <选项> <参数>
$ ls -l
```

- `ls -l`短格式选项是长格式选项的简写，`-`+一个字母
- `ls --all`长格式选项是完整的英文单词，`--`+一个单词


## shell 命令的本质

内置命令是自带的，外部命令可以无限扩展。外部命令就是一个程序，即命令就是一个可执行文件的名字。

除了名字，还得告诉shell去哪里找这个程序，这就是环境变量。

内置命令是个自带的函数，外部命令是个程序，执行内置命令就是调用一个函数速度很快，因为shell启动时就已经加载到内存了。外部命令在执行时要创建一个进程并加载应用程序的代码，所以外部命令执行会慢一点。

## shell 命令选项和参数

一些例子：
- `cd /` 这里`/`就是参数
- `ls -l` 这里`-l`是选项
- `ls --all` 这里`--all`是选项

自己写一个shell指令，比如经典两数求和
```c
#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int num1 = 0;
    int num2 = 0;
    int opt;
    char *optstring = ":a:b:";
    while((opt = getopt(argc, argv, optstring))!= -1)
    {
        switch(opt)
        {
            case 'a': num1 = atoi(optarg); break;
            case 'b': num2 = atoi(optarg); break;
            case ':': puts("Missing parameter"); exit(1);
        }
    }
    printf("num1: %5d  num2:%5d\n",num1,num2);
    printf("%d\n", num1 + num2);
    return 0;
}
```

编译生成可执行文件，执行
```bash
intsum -a 2 -b 3
```

指令后的参数原封不动的传进去，参数的解析，已经有前辈帮忙做好了，即函数`getopt()`

## shell 脚本

```shell
#!/bin/zsh
echo "hello world!"
```

第一行是约定标记。

在执行脚本前，要先给加上可执行权限。

脚本的运行实际上是新开了个进程。在shell脚本里输出`$$`就可以得到当前的PID。

关于脚本的执行，一种就是加了运行权限直接运行，新开进程。

还有一种是使用source命令。不需要可执行权限，这种方式是在当前shell的进程里复制脚本来执行。

## shell 配置文件加载

shell在启动时会加载一些配置信息，如运行环境之类的。

这些配置信息就是shell脚本文件，比如`~/.bashrc`就是一个配置文件，如果使用zsh的话`~/.zshrc`也是配置文件。

登录式的shell首先会读取和执行`/etc/profiles`全局配置文件，然后加载个人配置文件`~`里面。

非登录式的shell直接读取`~/.bashrc`，这个文件里会嵌套加载`/etc/bashrc`

既然配置文件也是脚本，那么也可以自己编写。

可以自己添加代码到`~/.bashrc`，比如ROS开发时候会加载一些环境变量进去，告诉shell可执行文件的存放地址。


## linux 环境变量

linux是个多用户多任务的系统


