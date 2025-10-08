

# AUTOSAR



DaVinci 
SIP 包
EB 工具
IAR 
MCAL 
RTD 


AUTOSAR 开发步骤
- 原材料 SIP MCAL DBC ARXML，包括 AUTOSAR 源码，MCU 驱动代码
- 工具对原始包进行一些配置 DaVinci EB，配置可运行的软件系统
- 配置生成代码添加到 IAR 中集成，系统集成能力
- Debug 应用开发


一些基本的概念需要清晰，有自己的一套描述（抽象）

- 一个 APP 有多个 SWC
- SWC 是开展配置工作的基本单位
- SWC 可以包含多个 runnable ，如 init deinit 用户定义的调度函数
- 同一个 SWC 内不同 runnable 

MATLAB 用 Simulink 生成代码，用用应用层软件开发
Developer 用于设计 APPL 的程序架构
Configurator 用户配置 BSW 和自动生成 RTE
EB Tresos 配置 MCAL，



APP 三个部分，RTE 之上的，SWC 可以简单的认为是一个 .c 文件，一个功能模块，
SWC 内部定义 Runnable 即一个函数，SWC 通过 Ports 对外交互，RTE 通过 Connector 将 ports 关联，片内通过 RTE 通信，简单理解为全局变量。

RTE 做的事情，提供 ECU 内外的通信管理，提供对 Runnable 的管理，Runnable 到 Task 的映射是 RTE 实现的，DaVinci 基于 APPL 和 BSW 的配置自动生成 RTE

BSW 包含的东西：板载相关的，微控制器相关的，如 MCAL 的底层驱动封装。ECU 抽象，服务层，包含 OS ，BSW 未定义的归纳到复杂驱动。

做一个最小系统，SWC 应用点一个灯，

## SIP 包

SIP 包 (System Integration Package)，Vector 提供给 ECU 项目的一个配置模板 + 驱动集 + 元数据定义包。告诉 DaVinci “这个芯片有哪些外设？BSW 支持哪些模块？各个模块的参数、版本、依赖关系是什么？”

DaVinci Configurator 本身只是一个 通用 AUTOSAR 配置工具，它并不知道你要用的 MCU 是谁家的、有哪些模块。SIP 就是告诉它这些信息的“插件”。

SIP 包也是通过配置生成的，开发人员直接拿来用就可以了。

## MCAL

MCAL 是芯片厂商提供的，

S32K3 平台，安装 MCAL 和 EB，需要将 MCAL 集成到 DaVinci 环境中。


实现一个最小的 AUTOSAR 系统，按键控制一个 LED 翻转。

DaVinci 的配置，可以先使用 EB 或者 S32DS 去熟悉，先研究官方的 demo，熟悉了配置项之后，







