---
sort: 3
---
# 镜像构建



## 烧写系统

### windows

windows 下 使用 NXP 提供的 mfgtool 向开发板烧写系统。此工具先向板上的 DDR 下载一个 linux，然后用这个 linux 完成后面的烧写工作。期间通过串口输出调试信息。

### ubuntu

向 SD 卡烧写一个 linux，从 sd 卡启动 linux，远程 ssh 上去，里通过执行脚本把系统烧写到 mmc 或者 nand 里。






## 镜像构建流程

所有的代码部分结束后，要开始编译打包了，这里给出最后的操作步骤，先体验一下流程。


工具准备

```
sudo apt install make git gcc-arm-none-eabi gcc bison flex libssl-dev dpkg-dev lzop libncurses5-dev
sudo apt install gcc-arm-linux-gnueabihf vim

```

### 1.uboot


```bash
# 1.获得 uboot 源码
git clone -b ebf_v2020_10_imx https://gitee.com/Embedfire/ebf_linux_uboot


# 2.编译 emmc 版本 uboot，生成配置文件
sudo make ARCH=arm CROSS_COMPILE=arm-none-eabi- mx6ull_fire_mmc_defconfig

# 3.根据配置文件编译 uboot
sudo make ARCH=arm CROSS_COMPILE=arm-none-eabi-

# 清除生成的文件 sudo make distclean

# 生成需要的文件
arm-none-eabi-objcopy --gap-fill=0xff  -j .text -j .secure_text -j .secure_data -j .rodata -j .hash -j .data -j .got -j .got.plt -j .u_boot_list -j .rel.dyn -j .binman_sym_table -j .text_rest -j .dtb.init.rodata -j .efi_runtime -j .efi_runtime_rel -O binary   u-boot u-boot-nodtb.bin
```


### 2.kernel


```bash
# 1.获得 linux kernel 源码
git clone -b ebf_4.19.35_imx6ul https://github.com/Embedfire/ebf_linux_kernel.git

# 2.内核配置
make menuconfig KCONFIG_CONFIG=arch/arm/configs/npi_v7_defconfig ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

# 3.根据配置文件编译 uboot，可以配置并行线程数
make ARCH=arm npi_v7_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j8

# 清除生成的文件 make mrproper
```

- 编译得到的 zImage 内核在 `arch/arm/boot` 目录下
- 设备树在 `arch/arm/boot/dts` 目录下
  - 分为 emmc 版本 imx6ull-mmc-npi.dtb 
  - 以及 nand 版本 imx6ull-nand-npi.dtb


### 3.根文件系统构建






