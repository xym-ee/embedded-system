---
sort: 2
---
# linux 操作系统

我们已经了解操作系统作为 “状态机的管理者”，通过为应用程序提供 fork, execve, exit 等系统调用使得第一个进程可以逐步构建出一个完整的应用世界。

这部分内容：完整的应用世界到底是如何构建的？在这节课中，我们用一个 “最小” 的 Linux 系统解答这个问题：
- Linux 操作系统
- Linux 系统启动和 initramfs
- Linux 应用世界的构建

## linux 操作系统


### minix

minix 年轻人的第一个全功能操作系统。


### linux 的成功

站在巨人的肩膀上构建自己的系统。给linux加一个补丁，就能适配自己的产品。linux 2.6 开始，2003年，大爆发。

<figure>
    <img src="https://jyywiki.cn/pages/OS/img/kernel-loc.png" >
</figure>

2003 后面几年，计算机系统的黄金时代。


### linux kernel

要注意前面是理论模型，并不是具体的那个操作系统。我们好奇 linux 到底符不符合前面的理论模型，我们日常看到的linux，比如 Ubuntu。

linux 的两面：
- kernel 
- kernel 系统调用上的发行版和生态。

github 上 linux 仅仅只是个内核，kernel。

kernel 可以理解成一个可执行的二进制文件，里面就是个指令序列，然后硬件厂商的固件和磁盘上的其它代码一起加载到内存上运行。运行起来就是 kernel，狭义的内核就是指一个在计算机启动后会被运行的程序，这个程序会加载第一个应用程序，还会创建一些对象，如 /dev/console，信息打印到这里。启动linux可能会发现，打印日志时，突然有一瞬间字体会变，这就是内核做了一些配置。最后启动完毕，对象创建完成，我们就可以使用系统调用操作这些对象了。

广义的 linux，我们看到的，图形界面，鼠标键盘能用，vscode 写代码，浏览器上网。或者 Android，底层也是 linux。所有我们早期使用的，都是linux kernel 系统调用上的发行版和应用生态
- 系统工具 coreutils, binutils, systemd, ...
- 桌面系统 Gnome, xfce, Android
- 应用程序 file manager, vscode, ...

```note
systemd，pstree 的根，随着我们对操作系统原理的理解越来越好，可以把一个合理的比较抽象的 kernel 概念映射到真实操作系统。后面会讲为什么 systemd 是根，事实上 init 进程并不是 systemd。
```

如果真想理解 linux 的启动到加载第一个进程的过程，能不能构建一个可以启动的最小的 kernel，然后运行我们自己的程序，一个输出 hello world 的程序，打印 hello world，然后退出。

## 构建最小的 linux

一个想法：我们能不能控制 kernel 加载的第一个状态机。

```note
在这个时代，更重要的是能不能想到好的问题，正确的问出来，今天，人工智能会比搜索引擎表现的更好。

求助于 chatgpt，如何问题好的问题。就需要把问题拆解为可以被一步步解决的问题。

如：我希望在给定的 linux 内核初始化完成后，直接执行我自己编写的静态链接的 init 二进制文件，我该怎么做。

有可能 chatgpt 给的细节信息并不正确，但是他给了足够多的信息，我们可以进一步重复上述过程。继续分解问题，然后提问。
```

成功实现后，会看到 hello world，用了几行脚本，正确的启动了我们自己的第一个进程。然后退出了，操作系统里没有任何进程了，然后内核报错：Kernel panic - not syncing: Attempted to kill init!

内核比较慌，😂。系统里没进程了。

既然可以控制启动程序，那正常来说，第一个启动的程序应该是什么？

一个练习，编译 linux 内核，启动后加载 busybox，实现一个比较完整的、可玩性比较高的 linux。

busybox 是个万能的程序，是个状态机，和 minimal 本质一样，静态链接的可执行文件，但是功能更强大，可以根据传入的参数变成任何东西，这是一个所有程序的集合的打包。unix 里重要的工具都有了。

```note
还有其他的如 toybox，安卓里常用，更小巧。
```

我们把 init 作为一个脚本，这个脚本用 busybox 来执行。

脚本里可以 echo ，也可以直接 `/bin/toybox sh` 启动成 shell，这就有点意思了。但是如果在这个终端里 ls 会提示找不到命令。很正常，没有这个可执行文件，没这个东西。但是我们可以 `/bin/busybox ls` 这就有了。

