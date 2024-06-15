---
sort: 1
---
# bsp 制作的相关只是

## STM 32 芯片 CubeMX 配置芯片初始化代码

在 `board/CubeMX_Config` 里启动 `CubeMX_Config.ioc`

- 选择芯片型号，关注 RAM 与 Flash 大小
- Pinout & Configuration 选项卡
  - System Core 关注 sys 里的调试接口与 rcc 时钟模块
  - Connectivity 里打开 uart
  - (可选)配置其他外设
- Clock Configuration
  - 配置时钟树
- Project Manager
  - Project
    - Name: CubeMX_Config
    - Location: rt-thread\bsp\stm32\stm32fxxxxxx\board
    - Toolchain/IDE: MDK-ARM

其他默认即可，生成代码后，移动 Core 里的 Src 和 Inc 到外面，关注 MDK-ARM 里 `.s` 文件的名字。

### board.c 时钟

复制 CubeMX 生成的 main 里的 void SystemClock_Config(void) 函数到 board.c里。

### board.h 内存参数

```c
#define STM32_FLASH_SIZE              (1024 * 1024)
#define STM32_SRAM_SIZE               128
```

## NXP 芯片MCUXpresso Config Tools 

## env 工具

- KConfig
- menuconfig


## 分散加载文件

C 语言的编译过程中会生成 `.o` 文件，此文件为可重定位的可执行文件，即这个文件已经是二进制的机器码了，可以使用 objdump 工具来反汇编查看了，但是








