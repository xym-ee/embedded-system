
# imx8mp



evk 快速构建 ，使用 yocto


终端设置代理

```sh
export http_proxy="http://Clash:s2KRAnIe@192.168.1.2:7893"
export https_proxy="http://Clash:s2KRAnIe@192.168.1.2:7893"
```



安装依赖工具

```sh
sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xzutils zstd efitools
```


```sh
sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget zstd efitools
```

安装 repo 工具

```sh
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
# 放到 /bin 或某个环境变量的目录里
```


`imx-manifest` 是 NXP 官方用于管理 i.MX Linux BSP（Board Support Package）源码的“入口仓库”。它本身不包含代码，而是通过多个 `.xml` manifest 文件来描述 所有需要拉取的子仓库，并用 repo 工具统一管理。

NXP 的 BSP 依赖几十个仓库，且版本组合高度固定，如果用 submodule 会非常难管理。

```sh
# 创建工作目录
mkdir imx-yocto-bsp
cd imx-yocto-bsp

# 可能需要代理
# 初始化 repo 仓库，获得依赖关系
repo init -u https://github.com/nxp-imx/imx-manifest -b imx-linux-kirkstone -m imx-5.15.71-2.2.2.xml

# 拉取 yocto 工程源码，poky meta-imx kernel uboot
repo sync
```

```sh
# 执行后，自动切换到了 build 目录
DISTRO=fsl-imx-xwayland MACHINE=imx8mp-ddr4-evk source imx-setup-release.sh -b build

# 在 build 目录下构建
bitbake imx-image-multimedia
```

bitbake core-image-minimal




烧镜像，

NXP 提供了 UUU 工具，


使用 UUU 工具，连接 USB 到 PC，

```sh
uuu.exe -b emmc_all OK8MP-BOOT.bin okmx8mp-c-linux-fs.sdcard
```

这种方式下载的内容，

emmc 

- mmcblk2boot0
- mmcblk2boot1

mmcblk2
- mmcblk2p1 挂载到 /run/media/Boot-mmcblk2p1 格式 fat，存放 Image ，dtb
- mmcblk2p2 /




启动流程


- IMX8MP 内部 Rom Code，初始化栈，内部 OCRAM
- 读取配置的 boot 模式
- 搜索启动设备
- 加载 SPL 到 OCRAM 并跳转

Secondary Program Loader 已经是 u-boot 的代码了，做 4 件事
- 初始化时钟 CCM
- 初始化 DDR (LPDDR4)，关键
- 初始化必要的外设 (最起码能读存放 uboot 的介质)
- 加载 u-boot.bin 到 DDR 并跳转

在 boot 日志中可以看到两阶段启动。新版的 boot 命令做了很多嵌套，更健壮，并且没有设置 bootargs

```sh
bootcmd=run sr_ir_v2_cmd;run distro_bootcmd;run bsp_bootcmd
```


可以设置好传递给内核的 bootatgs 后手动去从 mmc 中加载 kernel 与 dtb 并启动

```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait rw'
mmc dev 2
fatload mmc 2:1 ${kernel_addr_r} Image
fatload mmc 2:1 ${fdt_addr_r} OK8MP-C.dtb
booti ${kernel_addr_r} - ${fdt_addr_r}
```

```sh
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} OK8MP-C.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```

/dev/mmcblk2p2 在 linux 启动后挂载到了根文件系统的 `/run/media/Boot-mmcblk2p1` 下，可以直接替换这里的 Image 和 dtb ，uboot 在启动后自动加载。



下一步，通过网络 tftp 加载 kernel 与 dtb，并挂载 nfs 根文件系统


```sh
=> setenv ipaddr 10.10.10.10
=> setenv ethaddr ea:55:ac:b3:de:8f
=> setenv netmask 255.255.255.0
=> setenv gatewayip 10.10.10.1
=> setenv serverip 10.10.10.20

saveenv
```




ubuntu 安装 tftp 服务，
```sh
sudo apt install tftpd-hpa
```

安装完成后修改配置文件，`/etc/default/tftpd-hpa`，设置 tftp 目录

```conf
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/home/m/ws_linux/tftp"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure"
```

```sh
# 重启 tftp 服务
sudo systemctl restart tftpd-hpa

# 查看 tftp 状态
sudo systemctl status tftpd-hpa
```


从网络加载，在开发板上操作
```sh
tftp ${kernel_addr_r} Image
tftp ${fdt_addr_r} devicetree.dtb
booti ${kernel_addr_r} - ${fdt_addr_r}
```

或者设置为 bootcmd

```sh
setenv bootcmd 'tftp ${kernel_addr_r} Image; tftp ${fdt_addr_r} devicetree.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```


安装 nfs 服务


添加作为 nfs 共享的文件夹

```sh
/home/m/ws_linux/nfs *(rw,sync,no_root_squash,no_subtree_check)
```


```sh
# 重新加载配置
sudo exportfs -ra

# 重启服务
sudo systemctl restart nfs-kernel-server

# 检查状态
sudo systemctl status nfs-kernel-server
```



指定从 nfs 挂载根文件系统

设置 bootargs

```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/nfs nfsroot=10.10.10.20:/home/m/ws_linux/nfs,proto=tcp,nfsvers=3 rw ip=10.10.10.10:10.10.10.20:10.10.10.1:255.255.255.0::eth0:off'
```




sudo mount -o loop,offset=134217728 okmx8mp-c-linux-fs.sdcard /mnt/rootfs




一些启动方式

mmc 加载 kernel dtb 挂载 rootfs
```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/mmcblk2p2 rootwait rw'
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} OK8MP-C.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```


mmc 加载 kernel dtb ，nfs 挂载 rootfs，调应用
```sh
setenv bootargs 'console=ttymxc1,115200 root=/dev/nfs nfsroot=10.10.10.20:/home/m/ws_linux/nfs,proto=tcp,nfsvers=3 rw ip=10.10.10.10:10.10.10.20:10.10.10.1:255.255.255.0::eth0:off'
setenv bootcmd 'mmc dev 2; fatload mmc 2:1 ${kernel_addr_r} Image; fatload mmc 2:1 ${fdt_addr_r} OK8MP-C.dtb; booti ${kernel_addr_r} - ${fdt_addr_r};'
saveenv
```






---

构建最小的 linux

uboot 和 kernel 是两个程序，使用飞凌的 uboot ，引导一个最小的 linux ，调试一些外设，增加驱动。









