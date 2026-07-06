# ESP-IDF 组件机制

ESP-IDF 的组件机制是组织中等规模应用的核心。

在裸机工程里，代码常常只是按文件夹摆放。但在 ESP-IDF 中，组件是更明确的软件边界：每个组件可以声明源码、头文件、依赖、配置项和对外接口。

## 组件是什么

一个组件通常包含：

```text
components/
  app_service/
    CMakeLists.txt
    include/
      app_service.h
    app_service.c
    Kconfig
```

其中：

- `CMakeLists.txt`：告诉构建系统这个组件有哪些源文件和依赖。
- `include/`：放对外暴露的头文件。
- `.c` / `.cpp`：实现代码。
- `Kconfig`：组件自己的配置项。

## main 也是组件

ESP-IDF 里的 `main/` 目录本质上也是一个组件。

这点很重要。它说明应用入口并不应该无限膨胀。`main` 可以只负责启动和组装，把真正的业务代码放进自己的组件。

例如：

```text
main/
  app_main.c
components/
  board/
  device/
  app_fsm/
  net_service/
  storage_service/
```

## 组件依赖

组件之间通过 CMake 声明依赖。

示例：

```cmake
idf_component_register(
    SRCS "app_service.c"
    INCLUDE_DIRS "include"
    REQUIRES esp_event nvs_flash
)
```

`REQUIRES` 表示公共依赖。依赖关系越清晰，工程越容易维护。

## 组件划分思路

产品级工程可以按这些边界拆分：

- `board`：板级引脚、外设初始化、硬件版本差异。
- `drivers`：对具体芯片或外设的驱动封装。
- `device`：把传感器、执行器抽象成设备对象。
- `storage_service`：NVS、文件系统、配置读写。
- `net_service`：Wi-Fi、MQTT、HTTP 等联网能力。
- `app_fsm`：应用层状态机。
- `app_service`：业务流程和产品功能。
- `ui_service`：按键、屏幕、LED、蜂鸣器等交互逻辑。

这里的重点不是文件夹名字，而是让依赖方向稳定。

## 依赖方向

可以先采用这样的方向：

```text
app
  ↓
service
  ↓
device
  ↓
driver
  ↓
esp-idf
```

上层依赖下层，下层不要反向调用上层。

如果下层需要通知上层，优先通过事件、回调或消息队列，而不是直接包含上层头文件。

## 当前要回答的问题

- 哪些代码应该留在 `main`？
- 自己的组件应该放在 `components/` 还是 `main/` 下面？
- 组件之间如何声明依赖？
- 什么是公共头文件，什么是内部头文件？
- 如何避免组件互相包含，最后变成一团？

## 我的目标

后续自己的产品级应用层，应该尽量从一开始就按组件组织。

不追求过度抽象，但要避免所有逻辑都堆进 `app_main.c`。ESP-IDF 已经提供了组件机制，不使用它就等于放弃了框架给出的工程边界。

