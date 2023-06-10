---
sort: 6
---
# 嵌入式 linux 开发


## linux 开发流程

- 1.准备开发环境
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

## 学习路线

- linux 驱动
- linux 移植
- 

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


## 开发前准备

交叉编译环境。

嵌入式处理器，arm 架构，性能相比x86桌面处理器还是有差距，因此在 x86 上将源代码编译为 arm 架构上的可执行文件。

通过局域网，将 pc 上的工作目录以 nfs 形式挂载到开发板。

首先，开发主机，工具链，在 x86 平台，一些开发用到的和机器相关的东西

- gcc
- binutils 工具集
  - readelf
  - objdump
- glibc 库

## NFS 

主机

sudo apt install nfs-kernel-server



/home/embedfire/workdir 192.168.0.0/24(rw,sync,all_squash,anonuid=998,anongid=998,no_subtree_check)



