# Wi-Fi、BLE 与 IoT 接入

ESP32 的核心价值之一是联网能力。Wi-Fi、BLE、TCP/IP、MQTT、HTTP 和配网流程，决定了它能否成为一个真正的 IoT 设备。

## Wi-Fi 模式

常见模式：

- STA：作为客户端连接路由器。
- AP：自己开启热点。
- AP + STA：一边开热点，一边连接路由器。

产品中常见流程：

```text
首次启动
  ↓
进入配网模式
  ↓
获得 Wi-Fi 配置
  ↓
连接路由器
  ↓
获取 IP
  ↓
连接云端
```

## 配网

配网要解决的问题是：设备没有屏幕和键盘时，用户如何把 Wi-Fi 信息交给设备。

常见方式：

- SoftAP 配网
- BLE 配网
- SmartConfig
- 二维码或局域网发现配合 App

ESP32-S3 支持 Wi-Fi 和 BLE，因此 BLE 配网是一个比较自然的选择。

## 网络状态

联网产品至少要区分：

```text
WIFI_IDLE
WIFI_CONNECTING
WIFI_CONNECTED
IP_READY
CLOUD_CONNECTING
CLOUD_CONNECTED
OFFLINE
```

底层 Wi-Fi 事件最好转换成应用层事件：

```text
WIFI_EVENT_STA_DISCONNECTED → APP_EVENT_NET_LOST
IP_EVENT_STA_GOT_IP → APP_EVENT_NET_READY
```

## MQTT

MQTT 适合设备和云端之间的消息通信。

常见主题：

- 设备上线
- 属性上报
- 命令下发
- 事件上报
- OTA 通知
- 日志或诊断

产品代码里不要让 MQTT 回调直接操作所有业务。更好的方式是：

```text
MQTT message
  ↓
protocol parser
  ↓
app event
  ↓
state machine / service
```

## HTTP

HTTP 常用于：

- OTA 固件下载
- REST API 请求
- 配网页面
- 简单本地 Web 服务

如果产品主要使用 MQTT，也可能仍然需要 HTTP 来做升级或资源下载。

## BLE

BLE 适合：

- 配网
- 近场控制
- 设备发现
- 调试通道

BLE 和 Wi-Fi 同时使用时，需要关注内存占用、任务调度和射频共存。

## 当前要回答的问题

- 产品使用 SoftAP 配网还是 BLE 配网？
- Wi-Fi 凭据保存在哪里？
- 断网后如何重连，重试间隔如何设计？
- 云端协议使用 MQTT、HTTP，还是两者结合？
- MQTT topic 如何设计？
- 设备离线期间的数据是否需要缓存？
- BLE 是否只用于配网，还是长期保持连接？

