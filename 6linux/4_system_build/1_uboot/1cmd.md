---
sort: 1
---
# uboot 命令

为了方便，学习 uboot 期间可以把 uboot 烧到 SD 卡中启动。

SD 卡插到 imxdownload 中，和裸机下载程序一样。比较方便。

## 启动 log

```
U-Boot 2020.10-g92bbb671 (Feb 10 2022 - 02:36:31 +0000)

CPU:   Freescale i.MX6ULL rev1.1 792 MHz (running at 396 MHz)
CPU:   Industrial temperature grade (-40C to 105C) at 41C
Reset cause: POR
Model: Freescale i.MX6 UltraLiteLite 14x14 EVK Board
Board: MX6ULL 14x14 EVK
DRAM:  512 MiB
MMC:   FSL_SDHC: 0, FSL_SDHC: 1
Loading Environment from MMC... OK
In:    serial
Out:   serial
Err:   serial
Net:   eth1: ethernet@20b4000 [PRIME]Could not get PHY for FEC0: addr 2

Hit any key to stop autoboot:  0
Unknown command 'lhf' - try 'help'
switch to partitions #0, OK
mmc1(part 0) is current device
loading [mmc 1:1] /uEnv.txt ...
2584 bytes read in 13 ms (193.4 KiB/s)
Importing environment from mmc ...
loading vmlinuz-4.19.35-imx6 ...
10138912 bytes read in 459 ms (21.1 MiB/s)
loading imx6ull-mmc-npi.dtb ...
38529 bytes read in 69 ms (544.9 KiB/s)
5164702 bytes read in 242 ms (20.4 MiB/s)
debug: [console=ttymxc0 root=/dev/mmcblk1p2 rw rootfstype=ext4 rootwait coherent_pool=1M net.ifnames=0 vt.global_cursor_default=0] ...
debug: [bootz] ...
Kernel image @ 0x80800000 [ 0x000000 - 0x9ab520 ]
## Flattened Device Tree blob at 83000000
   Booting using the fdt blob at 0x83000000
   Using Device Tree in place at 83000000, end 8303cfff

Starting kernel ...
```

可以看出许多信息
- CPU信号、主频
- 开发板型号
- DRAM 大小
- MMC，emmc 和 sd 卡都算是 mmc，会显示两个
- 环境变量就是一些字符串，保存到 mmc 的一个位置，如果没保存 crc 校验失败，是使用默认的环境变量
- 标准输入标准输出标准错误设置到串口
- 切换到 #0 分区，




## 基本信息

- `help`
- `help [具体命令]`
- `bdinfo`
- `printenv`
- `version`



```
=> bdinfo
boot_params = 0x80000100
DRAM bank   = 0x00000000
-> start    = 0x80000000
-> size     = 0x20000000
flashstart  = 0x00000000
flashsize   = 0x00000000
flashoffset = 0x00000000
baudrate    = 115200 bps
relocaddr   = 0x9ff9b000
reloc off   = 0x1879b000
Build       = 32-bit
current eth = ethernet@20b4000
ethaddr     = (not set)
IP addr     = <NULL>
fdt_blob    = 0x9ef8fd70
new_fdt     = 0x9ef8fd70
fdt_size    = 0x00009160
lmb_dump_all:
    memory.cnt             = 0x1
    memory.size            = 0x0
    memory.reg[0x0].base   = 0x80000000
                   .size   = 0x20000000

    reserved.cnt           = 0x1
    reserved.size          = 0x0
    reserved.reg[0x0].base = 0x9ef8eb6c
                     .size = 0x1071494
arch_number = 0x00000000
TLB addr    = 0x9fff0000
irq_sp      = 0x9ef8fd60
sp start    = 0x9ef8fd50
Early malloc usage: 58c / 2000
```

含义
- boot 参数存放地址 0x80000100
- DDR 的起始地址 0x80000000
  - 有的板子会配置成两个 bank，两个不连续的地址空间
- 串口波特率
- 各种地址，先不关注


## 环境变量操作

- `printenv`
  - 有很多。关注 bootcmd 和 bootargs
- `setenv` / `saveenv`

设置环境变量

比如设置boot延时时间。

- `setenv bootdelay 5`
- `saveenv`

对于比较长的环境变量，带空格的，要加上字符串引用

- `setenv bootcmd 'console=ttymxc0,115200 root=/dev/mmcblk1p2 rootwait rw'`

