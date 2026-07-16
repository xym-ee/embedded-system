# 事件循环与消息机制

ESP-IDF 中有一套事件循环机制，核心是 `esp_event`。理解事件机制，对组织 Wi-Fi、网络连接、业务状态变化很重要。

https://docs.espressif.com/projects/esp-idf/zh_CN/v5.5.4/esp32/api-reference/system/esp_event.html

## esp_event

一种 订阅/发布 机制。

发布者提供消息内容，订阅者提供一个回调函数。

事件循环，完成在事件发生时执行对应的回调函数

特殊事件循环：esp_event_cloop_create_default

不需要句柄，系统级的，有专用 API。处理系统级的事件如 wifi 之类的




```c
// 1. 定义事件处理程序
void run_on_event(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data)
{
    // 事件处理程序逻辑
}

void app_main()
{
    // 2. 用一个类型为 esp_event_loop_args_t 的配置结构体，指定所创建循环的属性。获取一个类型为 esp_event_loop_handle_t 的句柄，用于其他 API 引用循环、执行操作。
    esp_event_loop_args_t loop_args = {
        .queue_size = ...,
        .task_name = ...
        .task_priority = ...,
        .task_stack_size = ...,
        .task_core_id = ...
    };

    esp_event_loop_handle_t loop_handle;

    esp_event_loop_create(&loop_args, &loop_handle);

    // 3. 注册在 (1) 中定义的事件处理程序。MY_EVENT_BASE 和 MY_EVENT_ID 指定了一个假设事件：将处理程序 run_on_event 发布到循环中时，执行该处理程序。
    esp_event_handler_register_with(loop_handle, MY_EVENT_BASE, MY_EVENT_ID, run_on_event, ...);

    ...

    // 4. 将事件发布到循环中。此时，事件排入事件循环队列，在某个时刻，事件循环会执行已注册到发布事件的事件处理程序，例如此处的 run_on_event。为简化过程，此示例从 app_main 调用 esp_event_post_to，实际应用中可从任何其他任务中发布事件。
    esp_event_post_to(loop_handle, MY_EVENT_BASE, MY_EVENT_ID, ...);

    ...

    // 5. 注销无用的处理程序。
    esp_event_handler_unregister_with(loop_handle, MY_EVENT_BASE, MY_EVENT_ID, run_on_event);

    ...

    // 6. 删除无用的事件循环。
    esp_event_loop_delete(loop_handle);
}

```


事件用 BASE_EVENT 和 EVENT_ID 共同决定。

BASE_EVENT 用宏来定义和声明。

ID 用 enum 来定义。

handler_register 可以用 ESP_EVENT_ANY_ID，具体的 handler 里用 switch 分流到具体地 ID。

其他的都和发布订阅模型一致。事件来源可以有多个，event_post_to 即可。事件处理也可以有多个，依次注册就行。

默认事件循环和用户事件循环的行为并无差异。实际上，用户甚至可以将自己的事件发布到默认事件循环中，以节省内存而无需创建自己的循环。


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

