# shell 指令

当可视化界面无法完成一些定制的功能时，shell 说不定可以。毕竟使用 UI 的功能也是开发 UI 的人设计的，不可能面面俱到。

shell 的文本工具缺可以相互组合，用不同的组合或者编程方式把一些 GUI 无法完成的工作完成。

windows 的 powershell ，linux sehll，形式、语法上可能不一样，但是思想是一样的。最常见的 shell bash，以此来学习。

## 

打开 shell，一个命令提示符，这些全都可以自己配置。和计算机交互的文本界面。

基本的使用方式，输入命令，当个命令加参数是最简单的使用方式。`date` ，执行一个名为 date 的程序。

```bash
m@vm:~$ date
2024年 08月 22日 星期四 12:20:37 CST
m@vm:~$
```

然后，shell 等待我们输入其他命令。可以在执行命令的同时向程序传递 参数 ：

m@vm:~$ echo hello
hello
m@vm:~$

执行一个名为 echo 的程序，输出一点东西。参数由空格分开，如果要输入一个包含空格的参数

m@vm:~$ echo "hello world"
hello world
m@vm:~$ echo hello\ world
hello world

当输入一个程序名时，shell 怎么找到程序在哪里的？首先这些程序肯定在计算机里，

通过环境变量来实现，环境变量像是个编程语言里的变量保存着一些东西，bash 也确实是一个编程语言。可以 while 循环 for 循环 条件语句 。在 shell 中定义变量，定义函数。下一节(shell 脚本)

环境变量在启动shell就设置了，有一堆这些东西，如主目录，用户名，搜索路径的变量是路径变量

m@vm:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/m/bare_metal/arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi/bin
m@vm:~$

用:分割的目录，当输入程序名时，shell 按照上面的路径依次查找。直到找到为止。使用 which 可以查看使用的是哪个可执行文件。

m@vm:~$ which echo
/usr/bin/echo
m@vm:~$

也可以绕过 $PATH 直接通过绝对路径指定要执行的可执行文件。

m@vm:~$ /usr/bin/echo hello
hello
m@vm:~$

当前目录 pwd，cd 切换，. 和 .. 的含义

注意，shell 会实时显示当前的路径信息。可以通过配置 shell 提示符来显示各种有用的信息。

运行一个程序时，如果我们没有指定路径，则该程序会在当前目录下执行。例如查看指定目录下包含哪些文件，我们使用 ls 命令默认列出当前的，也可以用参数指定

m@vm:/home$ ls /home/m

两个特殊的符号，`~` 扩展为用户文件夹，`-` 之前在的目录，一般 `cd -` 来快速切换

程序的参数或标志，ls --flag

ls -l 长列表，权限，chmod chown

文件的权限很好理解，目录的权限，
- 读取：是否被允许看到这个目录中的文件
- 写入：是否允许在目录中重命名、创建、删除文件
- 执行：搜索权限，是否允许进入该目录

如果对一个文件有写入权限，但没有对目录的写入权限，那么就不能删除文件，可以清空内容但不能删除，因为这要写入目录本身。

目录的执行权限，如果想打开一个文件，用 cd 进入一个目录，必须有该目录和父目录的执行权限。如要访问 /usr/bin/echo ，必须有 / usr bin 目录的执行权限。

还需要掌握的命令 mv cp mkdir rmdir rm 

mv 用来移动和重命名。cp 命令也很类似，在复制的时候可以指定复制过去的名字。

rm 命令，在linux默认删除不递归，无法用rm移除一个文件，需要加上 -r 进行递归删除，即删除一个目录下所有的东西。rmdir 只能删除一个空目录，这是一种安全机制。mkdir 创建新目录，对于包含空格的目录，则需要引用或加\

在没有网络的时代，查手册，man 以另一个程序的名字作为参数。给出了非常详细的说明。

ctrl + L 清除中断，返回顶部。

## 程序之间的连接

前面都是单独一个程序运行的情况，当开始组合不同的程序时，shell 的强大功能才能体现出来。

终端与文件交互，并让文件在不同程序之间传输。shell 实现这个东西的基础概念：流