如何操作一下，让他更像一个真实的能用的更好玩的 bash 呢？肯定也是有办法的。

```bash
for cmd in $($BB --list); do
  $BB ln -s $BB /bin/$cmd
done
mkdir -p /tmp
mkdir -p /proc && mount -t proc  none /proc
mkdir -p /sys  && mount -t sysfs none /sys
mknod /dev/tty c 4 1
setsid /bin/sh </dev/tty >/dev/tty 2>&1
```

所有在 busybox 里的命令，按照其命令的名字复制一份。这时候就可以用一些命令来做一些事情了，然后创建一些目录，挂载一些东西。

最后把终端从调试串口移动到真实的机器上去。

这时候我们得到了一个近乎完整的 linux 体验，因此许多嵌入式系统里就是用 busybox 。这里如果我们查看进程树 `pstree` 看到根进程名为 init。

所有的这些指令都是 busybox，那么 busybox 如何知道该执行什么呢？用 strace 看看，任何的指令都有参数列表，参数的第一个是文件名，busybox 用了这个参数。

这些好玩的东西补上了理论和实践的 gap，纯实践也挺痛苦，纯理论有点空洞。

还可以继续追问：如果我希望用 QEMU 启动我给定的 Linux 内核二进制文件 vmlinuz 和初始内存文件系统 initramfs，应该使用怎样的 QEMU 参数使得 initramfs 中的 /bin/hello 作为第一个执行的程序？

对于初次接触 linux 的人来说，自己定制可能有点难度，但是有了这些基础的了解，再去看相关教程也不会那么困难了。

```note
你完全可以构建一个 “只有一个文件” 的 Linux 系统——Linux 系统会首先加载一个 “init RAM Disk” 或 “init RAM FS”，在作系统最小初始化完成后，将控制权移交给 “第一个进程”。借助互联网或人工智能，你能够找到正确的文档，例如 The kernel’s command-line parameters 描述了所有能传递给 Linux Kernel 的命令行选项。

恰恰是 UNIX “干净” 的设计 (完成初始化后将控制权移交给第一个进程) 使得 Linus 可以在可控的工程代价下实现 (相当完善的) POSIX 兼容，从而掀起一场操作系统的革命。时至今日，实现接口级的兼容已经是一件极为困难的工程问题，典型的例子是微软的工程师最终抛弃了 API 行为兼容的 Windows Subsystem for Linux 1.0，进而转向了虚拟机上运行的 Linux 内核。
```

有了这些了解，就可以去真正看看文档了。

某种程度上，linux 成功是偶然的。作为任何一个后来者，想实现一个完全兼容的东西是不可能的。

为什么我们国家不投很多人力物力做一个操作系统呢？如果想做到和 linux 兼容是不可能的，在 linus 那个时代和 POSIX 兼容是做得到的，今天再去做操作系统不是一个好主意。

微软想去做一个 WSL，把 linux 的进程在 Windows上启动起来，程序执行系统调用时用 windows 用自己的方法实现。这件事情最后证明行不通，api 不多，但是 linux 里的对象太多了，有太多太多历史上积累的东西在里面。

现在在写操作系统，作为一个爱好可以，真去做，也不太可能成为像 linus 那样的人了。


可以研究一下 busybox 的代码，没多少行，而且很好读，是个大的 switch case，是个状态机。从这些成熟的，维护的很好的代码看看代码应该怎么写，代码格式、语法、好的用法之类的。

当我们看过足够多的代码后，就会明白怎么样写是好的，什么时候该用什么样的写法。看过了资深程序员写的代码，再回过头对比自己的代码，就会有进步。


## 

为什么 pstree 的根是 systemd，启动以后我们有个 ramfs，在 ram 里，仅仅供初始化使用，这个时候系统里还没有磁盘。

还得看看之后发生了什么，。

系统的启动分两个阶段，这个阶段完成后，有个应用程序需要调用 

```c
int pivot_root(const char *new_root, const char *put_old);
```

执行 `/usr/sbin/init` 即 Kernel 的 init 选项。这是个快捷方式，链接到了 `/lib/systemd/systemd`。

ramfs 的事情是创建好足够多的对象，。

