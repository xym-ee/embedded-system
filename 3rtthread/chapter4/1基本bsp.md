---
sort: 1
---
# 基本 bsp 

只包含 GPIO 与 FinSH 功能。

复制模板，改成自己的项目名。

## 1. CubeMX 配置芯片初始化代码

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

## 2. 芯片时钟初始化与内存配置

### board.c 时钟

复制 CubeMX 生成的 main 里的 void SystemClock_Config(void) 函数到 board.c里。

### board.h 内存参数

```c
#define STM32_FLASH_SIZE              (1024 * 1024)
#define STM32_SRAM_SIZE               128
```

## 4. Kconfig 配置

芯片型号和系列


## 5. IDE 相关配置

### linker_scripts

### SConscript

### MDK5 模板

