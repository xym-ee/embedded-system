# 笔记整理计划

## 整理目标

这个仓库当前主要整理“计算机系统与嵌入式软件系统”相关内容。

长期看，它可以扩展成一份更大的“工程系统知识地图”：计算机系统、电子系统、控制系统、数学工具、机器人系统都可以逐步纳入。但当前阶段先把计算机系统这条线整理清楚。

## 顶层分类

```text
00_worldview/              世界观：跨学科的系统观
10_computer_understanding/ 计算机系统的个人理解
20_cs_courses/             系统化学习的计算机课程
21_ee_courses/             电子、自动化、控制课程，未来扩展
30_engineering/            工程专题与实践
assets/                    图片与静态资源
```

## 00_worldview：世界观

这一类放最上层的思考，不局限于计算机。

它可以连接计算机、电子、电路、控制、数学、机器人、AI Agent 等话题，回答更大的问题：如何理解一个工程系统，如何从抽象、结构、控制、连接、复杂性等角度看待技术。

```text
00_worldview/
  README.md
  system-questions/
  computation-control-engineering/
  cross-scale-systems/
  agent-os/
```

适合放入这里的内容：

- 技术世界观
- 系统构造的基本问题
- 计算、控制与工程系统的关系
- 从电路到软件、从软件到机器人系统的跨尺度理解
- AI Agent 与未来软件/工程系统的关系

## 10_computer_understanding：计算机系统的个人理解

这一类是当前仓库的核心主线。

它用“五个问题”整理计算机系统与嵌入式软件系统，不按课程、书籍、技术栈分类，而是沉淀自己的理解。

```text
10_computer_understanding/
  README.md
  01_computation/     计算是什么？
  02_control/         控制如何建立？
  03_resources/       资源如何分配？
  04_connection/      系统如何连接？
  05_complexity/      复杂性如何被管理？
```

### 01_computation：计算是什么？

关注程序、数据、抽象、语言、编译、链接、指令、计算模型。

### 02_control：控制如何建立？

关注从代码到硬件行为的控制链路，包括外设、中断、状态机、裸机程序、RTOS 任务。

### 03_resources：资源如何分配？

关注 CPU、内存、文件、设备、进程、线程、调度、同步、虚拟化。

### 04_connection：系统如何连接？

关注接口、总线、协议、网络、设备间通信、系统间通信。

### 05_complexity：复杂性如何被管理？

关注模块化、分层、架构、构建系统、驱动框架、BSP、软件工程、AI/Agent 工具链。

## 20_cs_courses：系统化学习的计算机课程

这一类主要保留本科计算机课程体系，按课程名组织。

课程目录的职责是记录系统学习过程，不承担最终的抽象分类职责。真正形成自己的理解后，再提炼到 `10_computer_understanding`。

```text
20_cs_courses/
  README.md
  programming/
  data-structures/
  algorithms/
  discrete-mathematics/
  digital-circuit/
  computer-organization/
  computer-architecture/
  operating-system/
  computer-network/
  database-system/
  compiler/
  software-engineering/
  csapp/
  sicp/
  missing-semester/
```

可以放入这一类的内容：

- C / C++ / 程序设计基础
- 数据结构
- 算法
- 离散数学
- 数字电路
- 计算机组成原理
- 计算机体系结构
- 操作系统
- 计算机网络
- 数据库
- 编译原理
- 软件工程
- CSAPP
- SICP
- Missing Semester

## 21_ee_courses：电子、自动化、控制课程

这一类暂时作为未来扩展入口。

如果后续要系统整理电子、自动化、控制、数学、机器人相关内容，可以在这里按课程体系展开。它和 `20_cs_courses` 是并列关系，而不是计算机课程的子目录。

```text
21_ee_courses/
  README.md
  engineering-mathematics/
  circuit-analysis/
  analog-circuit/
  digital-electronics/
  signals-and-systems/
  automatic-control/
  modern-control/
  motor-control/
  power-electronics/
  robotics/
```

可以放入这一类的内容：

- 工程数学
- 电路分析
- 模拟电路
- 数字电子技术
- 信号与系统
- 自动控制原理
- 现代控制理论
- 电机控制
- 电力电子
- 机器人学

## 30_engineering：工程专题与实践

这一类放不直接属于本科课程主干，但对嵌入式、系统工程、AI 工具链很重要的内容。

它可以按技术栈、系统、框架、工具、板卡或具体研究主题组织。

```text
30_engineering/
  README.md
  linux/
  linux-system-programming/
  linux-image-build/
  linux-driver/
  embedded-linux/
  bare-metal/
  armv7-m/
  rt-thread/
  freertos/
  lvgl/
  autosar/
  openwrt/
  home-assistant/
  ai-agent/
  claude-code/
  codex/
  dify/
  projects/
    stm32/
    s32k3/
    imx6ull/
    imx8mp/
    zynq/
    esp32/
    nrf5340/
    jetson/
```

可以放入这一类的内容：

- Linux 使用、系统编程、镜像构建、驱动开发
- 嵌入式 Linux
- 裸机开发
- ARMv7-M
- RT-Thread
- FreeRTOS
- LVGL
- AUTOSAR
- OpenWrt
- Home Assistant
- Claude Code 原理
- Codex 使用与原理
- Dify
- AI Agent 工具链
- 具体板卡、芯片、项目实践

## 内容之间的关系

同一份内容可以被多个目录引用，但尽量只保留一个主要存放位置。

例如：

- SICP 原始学习笔记放在 `20_cs_courses/sicp/`
- SICP 中关于抽象、解释器、模块化的理解，提炼到 `10_computer_understanding/01_computation/` 或 `10_computer_understanding/05_complexity/`
- RT-Thread 学习笔记放在 `30_engineering/rt-thread/`
- 某块 STM32 板子的 RT-Thread 移植实践放在 `30_engineering/projects/stm32/`
- 控制系统、模拟电路、电机控制等内容，未来可以放入 `21_ee_courses/`
- 计算机系统、控制系统、机器人系统之间的共通理解，放入 `00_worldview/`

## 迁移步骤

### 第一阶段：先改索引，不移动文件

重写 `README.md` 和 `SUMMARY.md`，先把现有内容挂到新的顶层分类下面。

### 第二阶段：整理计算机课程

把本科计算机课程、经典教材、系统课程归入 `20_cs_courses`。

### 第三阶段：整理工程专题

把 Linux、RTOS、嵌入式、AI Agent 工具链等内容归入 `30_engineering`。

### 第四阶段：沉淀计算机系统理解

从课程和专题中提炼自己的理解，逐步写入 `10_computer_understanding` 的五个问题。

### 第五阶段：扩展电子与控制体系

当电子、自动化、控制、机器人相关内容积累到一定规模后，再逐步启用 `21_ee_courses`。

## 单篇笔记模板

```markdown
# 标题

## 这个问题是什么

## 核心模型

## 关键机制

## 工程例子

## 易错点

## 相关笔记
```
