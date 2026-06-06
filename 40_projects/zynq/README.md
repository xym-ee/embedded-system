---
sort: 7
---
# ZYNQ - FPGA


## ZYNQ 介绍

可编程逻辑器件 PLD (Programmable Logic Device)

上古时期，数字电路生产出来功能就确定了，如果想自己设计一个专用数字电路，就要使用可以修改内部连接的集成电路。
- PLD 内部电路的结构可以通过程序来修改
- 写入PLD的程序可以擦除重写

常用可编程器件：
- CPLD：Complex Programmable Logic Device，复杂可编程逻辑器件
- FPGA：Field Programmable Gate Array，现场可编程门阵列

这两个的差别：电路结构不同

CPLD内部是基于**乘积项**的与或逻辑阵列

FPGA内部是基于**查找表**(Look Up Table)的 CLB 阵列

ZYNQ = ARM + FPGA

## ZYNQ XC7Z020CLG400-2

7020

## Vivado 设计套件

### 简介

Vivado 可以实现 FPGA 不放呢的设计和开发，管脚和时许约束，编译和仿真，实现 RTL 到比特流的设计。

<https://china.xilinx.com/support/download.html>

只能用于 Xilinx 的高端芯片。Altera 芯片使用 Quartus。

开发全系列的软件 ISE，虽然已经停止更新了。

Vivado 支持 Block Design、Verilog、VHDL 等多种设计输入方法，内嵌综合器，仿真器。

仿真也可以用 Modelsim 第三方的仿真软件。

Vivado 继承了 HLS(High Level Synthesis)工具，实现直接使用 C, C++ 对 FPGA 器件直接编程，不同手动创建 RTL ，通过高层次综合生成 HDL 级的 IP 核。

### 开发流程

一般的开发过程

新建工程 -> 设计输入 -> 分析与综合 -> 约束输入 -> 设计实现 -> 生成和下载比特流

跟着做做就会了。


### 调试

Vivado 工具集成了逻辑分析仪，添加 ILA 核和 VIO 核实现硬件调试，通过 JTAG 接口和 PC 连接。

ILA(Integrated Logic Analyzer)，监控内部信号和端口信号，消耗存储资源，数据存放在 DRAM 里。

VIO(Virtual Input/Output)，实时监控和驱动逻辑内部信号和端口信号。






