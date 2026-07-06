# 产品级应用层架构

这里记录我自己的 ESP32 产品级应用层设计。

目标不是一开始做一个庞大的框架，而是在 ESP-IDF 的组件机制之上，逐步形成一套可维护、可复用、能支撑真实产品迭代的组织方式。

## 分层思路

先采用一个简单的分层模型：

```text
product app
  ↓
services
  ↓
devices
  ↓
drivers / board
  ↓
esp-idf
```

含义：

- `product app`：产品业务、状态机、用户可见行为。
- `services`：网络、存储、OTA、配置、日志、时间同步等系统服务。
- `devices`：传感器、执行器、屏幕、按键等设备抽象。
- `drivers / board`：具体硬件驱动和板级差异。
- `esp-idf`：官方框架和底层能力。

## main 的职责

`app_main` 只做组装：

```c
void app_main(void)
{
    platform_init();
    services_init();
    devices_init();
    product_app_init();
    product_app_start();
}
```

它不直接写复杂业务逻辑。

## 组件建议

初始可以这样拆：

```text
components/
  board/
  app_fsm/
  app_events/
  config_service/
  storage_service/
  wifi_service/
  mqtt_service/
  ota_service/
  device_manager/
```

后续根据产品实际复杂度增删。不要为了显得架构完整而提前拆太细。

## 依赖方向

尽量保持：

```text
app_fsm → services → devices → board → esp-idf
```

反向通知通过事件完成。

例如 Wi-Fi 服务不要直接调用产品业务函数，而是发布：

```text
APP_EVENT_NET_READY
APP_EVENT_NET_LOST
```

由应用状态机决定下一步动作。

## 配置管理

产品配置通常包括：

- Wi-Fi 配置
- 云端服务器地址
- 设备身份
- 用户参数
- 工厂参数
- 硬件版本和软件版本

这些配置不要散落在各个模块里。可以由 `config_service` 统一管理，再由 `storage_service` 负责持久化。

## 错误处理

产品级应用必须有统一错误处理思路。

至少要区分：

- 可恢复错误：Wi-Fi 断开、MQTT 断开、临时读写失败。
- 需要重试的错误：云端不可达、传感器初始化失败。
- 致命错误：配置损坏、关键硬件不可用、固件校验失败。

错误不应该只打印日志，还应该影响状态机。

## 日志和可观测性

产品调试时，日志是第一观察入口。

建议每个组件有自己的 TAG：

```c
static const char *TAG = "wifi_service";
```

状态切换、重连、配置修改、OTA、错误恢复都应该有清晰日志。

## 当前要回答的问题

- 我的产品是否需要明确的 `device_manager`？
- 服务层是否通过事件统一对上层通知？
- 配置项如何定义默认值、当前值和持久化值？
- 产品初始化失败时，是进入错误状态，还是降级运行？
- 工厂测试模式是否和正常应用共用一套状态机？
- 后续如果换芯片，哪些组件应该尽量不变？

