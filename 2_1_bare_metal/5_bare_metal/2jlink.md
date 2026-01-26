# 下载和调试


## 下载

使用 jlink 下载

安装好 jlink linux 版本。

https://kb.segger.com/UM08001_J-Link_/_J-Trace_User_Guide

https://kb.segger.com/J-Link_Commander

安装好后，下载的步骤

```sh
JLinkExe

connect stm32f407zg

swd

speed 默认
```

连接成功后下载的通用步骤
```
h
loadfile xxxx.elf
r
g
```

关于 elf 文件，带语义的程序，

hex 带地址的文本格式，

bin 纯数据。无上下文的字节流


## 偏硬件的调试

使用 jlink 

一些常用的指令。

```
loadfile    下载 ELF / HEX
loadbin     下载 BIN（需地址）
r           reset
g           go（继续运行）
h           halt（停住 CPU）
```

调试指令

regs

看 CPU 寄存器信息

读内存，寄存器
mem8 / mem16 / mem32 

```
mem32 0x08000000, 4     // 看向量表
mem32 0x40023800, 1     // 看 RCC
mem32 0x20000000, 8     // 看 SRAM
```


w8 w16 w32 写内存
```
w32 0x40023830, 0x1     // 写 RCC 寄存器
```


setpc 强行转转执行

```
setpc 0x08000000
g
```

单步执行
step
stepi 

speed 速度控制

speed 1000


从手动交互到自动执行一些简单任务

```
device STM32F407ZG
if SWD
speed 4000
loadfile rtthread.elf
r
g
exit
```

从交互到自动化脚本

```
JLinkExe flash.jlink
```

90% 的问题，只需要下面这些指令

```
loadfile
loadbin
r
g
h
regs
mem32
connect under reset
setpc
speed

```




jlink commander，调试器前端，偏硬件的 gdb

gdb 有符号，偏软件的 jlink/



## 

MCU 场景下，gdb 并不直连硬件，调试结构

```
arm-none-eabi-gdb
        │
        ▼
JLinkGDBServer   （J-Link 提供）
        │
        ▼
J-Link  →  STM32
```


需要做的事情，起一个 jlink GDB Server

然后用 gdb 连上。


```
JLinkGDBServer \
  -device STM32F407ZG \
  -if SWD \
  -speed 4000 \
  -port 2331
```

工具链自带了 gdb，但用的比较多的是，gdb-multiarch


调试的前提，elf 带调试信息，可以用 file xxx.elf 查看

启动 gdb

gdb-multiarch rtthread.elf

指定架构

set architecture arm

连接到 jlink gdb server

target remote :2331

复位 

monintor reset 

b main 

continue 或 c 继续

monintor 指令透传通道，原样发给 gdb server，在这个场合由 jlink 去解析


