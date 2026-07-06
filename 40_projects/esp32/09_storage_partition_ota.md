# 存储、分区表与 OTA

ESP32 的产品级开发一定会遇到 Flash 分区、NVS、文件系统和 OTA。

这部分决定了设备如何保存配置、保存数据、升级固件，以及升级失败后如何恢复。

## 分区表

ESP32 外部 SPI Flash 会被分成多个区域。

常见分区：

```text
nvs
phy_init
factory
ota_0
ota_1
ota_data
storage
```

如果只是实验，可以用 factory app。产品级应用通常需要 OTA 分区。

## 单应用分区

简单分区：

```csv
# Name,   Type, SubType,  Offset,   Size,     Flags
nvs,      data, nvs,      0x9000,   0x6000,
phy_init, data, phy,      0xf000,   0x1000,
factory,  app,  factory,  0x10000,  0x1F0000,
```

这种方式简单，但无法支持可靠 OTA。

## OTA 分区

OTA 通常需要两个 app 分区：

```csv
# Name,     Type, SubType, Offset,   Size,     Flags
nvs,        data, nvs,     0x9000,   0x6000,
otadata,    data, ota,     0xf000,   0x2000,
phy_init,   data, phy,     0x11000,  0x1000,
ota_0,      app,  ota_0,   0x20000,  0x200000,
ota_1,      app,  ota_1,   0x220000, 0x200000,
storage,    data, spiffs,  0x420000, 0x200000,
```

bootloader 通过 `otadata` 判断当前应该启动哪个 app 分区。

## NVS

NVS 是非易失键值存储，适合保存小型配置：

- Wi-Fi SSID 和密码
- 设备 ID
- token
- 用户配置
- 校准参数
- 启动计数

不适合把大量日志或文件直接塞进 NVS。

## 文件系统

ESP-IDF 常见文件系统：

- SPIFFS
- FATFS
- LittleFS，通常通过组件使用

文件系统适合保存：

- 较大的配置文件
- 音频、图片、网页资源
- 离线缓存
- 运行日志

## OTA 需要考虑的问题

产品级 OTA 不只是下载固件。

需要考虑：

- 当前固件版本
- 目标固件版本
- 下载来源
- 固件校验
- 断点和失败处理
- 首次启动确认
- 回滚策略
- 升级过程中的电源风险

OTA 过程应该进入明确状态，例如：

```text
RUNNING → OTA_DOWNLOADING → OTA_VERIFYING → OTA_REBOOTING
```

## 当前要回答的问题

- 当前模组 Flash 是 8 MB、16 MB 还是更大？
- 产品是否需要双 OTA 分区？
- NVS 中保存哪些配置？
- 文件系统保存哪些数据？
- 恢复出厂设置应该擦除哪些分区？
- OTA 失败如何回滚？

