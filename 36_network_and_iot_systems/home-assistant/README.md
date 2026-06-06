

Home Assistant 的世界观

“家庭状态操作系统”

设备 => 抽象为实体 => 实体有状态 => 状态变化触发自动化 => 自动化执行服务


Integration (集成) = 驱动 + 协议栈

一个设备想接入 HA，通过 Integration 实现
- 米家 / HomeKIt / MQTT / ESP / Modbus / 蓝牙
- 每一个集成：
  - 如何发现设备
  - 如何读状态
  - 如何发控制指令


Device(设备) 和 Entity(实体) 的概念

Device(设备) 为真实存在的，如
- 一个插座
- 一个台灯
- 一个手机
- 一个 ESP32

Entity(实体) 为设备上具备的“能力/状态点”

一个设备 = 多个实体


比如一个灯(device)的实体(entity)
- `light.xxx`  开关
- `light.xxx_brightness` 亮度
- `sensor.xxx_power` 功率
- `sensor.xxx_temp` 温度

HA 在操作状态，整个系统就是一个状态机。



State(状态)为系统真正关心的东西，HA 以状态为核心

每个 entity 都有
- `state` 主状态
- `attributes` 附加属性

比如
```yaml
state: "on"
attributes:
  brightness: 180
  color_temp: 370
```


动化、面板、历史记录全部都是围绕 state 在转.

可以把 HA 当成一个：持续运行的、全家状态数据库 + 事件系统


看起来智能的几个功能

Automation(自动化)，规则引擎

Automation = Trigger + Condition + Action

一些物联网最经典的结构
```
当 发生了某件事
如果 满足一些条件
那么 执行一些动作
```

如

```
当 `sensor.motion == on`
且 `sun == below_horizon`
那么 `light.turn_on`
```


本质上，事件驱动系统

相似的一些系统
- topic + callback
- INT + handler



Script(脚本) ，可以复用的动作序列

script 是 一串 action，可以被 Automation 调用，被面板按钮点击，被语音触发。

script = 没有状态的 Action 流程，

如果 Automation 是 if / when ，那么 script 就是 do。


Action(服务)，“系统调用”

HA 里真正执行动作的是 Action，

比如
- light.turn_on
- climate.set_temperature
- notify.mobile_app_iphone


automation 和 script，本质是在调 动作。


面板是状态的可视化，的入口。




## 一个演示

手动触发一个动作，

全局的通知。

动作中，


notify.persistent_notification



做一个最简单的自动化


利用现有的 entity，

手机电池，提供了两个状态，

battery，level 和 state



<img src="http://10.0.0.202:8080/?action=stream" />




