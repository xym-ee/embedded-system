
# 计算机与嵌入式学习笔记目录整理思路

## 基本判断

工程专题不应该只放在一个巨大的 `30_engineering/` 里面。

更好的方式是：把 `30~39` 作为“工程专题编号段”，但不需要把每个接触过的方向都抬成顶层主线。长期反复使用、会持续展开的方法论和系统能力，可以独立成工程专题；只是浅尝、作为背景知识或项目经历出现的内容，降到子目录、项目目录或索引页里更舒服。

当前主线可以先收敛成：

```text
00_worldview/                         跨学科世界观
10_five_questions_of_computer_systems/ 计算机系统的五个问题
20_cs_courses/                        本科计算机课程
21_ee_courses/                        电子、自动化、控制课程，未来扩展

30_bare_metal_and_interfaces/         裸机开发与外设接口
31_embedded_software_frameworks/      嵌入式软件框架
32_rtos_kernel/                       RTOS 内核专题
33_linux_systems/                     Linux 使用与系统编程
34_embedded_linux_systems/            嵌入式 Linux 系统构建
36_network_and_iot_systems/           网络、OpenWrt 与 IoT 系统
37_ai_agent_tools/                    AI Agent 工具链

40_projects/                          具体板卡、芯片、项目实践，也承接非主业方向
assets/                               图片与静态资源
```

其中 Linux 驱动、FPGA / Zynq、汽车电子 / AUTOSAR 先不作为顶层主线：

```text
34_embedded_linux_systems/linux-drivers/  Linux 驱动接触型笔记
40_projects/zynq/                         FPGA / Zynq 实验
40_projects/s32k3/                        S32K3 与车规 MCU 实验
40_projects/automotive-notes/             AUTOSAR、MCAL、线束等接触型索引
```

## 分类原则

### 1. 培养计划有的系统化课程


如果内容是本科课程中的通用理论，放入 `20_cs_courses/` 或未来的 `21_ee_courses/`。

例如：

- 操作系统的进程、线程、调度、同步、内存管理：`20_cs_courses/operating-system/`
- 计算机网络的 TCP/IP、路由、应用层协议：`20_cs_courses/computer-network/`
- 自动控制、现代控制、电机控制理论：未来放入 `21_ee_courses/`

### 2. 主线工程专题放 30~39，但不用填满

如果内容是围绕某类系统、框架、平台或工具展开，并且未来会持续积累、反复使用，就放入 `30~39`。

例如：

- RTOS 内核：`32_rtos_kernel/`
- Linux 镜像构建：`34_embedded_linux_systems/`
- Claude Code / Codex / Dify：`37_ai_agent_tools/`

编号可以留空，不需要为了连续而给旁支方向单独开顶层目录。

### 3. 具体对象放 projects

如果内容围绕某块板子、某颗芯片、某个项目、某次移植实践展开，放入 `40_projects/`。

例如：

- STM32 实验
- S32K3 实验
- i.MX6ULL 镜像构建实践
- Zynq 实验
- ESP32 项目
- nRF5340 项目
- OpenClaw 项目

### 4. 允许交叉引用，不强行唯一解释

同一份内容只保留一个主要位置，但可以从多个索引页引用。

例如 RTOS：

- 操作系统通用理论：`20_cs_courses/operating-system/`
- RTOS 内核机制：`32_rtos_kernel/`
- RT-Thread 应用、设备框架、BSP：`31_embedded_software_frameworks/`
- 某个 STM32 上的 RT-Thread 移植：`40_projects/stm32/`

### 5. 接触型方向降级处理

如果只是“接触过、能读懂、未来可能偶尔查”，但不是长期主业，就不要放在和主线专题同等的顶层。

更适合的处理方式：

- Linux 驱动：作为 `34_embedded_linux_systems/linux-drivers/` 的补充主题。
- FPGA / Zynq：作为 `40_projects/zynq/` 的项目实践；数字电路理论以后可放 `21_ee_courses/`。
- 汽车电子 / AUTOSAR：作为 `40_projects/s32k3/`、`40_projects/automotive-notes/` 的项目与索引，不单独扩成主线。

