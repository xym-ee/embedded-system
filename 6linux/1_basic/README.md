---
sort: 2
---
# 嵌入式 linux 基础

- 开发板基本使用
  - shell 操作硬件
  - 嵌入式 linux 环境熟悉
  - 纯 CLI 操作一些东西
- 系统编程工具
  - 交叉编译工具
  - 远程终端工具
  - 代码编辑器
  - NFS
- 镜像烧写与生成
  - uboot 编译
  - kernel 编译
  - 设备树
  - 根文件系统
  - 镜像打包
- 镜像相关的开发调试(uboot里的工具) 
  - 内核网络启动
  - 设备树网络启动
  - 根文件系统网络挂载

## 开发板参数

### 野火 IMX6ULL

- RAM DDR3 512MB
- eMMC 8GB


启动方式
- bit[7:0] nand启动 0101 1010
- bit[7:0] usb启动  0010 0101

## sd 卡烧录镜像

- [etcher](https://www.balena.io/etcher/)


镜像下载链接：
- [野火的镜像](https://doc.embedfire.com/lubancat/os_release_note/zh/latest/index.html)


## usb 烧写镜像

mftools 工具，cfg.ini 配置烧写信息



