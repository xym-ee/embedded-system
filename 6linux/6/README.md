---
sort: 3
---
# 根文件系统

rootfs

stm32 里要想驱动 sd 卡，需要移植一个 fatfs 文件系统。

这两个不是一个东西。这里的 rootfs 并不是一个代码实现上的东西。

fatfs、ext4、ntfs 这类文件系统类型，在 linux 内核里已经有实现代码了。

这里的根文件系统，根/文件/系统。即 linux 所需要的文件，软件、配置文件、依赖库。

zImage 的内核只有 6M 大小。而 Ubuntu 镜像有 3G，ubuntu 跑的内核也就这么大，其他的都是各种文件。Ubuntu
装好后有各种软件，。

嵌入式 linux 里也需要构建这么一个东西，准备好系统运行需要的东西。

大型的发行版的系统，ubuntu 等，都需要创建对应的根文件系统。一些典型的东西
- 命令
- 库
- 配置文件


bin 中的命令的源码在 [coreutils](https://github.com/coreutils/coreutils/tree/master/src) 可以看到。

在嵌入式领域，常用 busybox，一个可执行文件整合了大部分的基础工具。在这个工具的基础上，可以做更多的事情。

此外还有 buildroot、yocto，相当完善的。

## busybox

BusyBox 可以在其官网下载到，官网地址为：https://busybox.net/

下载源码，

