程序有两个主要的“流”：它们的输入流和输出流。当程序尝试读取信息时，它们会从输入流中进行读取，当程序打印信息时，它们会将信息输出到输出流中。通常，一个程序的输入输出流都是终端。也就是，键盘作为输入，显示器作为输出。shell 提供了重定向的方法，改变程序输入输出的指向。

最简单的重定向是 < file 和 > file。这两个命令可以将程序的输入输出流分别重定向到文件：

m@vm:~/missing$ echo hello > hello.txt

没有输出，输出被定向到了 Hello.txt 中。用 cat 可以查看。

cat 可以将输入与输出连接起来。比如一个例子

m@vm:~/missing$ cat < hello.txt > hello2.txt

不使用 cp 命令的复制。关键在在于，cat 并不知道自己在干什么，不知道重定向，也不知道什么是复制，只是按照规定的方式运行。但是让 shell 使用 hello.txt 作为 cat 的输出，并将 cat 打印的任何输出写入 hello2.txt，实现了和 cp hello.txt hello2.txt 一样的功能。这部分是 shell 设计的核心理念，用简单的工具组合来做更复杂的事。

`>>` 表示追加，

这些也只是简单的操作。shell 提供另一个运算符，管道 | ，左边的程序作为输出，右边的程序作为输入。

比如只看根目录的最后一行 `ls -l / | tail`

m@vm:~/missing$ ls -l / | tail --lines=1
m@vm:~/missing$ ls -l / | tail -n1


ls 不知道 tail 的存在，tail 也不知道有 ls，这是两个不同的程序，也没再设计时做兼容性的适配，他们只是从输入读了一些东西，然后按照自己的处理方式处理后输出。管道连接二者，，希望ls的输出作为tail的输入。

可以做一些更有趣的事情，数据处理。

m@vm:~/missing$ curl --head --silent baidu.com | grep --ignore-case content-length | cut --delimiter=' ' -f2
81

这个命令的作用是从 baidu.com 的 HTTP 响应头中提取 Content-Length 头的值。或者从 ifconfig 的输出中提取 ip

ifconfig ens33 | grep 'inet' | head --lines=1 |  cut --delimiter=' ' -f10

可以看到用各种工具可以实现有趣的事情。除了文本，管道还可以处理图像甚至是视屏。

后面数据处理更详细的学。

## root 用户的讨论

对于大多数的类 Unix 系统，根用户（root user）是非常特殊的，在上面的输出结果中，根用户几乎不受任何限制，他可以创建、读取、更新和删除系统中的任何文件。 通常在我们并不会以根用户的身份直接登录系统，因为这样可能会因为某些错误的操作而破坏系统。 取而代之的是我们会在需要的时候使用 sudo 命令。

向 sysfs 文件写入内容必须根用户才能做。sysfs 挂在到 /sys 下，里面有各种内核参数，不需要任何专业工具，可以直接访问操作系统内核的东西。

在 /sys/class/leds/input1::capslock 下有个 brightness 文件夹，可以直接写入参数控制 led 亮度。

如果尝试 `echo 1 > brightness` 没有权限，会被拒绝，修改内核是不被允许的。如果 `sudo echo 1 > brightness` 也是不被允许的。问题出在了管道的设计上。

输入输出重定向程序并不知道。| <> 都是通过shell 执行的，上面的代码为了能让 sudo echo 的输出写入 brightness，会先打开 brightness(这个设计也很好理解)，此时还是普通用户。

解决方法，直接整个切换，su 换到root，提示符也变成了 #，然后上面的就可以执行了。

基于对 shell 工作方式的理解，还可以有一种方法

```bash
m@vm:/sys/class/leds/input1::capslock$ echo 1 | sudo tee brightness
```

tee 用来读取标准输入的内容，然后输出到一个文件和标准输出。标准输入一分二。

让 tee 以 root 用户执行，输出到 brightness，这个事情是可以的。

如果写一个程序，在收到邮件时，让键盘上的一个灯亮起来，这也是个很好玩的事情。



## 

xdg-open 

touch




