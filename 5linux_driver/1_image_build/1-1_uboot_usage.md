---
sort: 1
---
# u-boot 编译与使用


## uboot 简介

uboot(Universal Boot Loader) 是一个综合的裸机程序。现在的 uboot 已经支持液晶屏、网络、USB 等高级功能。

uboot 最主要的工作是初始化 DDR，linux 是运行在 DDR 里的。因此在启动 linux 内核前，就要初始化完成 DDR。对于 6u 芯片，DDR 的初始化代码在芯片 rom 中。因此在 imx 系列芯片，uboot 的代码并不需要去初始化 DDR。但是大部分的芯片都需要在 uboot 中去初始化 DDR。

linux 镜像(zImage, uImage)和设备树(*.dtb)存放在 EMMC，NAND，Flash等，因此系统要想运行，还需要把代码从持久化存储设备中复制到RAM中，因此 uboot 还需要初始化完成这些设备。

uboot 会做为了linux系统启动需要准备的所有东西，启动后，uboot就消失了。操作系统接手后面的事情。

uboot 本身是个通用的 bootloader，支持不同的板子、不同的操作系统。

不同的板子外设不同，使用时先要配置成我们需要的样子，然后编译成和板子匹配的可执行文件，一般是 uboot.bin，对于 i.mx 芯片，还要加上ivt dcd 等，就可以正常启动了。

系统启动时，会输出各种信息，属于 uboot 阶段的：

```
U-Boot 2020.10-g92bbb671 (Feb 10 2022 - 02:36:31 +0000)

CPU:   Freescale i.MX6ULL rev1.1 792 MHz (running at 396 MHz)
CPU:   Industrial temperature grade (-40C to 105C) at 41C
Reset cause: POR
Model: Freescale i.MX6 UltraLiteLite 14x14 EVK Board
Board: MX6ULL 14x14 EVK
DRAM:  512 MiB
MMC:   FSL_SDHC: 0, FSL_SDHC: 1
Loading Environment from MMC... OK
In:    serial
Out:   serial
Err:   serial
Net:   eth1: ethernet@20b4000 [PRIME]Could not get PHY for FEC0: addr 2

Hit any key to stop autoboot:  0
Unknown command 'lhf' - try 'help'
switch to partitions #0, OK
mmc1(part 0) is current device
loading [mmc 1:1] /uEnv.txt ...
2584 bytes read in 13 ms (193.4 KiB/s)
Importing environment from mmc ...
loading vmlinuz-4.19.35-imx6 ...
10138912 bytes read in 459 ms (21.1 MiB/s)
loading imx6ull-mmc-npi.dtb ...
38529 bytes read in 69 ms (544.9 KiB/s)
5164702 bytes read in 242 ms (20.4 MiB/s)
debug: [console=ttymxc0 root=/dev/mmcblk1p2 rw rootfstype=ext4 rootwait coherent_pool=1M net.ifnames=0 vt.global_cursor_default=0] ...
debug: [bootz] ...
Kernel image @ 0x80800000 [ 0x000000 - 0x9ab520 ]
## Flattened Device Tree blob at 83000000
   Booting using the fdt blob at 0x83000000
   Using Device Tree in place at 83000000, end 8303cfff

Starting kernel ...
```

## 源码编译


### source code 在哪里？

uboot 的源码

- u-boot 项目
  - <https://ftp.denx.de/pub/u-boot/>
  - <https://github.com/u-boot/u-boot>
  - 支具体的某款芯片的驱动不完善，但是不断有人会贡献代码，修复bug
