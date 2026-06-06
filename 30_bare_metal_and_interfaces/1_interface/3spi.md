---
sort: 3
---
# SPI 接口


## 简介

SPI（Serial Peripheral Interface，串行外设接口）是一种高速、全双工、同步通信总线，常用于短距离通讯，主要应用于 EEPROM、FLASH、实时时钟、AD 转换器、还有数字信号处理器和数字信号解码器之间。SPI 一般使用 4 根线通信，如下图所示：

<img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/device/spi/figures/spi1.png" width=350>

- MOSI –主机输出 / 从机输入数据线（SPI Bus Master Output/Slave Input）。
- MISO –主机输入 / 从机输出数据线（SPI Bus Master Input/Slave Output)。
- SCLK –串行时钟线（Serial Clock），主设备输出时钟信号至从设备。
- CS –从设备选择线 (Chip select)。也叫 SS、CSB、CSN、EN 等，主设备输出片选信号至从设备。

主设备通过控制 CS 引脚对从设备进行片选，一般为低电平有效。任何时刻，一个 SPI 主设备上只有一个 CS 引脚处于有效状态，与该有效 CS 引脚连接的从设备此时可以与主设备通信。

SPI 是同步通信，速度可以做到很快，通常 SPI 通信速率在 1 - 50 MHz 。只要从机能忍，那么通信速率就是由主机输出的频率决定的。


## 通信原理

SPI 主设备和从设备都有一个串行移位寄存器，主设备通过向它的 SPI 串行寄存器写入一个字节来发起一次传输。

<img src="https://ask.qcloudimg.com/http-save/yehe-8201782/904ef0fbbf4cff09aeed50103b7974e8.png" width=350>


SPI 硬件原理：**主设备（Master）与从设备（Slave）之间通过移位寄存器（Shift Register）的同步交换（Shift + Exchange）来完成数据通信。**

SPI 的所有行为都能从“移位寄存器交换”推导。

从设备的时钟由主设备的 SCLK 提供，MOSI MISO 基于此脉冲完成数据传输

在每个CLK MISO 和 MOSI 都在同时有数据传送吗

“写操作”也会“收到垃圾数据”

半双工的使用方式第一段纯 MOSI 写命令，第二段纯 MISO 读数据，但本质上第一段 MISO 依然会传送数据，只不过忽略。第二段主机任然必须发送 dummy bytes，产生时钟让从机数据移出。

例如
```
MOSI: CMD, ADDR, DUMMY  
MISO:  XX,  XX,  DATA...
```

硬件上决定了 SPI 无法，只读只写。

基于这个原理，SPI Master 无法从硬件层面检测到 Slave 是否存在。即使没有从机，Master 的 SPI transfer 会看起来“正常完成”，并返回一串固定值（0 或 0xFF），但从机根本不存在。SPI 主机并不需要收到从机的响应，也无法知道对方是否“真实存在”。不同于 IIC 的 ACK 机制。






此外，还有扩展板
- Dual SPI Flash: 对于 SPI Flash 而言全双工并不常用，可以发送一个命令字节进入 Dual 模式，让它工作在半双工模式，用以加倍数据传输。这样 MOSI 变成 SIO0（serial io 0），MISO 变成 SIO1（serial io 1）,这样一个时钟周期内就能传输 2 个 bit 数据，加倍了数据传输。
- Quad SPI Flash: 与 Dual SPI 类似，Quad SPI Flash增加了两根 I/O 线（SIO2,SIO3），目的是一个时钟内传输 4 个 bit 数据。





