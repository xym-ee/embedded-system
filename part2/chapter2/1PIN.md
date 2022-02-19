---
sort: 2
---
# PIN设备

## 接口

常用的 PIN 设备的 API 有以下几个：

| API                 | 描述                       |
| ------------------- | -------------------------- |
| `rt_pin_mode`       | 设置 GPIO 模式             |
| `rt_pin_write`      | 输出电平                   |
| `rt_pin_read`       | 读取 GPIO 输入电平         |
| `rt_pin_attach_irq` | 挂载 GPIO 外部中断回调函数 |
| `rt_pin_detach_irq` | 脱离 GPIO 外部中断回调函数 |
| `rt_pin_irq_enable` | 配置 GPIO 外部中断开关     |



PIN设备的使用步骤：
- 使用 rt_pin_mode 函数将驱动 LED 的 IO 口初始化为推挽输出模式，
- 使用 rt_pin_write 函数来控制 IO 口的电平高低，
- 使用 rt_pin_read 函数来读取 IO 口的电平高低。


## LED

LED 模块是最简单的一个模块，它只需要有几个API 即可，像初始化、开/关、翻转即可。

```c
/* led.h */
#ifndef APPLICATIONS_LED_H_
#define APPLICATIONS_LED_H_

#define LED1 122
#define LED2 123

int led_init(void);
int led_on(void);
int led_off(void);
int led_toggle(void);

#endif
```


```c
/* led.c */
#include <rtdevice.h>
#include "led.h"

int led_init(void)
{
    /* 设定 LED 引脚为推挽输出模式 */
    rt_pin_mode(LED1, PIN_MODE_OUTPUT);
    return 0;
}


int led_on(void)
{
    /* 调用 API 输出低电平 */
    rt_pin_write(LED1, PIN_LOW);
    return 0;
}

int led_off(void)
{
    /* 调用 API 输出高电平 */
    rt_pin_write(LED1, PIN_HIGH);
    return 0;
}

int led_toggle(void)
{
    /* 调用 API 读出当前电平 然后输出相反电平 */
    rt_pin_write(LED1, !rt_pin_read(LED1));
    return 0;
}
```

下面是一段控制 LED 灯每隔 500 ms 闪烁一次的函数，运行的结果如下图所示。

```c
/* main.c */
#include <rtthread.h>
#include "led.h"

int main(void)
{
    /* user app entry */
    led_init();
    led_on();
    while (1)
    {
        led_toggle();
        rt_thread_mdelay(500);
    }

    return 0;
}
```