## 30_bare_metal_and_interfaces

定位：不依赖通用操作系统，直接理解和控制芯片、外设、启动流程。

适合内容：

- GPIO
- UART
- SPI
- I2C
- CAN
- PWM
- ADC / DAC
- USB
- Ethernet MAC / PHY
- MCU 时钟、中断、启动文件
- J-Link、烧录、调试
- 裸机工程环境
- STM32 / S32K3 / i.MX 的裸机基础

现有内容可映射：

```text
2_1_bare_metal/1_interface/
2_1_bare_metal/3_arm_mcu/
2_1_bare_metal/4_mpu/
2_1_bare_metal/5_bare_metal/
```

## 31_embedded_software_frameworks

定位：嵌入式中等规模软件的组织方式，不重点讨论内核实现。

适合内容：

- LVGL
- 状态机
- 事件驱动
- 发布订阅
- 简单任务调度
- RT-Thread 应用开发
- RT-Thread 设备框架
- RT-Thread BSP
- RT-Thread 软件包
- FreeRTOS 应用开发
- 嵌入式软件架构

现有内容可映射：

```text
2_2_medium_system/1lvgl/
2_2_medium_system/2rtt_basic/
2_2_medium_system/3rtt_device/
2_2_medium_system/4rtt_thread/
2_2_medium_system/5rtt_bsp/
2_2_medium_system/6rtt_package/
2_2_medium_system/7freeRTOS/
```

说明：

如果某篇 FreeRTOS 或 RT-Thread 笔记主要讲 API 和应用，放这里；如果主要讲调度器、上下文切换、临界区、内存管理源码，放 `32_rtos_kernel/`。

## 32_rtos_kernel

定位：RTOS 内核机制与实时系统实现。它既有理论，也有实践，不需要强行放进操作系统课程。

适合内容：

- ARMv7-M / Cortex-M 架构
- 异常与中断
- PendSV / SysTick / SVC
- 线程上下文切换
- 调度器
- 临界区
- 线程同步
- 线程通信
- 信号量、互斥量、事件集、消息队列
- 内存池、堆管理
- RT-Thread 内核源码
- FreeRTOS 内核源码
- RTOS 驱动模型中偏内核机制的部分

现有内容可映射：

```text
30_engineering/2_3_rtos_kernel/
```

建议未来目标：

```text
32_rtos_kernel/
  armv7-m/
  scheduling/
  synchronization/
  memory/
  rt-thread-kernel/
  freertos-kernel/
  driver-model/
```

## 33_linux_systems

定位：把 Linux 作为通用操作系统来使用和编程。

适合内容：

- Linux 基本使用
- Shell
- Vim
- GCC
- Makefile
- 包管理
- 环境变量
- 文件系统 API
- 进程、线程、信号
- Linux 系统编程
- Linux 应用开发
- Docker 基础使用

现有内容可映射：

```text
3_1_linux_usage/
4_ai_develop/linux_app.md
4_ai_develop/docker.md
```

说明：

这里的 Linux 偏“用户态”和“通用系统”。如果是给板子构建 Linux 系统，放 `34_embedded_linux_systems/`；如果是写内核驱动，当前也作为 `34_embedded_linux_systems/linux-drivers/` 的补充主题处理。

## 34_embedded_linux_systems

定位：面向开发板构建、裁剪、启动一个完整 Linux 系统。

适合内容：

- U-Boot 使用、移植、启动流程
- Linux Kernel 移植与配置
- Device Tree
- Root Filesystem
- BusyBox
- init 系统
- 文件系统镜像
- Buildroot
- Yocto
- OpenWrt 镜像构建
- i.MX6ULL / i.MX8MP 等板级 Linux

现有内容可映射：

```text
3_2_linux_image/
```

建议未来目标：