- 芯片厂商适配的 uboot
  - <https://github.com/nxp-imx/uboot-imx>
  - 芯片厂商会基于某个版本的 uboot，深度适配自己的 evk 评估板，如 [i.mx6ull evk](https://www.nxp.com.cn/design/development-boards/i-mx-evaluation-and-development-boards/evaluation-kit-for-the-i-mx-6ull-and-6ulz-applications-processor:MCIMX6ULL-EVK) 板
- 二级开发板厂商的 uboot
  - 如野火、正点原子、飞凌等公司开发板的 uboot
  - 开发板厂商会参考芯片厂商的 evk ，定制自己的开发板，在芯片厂商 uboot 的基础上适配开发板的功能


所以 uboot 移植，实际上是适配自己的板子，真正的最复杂的移植部分厂商的工程师已经解决掉了。

对于 nxp imx6ull 这个芯片，uboot 源码里由这个配置。


### 源码编译

不论是从哪里得到的源码，编译过程：

```bash
# 清理工程
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean

# 使用默认配置文件配置编译选项
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- mx6ull_14x14_ddr512_emmc_defconfig

# 编译
make V=1 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j12
```

- 工程清理。`ARCH=arm` 设置目标为 arm 架构，`CROSS_COMPILE` 指定所使用的交叉编译器。第一条命令相当于“make distclean”，清除工程
- 配置 uboot。`make mx6ull_14x14_ddr512_emmc_defconfig`，使用默认配置文件，把配置项写到 `.config` 里
- 编译。最后一条指令相当于 `make -j12` 也就是使用 12 核来编译 uboot，`V=1` 输出中间信息

makefile 里要判断架构，相当于传入参数里设置了架构。以及使用的交叉编译器。

编译完成后，会出来一些文件。

- uboot.bin 编译完成无法启动，需要添加其他信息(imx系列)。这里从编译信息可以看到最后一步

./tools/mkimage -n board/freescale/mx6ullevk/imximage-ddr512.cfg.cfgtmp -T imximage -e 0x87800000 -d u-boot.bin u-boot.imx

用这个工具完成的。最终可以用的是 `u-boot.imx`

otg 烧写，工具，mfgtools，
- firmware 先下载到 DDR 里的中间系统
- files 最终下载到 mmc 里的系统。

替换文件即可。

用这个东西烧写会重新烧录所有东西进去。烧写完成设置 emmc 启动，在此启动就能看到编译编译时间。


### 自动化脚本

再精简一下整个流程。

```makefile
#!/bin/bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- mx6ull_14x14_ddr512_emmc_defconfig
make V=1 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j12
```

通过图形化界面配置后，就不可以 distclean 了。

此外，还可以直接给 Makefile 里的传入的变量赋值，就不用每次输这么多指令了。


```bash
sudo apt install make git gcc-arm-none-eabi gcc bison flex libssl-dev dpkg-dev lzop libncurses5-dev
```

- make : 自动化编译工具
- git : 版本管理工具
- gcc-arm-none-eabi : 交叉编译的工具链
- gcc : 本地编译的工具链
- bison : 



为了方便，学习 uboot 期间可以把 uboot 烧到 SD 卡中启动。

SD 卡插到 imxdownload 中，和裸机下载程序一样。比较方便。


## u-boot 命令使用

### 基本信息

- `help`
- `help [具体命令]`
- `bdinfo`
- `printenv`
- `version`



```
=> bdinfo
boot_params = 0x80000100
DRAM bank   = 0x00000000
-> start    = 0x80000000
-> size     = 0x20000000
flashstart  = 0x00000000
flashsize   = 0x00000000
flashoffset = 0x00000000
baudrate    = 115200 bps
relocaddr   = 0x9ff9b000
reloc off   = 0x1879b000
Build       = 32-bit
current eth = ethernet@20b4000
ethaddr     = (not set)
IP addr     = <NULL>
fdt_blob    = 0x9ef8fd70
new_fdt     = 0x9ef8fd70
fdt_size    = 0x00009160
lmb_dump_all:
    memory.cnt             = 0x1
    memory.size            = 0x0
    memory.reg[0x0].base   = 0x80000000
                   .size   = 0x20000000

    reserved.cnt           = 0x1
    reserved.size          = 0x0
    reserved.reg[0x0].base = 0x9ef8eb6c
                     .size = 0x1071494
arch_number = 0x00000000
TLB addr    = 0x9fff0000
irq_sp      = 0x9ef8fd60
sp start    = 0x9ef8fd50
Early malloc usage: 58c / 2000
```

含义
- boot 参数存放地址 0x80000100
- DDR 的起始地址 0x80000000
  - 有的板子会配置成两个 bank，两个不连续的地址空间
- 串口波特率
- 各种地址，先不关注


### 环境变量操作

- `printenv`
  - 有很多。关注 bootcmd 和 bootargs
- `setenv` / `saveenv`

设置环境变量

比如设置boot延时时间。

- `setenv bootdelay 5`
- `saveenv`

对于比较长的环境变量，带空格的，要加上字符串引用

- `setenv bootcmd 'console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw'`

设置一个控制台串口，以及挂载根文件系统的设备。

新建一个没有的环境变量也用此命令

- `setenv xymenv xym`

删除环境变量，即给环境变量一个空的值

- `setenv xymenv`


### 内存操作

具体的操作，可以看 uboot 中的帮助

- `md`
- `nm`
- `mm`
- `mw`
- `cp`
- `cmp`

#### md(memory display)

查看指定位置的内存值

- `md[.b .w .l] {address} {length}`
  - `md.b 80000000 64`
  - `md.w 80000000 128`
  - `md.l 80000000 256`

#### nm()

修改指定位置的值

- `nm[.b .w .l] {address}`
  - `nm.b 80000000`
  - `nm.w 80000000`
  - `nm.l 80000000`


```
=>nm.b 80000000
80000000: 00 ? 55
80000000: 55 ? q
```
可以多次修改，按 q 退出。

#### mm(memory modify (auto-incrementing address))


#### mw(memory write (fill))

- `mw[.b .w .l] {address} {value} {count}`



#### cp

- `cp[.b .w .l] {source} {target} {count}`

DRAM 中复制，或者NOR FLASH向DRAM复制。


### 网络操作

在网络操作前，先要联网，用环境变量设置一些信息
```
=> setenv ipaddr 10.0.0.11
=> setenv ethaddr 88:b2:77:40:8e:48
=> setenv netmask 255.255.255.0
=> setenv gatewayip 10.0.0.1
=> setenv serverip 10.0.0.22
```

- `ping`
- `nfs`

主要是从网络上下载文件到 DRAM 中。如编译好的 linux 内核加载到 RAM 的 0x80800000 上

- `nfs 80800000 192.168.1.201:/home/xym/ws_linux/kernel/zImage`

### mmc sd 卡操作

- `mmc list`
  - 列出可选的 mmc 设备
- `mmc rescan`
  - 扫描mmc设备
- `mmc dev 1`
  - 切换设备1
  - 如果切换设备1的分区2 `mmc dev 1 2`
- `mmc info`
  - 查看设备信息
- `mmc part`
  - 查看分区情况
  - 分区0，存放uboot，未格式化，所以看不到
  - 分区1，存放 linux 镜像和设备树
  - 分区2，存放根文件系统
- `mmc read addr blk# cnt`
  - 按块读取到 DRAM 中
  - `mmc dev 1 0`
  - `mmc read 80800000 600 10`


### FAT 文件系统操作

- fatinfo
- fatls
- fstype
- fatload
- fatwrite


### ext4 文件系统操作

指令类似

### boot 操作

最核心的功能。

- `bootz`
- `bootm`
- `boot`

启动 linux 核前，先要将镜像加载到 DDR 中，如果用到设备树的话也要加载到 DDR 中。

可以从 EMMC、NAND、中复制到 DDR 中，也可以通过 nfs、tftp 复制到 DDR 中。最终只要 DDR 中有这些东西就行。

bootz 用来启动 zImage，命令格式

- `bootz [addr [initrd[:size]] [fdt]]`
  - addr: 镜像在 DDR 中的地址
  - initrd: initrd文件在 DDR 中的地址，不使用的话用 `-` 代替
  - fdt: 设备树在 DRAM 中的地址


nfs 网络启动
```
nfs 80800000 192.168.1.201:/home/home/ws_linux/kernel/zImage
nfs 83000000 192.168.1.201:/home/home/dtb/imx6ull-14x14-emmc-7-1024x600-c.dtb
bootz 80800000 - 83000000
```

mmc 启动
```
fatload mmc 1:1 80800000 zImage
fatload mmc 1:1 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb
bootz 80800000 - 83000000
```


bootm 和 bootz 类似。

boot 命令会读取环境变量 bootcmd 来启动系统。即启动命令的集合。

```
setenv bootcmd 'tftp 80800000 zImage; tftp 83000000 imx6ull-14x14-emmc-7-1024x600-c.dtb;
bootz 80800000 - 83000000'
saveenv
boot
```

```
setenv bootcmd 'fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000 imx6ull-14x14-
emmc-7-1024x600-c.dtb; bootz 80800000 - 83000000'
savenev
boot
```

uboot 倒计时结束，执行的就是 bootcmd 中的启动命令。


这时候在启动内核时会遇到下面的错误
```
Kernel panic – not Syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```


### 其他常用命令

- `reset`
  - 复位
- `go`
  - 跳转指定地址执行
  - `go addr [arg...]`
- `run`
- `mtest`


go 命令，可以编译裸机程序，然后 nfs 挂载到 DDR 中，使用此命令运行。uboot 初始化好了 IVT 等，直接就能运行。

run 用来运行定义在环境变量中的命令。如 `run bootcmd`

