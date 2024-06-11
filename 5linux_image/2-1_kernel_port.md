---
sort: 6
---
# kernel 新板适配


## 厂商 kernel 测试


顶层 makefile 指定架构和编译器
```
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

得到evk对应的 kernel 和 dtb。uboot 引导测试一下。

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

基于官方的 evk 修改，

添加开发板配置文件，修改 dtb 的 makefile，重新编译即可


## 开发板适配

### CPU 主频修改

### emmc 驱动适配

### 网络驱动适配



