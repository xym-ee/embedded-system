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

`arch/arm/cpu/u-boot.lds` 是整个 uboot 的链接脚本，在编译完成后，根目录下也有一个 lds，这个是由 cpu 目录里生成的。

`board/freescale/mx6ullevk/` 是需要关注的，这份代码是从 NXP 下载的，使用这个芯片的话也是基于这个去修改。

uboot 各种架构芯片都可以进行适配，对于具体的开发板的配置，存放在 `configs` 里，这是 uboot 的默认配置文件的文件夹，文件名都为 `xxxxx_defconfig`

移植的时候关注
- `board`
- `configs`


根目录的文件

执行完 `make xxx_defconfig` 后，胜过 `.config` 文件，保存所有的配置信息，这些配置信息最终决定了哪些代码被最终编译。

`.xxx.cmd` 是命令。

`Kconfig` 是图形化配置界面的文件。更多的东西，在根目录下的 README 有完整、详细的介绍。

最重要的，`Makefile` ，分析一个项目的时候，从顶层开始分析。

编译后，会有好多个 `u-boot` 的文件，
- `u-boot` ELF 格式的镜像
- `u-boot.bin` 二进制格式可执行镜像
- `u-boot.imx` 添加 ivt dcd 的NXP专用文件
- `u-boot.lds` 链接脚本
- `u-boot.map` 映射文件
- `u-boot.srec` S-Record 格式镜像文件


## 顶层 makefile

makeflie 定义了如果编译工程，分析可以大概知道工程的主旨结构。

V=1 或 V=0 时的实现。

在获取主机架构获取和主机系统之前，并没有做编译相关的事情，一些指令
- `uname`
- `sed` 替换或删除文本
- `tr` 转换或删除字符
  - `echo "hello world" | tr 'a-z' 'A-Z'`

获取了主机架构和秒架构后，可以指定编译器了，后面紧接着制定了配置项保存文件 `.config`，并导出给子 makefile


在 makefile 中，还引用了一些东西，用 `include` 指令

随后定义了所有工具链中的工具，然后导出许多变量，重点关注 ARCH CPU BOARD VENDOR SOC CPUDIR BOARDDIR 这些变量，直接分析 makefile 可能不好分析，定义一个伪目标，直接 ehco 出来看看

```
echovar:
  @echo ARCH = $(ARCH)
  @echo CPU = $(CPU)
  @echo BOARD = $(BOARD)
  @echo VENDOR = $(VENDOR)
  @echo SOC = $(SOC)
  @echo CPUDIR = $(CPUDIR)
```

这些内容是在 `.config` 中配置的，中间经过了 `config.mk` ，


### make xxx_defconfig

重点分析执行 `make xxx_defconfig` 时发生了什么。

执行这个指令的时候，按照 make 工具的含义，是以 `xxx_defconfig` 为目标，这里用到了通配符，在顶层 makefile 里，匹配 `%defconfig` 这一目标，

```makefile
%config: scripts_basic outputmakefile FORCE
	$(Q)$(MAKE) $(build)=scripts/kconfig $@
```

FORCE 为总是执行(规则为空，没有任何依赖，类似于 clean，所以总会被重新执行生成，这也是makefile中的一个常用用法)，此目标依赖的是 scripts_basic outputmakefile 这两个目标。

其中 scripts_basic 目标的规则为 

```
scripts_basic:
	$(Q)$(MAKE) $(build)=scripts/basic
	$(Q)rm -f .tmp_quiet_recordmcount
```


$(Q) 为是否显示完整的命令行，$(MAKE) 展开后为 make ，$(build) 在 Kbuild.include 中定义 

### make 

执行这条指令，默认目标，

```makefile
# That's our default target when none is given on the command line
PHONY := _all
_all:
```


## uboot 链接脚本

分析启动流程，首先去看链接脚本，找到整个编译出的可执行文件的入口，找到第一行程序在什么位置。

查看 u-boot.lds 可以看到整个可执行文件 ENTRY(_start) 的入口地址为 `_start`，那么就要去看看这个标识符的位置了。

```
 . = 0x00000000;
 . = ALIGN(4);
 .text :
 {
  *(.__image_copy_start)
  *(.vectors)
  arch/arm/cpu/armv7/start.o (.text*)
  *(.text*)
 }
```

lds 的 text 段最开始，`. = 0` 会被重新配置为87800000。整个text段的开始，是__image_copy_start 这个符号，这个位置也是 87800000，.vectors 这个段，也是这个地址开始，这个段名是自己写的，中断向量表在最前面，之后还是启动文件 start.o 中的代码段。后面的代码段就随便链接。


代码段就结束了。

一直到后面有个 __image_copy_end，这两个符号中间就是整个镜像的内容。

之后为 .rel_dyn_start 段，rel 段，


一些关注的段，以及标识符，这些段的起始地址和结束地址后面都会用到。


## 启动流程：架构初始化

