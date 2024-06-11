---
sort: 2
---
# u-boot 开发板适配

参考芯片厂商的 SDK。

## 厂商 SDK 的 uboot 测试

首先编译一下。

NXP 的配置，mx6ull_14x14_evk_emmc_defconfig

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- mx6ull_14x14_evk_emmc_defconfig
make V=1 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j16
```

同样的，也可以把上面的命令写进一个脚本。

也可以在顶层 Makefile 里直接给传入的参数赋值。

对于一个开发板，要运行 uboot ，必须要支持的东西
- DDR
- UART
- 支持的不同的启动介质
  - SD 卡
  - MMC
  - NAND Flash


这些设备东西如果和官方的一样，那么芯片原厂的 uboot 是能在自己的开发板上跑起来的。只是有些地方会提示有问题。

烧写 uboot 到 SD 卡


可以看到，屏幕背点亮了，但是有些异常。NXP 配的屏幕是 480x272 的屏幕。

此外，查看 uboot 日志，首先能看到日志说明串口驱动没问题。

```
U-Boot 2016.03 (Jul 06 2023 - 20:10:53 +0800)

CPU:   Freescale i.MX6ULL rev1.1 69 MHz (running at 396 MHz)
CPU:   Industrial temperature grade (-40C to 105C) at 37C
Reset cause: POR
Board: MX6ULL 14x14 EVK
I2C:   ready
DRAM:  512 MiB
MMC:   FSL_SDHC: 0, FSL_SDHC: 1
*** Warning - bad CRC, using default environment

Display: TFT43AB (480x272)
Video: 480x272x24
In:    serial
Out:   serial
Err:   serial
switch to partitions #0, OK
mmc0 is current device
Net:   Board Net Initialization Failed
No ethernet found.
Normal Boot
Hit any key to stop autoboot:  0
switch to partitions #0, OK
mmc0 is current device
switch to partitions #0, OK
mmc0 is current device
reading boot.scr
** Unable to read file boot.scr **
reading zImage
** Unable to read file zImage **
Booting from net ...
No ethernet found.
No ethernet found.
Bad Linux ARM zImage magic!
=>
```

可以看到，DRAM 识别出来了，Net 初始化失败，mmc 通过命令测试驱动正常，SD 必然正常。

所以，接下来移植这套代码，要把不正常的驱动改正常。即在官方开发板修改使得支持自己的开发板。


## 适配自己的开发板

### 1.开发板 config 文件

`configs` 中都是已经有的板的配置文件，在这里以官方板为基础添加一个新的。

基于 `mx6ull_14x14_evk_emmc_defconfig` 来修改，可以改成自己的开发板的名字。这里改成 `mx6ull_14x14_mini_emmc_defconfig`，对此文件要做一些修改。

```
CONFIG_SYS_EXTRA_OPTIONS="IMX_CONFIG=board/freescale/mx6ullevk/imximage.cfg,MX6ULL_EVK_EMMC_REWORK"
CONFIG_ARM=y
CONFIG_ARCH_MX6=y
CONFIG_TARGET_MX6ULL_14X14_EVK=y
CONFIG_CMD_GPIO=y
```

这个配置文件使用了一些配置文件。整个复制一份，进行适配，

修改配置文件为


### 2.配置头文件


### 3.板级配置文件


### 4.Kconfig


### 编译测试


## LCD 适配


### 1.LCD IO


### 2.LCD 参数


ATK4384 显示屏参数
- HSPW(thp) hsync_len：48
- HBP(thb) left_margin：88
- HFP(thf) right_margin：40
- VSPW(tvp) vsync_len：3
- VBP(tvb) upper_margin：32
- VFP(tvf) lower_margin：13
- CLOCK：31 MHz


修改 mx6ull_mini.c

```c
struct display_info_t const displays[] = {
    {
        .bus = MX6UL_LCDIF1_BASE_ADDR,
        .addr = 0,
        .pixfmt = 24,
        .detect = NULL,
        .enable	= do_enable_parallel_lcd,
        .mode	= {
            .name			= "TFT4384",
            .xres           = 800,
            .yres           = 480,
            .pixclock       = 32258,
            .left_margin    = 88,   //HBPD
            .right_margin   = 40,   //HFPD
            .upper_margin   = 32,   //VBPD
            .lower_margin   = 13,   //VFBD
            .hsync_len      = 48,   //HSPW
            .vsync_len      = 13,   //VSPW
            .sync           = 0,
            .vmode          = FB_VMODE_NONINTERLACED
        }
    }
};
```

### 3.uboot环境变量

修改 `include/configs/mx6ull_mini.h` 里的 `panel` 环境变量为 `TFT4384` 

编译烧录测试。

## 网络驱动修改

网络方案。

IMX6ULL 内部有以太网 MAC 外设，需要外接一个 PHY 芯片。

在内部无 MAC 的芯片中，使用外接的 MAC+PHY ，如 DM9000 有一个类似 SRAM 的接口。W5500 使用 SPI 接口实现通信。

内部 MAC 的速度会快相当多，内部 MAC 会集成 DMA。具体的可以取看手册。

NXP EVK 使用的 PHY 为 KSZ8081，我手里这块板为 SR8201F，所以 uboot 启动会提示网络初始化失败。

MDIO 作为 PHY 的管理接口，用两根线实现与芯片通信，SDIO 和 SDC。


### 1.引脚

ENET2_RESET


### 2.器件ID




## boot 测试

uboot 最终目的，启动 kernel，

### 从 EMMC 启动

现在的 uboot 在 SD 卡中。要去启动 MMC 中的 kernel，kernel 已经烧写在 mmc 了，要确定这里有内核。

先确定mmc 中有内核 `fatls mmc 1:1`

```
mmc dev 1                                   #切换当前设备为 mmc
fatls mmc 1:1                               #查看此分区的文件
fatload mmc 1:1 80800000 zImage
fatload mmc 1:1 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb
bootz 80800000 - 83000000
```

启动后，内核可以启动起来，但是有点小问题，还需要设置环境变量，指定根文件系统的位置。

```
setenv bootargs 'console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw'
setenv bootcmd 'mmc dev 1; fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000
imx6ull-alientek-emmc.dtb; bootz 80800000 - 83000000;'
```


可以把这个命令设置为自动运行的启动命令。
```
setenv bootcmd 'mmc dev 1; fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb; bootz 80800000 - 83000000;'
```

此外，还可以在屏幕上也启动一个控制台。
 
setenv bootargs 'console=tty1 console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw'


### 网络启动

```
tftp 80800000 zImage
tftp 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb
tftp 83000000 imx6ull.dtb
bootz 80800000 - 83000000
```



```
tftp 80800000 zImage
tftp 83000000 imx6ull-alientek-emmc.dtb
bootz 80800000 - 83000000
```

```
setenv bootcmd 'tftp 80800000 zImage; tftp 83000000 imx6ull-alientek-emmc.dtb; bootz 80800000 - 83000000;'
```