设置一个控制台串口，以及挂载根文件系统的设备。

新建一个没有的环境变量也用此命令

- `setenv xymenv xym`

删除环境变量，即给环境变量一个空的值

- `setenv xymenv`


## 内存操作

具体的操作，可以看 uboot 中的帮助

- `md`
- `nm`
- `mm`
- `mw`
- `cp`
- `cmp`

### md(memory display)

查看指定位置的内存值

- `md[.b .w .l] {address} {length}`
  - `md.b 80000000 64`
  - `md.w 80000000 128`
  - `md.l 80000000 256`

### nm()

修改指定位置的值

- `nm[.b .w .l] {address}`
  - `nm.b 80000000`
  - `nm.w 80000000`
  - `nm.l 80000000`


```
=>nm.b 80000000
80000000: 00 ? 55
80000000: 55 ? q
```
可以多次修改，按 q 退出。

### mm(memory modify (auto-incrementing address))


### mw(memory write (fill))

- `mw[.b .w .l] {address} {value} {count}`



### cp

- `cp[.b .w .l] {source} {target} {count}`

DRAM 中复制，或者NOR FLASH向DRAM复制。


## 网络操作

- `ping`
- `nfs`

主要是从网络上下载文件到 DRAM 中。如编译好的 linux 内核加载到 RAM 的 0x80800000 上

- `nfs 80800000 192.168.1.201:/home/xym/ws_linux/kernel/zImage`

## mmc sd 卡操作

- `mmc list`
  - 列出可选的 mmc 设备
- `mmc rescan`
  - 扫描mmc设备
- `mmc dev 1`
  - 切换设备1
  - 如果切换设备1的分区2 `mmc dev 1 2`
- `mmc info`
  - 查看设备信息
- `mmc part`
  - 查看分区情况
  - 分区0，存放uboot，未格式化，所以看不到
  - 分区1，存放 linux 镜像和设备树
  - 分区2，存放根文件系统
- `mmc read addr blk# cnt`
  - 按块读取到 DRAM 中
  - `mmc dev 1 0`
  - `mmc read 80800000 600 10`


## FAT 文件系统操作

- fatinfo
- fatls
- fstype
- fatload
- fatwrite


## ext4 文件系统操作

指令类似

## boot 操作

最核心的功能。

- `bootz`
- `bootm`
- `boot`

启动 linux 核前，先要将镜像加载到 DDR 中，如果用到设备树的话也要加载到 DDR 中。

可以从 EMMC、NAND、中复制到 DDR 中，也可以通过 nfs、tftp 复制到 DDR 中。最终只要 DDR 中有这些东西就行。

bootz 用来启动 zImage，命令格式

- `bootz [addr [initrd[:size]] [fdt]]`
  - addr: 镜像在 DDR 中的地址
  - initrd: initrd文件在 DDR 中的地址，不使用的话用 `-` 代替
  - fdt: 设备树在 DRAM 中的地址


nfs 网络启动
```
nfs 80800000 192.168.1.201:/home/home/ws_linux/kernel/zImage
nfs 83000000 192.168.1.201:/home/home/dtb/imx6ull-14x14-emmc-7-1024x600-c.dtb
bootz 80800000 - 83000000
```

mmc 启动
```
fatload mmc 1:1 80800000 zImage
fatload mmc 1:1 83000000 imx6ull-14x14-emmc-7-1024x600-c.dtb
bootz 80800000 - 83000000
```


bootm 和 bootz 类似。

boot 命令会读取环境变量 bootcmd 来启动系统。即启动命令的集合。

```
setenv bootcmd 'tftp 80800000 zImage; tftp 83000000 imx6ull-14x14-emmc-7-1024x600-c.dtb;
bootz 80800000 - 83000000'
saveenv
boot
```

```
setenv bootcmd 'fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000 imx6ull-14x14-
emmc-7-1024x600-c.dtb; bootz 80800000 - 83000000'
savenev
boot
```

uboot 倒计时结束，执行的就是 bootcmd 中的启动命令。


这时候在启动内核时会遇到下面的错误
```
Kernel panic – not Syncing: VFS: Unable to mount root fs on unknown-block(0,0)
```


## 其他常用命令

- `reset`
  - 复位
- `go`
  - 跳转指定地址执行
  - `go addr [arg...]`
- `run`
- `mtest`