`arch/arm/lib/vector.S` 中的 `_start` 是上电的入口。第一条指令 `b reset` ，相当于复位中断。reset 函数在 `arch/arm/cpu/armv7/start.S` 中定义。这也是链接脚本中能看到的紧跟在 `.vectors` 段后的要被链接的代码段所在的文件。

`reset` 调用了 `save_boot_params` 函数，此函数调用`save_boot_params_ret` ，又回到 reset 了，预留了接口，可能有的芯片需要保存一下启动参数。总之是要读取 cpsr 寄存器，来判断 CPU 所处的模式，并将处理器模式设置为 SVC 模式，关闭 FIQ 和 IRQ 中断。

设置向量表重定位，需要把 SCTLR 寄存器中 V 设置为 0，才可以重定位。取 _start 这个地址。之后设置 CP15 寄存器，Cache、MMU、TLB 等。

之后执行 cpu_init_crit ，配置关键寄存器和初始化，这里调用了 lowlevel_init，lowlevel_init 定义在 `arch/arm/cpu/armv7/lowlevel_init.S` 中，这个函数主要用来设置栈指针和 r9 寄存器。

- 设置 sp 指向 CONFIG_SYS_INIT_SP_ADDR=0X0091FF00 ，即芯片内部的 IRAM 地址和大小，
- 设置 SP 8字节对齐，即清除低 3 bit
- 设置 gd (global data) 为 248 Byte
- 将 SP 地址保存在 r9 寄存器中
- ip lr 入栈
- 跳转 s_init
- ip lr 出栈，lr 赋值给 pc

这部分就是把 SP 指针指向芯片内部 128K 空出 256字节*248字节 之后的地址。r9 在后面比较重要。。

s_init 函数要做的是初始化时钟，但是mx系列芯片并不需要在这里配置。因此直接返回就好了。然后又返回到 reset 这边了、这时候架构初始化就完成了，可以进入到板级初始化了。调佣 _main

此函数定义在 `arch/arm/lib/crt0.S` 中


lowlevel_init 做的事情
- 让系统能够执行到 `board_init_f`
- 无全局数据或bss
- 没有栈



## 启动流程：板级初始化


_main 中做的事情
- 1. 初始化基本的C运行环境并调用 `board_init_f` 基本外设初始化
  - 全局数据可以用
  - 堆栈在片内 SRAM 中
  - bss不可用，无法使用全局变量和静态变量，只能用堆栈上的东西和全局数据
- 2. 重定位 uboot 代码
- 3. 设置完整的运行环境，并调用 `board_init_r` 完成所有外设初始化
  - 完整的环境
  - C 语言所有需要的东西都准备完毕，


_main 执行的流程
- 设置栈指针
- 调用 `board_init_f_alloc_reserve`
  - 留出这个阶段 malloc 内存区域
- 调用 `board_init_f_init_reserve` 
- 调用 `board_init_f(0)`

- 重定位代码 `relocate_code`
- 重定位向量表 `relocate_vectors`
- 配置完整的 C 运行环境 `c_runtim_cpu_setup`
- 清除 bss 段
- 跳转 `board_init_r` 后面所有的程序都为 C 语言实现





Board Initialisation Flow:
--------------------------

This is the intended start-up flow for boards. This should apply for both
SPL and U-Boot proper (i.e. they both follow the same rules).

Note: "SPL" stands for "Secondary Program Loader," which is explained in
more detail later in this file.

At present, SPL mostly uses a separate code path, but the function names
and roles of each function are the same. Some boards or architectures
may not conform to this.  At least most ARM boards which use
CONFIG_SPL_FRAMEWORK conform to this.

Execution typically starts with an architecture-specific (and possibly
CPU-specific) start.S file, such as:

	- arch/arm/cpu/armv7/start.S
	- arch/powerpc/cpu/mpc83xx/start.S
	- arch/mips/cpu/start.S

and so on. From there, three functions are called; the purpose and
limitations of each of these functions are described below.

lowlevel_init():
	- purpose: essential init to permit execution to reach board_init_f()
	- no global_data or BSS
	- there is no stack (ARMv7 may have one but it will soon be removed)
	- must not set up SDRAM or use console
	- must only do the bare minimum to allow execution to continue to
		board_init_f()
	- this is almost never needed
	- return normally from this function

board_init_f():
	- purpose: set up the machine ready for running board_init_r():
		i.e. SDRAM and serial UART
	- global_data is available
	- stack is in SRAM
	- BSS is not available, so you cannot use global/static variables,
		only stack variables and global_data

	Non-SPL-specific notes:
	- dram_init() is called to set up DRAM. If already done in SPL this
		can do nothing

	SPL-specific notes:
	- you can override the entire board_init_f() function with your own
		version as needed.
	- preloader_console_init() can be called here in extremis
	- should set up SDRAM, and anything needed to make the UART work
	- these is no need to clear BSS, it will be done by crt0.S
	- must return normally from this function (don't call board_init_r()
		directly)

Here the BSS is cleared. For SPL, if CONFIG_SPL_STACK_R is defined, then at
this point the stack and global_data are relocated to below
CONFIG_SPL_STACK_R_ADDR. For non-SPL, U-Boot is relocated to run at the top of
memory.

