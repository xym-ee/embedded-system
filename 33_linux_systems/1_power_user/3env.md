---
sort: 3
---
# 环境变量

## 变量

变量就是程序语言里的变量的意思，比如`int a`，定义一个变量。

直接在shell定义的变量为全局变量，

```shell
$ abc=123
$ echo abc
123
$ /bin/bash    # 子进程
$ echo abc

$ exit
exit
$ echo abc
123

# 如何让子进程也能访问这个变量的呢？
$ export abc
$ /bin/bash
$ echo abc
123
```
但是呢，如果再新开一个终端，这个abc就不能用了。

shell进程每次启动时，都会执行shell配置文件里的代码，那么如果把定义这些变量到配置文件里，shell在每次启动时，就会先完成这一操作了。

ubuntu的默认shell是bash，他的配置文件有
- /etc/profile
- ~/.bash_profile
- ~/.bash_login
- ~/.profile
- ~/.bashrc
- /etc/bashrc
- /etc/bash.bashrc

执行顺序，先从etc开始执行，然后去家目录。

/etc/profile所有用户登录时都会执行，家目录只有当前用户登录才执行。

如果想让全部用户全部进程都共享一个变量，那么就添加到/etc/bashrc里。

如果想让一个用户的全部进程都共享一个变量，那么就添加到~/.bashrc里。


对于脚本的启动方式，有4种

```shell
# test.sh
$ source test.sh    # 当前进程运行脚本
$ . test.sh         # 当前进程运行脚本
$ /bin/bash test.sh # 指定shell，新进程运行
$ ./test.sh         # 新进程运行

```


