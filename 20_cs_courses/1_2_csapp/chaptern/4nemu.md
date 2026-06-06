---
sort: 3
---
# NEMU代码导读


## 如何读代码

拿到一个项目，先看看目录结构，比如`tree`,


```bash
find . -name "*.c" -o -name "*.h"
```

指令和字符串，shell指令使用C语言实现，是对字符串的处理。`-o` 为或。这个命令输出了项目里的源文件，

查看代码行数

```bash
find . -name "*.c" -o -name "*.h" | xargs cat | wc -l
```

`xargs`把前面的标准输出（路径和文件名）作为标准输入作为参数给到到`cat`。


读C语言代码，可以从main开始

尝试读代码，从`main`开始。那么这个文件在那里呢？

IDE搜索文件，命令行可以直接用vim打开目录。


```bash
grep -n main $(find . -name "*.c")
```

把$之后的命令的结果作为输入

能找到我们需要的main函数了。

关于工具，一个用来模糊查找文件shell工具，fzf。这个工具可以弹出命令行菜单，有意思的用法，可以放在命令行的参数里：

```bash
vim $(fzf)
```

unix世界的惊喜是所有的东西都可以组合，可以用`$()`来把命令的输出粘贴到参数里，也可以用管道把一个程序的输出作为另一个程序的输入。

使用计算机，实际上随时都在编程。Ubuntu手边的工具，不像VSC一样主动，随时随地弹出一个消息框提醒该安装东西了。虽然没这么贴心，但是命令行工具一直都在那里，他不会主动推销任何东西。

所以需要学习者主动去开源社区寻找，去发现。这种感觉可能像是在Geeker的道路越走越远，但实际上是在professional的道路上越走越远。一个优秀的开发者一定是一个power user。


找到main了，找里面的函数，这又该怎么找呢？当然直接使用IDE编译以后跳转也没有任何问题。但如果想坚持在命令行里操作呢


如果希望一个函数去解析主演书传入的参数，那么可以定义和main相同的参数。这在rtt的指令导出里用到了。这里来看看`argc`和`argc`是啥
```c

```

`argv`是指针的指针，argv指向了一个指针数组，即argv里的地址是一个数组的起始地址。这个指针数组里面的指针又指向一系列字符串的位置。

```c
static int parse_args(int argc, char *argv[]) {
  const struct option table[] = {
    {"batch"    , no_argument      , NULL, 'b'},
    {"log"      , required_argument, NULL, 'l'},
    {"diff"     , required_argument, NULL, 'd'},
    {"port"     , required_argument, NULL, 'p'},
    {"help"     , no_argument      , NULL, 'h'},
    {0          , 0                , NULL,  0 },
  };
  int o;
  while ( (o = getopt_long(argc, argv, "-bhl:d:p:", table, NULL)) != -1) {
    switch (o) {
      case 'b': sdb_set_batch_mode(); break;
      case 'p': sscanf(optarg, "%d", &difftest_port); break;
      case 'l': log_file = optarg; break;
      case 'd': diff_so_file = optarg; break;
      case 1: img_file = optarg; return 0;
      default:
        printf("Usage: %s [OPTION...] IMAGE [args]\n\n", argv[0]);
        printf("\t-b,--batch              run with batch mode\n");
        printf("\t-l,--log=FILE           output log to FILE\n");
        printf("\t-d,--diff=REF_SO        run DiffTest with reference REF_SO\n");
        printf("\t-p,--port=PORT          run DiffTest with port PORT\n");
        printf("\n");
        exit(0);
    }
  }
  return 0;
}

```
这个函数看起来是处理指令的。

default会去打印一个使用方法。

这里有一些很有意思的东西，可以试着看看。linux有个函数是`getopt`

命令行输入`man getopt`，得不到想要的，输`man getopt_long`。翻到最后有个see also。

可以输入`man 3 getopt`一样的，。

这里可以看到一小段程序：
```c
int main(int argc, char **argv) {
    int c;
    int digit_optind = 0;

    while (1) {
        int this_option_optind = optind ? optind : 1;
        int option_index = 0;
        static struct option long_options[] = {
            {"add",     required_argument, 0,  0 },
            {"append",  no_argument,       0,  0 },
            {"delete",  required_argument, 0,  0 },
            {"verbose", no_argument,       0,  0 },
            {"create",  required_argument, 0, 'c'},
            {"file",    required_argument, 0,  0 },
            {0,         0,                 0,  0 }
        };

        c = getopt_long(argc, argv, "abc:d:012",
                long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {
        case 0:
            printf("option %s", long_options[option_index].name);
            if (optarg)
                printf(" with arg %s", optarg);
            printf("\n");
            break;

        case '0':
        case '1':
        case '2':
            if (digit_optind != 0 && digit_optind !=  this_option_optind)
                printf("digits occur in two different argv-elements.\n");
            digit_optind = this_option_optind;
            printf("option %c\n", c);
            break;

        case 'a':
            printf("option a\n");
            break;

        case 'b':
            printf("option b\n");
            break;
        case 'd':
            printf("option d with value '%s'\n", optarg);
            break;

        case '?':
            break;

        default:
            printf("?? getopt returned character code 0%o ??\n", c);
        }
    }

    if (optind < argc) {
        printf("non-option ARGV-elements: ");
        while (optind < argc)
            printf("%s ", argv[optind++]);
        printf("\n");
    }

    exit(EXIT_SUCCESS); 
}
```

如果读过这个手册，就可以理解这些代码的含义了。可以理解unix如何设计api是帮我们完成事情的，而且这是一种内在的通用原则，了解了如何实现指令，在自己使用的时候，更有感觉。
