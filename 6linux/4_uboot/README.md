---
sort: 4
---
# uboot


## 参考资料





## uboot 简介

uboot(Universal Boot Loader) 是一个综合的裸机程序。现在的 uboot 已经支持液晶屏、网络、USB 等高
级功能。


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


## source code 在哪里？

uboot 的源码

- u-boot 项目
  - <https://github.com/u-boot/u-boot>
  - 支具体的某款芯片的驱动不完善，但是不断有人会贡献代码，修复bug
- 芯片厂商适配的 uboot
  - <https://github.com/nxp-imx/uboot-imx>
  - 芯片厂商会基于某个版本的 uboot，深度适配自己的 evk 评估板，如 [i.mx6ull evk](https://www.nxp.com.cn/design/development-boards/i-mx-evaluation-and-development-boards/evaluation-kit-for-the-i-mx-6ull-and-6ulz-applications-processor:MCIMX6ULL-EVK) 板
- 二级开发板厂商的 uboot
  - 如野火、正点原子、飞凌等公司开发板的 uboot
  - 开发板厂商会参考芯片厂商的 evk ，定制自己的开发板，在芯片厂商 uboot 的基础上适配开发板的功能


所以 uboot 移植，实际上是适配自己的板子，真正的最复杂的移植部分厂商的工程师已经解决掉了。


## 源码编译

开发板厂商的源码解压缩，初次编译。

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- mx6ull_14x14_ddr512_emmc_defconfig
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


## 自动化脚本

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