board_init_r():
	- purpose: main execution, common code
	- global_data is available
	- SDRAM is available
	- BSS is available, all static/global variables can be used
	- execution eventually continues to main_loop()

	Non-SPL-specific notes:
	- U-Boot is relocated to the top of memory and is now running from
		there.

	SPL-specific notes:
	- stack is optionally in SDRAM, if CONFIG_SPL_STACK_R is defined and
		CONFIG_SPL_STACK_R_ADDR points into SDRAM
	- preloader_console_init() can be called here - typically this is
		done by defining CONFIG_SPL_BOARD_INIT and then supplying a
		spl_board_init() function containing this call
	- loads U-Boot or (in falcon mode) Linux















## 启动流程总览

### XIP 设备

XIP 的概念。芯片上有 CPU、SRAM、Flash只读ROM、还有各种外设控制器。

芯片一通电就必须要有指令来执行，无论外挂的东西是什么样的，arm 内核必定从 0x0 开始取第一条指令。

从硬件上来说，芯片内部的要有数据总线和地址总线连接的存储设备，这就是 XIP 设备，execute in place，即代码存在这个设备里，代码可以直接被CPU读取执行。

对于 NAND Flash 来说，芯片上是 flash 控制器，CPU 需要通过控制器来间接访问 flash。这种情况下，做不到一上电就直接访问。flash 控制器是一个比较复杂的设备，需要一系列复杂的指令通过控制器读 flash 的第一条指令。所以flash 里的第一条指令没法在一上电执行。

所以 flash 里的第一条指令距离一上电执行的第一条指令已经过去好多了。所以支持 NAND SD 这些设备启动的芯片，芯片里必定有 boot ROM，必须要有一个 ROM 设备，提供给芯片一上电来执行，把 NAND flash 复制到 RAM ，然后跳转取执行。

boot ROM 的作用：硬件初始化，把程序从非 XIP 设备复制到 RAM，从RAM里执行代码。

所以支持多种设备启动的芯片一般都有拨码开关来设置启动的设备，bootROM读取设置，然后做对应的处理。比如 NAND FLASH ，初始化控制器，搬到RAM，跳转执行。NOR flash，直接取执行。

### uboot 拷贝

支持非 XIP 设备启动芯片里必定有 boot ROM，一般来说还有片内 SRAM，此外还有外接巨大容量的 DDR，DDR需要配置初始化后才能当做内存使用。boot ROM 一般也是 C 语言开发的，既然是 C 语言，就有栈的问题。完全用汇编写代码的话，就不用栈了，然后也完全不用 RAM 了。所以芯片内部的 RAM 是给 boot ROM 提供栈的。boot ROM 最终目的是把非 XIP 设备上的程序读进片内 RAM 里。boot ROM 不知道如何初始化不同型号的 DDR，所以这部分代码需要用户去实现，所以这部分代码必定会被读入片内 SRAM，然后执行.

片内 SRAM 很贵，最大也就几百k，如果说用户的程序很大，这时候该如何处理？比如mx6ull 的片内 RAM 128KB，uboot 编译出来大概300K出头，这时候的解决方案：
- boot ROM 只复制前 n K ，前 n k 要保证初始化 DDR 并复制整个程序到 DDR，然后跳转执行。在程序设计的时候就要做好这方面的考虑
- 用户程序拆成两段代码，SPL代码和应用程序。SPL(secondary program loader) 二级加载，

boot ROM 为一级加载，将 SPL 程序读到 RAM 后运行，SPL 实现二级加载读取整个用户程序到 DDR。


注意：直接将 uboot 拷贝至其他地方后，函数调用、全局变量引用可能会出问题。

代码的地址最终是有连接程序决定的，如果 SPL 代码把程序正好复制到了 DDR 上的链接的地址，那么所有的东西都好说，各个调用都没问题，相对跳转和绝对跳转都没有关系链接地址和实际地址都能对得上。所以说一个程序“应该”位于链接地址的位置，如果复制的时候不在链接地址上，需要处理一下
- 把自己复制到应该在的位置
- 修改代码，自己改自己改成正确的位置

uboot 采用位置无关码来处理该类问题（简单说采用相对地址寻址，而不是采用绝对地址寻址，并且重定位后需要将Label+offset）。在使用 ld 进行链接的时候使用选项”- pie” 生成位置无关的可执行文件。具体为.rel.dyn段。

### 启动流程


带 SPL 程序的启动流程
- boot ROM 从 flash 中读 SPL 程序到片内 SRAM
- SPL 完成 DDR 初始化，并从 flash 中读 uboot 到 DDR 中，跳转执行
- uboot 重定位，把自己挪到比较靠上的地方，为 kernel 留出空间

无 SPL 的启动流程，功能比较强大的芯片bootROM能完成更多的功能，6ull就是这样的，flash里只有uboot，头部有一些DDR的配置信息
- bootROM 初始化 DDR，并把 uboot 复制到 DDR 中
- 跳转到 uboot 运行
- uboot 重定位







