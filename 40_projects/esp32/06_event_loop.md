# 事件循环与消息机制

ESP-IDF 中有一套事件循环机制，核心是 `esp_event`。理解事件机制，对组织 Wi-Fi、网络连接、业务状态变化很重要。

## 为什么需要事件

嵌入式系统不是只按顺序执行的程序。它一直在响应各种外部和内部变化：

- 按键按下
- Wi-Fi 连接成功
- MQTT 断开
- 传感器数据到达
- 定时器超时
- 配置被修改
- OTA 开始或失败

如果所有模块之间直接互相调用，系统很快就会变得混乱。

事件机制的作用是把“发生了什么”和“谁来处理”解耦。

## ESP-IDF 事件模型

ESP-IDF 中常见概念：

- event loop：事件循环。
- event base：事件类别。
- event id：具体事件。
- event data：事件数据。
- handler：事件处理函数。

可以先把它理解成：

```text
事件源发布事件
  ↓
事件循环分发
  ↓
注册过的 handler 被调用
```

## 系统事件

Wi-Fi、IP、BLE 等组件会发布系统事件。

例如：

- Wi-Fi 启动
- Wi-Fi 连接
- Wi-Fi 断开
- 获取 IP 地址

应用层通常通过注册 handler 来响应这些事件。

## 自定义事件

产品应用中也可以定义自己的事件：

```text
APP_EVENT_BUTTON_CLICK
APP_EVENT_NET_READY
APP_EVENT_MQTT_CONNECTED
APP_EVENT_CONFIG_CHANGED
APP_EVENT_OTA_REQUEST
APP_EVENT_ERROR
```

这样应用层状态机不需要关心底层事件来自 Wi-Fi、按键、中断还是云端命令，只关心它收到的产品事件。

## 事件和状态机

事件本身只是“发生了什么”，状态机决定“当前状态下应该怎么处理”。

例如：

```text
state: WIFI_CONNECTING
event: WIFI_GOT_IP
action: start_mqtt()
next state: CLOUD_CONNECTING
```

这比在多个回调函数里到处改全局变量更清楚。

## 和队列的关系

队列更像点对点的数据传递。

事件更像发布和订阅。

在产品工程中可以这样用：

- 驱动层用队列接收高频数据。
- 服务层处理数据后发布应用事件。
- 应用层状态机消费事件，决定业务动作。

## 当前要回答的问题

- 默认事件循环什么时候创建？
- 自定义事件循环和默认事件循环怎么选择？
- 事件 handler 里能不能阻塞？
- 事件数据的生命周期如何管理？
- 哪些事件应该暴露给应用层，哪些只在服务内部使用？

