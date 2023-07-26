---
sort: 1
---
# 系统镜像构建




- bootlader 
- kernel
- root filesystem
- device tree





依赖工具

```bash
sudo apt install make gcc-arm-linux-gnueabihf gcc bison flex libssl-dev dpkg-dev lzop vim
```


- [i.MX软件和开发工具](https://www.nxp.com.cn/design/software/embedded-software/i-mx-software:IMX-SW)

内核编译

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- imx_v7_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- all -j16
```

vscode 远程 ssh 的环境变量，可以手动设置 `set PATH $PATH /usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/` ，拼接一个 gcc 的路径上去。


启动一个串口终端
```
sudo vim /etc/default/grub
```

加上一些配置
```
GRUB_CMDLINE_LINUX="console=ttyS1,115200"
GRUB_TERMINAL="console serial"
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop==
1"
```

更新 grub 设置
```
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

重启
```
reboot
```



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


