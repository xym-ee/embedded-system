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

或者直接写一个脚本。

得到evk对应的 kernel 和 dtb。uboot 引导测试一下。

```
tftp 80800000 zImage
tftp 83000000 imx6ull-14x14-evk.dtb
bootz 80800000 - 83000000
```

可以设置  bootargs 为
```
console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw
```

或者就直接
```
console=ttymxc0,115200
```

内核成功引导了，提示 kernel panic 后面再解决。


## 添加开发板配置文件

基于官方的 evk 修改，

添加开发板配置文件，修改 dtb 的 makefile，重新编译即可


## 开发板适配

### CPU 主频修改

### emmc 驱动适配

### 网络驱动适配



