---
sort: 4
---
# IIC 接口

I2C（Inter Integrated Circuit）总线是一种半双工、双向二线制同步串行总线。I2C 总线传输数据时只需两根信号线，一根是双向数据线 SDA（serial data），另一根是双向时钟线 SCL（serial clock）。SPI 总线有两根线分别用于主从设备之间接收数据和发送数据，而 I2C 总线只使用一根线进行数据收发。

I2C 和 SPI 一样以主从的方式工作，不同于 SPI 一主多从的结构，它允许同时有多个主设备存在，每个连接到总线上的器件都有唯一的地址，主设备启动数据传输并产生时钟信号，从设备被主设备寻址，同一时刻只允许有一个主设备。如下图所示：

<img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/device/i2c/figures/i2c1.png" width=500>

I2C 总线数据传输的格式 

<img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/device/i2c/figures/i2c2.png" width=500>

IIC 通信是可以用软件模拟出来的，只要按照约定的时序来软件编程向总线发送信号即可。






