---
sort: 1
---
# linux 基础使用

## 安装 linux

- 物理机装Ubuntu
- windows虚拟机装Ubuntu
- linux服务器 + windows客户端

## 文件目录

结构很清晰。入口，根目录`/`

文件系统层次结构标准，FHS3.0，文件结构层次是约定好的。

随便看几个文件夹。

- `bin`里是二进制文件，可执行程序，终端里输入的命令本质上就是在运行这里的可执行程序
- `boot`里存放的都是和启动相关的文件
- `cdrom`快要被淘汰了，媒体挂在media了
- `dev`操作外设就是操作这个文件夹里的东西
- `etc`配置文件
- `home`用户的文件
- `lib`bin里面东西依赖的东西
- `media`如果挂一个读卡器，那么就在这里面
- `mnt`也是设备的挂载
- `opt`options的简写，像是个临时文件夹的感觉
- `proc`存放程序，这些数字都是运行的程序的代号
- `root`
- `run`系统运行依赖的信息
- `sbin`和bin有区别，这里的命令只有root用户可以用
- `snap`
- `srv`网络服务相关
- `sys`硬件操作接口，可以在终端对外设简单做控制
- `tmp`
- `usr`存放大部分软件
- `var`易变的文件，日志，缓存，...


## 系统路径

- 绝对路径`/`起始
- 相对路径


最重要的，当前路径`.`或者用`./`

上一层目录`..`


## linux 文件类型

终端指令`ls -l`可以看到当前目录所有文件，文件的类型：

- 普通文件
- 目录文件
- 链接文件
- 设备文件
- 套接字文件
- 管道文件

一切皆文件

比如前面的根目录
```bash
lrwxrwxrwx   1 root root          7 7月  30 21:45 bin -> usr/bin
drwxr-xr-x   4 root root       4096 7月  30 22:05 boot
drwxr-xr-x  19 root root       4060 7月  31 10:31 dev
drwxr-xr-x 129 root root      12288 7月  30 22:13 etc
drwxr-xr-x   3 root root       4096 7月  30 21:47 home
lrwxrwxrwx   1 root root          7 7月  30 21:45 lib -> usr/lib
drwxr-xr-x   3 root root       4096 7月  30 21:54 media
drwxr-xr-x   2 root root       4096 2月  23 16:47 mnt
drwxr-xr-x   3 root root       4096 7月  30 21:50 opt
dr-xr-xr-x 280 root root          0 7月  31 10:31 proc
drwx------   4 root root       4096 7月  30 21:49 root
```

前面的`l`表示这个是链接，后面有个`->`也指向链接位置。`d`自然就是目录，所以第一个字母表示文件类型。

## 用户和用户组

linux 是多用户多任务系统，不同用户自己干自己的事情，个人开发都是有所有权限的。但是在团队开发时，要考虑权限了，一个工程师只能访问自己部分的东西。一上来就给root权限，出了字节实习生删库的事情就不太好了。

- UID：用户ID
- GID：组ID

几个与此相关的文件存放在`etc`配置文件夹里
- `/etc/passwd`
- `/etc/shadow`
- `/etc/group`

在电脑开机时，要输入密码才行。按下登录按钮后，根据用户名去passwd里找到UID，然后去group找到GID，如果都能找到那就意味着用户合法，最后去shadow找密码，全部对上就可以顺利进入系统。

passwd文件里面
```
root:x:0:0:root:/root:/bin/bash
meng:x:1000:1000:meng,,,:/home/meng:/bin/zsh
```

用户名：密码：UID：GID：记录乱七八糟信息：用户主目录：指定shell解析器

密码部分在上古时期确实放着密码，但这个文件是可读的，后来为了安全，这个字段代替了，真实密码加密放在shadow里。linux系统里实际上并不认识用户名，是只认UID的。

UID:
- root：0 所有权限
- 系统用户：1-999 管理系统运行服务
- 普通用户：1000 


还有个文件权限的问题，从左到右依次为

用户权限，用户组权限，其他用户权限。

## shell

shell是个应用程序，接收用户输入的指令，通过系统调用传送给内核运行，呈现内核运行结果。

另一个同等层次的应用程序时图形化界面。

基础指令，多用就完事了。

查询命令使用方式
- man #详细的手册
  - man 3 printf #指定查找章节
- cd --help #简短的帮助
- tldr #社区维护的帮助

文件和目录
- pwd #当前目录
- mkdir
- rmdir #删除空目录
- rm #删除
- mv #移动文件

文本操作
- touch
- cat
- echo
  - echo 1212 > a.txt
  - echo 4132 >> a.txt
- wc
- ln #

用户管理

文件权限
- chmod
  - sudo chmod 777 1.txt
- chown
- chgrp

磁盘管理
- df
- du
- mount
- umount

网络
- ping
- ifconfig

开关机
- reboot
- poweroff


## 编辑器

系统自带 gedit ，轻巧。

vscode 现代的编辑器。

vim，工程惯性。
