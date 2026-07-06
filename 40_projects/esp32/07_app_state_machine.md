# 应用层状态机

产品级嵌入式应用最终要管理的是状态。

设备不是简单地执行一串函数，而是在不同状态之间切换：启动、初始化、联网、待机、运行、故障、升级、恢复出厂设置等。

## 为什么要显式状态机

如果不显式设计状态机，状态仍然存在，只是散落在全局变量、标志位、回调函数和任务循环里。

显式状态机的好处是：

- 能看清产品当前处于什么状态。
- 能明确某个事件在当前状态下是否有效。
- 能避免回调函数互相穿透业务逻辑。
- 能更容易处理异常、重连、升级和恢复。

## 基本模型

状态机可以先按这个模型思考：

```text
当前状态 + 事件 → 动作 + 下一个状态
```

例如：

```text
BOOTING + INIT_DONE → start_wifi() + WIFI_CONNECTING
WIFI_CONNECTING + WIFI_GOT_IP → start_mqtt() + CLOUD_CONNECTING
CLOUD_CONNECTING + MQTT_CONNECTED → report_online() + RUNNING
RUNNING + OTA_REQUEST → stop_services() + OTA_UPDATING
ANY + FATAL_ERROR → save_error() + ERROR
```

## 可能的产品状态

一个联网设备可以先粗略分成：

```text
BOOTING
INIT
CONFIG_MODE
WIFI_CONNECTING
CLOUD_CONNECTING
RUNNING
OTA_UPDATING
ERROR
FACTORY_RESET
```

这些状态不一定一次设计完。可以先从最小产品流程开始：

```text
INIT → WIFI_CONNECTING → RUNNING → ERROR
```

后续再加入配网、云连接、OTA 等状态。

## 事件来源

状态机处理的事件可能来自：

- 系统初始化结果
- Wi-Fi 事件
- MQTT 事件
- 按键事件
- 定时器事件
- 传感器事件
- 云端命令
- 错误上报

应用层最好不要直接消费所有底层事件，而是由服务层转换成产品语义更清晰的事件。

例如：

```text
IP_EVENT_STA_GOT_IP → APP_EVENT_NET_READY
MQTT_EVENT_CONNECTED → APP_EVENT_CLOUD_READY
GPIO button interrupt → APP_EVENT_BUTTON_CLICK
```

## 状态机实现方式

可以从简单 switch-case 开始：

```c
void app_fsm_dispatch(app_event_t event)
{
    switch (current_state) {
    case APP_STATE_INIT:
        handle_init_state(event);
        break;
    case APP_STATE_RUNNING:
        handle_running_state(event);
        break;
    default:
        break;
    }
}
```

不要一开始就追求复杂框架。先让状态和事件清楚，比抽象得很漂亮更重要。

## 当前要回答的问题

- 我的产品有哪些稳定状态？
- 哪些事件会触发状态变化？
- 哪些动作是进入状态时执行，哪些动作是离开状态时执行？
- 错误是否有统一状态？
- OTA、恢复出厂设置、低功耗是否应该进入独立状态？
- 状态机运行在独立任务里，还是由事件回调驱动？

## 后续实践

- 画出第一个产品状态图。
- 用枚举定义状态和事件。
- 写一个最小 `app_fsm` 组件。
- 加日志打印每次状态转换。
- 把 Wi-Fi 连接流程接入状态机。

