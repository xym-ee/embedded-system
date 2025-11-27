

安装好 EB，

K312 的主频 120MHz，

时钟配置在 Mcu 模块中

Gernel 中使能常用的 api

有个选项卡是 McuClockSettingConfig

Mcu 里面比较重要的是时钟配置，都是和 mcu 相关的

选项卡里配置的是

与手写代码最大的区别是做一个配置上的检查，配置的话还是需要去看手册，不然每个选项是什么不清楚，脱离不了数据手册。

大部分都是固定的配置。

后期用的比较多的是外设时钟参考点


LPUART3
TX PTD2 GPIO98
RX PTD3 GPIO99


ConfigTimeSupport 中 Post Build Variant Used 勾选


