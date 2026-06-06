---
sort: 5
---
# pinctrl 和 gpio 子系统



- 设备树中添加节点，在 reg 属性中设置寄存器地址
- 驱动中获得 reg 的物理地址，完成映射
- 设置 GPIO
  - 复用功能设置
  - 电气属性设置
  - GPIO 方向设置


这个芯片是 NXP 的，对于 STM32 来说，也是类似的。因此 linux 内核针对 PIN 配置开发了 pinctrl 子系统。对于 GPIO 的配置开发了 gpio 子系统。

大多数SOC的pin都是可以复用的，


pin 子系统完成的工作
- 获取设备树中的 pin 信息
- 设置复用功能
- 设置电气属性

对于使用者，只需要在设备树中设置好某个 pin 的相关属性即可，剩下的工作全都由 pinctrl 子系统来完成。

```dts
iomuxc: iomuxc@020e0000 {
  compatible = "fsl,imx6ul-iomuxc";
  reg = <0x020e0000 0x4000>;
};
```

在不同开发板中，添加了更多属性

```dts
&iomuxc {
  pinctrl-names = "default";
  pinctrl-0 = <&pinctrl_hog_1>;
  imx6ul-evk {
    pinctrl_hog_1: hoggrp-1 {
      fsl,pins = <
        MX6UL_PAD_UART1_RTS_B__GPIO1_IO19     0x17059 /* SD1 CD */
        MX6UL_PAD_GPIO1_IO05__USDHC1_VSELECT  0x17059 /* SD1 VSELECT */
        MX6UL_PAD_GPIO1_IO09__GPIO1_IO09      0x17059 /* SD1 RESET */
      >;
    };
```

举例，pinctrl_hog_1 节点中，和热拔插有关的 PIN 集合。UART1_RTS_B 这个引脚作为 SD 卡的检测引脚。MX6UL_PAD_UART1_RTS_B__GPIO1_IO19 为宏定义，包含了寄存器的便宜地址以及值。

iomuxc 中的 compatible 属性为 "fsl,imx6ul-iomuxc"，可以在 kernel 源码全局搜索，在 `drivers/pinctrl/freescale/pinctrl-imx6ul.c` 中可以找到 of_device_id 中匹配到的值。因此 pinctrl-imx6ul.c 中完成 PIN 的配置工作。


## 设备树添加 Pinctrl 




## GPIO 子系统

pinctrl 将一个 PIN 设置好复用功能和电气属性，如果设置为 GPIO ，那么 linux 也提供 gpio 子系统。

- 初始化 GPIO
- 读写 API

只要在设备树中添加 GPIO 相关信息，就可以在驱动程序中使用 gpio 子系统的 API 来操作了。所有的设置过程都由内核实现。


## gpio api

对于驱动开发来说，设置好设备树后就可以使用 gpio 的 API 来操作了。一些常用的

- `int gpio_request(unsigned gpio, const char *label)`

申请一个 GPIO ，使用前一定要申请


