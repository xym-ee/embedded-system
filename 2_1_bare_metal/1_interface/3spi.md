---
sort: 3
---
# SPI 接口

SPI（Serial Peripheral Interface，串行外设接口）是一种高速、全双工、同步通信总线，常用于短距离通讯，主要应用于 EEPROM、FLASH、实时时钟、AD 转换器、还有数字信号处理器和数字信号解码器之间。SPI 一般使用 4 根线通信，如下图所示：

<img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/device/spi/figures/spi1.png" width=350>

- MOSI –主机输出 / 从机输入数据线（SPI Bus Master Output/Slave Input）。
- MISO –主机输入 / 从机输出数据线（SPI Bus Master Input/Slave Output)。
- SCLK –串行时钟线（Serial Clock），主设备输出时钟信号至从设备。
- CS –从设备选择线 (Chip select)。也叫 SS、CSB、CSN、EN 等，主设备输出片选信号至从设备。

主设备通过控制 CS 引脚对从设备进行片选，一般为低电平有效。任何时刻，一个 SPI 主设备上只有一个 CS 引脚处于有效状态，与该有效 CS 引脚连接的从设备此时可以与主设备通信。

SPI 是同步通信，速度可以做到很快。只要从机能忍，那么通信速率就是由主机输出的频率决定的。

比如 STM32F407 最高时钟频率(SYSCLK) 为 168MHz，SPI1 挂在 APB2 总线上，APB2 的最高时钟频率为 82 MHz，SPI 外设中也有自己的分频器。分频系数可取 2、4、8、16、32、64、128 和 256 等。最小取 2，那么最大的通信频率就是 42MHz。

通常 SPI 通信速率在 1 - 50 MHz 。

此外，还有扩展板
- Dual SPI Flash: 对于 SPI Flash 而言全双工并不常用，可以发送一个命令字节进入 Dual 模式，让它工作在半双工模式，用以加倍数据传输。这样 MOSI 变成 SIO0（serial io 0），MISO 变成 SIO1（serial io 1）,这样一个时钟周期内就能传输 2 个 bit 数据，加倍了数据传输。
- Quad SPI Flash: 与 Dual SPI 类似，Quad SPI Flash增加了两根 I/O 线（SIO2,SIO3），目的是一个时钟内传输 4 个 bit 数据。


