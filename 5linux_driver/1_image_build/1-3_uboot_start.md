---
sort: 3
---
# u-boot 启动流程分析

使用 vscode 远程访问虚拟机的 uboot 工程文件夹

## vscode 工程设置

屏蔽和工程无关的



## 工程目录

- `api/` uboot 提供的硬件无关的接口
- `arch/` 架构相关的代码
  - `arch/arm/cpu/armv7` A7、A9芯片
  - `arch/arm/cpu/armv8` 手机上的芯片 64 位
  - `arch/arm/cpu/u-boot.lds` 整个工程的链接脚本
  - `arch/arm/dts` 设备树
  - `arch/arm/imx-common` 恩智浦芯片通用
- `board/` 开发板相关
  - `freescale` imx 开发板相关
- `cmd/` uboot 中使用的命令的实现
- `common/` 
- `config/` 所有支持的**开发板**的配置文件
- `disk/` 磁盘相关
- `doc/` 文档，
- `drivers/` 驱动
- `dts/` 设备树
- `fs/` uboot支持的一些文件系统
- `include/`
- `lib/`
- `net/` 一些网络相关命令的实现
- `post/` 上电自检
- `.config` 执行 make xxx_deconfig 后生成的配置参数
- `.uboot***.cmd` 一些命令，用来生成最终的 uboot

和做 uboot 移植密切相关的是 board 文件夹，与 config 文件夹。

编译出来有一个带 elf 文件头的 u-boot 文件，u-boot.bin 是编译出来的二进制格式的可执行文件，对于 nxp 的芯片，还需要添加文件头如 dcd ivt，打包成 .imx 给imx芯片使用。

## 顶层 makefile


