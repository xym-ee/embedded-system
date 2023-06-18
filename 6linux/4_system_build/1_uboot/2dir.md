---
sort: 2
---
# uboot 源码结构


- `api/` uboot 提供的硬件无关的接口
- `arch/` 架构相关的代码
  - `arch/arm/cpu/armv7` A7、A9芯片
  - `arch/arm/cpu/armv8` 手机上的芯片 64 位
  - `arch/arm/cpu/u-boot.lds` 整个工程的链接脚本
  - `arch/arm/dts` 设备树
  - `arch/arm/imx-common` 恩智浦芯片通用
- `board` 开发板相关
  - `freescale` imx 开发板相关
- `cmd` uboot 中使用的命令的实现
- `common` 
- `config` 所有支持的**开发板**的配置文件


