---
sort: 4
---
# rt-thread 设备驱动


- [STM32系列驱动介绍](https://www.rt-thread.org/document/site/#/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/STM32%E7%B3%BB%E5%88%97%E9%A9%B1%E5%8A%A8%E4%BB%8B%E7%BB%8D)


## STM32系列驱动介绍

在 RT-Thread 实时操作系统中，各种各样的设备驱动是通过一套 I/O 设备管理框架来管理的。设备管理框架给上层应用提供了一套标准的设备操作 API，开发者通过调用这些标准设备操作 API，可以高效地完成和底层硬件外设的交互。设备管理框架的结构如下图所示：

<figure>
  <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/figures/rt_device.png" width=350>
</figure>


使用 I/O 设备管理框架开发应用程序，有如下优点：

使用同一套标准的 API 开发应用程序，使应用程序具有更好的移植性
底层驱动的升级和修改不会影响到上层代码
驱动和应用程序相互独立，方便多个开发者协同开发


<figure>
  <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/figures/Peripheral.png" width=420>
</figure>

