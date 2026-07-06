# ESP32-S3 启动流程

启动流程要回答的问题是：芯片上电以后，到 `app_main` 被调用之前，控制权经过了哪些层次？

对于 ESP-IDF 来说，启动不是简单地从用户代码开始。它大致经历：

```text
Reset
  ↓
ROM bootloader
  ↓
Second stage bootloader
  ↓
Partition table
  ↓
Application image
  ↓
ESP-IDF system init
  ↓
FreeRTOS scheduler
  ↓
app_main
```

## ROM bootloader

ROM bootloader 固化在芯片内部 ROM 中，不能被普通用户修改。

它的职责大概是：

- 根据启动模式判断从哪里加载程序。
- 初始化最基本的硬件环境。
- 从 SPI Flash 中加载二级 bootloader。
- 支持下载模式，用于烧录固件。

这部分有点像很多 MCU 里的系统 bootloader，只是 ESP32 的启动链更复杂，因为应用通常在外部 SPI Flash 中。

## Second stage bootloader

ESP-IDF 工程会生成二级 bootloader。

它的职责包括：

- 初始化 SPI Flash。
- 读取分区表。
- 判断应该启动哪个 app 分区。
- 做安全启动、Flash 加密、OTA 选择等相关处理。
- 加载应用固件并跳转。

二级 bootloader 是理解 ESP-IDF 启动流程的重点。它是 ROM 和应用程序之间的一层可配置软件。

## 分区表

ESP32 的应用固件、NVS、文件系统、OTA 数据等都放在 SPI Flash 的不同分区里。

bootloader 通过分区表找到应用程序。没有分区表，就无法知道 Flash 中哪些区域是应用，哪些区域是数据。

常见分区：

- `nvs`：非易失键值存储。
- `phy_init`：射频初始化数据。
- `factory`：出厂应用固件。
- `ota_0`、`ota_1`：OTA 应用分区。
- `ota_data`：记录当前应该启动哪个 OTA 分区。
- `spiffs`、`fat`：文件系统数据分区。

## app_main

ESP-IDF 中用户入口函数是 `app_main`，不是标准 C 程序里的 `main`。

这是因为在调用 `app_main` 之前，ESP-IDF 已经完成了一系列系统初始化：

- CPU 和基础运行环境初始化
- heap 初始化
- 日志系统初始化
- FreeRTOS 初始化
- 部分系统任务创建
- C/C++ 运行时准备

可以把 `app_main` 理解为：系统框架初始化完成后，交给应用层的入口。

## 双核启动问题

ESP32-S3 是双核 Xtensa LX7。启动时需要关注：

- 哪个核心先启动。
- FreeRTOS 调度器如何管理两个核心。
- 任务是否固定到某个核心。
- Wi-Fi、BLE 等系统任务运行在哪些核心上。

后续分析多任务和产品架构时，需要留意 `xTaskCreatePinnedToCore` 这类 API。

## 后续要补充

- 阅读 bootloader 启动日志。
- 对比单 app 分区和 OTA 分区表的启动差异。
- 整理 `idf.py build` 生成的 bootloader、partition table、app image 文件。
- 记录一次从上电日志追踪到 `app_main` 的过程。





