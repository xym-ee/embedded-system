---
sort: 6
---
# kernel 新板适配

设备树初步。

先调通能用，具体的驱动，原理后面再说。

## 厂商 kernel 测试

linux-imx-rel_imx_4.1.15_2.1.0_ga


顶层 makefile 指定架构和编译器，直接修改 252、253 行
```makefile
ARCH			?= arm
CROSS_COMPILE	?= arm-linux-gnueabihf-
```

指令编译

```
make distclean
make imx_v7_defconfig
make menuconfig
make all
```

在编译时，可能会遇到 /usr/bin/ld: scripts/dtc/dtc-parser.tab.o:(.bss+0x50): multiple definition of `yylloc'; scripts/dtc/dtc-lexer.lex.o:(.bss+0x0): first defined here 的问题。ubuntu22.04 自带的 gcc 为 11.4，换成 9.5 就可以正常编译内核了。

```bash
sudo apt install gcc-9 g++-9

# 后面的数字为赋予的优先级
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 1
sudo update-alternatives --install /usr/bin/++ g++ /usr/bin/g++-9 1

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 2
sudo update-alternatives --install /usr/bin/++ g++ /usr/bin/g++-11 2

#查看优先级，选择默认的编译器
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

得到 evk 对应的 kernel 和 `imx6ull-14x14-evk.dtb`。uboot 引导测试一下。

可以设置  bootargs 为
```
console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw
```

或者就直接
```
console=ttymxc0,115200
```

```
tftp 80800000 zImage
tftp 83000000 imx6ull-14x14-evk.dtb
bootz 80800000 - 83000000
```

内核成功引导了，提示 kernel panic 后面再解决。


## 添加开发板配置文件

基于官方的 evk 修改，一个默认配置文件，还有一个就是设备树。

在 `arch/arm/configs` 目录中，复制官方evk的配置文件，命名为自己的。

在 `arch/arm/boot/dts` 目录中，复制对应的设备树，命名为自己的，并修改 makefile 添加自己的。

添加开发板配置文件，修改 dtb 的 makefile，重新编译即可


## 开发板适配

### CPU 主频修改

### emmc 驱动适配

SD 是 4 线的，emmc 为 8线，但是 4 线也能用。

### 网络驱动适配

NXP EVK 使用的是 KSZ8081。

MAC+PHY，PHY 芯片为 SR8201F。

6ULL 芯片内部有以太网 MAC 外设，也即 ENET，内部 MAC+外部 PHY 实现。在一些无内部 MAC 的CPU中，使用DM9000方案，集成MAC+PHY，提供一个类似SRAM的接口，一般内部 MAC 都和专用 DMA，性能会高很多。

mini板上，ENET2，复位脚接到了 SNVS_TAMPER8

PHY 器件地址 0x01



