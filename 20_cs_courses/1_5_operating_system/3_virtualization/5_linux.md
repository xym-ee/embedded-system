
# linux 操作系统

我们已经了解操作系统作为 “状态机的管理者”，通过为应用程序提供 fork, execve, exit, mmap, pipe, open, read, write 等系统调用，配合 C/汇编实现的运行库，就为 “一个进程” 逐步构建出完整的应用世界做好了准备。

这部分内容：从理论到实践，Linux 世界到底是如何构建起来的？我们用一个 “最小” 的 Linux 系统的启动、initramfs 的探索，最终看到 systemd 是如何作为 “第一个进程” 真正被启动的。
- Linux 操作系统
- Linux 系统启动和 initramfs
- Linux systemd


复习，操作系统是对象+api，
- 对象：进程、文件、
- api：开关读写

系统调用之上，封装更好用的api，libc，在此之上构建应用程序，然后有了更多的东西。

## 1. linux 操作系统

### minix

minix 年轻人的第一个全功能操作系统。

minix3，一度是世界上应用最广的操作系统，因为 intel 把其移植到了一个固件上。

[如何看待英特尔管理引擎(Intel ME)被爆出运行在 Minix3 操作系统？](https://www.zhihu.com/question/67749141/answer/258836782)

### linux 的成功

站在巨人的肩膀上构建自己的系统。给linux加一个补丁，就能适配自己的产品。linux 2.6 开始，2003年，大爆发。

<figure>
    <img src="https://jyywiki.cn/pages/OS/img/kernel-loc.png" >
</figure>

2003 后面几年，计算机系统的黄金时代。

### linux kernel

要注意前面学的是**理论模型**，并不是具体的哪个操作系统(虽然有时候会用 linux 的 api 举例)。我们好奇 linux 到底符不符合前面的理论模型，我们日常看到的 linux，比如 Ubuntu。

linux 的两面：
- 1.**kernel** 
  - 加载第一个进程
    - 放置一个位于初始状态的状态机
    - initramfs 模式
  - 包含一些进程可操作的操作系统对象
  - 其他的没有了，变成 trap handler
- 2.**kernel 系统调用上的发行版和应用生态**
  - 系统工具 coreutils, binutils, systemd, ...
  - 桌面系统 Gnome, xfce, Android
  - 应用程序 file manager, vscode, ...

github 上 linux 仅仅只是个内核，kernel。

kernel 可以理解成一个可执行的二进制文件，里面就是个指令序列，然后硬件厂商的固件和磁盘上的其它代码一起加载到内存上运行。运行起来就是 kernel，狭义的内核就是指一个在计算机启动后会被运行的程序，这个程序会加载第一个应用程序，还会创建一些对象，如 /dev/console，信息打印到这里。启动linux可能会发现，打印日志时，突然有一瞬间字体会变，这就是内核做了一些配置。最后启动完毕，对象创建完成，我们就可以使用系统调用操作这些对象了。

广义的 linux，我们看到的，图形界面，鼠标键盘能用，vscode 写代码，浏览器上网。或者 Android，底层也是 linux。所有我们早期使用的，都是linux kernel 系统调用上的发行版和应用生态


```note
systemd，pstree 的根，随着我们对操作系统原理的理解越来越好，可以把一个合理的比较抽象的 kernel 概念映射到真实操作系统。后面会讲为什么 systemd 是根，事实上 init 进程并不是 systemd。

如果真想理解 linux 的启动到加载第一个进程的过程，能不能构建一个可以启动的最小的 kernel，然后运行我们自己的程序，一个输出 hello world 的程序，打印 hello world，然后退出。
```

## 2. 启动 Linux

回顾计算机的启动，CPU reset，firmware 执行，加载 linux 内核，启动 init 进程。

如果能控制 init 进程，在加载 init 的时候，此时有些什么内核对象呢。

在 ubuntu 更新的时候，可能偶尔会见到 update-initramfs，这个卡的时间比较久。

搞一个最小的 linux，需要的东西，vmlinuz ，init 文件，busybox ，把busybox和init脚本打包，放到一个初始的文件系统里。然后用 qemu 启动，指定使用的内核和使用的文件系统镜像。还指定了当前终端作为一个调试串口。

启动以后，可以发现里面几乎没什么东西，就 `/bin/busybox` `/dev/console` 就这两个。

整个完整的 linux 就基于此来构建。创建出更多的对象。

- 首先要有更多的命令，基于 busybox 的软连接。
- 然后就可以使用一些命令了，mkdir 创建一些目录，用 mount 挂在 procfs 和 sysfs，在 /dev 下创建一些设备。
- 输出一些启动日志
- 最后启动一个 busybox 的 sh。

这时候基本上就能有个完整的linux使用体验了。也就是说，只要加载了第一个我们能控制的 init ，就能创建所有的东西。






为什么 pstree 的根是 systemd，启动以后我们有个 ramfs，在 ram 里，仅仅供初始化使用，这个时候系统里还没有磁盘。

还得看看之后发生了什么，。

系统的启动分两个阶段，这个阶段完成后，有个应用程序需要调用 

```c
int pivot_root(const char *new_root, const char *put_old);
```

执行 `/usr/sbin/init` 即 Kernel 的 init 选项。这是个快捷方式，链接到了 `/lib/systemd/systemd`。

ramfs 的事情是创建好足够多的对象，。

## 3. 应用程序的世界

到这里，是没有磁盘的，使用 df 命令会报错，这个阶段是启动的初级阶段，内核启动起来了，小的内存里的fs也有了，这时候可以加载必要的驱动程序，如磁盘驱动，挂在必要的fs，最后要做的事情，把根文件系统的控制移交给另一个程序。

看 ubuntu ，pstree 是 systemd，但是 这里的 init 又不是 systemd，。

此时 init 进程还在继续，如果退出以后，一开始启动的脚本还在继续，后面做了更重要的事情，创建了一个新目录，挂载了一个磁盘，然后准备所有的完整的系统需要的东西，最后调用一个 switch_root 这个命令，直接把根目录切换了。

一些要求，调用这个命令的进程的 pid 必须是 1，没有任何一个 libc 会调用此命令，只有最底层的系统开发者才会用到这个。

然后，就成功的得到了一个完整的 linux，直接在机器上跑起来了。对于现在的linux，会在switchroot的时候会去找 /sbin/init。这个就是 systemd。 

刚刚还往文件系统里塞了一个网卡.ko，加载上去，然后可以启动网卡，加一个 ip 地址，这已经是完整的 linux 了，开一个 http 服务器。busbox 提供了一个 httpd，然后就可以访问了。

本质上和云服务器的 systemd 启动一个 Nginx 服务器是一样的。


```bash
python3 -m http.server
```

另一个想象，这些程序甚至不需要跑在 linux kernel 上，只要实现了 linux 的系统调用，然后就能运行起来 linux 的程序了。linux subsystem for Linux，用所有的 windows api 实现





## 总结(2022版未整理)

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








