# ESP-IDF 中的 FreeRTOS

ESP-IDF 使用 FreeRTOS 作为基础调度系统。对应用层来说，这意味着产品逻辑通常不是一个永久运行的 `while (1)`，而是多个任务、队列、事件和定时器协同工作。

## app_main 和任务

`app_main` 被 ESP-IDF 框架调用。进入 `app_main` 时，FreeRTOS 调度器已经在运行。

因此在 `app_main` 中可以：

- 初始化 NVS、事件循环、网络等系统服务。
- 初始化自己的组件。
- 创建应用任务。
- 启动状态机或消息循环。

一个常见思路：

```c
void app_main(void)
{
    system_services_init();
    board_init();
    app_init();
    app_start();
}
```

`app_main` 不应该变成一个巨大的业务函数。

## 常见对象

FreeRTOS 中常用对象：

- task：任务。
- queue：队列。
- semaphore：信号量。
- mutex：互斥量。
- event group：事件组。
- software timer：软件定时器。

在 ESP-IDF 中还要同时关注：

- `esp_event`：ESP-IDF 的事件循环机制。
- `esp_timer`：高精度定时器。
- 系统任务：Wi-Fi、TCP/IP、事件循环等框架内部任务。

## 任务设计

产品工程里不要随意为每个小功能都创建任务。

任务适合用来承接：

- 阻塞等待的外设或协议处理。
- 周期性采集和控制。
- 独立的通信链路。
- 需要明确优先级和栈空间的执行单元。

一些简单的业务动作可以通过事件和状态机处理，不一定要单独开任务。

## 双核和任务亲和性

ESP32-S3 是双核芯片。创建任务时可以选择是否固定到某个核心。

相关 API：

```c
xTaskCreate(...)
xTaskCreatePinnedToCore(...)
```

需要关注：

- Wi-Fi / BLE 系统任务是否占用某些核心。
- 应用任务是否有实时性要求。
- 是否需要避免跨核资源竞争。
- 栈大小是否足够。

## 队列和事件

队列适合传递明确的数据包。

事件适合表达“某件事发生了”。

状态机适合根据当前状态和事件决定下一步动作。

三者可以组合：

```text
driver interrupt
  ↓
queue
  ↓
service task
  ↓
app event
  ↓
state machine
```

## 当前要回答的问题

- `app_main` 是在哪个任务里运行的？
- 一个产品工程应该创建多少任务？
- 哪些任务需要固定核心？
- 队列、事件组、`esp_event` 分别适合什么场景？
- 如何设置任务优先级和栈大小？
- 如何定位栈溢出、看门狗和死锁问题？

