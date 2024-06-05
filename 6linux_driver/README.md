---
sort: 5
---
# linux 驱动开发

完整的基于 linux 的产品开发过程

- 1.开发环境
  - Linux 开发主机
  - 串口终端调试工具(开发板控制台)
  - NFS 服务(传输文件)
- 2.bootloader
  - 根据开源的代码修改芯片
  - 编译烧录
- 3.linux kernel
  - 根据芯片供应商提供的源码修改
- 4.建立根文件系统
- 5.添加设备驱动程序
- 6.开发应用程序


## 开发板

使用正点原子 imx6ull-mini 开发板，8GB eMMC，512 MB DDR。

<figure>
    <img src="./1_image_build/images/3.png" width=250>
    <figcaption>开发板</figcaption>
</figure>


## 开发环境

ubuntu 的任意版本，debian 等，基于 linux 的，应该都可以。

### 工具链

- [Linaro GCC 4.9-2017.01](https://releases.linaro.org/components/toolchain/binaries/latest-7/arm-linux-gnueabihf/)
- [Linaro GCC 最新](https://releases.linaro.org/components/toolchain/binaries/4.9-2017.01/arm-linux-gnueabihf/)

下载后解压，一般放在 `/usr/local/arm` 目录中

还需要把路径导出的环境变量中，在 `/etc/profile` 中新增一行

```bash
export PATH=$PATH:/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin
```

或者在相应的终端工具启动执行文件里新增脚本，都可以的。

安装依赖库
```bash
sudo apt install lsb-core lib32stdc++6
```

如果是一个全新安装的系统，需要安装所有用到的东西

```bash
sudo apt install make gcc-arm-linux-gnueabihf gcc bison flex libssl-dev dpkg-dev lzop vim
```


### NFS 服务

主机安装

- `sudo apt install nfs-kernel-server`
- `sudo vim /etc/exports` 配置要共享的文件夹，增加配置项
  - `/home/xym/ws_linux *(rw,sync,no_root_squash)`
    - `/home/xym/ws_linux` 目录
    - `*` 所有网段，也可设置为 10.0.0.0/24 指定网段
    - `rw` 可读可写
    - `sync` 同步缓存
    - `no_root_squash` 访问者给 root 权限
- `sudo /etc/init.d/nfs-kernel-server restart` 重启一下 nfs 服务
- `showmount -e` 可以看到挂载的共享目录

开发板挂载共享文件系统
- `mount -t nfs 10.0.0.10:/home/xym/ws_linux /mnt`
- `mount -t nfs -o nolock,nfsvers=3 10.0.0.10:/home/xym/ws_linux /mnt`


### tftp 服务

uboot里用来加载 内核等到 DDR 中

- `sudo apt install xinetd`
- 若无`/etc/xinetd.conf`文件，新建一个，内容在后面
- `sudo apt install tftp-hpa tftpd-hpa`
- 配置共享文件夹 `sudo vim /etc/default/tftpd-hpa`


```
# Simple configuration file for xinetd
#
# Some defaults, and include /etc/xinetd.d/

defaults
{

# Please note that you need a log_type line to be able to use log_on_success
# and log_on_failure. The default is the following :
# log_type = SYSLOG daemon info

}

includedir /etc/xinetd.d
```


## 一些源码的下载地址


- [i.MX软件和开发工具](https://www.nxp.com.cn/design/software/embedded-software/i-mx-software:IMX-SW)

内核编译

```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- imx_v7_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- all -j16
```

vscode 远程 ssh 的环境变量，可以手动设置 `set PATH $PATH /usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/` ，拼接一个 gcc 的路径上去。


## 桌面版 linux 使用串口控制台

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



## 学习路线

应用开发，比如多线程、网络开发，shell 脚本，基本的 linux 使用之类的，放到计算机的学习笔记里，这里只记录和嵌入式强相关的。

野火的开发板为实验板。

- [野火i.MX6ULL Linux开发板资料下载链接合集](https://doc.embedfire.com/products/link/zh/latest/linux/ebf_i.mx6ull.html)
- [野火EBF6ULL 硬件资料](https://doc.embedfire.com/linux/imx6/hardware/zh/latest/index.html)
- [6ULL开发板开发文档](https://doc.embedfire.com/products/link/zh/latest/linux/ebf_i.mx6ull_doc.html)
  - [开发板快速使用手册](https://doc.embedfire.com/linux/imx6/quick_start/zh/latest/index.html)
  - [Linux基础与应用开发](https://doc.embedfire.com/linux/imx6/linux_base/zh/latest/index.html)
  - [Linux驱动开发](https://doc.embedfire.com/linux/imx6/driver/zh/latest/index.html)
  - [Linux镜像构建与部署](https://doc.embedfire.com/lubancat/build_and_deploy/zh/latest/index.html#)


传统的linux的学习路线
- linux + c 进阶
- arm 裸机开发
- linux 移植(boot,kernel,文件系统)
- linux 驱动开发
- linux 应用开发
- 项目实战

很系统，周期也很长。

基础很重要。linux 内核使用的是 GNU C ，和 C99 还是有区别的。此外写单片机时的面向过程的思维，如果还用这个思路去研究内核代码，也会很难懂。




## 烧系统








