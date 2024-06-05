---
sort: 9
---
# rootfs : busybox 构建

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


nfs 挂载

```
root=/dev/nfs nfsroot=10.0.0.10:/home/xym/ws_linux/rootfs,proto=tcp rw
ip=10.0.0.11:10.0.0.10:10.0.0.1:255.255.255.0::eth0:off
```

启动参数
```
setenv bootargs 'console=ttymxc0,115200 root=/dev/nfs nfsroot=10.0.0.22:/home/xym/ws_linux/rootfs,proto=tcp,nfsvers=3 rw ip=10.0.0.11:10.0.0.22:10.0.0.1:255.255.255.0::eth0:off'
```

```
setenv bootargs 'console=tty1 console=ttymxc0,115200 root=/dev/nfs nfsroot=10.0.0.10:/home/xym/ws_linux/rootfs,proto=tcp,nfsvers=3 rw ip=10.0.0.11:10.0.0.10:10.0.0.1:255.255.255.0::eth0:off' 
```

uboot 有比较强的容错能力，可能首选非从 nfs 挂载，遇到这种情况，手动写死 bootcmd

```
setenv bootcmd 'tftp 80800000 zImage; tftp 83000000 imx6ull-mini.dtb; bootz 80800000 - 83000000;'
```

```
setenv bootcmd 'mmc dev 1; fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb; bootz 80800000 - 83000000;'
```


## 测试和完善

系统启动后

```
[    8.622515] VFS: Mounted root (nfs filesystem) on device 0:14.
[    8.630672] devtmpfs: mounted
[    8.634627] Freeing unused kernel memory: 528K (80b48000 - 80bcc000)
can't run '/etc/init.d/rcS': No such file or directory

Please press Enter to activate this console. 
```


提示 kernel(先笼统的这么讲) 想运行一个东西，但是没有。事实上这是个脚本，我们自己创建就好了。

kernel 启动后需要启动一些服务， `/etc/init.d/rcS` 脚本里启动了一些东西。


