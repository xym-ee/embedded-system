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


## 启动流程

`arch/arm/lib/vector.S` 中的 `_start` 是上电的入口。第一条指令 `b reset` ，相当于复位中断。