```text
34_embedded_linux_systems/
  bootloader/
  kernel/
  device-tree/
  rootfs/
  image-build/
  buildroot/
  yocto/
  openwrt-image/
```

## 34_embedded_linux_systems/linux-drivers

定位：嵌入式 Linux 的补充主题。只保留入门、读代码、查机制所需的驱动开发笔记，不把它扩成长期主线。

适合内容：

- 字符设备驱动
- platform driver
- file_operations
- sysfs / procfs
- 设备树匹配
- pinctrl
- GPIO
- 中断
- 并发控制
- Linux 内核模块
- 驱动调试

现有内容可映射：

```text
3_3_linux_driver/
```

说明：

如果未来真的长期做 Linux 内核驱动，可以再把它升为独立的 `35_linux_drivers/`。在当前定位下，它放在 `34_embedded_linux_systems/` 下面更合适：它依赖板级 Linux、设备树、内核配置和调试环境，本质上是嵌入式 Linux 主线的一段深入补充。

## 36_network_and_iot_systems

定位：网络系统、路由系统、家庭自动化、物联网系统的工程实践。

适合内容：

- OpenWrt 使用与路由系统
- 家庭网络
- Home Assistant
- W5500
- LAN8720
- MQTT
- 局域网服务
- 设备接入
- IoT 网关

现有内容可映射：

```text
1_4_network/8_home.md
1_4_network/9_openwrt.md
4_1_home_assistant/
2_2_medium_system/6rtt_package/
```

说明：

计算机网络理论仍然放 `20_cs_courses/computer-network/`。这里放网络相关的系统搭建、设备接入和工程实践。

## 37_ai_agent_tools

定位：AI Agent、编程助手、自动化工具链的使用和原理。

适合内容：

- Claude Code
- Codex
- Dify
- MCP
- hooks
- subagent
- prompt workflow
- Agent OS 中偏工具实现的部分
- AI 辅助工程开发流程

现有内容可映射：

```text
4_ai_develop/
4_ai_develop/learn_cc/
4_ai_develop/codex/
4_ai_develop/dify/
```

说明：

如果是关于“AI Agent 会如何改变软件与工程系统”的世界观思考，放 `00_worldview/`；如果是 Claude Code、Codex、Dify 的具体使用和机制，放这里。

## 40_projects/zynq

定位：FPGA / Zynq 的接触型项目实践。当前不把 FPGA、SoC 软硬件协同作为主业主线，只记录能帮助理解系统边界和项目经验的内容。

适合内容：

- Zynq
- PS / PL 协同
- HDLBits 实践
- FPGA 工程流程
- Verilog 工程实践
- SoC 外设实验

现有内容可映射：

```text
11zynq/
```

说明：

数字电路、计算机组成里的理论部分可以放 `20_cs_courses/` 或未来 `21_ee_courses/`；Zynq 这类具体 SoC 实践优先放 `40_projects/zynq/`。只有当 FPGA 工程成为长期主线时，再考虑升为独立的 `38_fpga_soc_systems/`。

## 40_projects/s32k3 与 automotive-notes

定位：汽车电子、AUTOSAR、MCAL、车规 MCU 与线束工程的接触型记录。当前只作为项目背景和扩展知识，不单独作为顶层主业方向。

适合内容：

- AUTOSAR
- MCAL
- S32K3
- CAN / LIN / FlexRay / Ethernet
- 车规 MCU 启动、时钟、外设
- 线束工程
- 车载嵌入式软件架构

现有内容可映射：

```text
12automotive/
2_1_bare_metal/3_arm_mcu/2_s32k3/
4_ai_develop/HarnessEngineering/
```

说明：

如果 S32K3 笔记主要讲裸机外设，可以放 `40_projects/s32k3/`，并从 `30_bare_metal_and_interfaces/` 引用；如果主要讲 AUTOSAR、MCAL、线束等行业背景，则放 `40_projects/automotive-notes/` 做索引即可。只有当汽车电子成为长期方向时，再考虑升为独立的 `39_automotive_systems/`。

