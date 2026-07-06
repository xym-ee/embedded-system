
# ESP32-S3

这里记录 ESP32-S3 和 ESP-IDF 的学习与产品级应用开发实践。

ESP32 不是传统意义上只用来点灯的 MCU，它更像一个带 Wi-Fi、BLE、Flash、PSRAM、RTOS 和完整 SDK 的小型 IoT 系统。学习 ESP-IDF 时，不只是学习几个外设 API，而是在学习一套厂商提供的嵌入式系统框架。

ESP-IDF 编程指南：

https://docs.espressif.com/projects/esp-idf/zh_CN/v6.0/esp32s3/index.html

## 学习路线

- [ESP-IDF 框架总览](./01_esp_idf_overview.md)：先知道 ESP-IDF 提供了什么，以及它和裸机、RTOS、Arduino 的关系。
- [ESP32-S3 启动流程](./02_startup.md)：从 ROM、bootloader、分区表到 `app_main`，理解第一行应用代码之前发生了什么。
- [ESP-IDF 构建系统](./03_build_system.md)：理解 `idf.py`、CMake、Kconfig、`sdkconfig` 和工程目录。
- [ESP-IDF 组件机制](./04_components.md)：把组件看成 ESP-IDF 里的软件边界，学习如何组织自己的代码。
- [ESP-IDF 中的 FreeRTOS](./05_freertos_in_idf.md)：任务、队列、定时器、同步机制，以及它们在 IDF 中的用法。
- [事件循环与消息机制](./06_event_loop.md)：理解 `esp_event`、回调、消息队列和系统事件。
- [应用层状态机](./07_app_state_machine.md)：把产品行为建模为状态、事件和动作。
- [产品级应用层架构](./08_product_app_architecture.md)：沉淀自己的业务层、服务层、驱动适配层和配置管理。
- [存储、分区表与 OTA](./09_storage_partition_ota.md)：NVS、文件系统、分区规划、固件升级。
- [Wi-Fi、BLE 与 IoT 接入](./10_wifi_ble_iot.md)：联网、配网、MQTT、设备接入和云端协议。

## 简介

ESP32 是 Wi-Fi MCU。可以理解为 MCU、Wi-Fi、蓝牙三合一。

ESP8266 是更早的低成本 Wi-Fi 芯片。ESP32-S3 则强化了 AIoT 方向，常见配置包括双核 Xtensa LX7、较大的片外 Flash 和 PSRAM。

它适合做：

- IoT 设备
- 联网控制器
- Wi-Fi / BLE 网关
- 小型人机交互设备
- AIoT 入门实验

它的特点也很明显：开发速度快，系统能力强，但底层细节有一部分被 ESP-IDF 框架封装了。对学习来说，既要会用，也要逐步拆开看。

## 开发方式

ESP32 常见开发方式：

- ESP-IDF：官方框架，C/C++，适合系统级开发和产品级工程。
- Arduino：上手快，适合快速实验。
- MicroPython：适合脚本化控制和教学实验。

这里主要记录 ESP-IDF。

ESP-IDF 提供：

- 工具链
- 构建、烧录、监视工具
- FreeRTOS
- 外设驱动
- Wi-Fi / BLE 协议栈
- 分区表、NVS、文件系统、OTA
- 组件机制和组件注册表

## 环境记录

Linux 下可以安装 EIM，也就是 ESP-IDF Installation Manager，通过 EIM 安装 ESP-IDF。

```sh
# apt source
echo "deb [trusted=yes] https://dl.espressif.com/dl/eim/apt/ stable main" | sudo tee /etc/apt/sources.list.d/espressif.list

sudo apt update

# GUI 和 CLI
sudo apt install eim

# CLI
sudo apt install eim-cli
```

SDK 和工具链准备好以后，可以用 IDE 或命令行构建项目。命令行最接近原始工具链，适合学习框架内部做了什么。

```sh
cd 到 project

idf.py set-target esp32s3
idf.py menuconfig

idf.py build

idf.py -p COM16 flash

idf.py -p COM16 monitor
```

`Ctrl + ]` 退出串口监视。

## VS Code

可以安装 ESP-IDF 的 VS Code 扩展。

直接 `printf("hello world")` 能跑起来，但是中间隐藏了非常多的细节，而且编译出来的固件也很大。这里后续要重点追踪：

- 工程是怎么被 CMake 组织起来的
- IDF 默认链接了哪些组件
- FreeRTOS 是如何进入 `app_main` 的
- 启动代码、分区表、bootloader 和应用固件之间是什么关系

## 常用配置记录

基础配置：

- CPU：240 MHz
- SPI Flash：QSPI 80 MHz，16 MB
- PSRAM：Octal mode
- 常见模组：N16R8，16 MB Flash，8 MB PSRAM
- FreeRTOS：`TICK_RATE_HZ` 可以设置为 1000

分区表用于划分外挂 SPI Flash。

```csv
# ESP-IDF Partition Table
# Name,   Type, SubType,  Offset,   Size,     Flags
nvs,      data, nvs_keys, 0x9000,   0x6000,
phy_init, data, phy,      0xf000,   0x1000,
factory,  app,  factory,  0x10000,  0x1F0000,
vfs,      data, fat,      0x200000, 0xA00000,
storage,  data, spiffs,   0xC00000, 0x400000,
```

后续需要结合 OTA、NVS、文件系统和产品数据持久化来重新设计分区表。
