

# ESP32-S3

ESP-IDF 编程指南

https://docs.espressif.com/projects/esp-idf/zh_CN/v6.0/esp32s3/index.html

## 简介

wifi BLE，AI 入门，适合 IoT，联网应用。

半黑盒，开发快速。

vscode，ESP-IDF，

基础，环境，工程，分区表，IDF 注册表，基础外设

网络，wifi



ESP32，wifi mcu。三合一 MCU + wifi + 蓝牙

ESP8266，最早的。

ESP32-S3 强化 AI 能力，AIoT，

双核 Xtensa，LX

## 开发

ESP-IDF，官方框架，C/C++，

Arduino，使用 Arduino IDE 上开发

Micro Python，

esp-idf，系统级驱动支持，全系列 esp 支持。物联网组件。构建、烧录与调试工具。

可以使用 idf.py 


linux 安装开发环境。

工具链 + sdk，

使用 


安装 EIM(ESP-IDF Installation Manager)，通过 EIM 安装 ESP-IDF

```sh

# apt source
echo "deb [trusted=yes] https://dl.espressif.com/dl/eim/apt/ stable main" | sudo tee /etc/apt/sources.list.d/espressif.list

sudo apt update

# GUI 和 CLI
sudo apt install eim

# CLI
sudo apt install eim-cli
```

SDK 和工具链有了以后，可以构建项目。

IDE 或命令行。

### 命令行构建体验

带环境变量的终端，如果需要手动添加



命令行，最接近原始工具
```
cd 到 project

idf.py set-target esp32s3
idf.py menuconfig

idf.py build

idf.py -p COM16 flash

idf.py -p COM16 monitor
```

`ctrl + ]` 退出监视

### vscode 安装

安装 ESP-IDF 的 vscode 扩展。

直接 printf hello world ，中间隐藏了非常非常多的细节，并且编译出来的固件也很大。带了特别多的东西。


基础的配置

240MHz

spi flash，QSPI 80MHz，16 MB

PSRAM octal mode

N16R8 模组手册，S3R8，16MB,8M PSRAM，Octal SPI，RAM clock ，80MHz

RTOS 的 TICK_RATE_HZ 设置为 1000


分区表配置。partition table 里，

自定义分区，


```cs
# ESP-IDF Partition Table
# Name,   Type, SubType,  Offset,   Size,     Flags
nvs,      data, nvs_keys, 0x9000,   0x6000,
phy_init, data, phy,      0xf000,   0x1000,
factory,  app,  factory,  0x10000,  0x1F0000,
vfs,      data, fat,      0x200000, 0xA00000,
storage,  data, spiffs,   0xC00000, 0x400000,
```

分区表，对外挂的 SPI flash 划分。