## 40_projects

定位：具体工程对象和项目日志。

适合内容：

- 某块板子的实验记录
- 某个芯片的 bring-up
- 某次系统移植
- 某个机器人或硬件项目
- 某个可运行应用的完整过程

建议目录：

```text
40_projects/
  stm32/
  s32k3/
  imx6ull/
  imx8mp/
  zynq/
  esp32/
  nrf5340/
  jetson/
  openclaw/
  openwrt-router/
  home-assistant/
  automotive-notes/
```

现有内容可映射：

```text
2_2_medium_system/8nrf5340/
2_2_medium_system/esp32/
11zynq/
12automotive/
2_1_bare_metal/3_arm_mcu/2_s32k3/
4_ai_develop/openclaw/
assets/images/jetson.png
```

## 当前目录迁移建议

| 当前目录 | 建议归类 |
| --- | --- |
| `2_1_bare_metal/` | `30_bare_metal_and_interfaces/` |
| `2_2_medium_system/1lvgl/` | `31_embedded_software_frameworks/lvgl/` |
| `2_2_medium_system/2rtt_basic/` | `31_embedded_software_frameworks/rt-thread/` |
| `2_2_medium_system/3rtt_device/` | `31_embedded_software_frameworks/rt-thread-device/` |
| `2_2_medium_system/4rtt_thread/` | `31_embedded_software_frameworks/rt-thread-threading/` |
| `2_2_medium_system/5rtt_bsp/` | `31_embedded_software_frameworks/rt-thread-bsp/` |
| `2_2_medium_system/6rtt_package/` | `31_embedded_software_frameworks/rt-thread-packages/` 或 `36_network_and_iot_systems/` |
| `2_2_medium_system/7freeRTOS/` | `31_embedded_software_frameworks/freertos/` |
| `30_engineering/2_3_rtos_kernel/` | `32_rtos_kernel/` |
| `3_1_linux_usage/` | `33_linux_systems/` |
| `3_2_linux_image/` | `34_embedded_linux_systems/` |
| `3_3_linux_driver/` | `34_embedded_linux_systems/linux-drivers/` |
| `1_4_network/8_home.md` | `36_network_and_iot_systems/home-network/` |
| `1_4_network/9_openwrt.md` | `36_network_and_iot_systems/openwrt/` 或 `34_embedded_linux_systems/openwrt-image/` |
| `4_1_home_assistant/` | `36_network_and_iot_systems/home-assistant/` |
| `4_ai_develop/` | `37_ai_agent_tools/` |
| `11zynq/` | `40_projects/zynq/` |
| `12automotive/` | `40_projects/automotive-notes/` 或 `40_projects/s32k3/` |

## 本次执行记录

2026-06-07 已按上面的收敛思路完成一轮顶层目录调整：

- `35_linux_drivers/` 已降级为 `34_embedded_linux_systems/linux-drivers/`。
- `38_fpga_soc_systems/` 已降级为 `40_projects/zynq/`。
- `39_automotive_systems/s32k3/` 已移动到 `40_projects/s32k3/`。
- `39_automotive_systems/` 中 AUTOSAR、MCAL 等汽车电子背景笔记已移动到 `40_projects/automotive-notes/`。
- 原 `39_automotive_systems/harness-engineering/` 实际内容是 AI Agent harness engineering，已移动到 `37_ai_agent_tools/harness-engineering/`。
- 新增 `20_cs_courses/README.md`、`36_network_and_iot_systems/README.md`、`40_projects/README.md` 作为主目录入口。
- `SUMMARY.md` 已使用 `docs/tools/gen_summary.py` 重新生成。

## 后续扩展

如果未来控制、电机、机器人内容明显增多，可以新增：

```text
41_control_and_robotics_systems/
```

适合内容：

- 电机控制系统
- 机器人控制系统
- 运动控制
- 传感器融合
- 控制器工程实现
- 仿真与实物系统闭环

对应课程理论仍然放入未来的 `21_ee_courses/`。
