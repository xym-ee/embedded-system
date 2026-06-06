

```sh
make distclean
make imx8mp-biomatic-board_defconfig
make menuconfig
make all
```


scp /home/m/linux-imx-biomatic/arch/arm64/boot/dts/freescale/imx8mp-biomatic-board.dtb root@10.10.10.16:/run/media/boot-mmcblk2p1/imx8mp-biomatic-board.dtb

scp /home/m/linux-imx-biomatic/arch/arm64/boot/Image root@192.168.0.16:/run/media/boot-mmcblk2p1/Image


手动设置和从 tftp 加载 kernel
```sh
# 设置网络信息
setenv ipaddr 10.10.10.11
setenv netmask 255.255.255.0
setenv gatewayip 10.10.10.1
setenv serverip 10.10.10.10   

tftp ${kernel_addr_r} Image
tftp ${fdt_addr_r} imx8mp-biomatic-board.dtb
setenv bootargs console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait rw
booti ${kernel_addr_r} - ${fdt_addr_r}
```





成功挂载，然后网络问题，


uboot 阶段，手动指定了，mac，但是不知道分配给了哪个网口。包括 ip ，

两个网口如如何选择的。正好插上了就能用？

然后进入 linux 以后，eth0 和 eth1 ，逻辑上的关系

eth0 的 mac 是居然我在 uboot 阶段的使用的，会想当然的认为 eth0 是要用的网卡

但是实际情况是 eth1 才是真正使用的


uboot 中的网络设备

```sh
u-boot=> net list
eth0 : ethernet@30be0000 00:04:9f:01:ba:03
eth1 : ethernet@30bf0000 00:04:9f:01:ba:04 active
```





一些启动方式

mmc 加载 kernel dtb 挂载 rootfs
```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait rw'
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} imx8mp-biomatic-board.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```


```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait rw'
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} imx8mp-biomatic-board.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```



mmc 加载 kernel dtb ，nfs 挂载 rootfs，调应用
```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/nfs nfsroot=10.10.10.20:/home/m/ws_linux/nfs,proto=tcp,nfsvers=3 rw ip=10.10.10.10:10.10.10.20:10.10.10.1:255.255.255.0::eth0:off'
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} OK8MP-C.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```


一些快捷的 boot 变量
```sh
run mmcargs;
mmc dev 2;
fatload mmc 2:1 ${kernel_addr_r} Image;
fatload mmc 2:1 ${fdt_addr_r} imx8mp-biomatic-board.dtb;
booti ${kernel_addr_r} - ${fdt_addr_r};

setenv boot_from_mmc 'run mmcargs; mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} imx8mp-biomatic-board.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'

```

```sh
setenv boot_from_tftp 'run mmcargs; tftp ${kernel_addr_r} ${image}; tftp ${fdt_addr_r} ${fdtfile}; booti ${loadaddr} - ${fdt_addr_r};'
```

```sh
setenv bootcmd 'run boot_from_tftp'
setenv bootcmd 'run boot_from_mmc'

```




引入 USB Path Mux 驱动并完成板级接入与默认模式调整

## 背景

当前板级 USB 路径切换最初通过 PCA6416 的 GPIO hog 在设备树中固定默认电平，虽然可以保证上电状态，但 GPIO 被静态占用，运行时无法切换模式，也不利于将 USB Path 作为一个系统能力进行统一管理。

Commit 1：引入 USB Path Mux 内核驱动
- 新增 usb_path_mux 内核驱动源码
- 补充对应的 Kconfig 与 Makefile，支持内核配置与编译
- 驱动基于 platform + device tree 方式工作：
  - 从 DTS 获取 GPIO 资源与默认模式
  - 将 USB 路径选择抽象为 mode (0..3)
  - 通过 sysfs 暴露统一控制接口

该提交完成了 USB Path Mux 作为板级功能驱动的基础实现。


Commit 2：板级接入与默认模式调整
- 将 USB Path Mux 默认模式调整为 mode=1，用于 i.MX8 A 核调试接口场景
- 移除 DTS 中 PCA6416 上 USB 相关无关代码



## 设计说明

本 MR 的核心目标不是功能扩展，而是一次分层设计优化：
- 将 USB 路径选择从 GPIO 电平控制提升为板级能力抽象
- 用户空间不直接操作 GPIO，仅通过语义化接口控制模式
- 设计思路与 LED、regulator 等内核子系统保持一致

有助于后续系统演进与统一管理。


## 影响范围

- 新增：drivers/misc/usb_path_mux.*
- 修改：相关 Kconfig / Makefile
- DTS：移除 USB 相关 GPIO hog 配置并接入驱动

对现有 USB 功能无破坏性影响。


