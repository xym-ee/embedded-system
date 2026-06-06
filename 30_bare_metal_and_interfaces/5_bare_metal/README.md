# 不使用 IDE 的裸机开发

用 gcc 编译器和数据手册，为微控制器（单片机）编程。更好地理解像 STM32Cube、Keil、 Arduino 和其他框架或 IDE 的工作原理。

一些涉及到的知识
- 存储和寄存器
- 中断向量表
- 启动代码
- 链接脚本
- 使用make进行自动化构建
- GPIO外设和闪烁LED
- SysTick定时器
- UART外设和调试输出
- printf重定向到UART
- 用Segger Ozone进行调试
- 系统时钟配置
- 实现一个带设备仪表盘的 web 服务器


## 环境

ubuntu

- gcc-arm-none-eabi
- make
- stlink-tools

```bash
sudo apt install make
sudo apt install stlink-tools
sudo apt install gcc-arm-none-eabi
```