## 实际操作部分

## 操作系统启动后到底做了什么？(2022版未整理)

- 操作系统启动后到底做了什么？ 
  - CPU Reset → Firmware → Loader → Kernel _start() → 执行第一个程序 /bin/init → 中断/异常处理程序
  - 一个最小的 Linux 系统的例子
回顾操作系统内核的启动

cpu reset -> fireware -> boot loader -> kernel_start()

lagecay bios 固件完成操作系统加载。uefi里也有类似的东西。

Q1: 操作系统启动后到底做了什么？
Q2: 操作系统如何管理程序 (进程)？

```note
thread-os 在 main 开始后做一些系统的初始化，然后这个小操作系统会创建许多线程。这个有点像嵌入式系统里运行的小操作系统，CPU\MCU 里没有 MMU，没做虚拟内存的能力，只支持几个线程的执行。

等到任务创建完后，操作系统就不做事情了。
```

操作系统启动后，加载“第一个程序”，然后把所有的控制权交给这个程序。所有其他看到的东西( `pstree` )都是由这个程序启动的。

```bash
systemd─┬─YDLive───7*[{YDLive}]
        ├─YDService─┬─sh───9*[{sh}]
        │           └─23*[{YDService}]
        ├─acpid
        ├─2*[agetty]
        ├─barad_agent─┬─barad_agent
        │             └─barad_agent───2*[{barad_agent}]
        ├─cron
        ├─dbus-daemon
        ├─networkd-dispat
        ├─ntpd───{ntpd}
        ├─packagekitd───2*[{packagekitd}]
        ├─polkitd───2*[{polkitd}]
        ├─rsyslogd───3*[{rsyslogd}]
        ├─sgagent───{sgagent}
        ├─sshd─┬─sshd───sshd───fish
        │      ├─sshd───sshd───fish───sftp-server
        │      ├─sshd───sshd───fish─┬─pstree
        │      │                    └─{fish}
        │      └─sshd───sshd───fish─┬─sftp-server
        │                           └─{fish}
        ├─systemd-journal
        ├─systemd-logind
        ├─systemd-network
        ├─systemd-resolve
        ├─tat_agent───6*[{tat_agent}]
        ├─tmux: server───5*[fish]
        └─unattended-upgr───{unattended-upgr}
```

[linux内核启动代码](https://elixir.bootlin.com/linux/latest/source/init/main.c#L1555)

linux 试图启动一些东西。`try_to_run_init_process("/sbin/init")` ，试图启动这个程序，确实也是有的，软连接到 `init -> /lib/systemd/systemd` 确实是 systemd。

如果找不到这个文件，还会往下找。如果所有的都找不到，那么直接拒绝启动。可以试试，删掉这些文件，就无法启动系统了。但是还是有办法的，给内核加个选项。

第一个程序加载好，状态机就开始运行了。第一个程序创建其他程序，一级一级创建出来。

如果真的想让对进程或者linux的理解往前推一步的话，应该做什么呢？

是不是可以实现一个最小的Linux内核的镜像，只有一个程序，只要有一个程序，那么整个操作系统应该就能启动起来。

如果第一个进程，返回了，操作系统里就没有进程了，内核就不知道该干什么了。Kernel panic了。所以我们的第一个进程应该是一个不会终止的。

这个最小 linux 几乎啥也不能做。cpu reset 经过 fireware 然后 loader 加载 os，然后 init 启动第一个进程，然后所有的东西都有了。

创建一些目录，创建一些链接，然后体验就像是普通的 Linux 了。从啥也不能用，再到都能用，甚至可以编译程序。

实际上不仅是 linux ，其他的设备也是类似的模式，华为的鸿蒙。

这个东西可以玩玩，还是挺好玩的。

小结：

linux 操作系统的启动流程

cpu reset -> firmware -> loader -> kernel_start() -> 第一个程序 `/bin/init` -> 程序执行 + 系统调用

操作系统为 (所有) 程序提供 API
- 进程 (状态机) 管理
  - fork, execve, exit - 状态机的创建/改变/删除。这一节的主题
- 存储 (地址空间) 管理
  - mmap - 虚拟地址空间管理
- 文件 (数据对象) 管理
  - open, close, read, write - 文件访问管理
  - mkdir, link, unlink - 目录管理








