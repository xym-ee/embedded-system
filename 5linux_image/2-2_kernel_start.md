---
sort: 7
---
# kernel 启动流程

- `/arch` 架构相关
  - `/arch/arm/boot/zImage` 编译出的内核镜像
  - `/arch/arm/boot/dts` 设备树
- `/block` 块设备相关
- `/crypto` 各种加密算法
- `/Documentation` 各种文档
- `/driver` 驱动
- `/firmware` 有些外设或模块需要
- `/fs` 文件系统相关
- `/include` 头文件
- `/init` 初始化相关
- `/ipc` 进程间通信
- `/kernel` 内核相关
- `/lib` 库
- `/mm` 内存管理相关算法、机制实现
- `/net` 网络协议
- `/sample` 简单的示例代码
- `/script` 各种脚本
- `/security` 安全相关
- `/sound` 音频相关的，包含驱动
- `/usr` 
- `/virt` 虚拟化相关
- `Kconfig` menuconfig 用到的
- `Makefile` 顶层的 
- `vmlinux` 


做嵌入式 linux 开发，关注 boot 里的东西。还有参考现成驱动 driver 里的东西。老的 uboot 用 uImage 镜像。




## 启动流程

内核链接脚本 `arch/arm/kernel/vmlinux.lds` 里，可以找到 `ENTRY(stext)` 指定了内核入口，这个标识符定义在 `arch/arm/kernel/head.S` 中。

linux 内核启动之前的要求
- 关闭 MMU
- 关闭 D-Cache
- I-Cache
- 需要准备的参数
  - r0 = 0
  - r1 = machine nr (机器ID)
  - r2 = atage 或者是 设备树的地址


最终调用定义在 `init/main.c` 里的 `start_kernel()` 函数来启动内核，这个函数调用了相当多的东西，最后调用了 `rest_init()` 函数，此函数会调用 `kernel_thread(kernel_init, NULL, CLONE_FS);` 创建 init 内核进程，此进程 PID 为 1。

init 进程一开始为内核进程，此进程会在后面根文件系统中查找名为 `init` 的程序，此程序处于用户态，通过运行此程序，init进程从内核态转到用户态。

之后还会创建 kthread 内核进程，PID 为 2 ，负责所有内核进程的调度和管理。

kernel_thread 中传入的第一个参数便是进程入口，此函数也定义 `init/main.c` 中。此进程中，首先看看有没有 Uboot 传入要执行的 init 的地址参数。如果没有的话，后面尝试去找 `/sbin/init`  `/etc/init` `/bin/init` `/sbin/sh`  启动起来。如果什么东西都没有，那就 kernel panic 了。










