---
sort: 3
---
# 基于 RTOS 开发

先学如何使用 RTOS，如何创建线程，实现线程之间的通信，让多任务协同运行，推动系统向前运转。用别人写好的库，实现出来的驱动。

学习 rt-thread 与 freeRTOS 的接口使用。

## RT-Thread 介绍

首先 RT-Thread 是国内团队开发的，一些文档都是原生中文，很好。

RT-Thread 用 C 语言实现，但是又卖你先对象的设计方法，不仅仅是 RTOS 本身，其设计思想、代码风格、系统架构也是非常值得研究学习的。

除了用于传统工业控制领域，这也是个**物联网操作系统**( IoT OS )。

感觉 IoT OS 更像是一些列技术的集合，也没有具体的教科书定义，其指的是含操作系统的、包括文件系统图形库等比较完成的中间组件，具备低功耗、链接云端能力的软件。

FreeRTOS、μC/OS 这两种 RTOS 实际上仅仅有个“内核”， RT-Thread 除了实时内核，还有特别丰富的中间层组件。


<figure>
    <img src = "https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/figures/02Software_framework_diagram.png" width=600 />
    <figcaption>RT-Thread 架构（官方文档）</figcaption>
</figure>

- 内核指的是多线程实现、RTOS 使用的接口、内存管理等CPU实现多任务最基础的东西。
- 组件和服务层在基于内核上，提供了上层的一些软件
- 软件包是 RT-Thread 的特色，生态的问题


## freeRTOS 介绍


## 用户入口

前面是必要的内核启动，对于用户程序，还是经典的 `main()` 函数，这里也能看出前面定义 `$Sub$$main()` 的含义，这是函数标识符，具体可以参考[ARM® Compiler v5.06 for µVision® armlink User Guide](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0377g/pge1362065967698.html)。


```c
int main(void)
{
  /* user app entry */
  return 0;
}
```

这么设计符合以前不用RTOS的开发者的习惯，只是用就可以了，不需要关注应用之外的东西。


## RTOS 点灯

这是一个线程，

```c
int led(void)
{
    rt_uint8_t count;

    rt_pin_mode(34, PIN_MODE_OUTPUT);  
    
    for(count = 0 ; count < 10 ;count++)
    {       
        rt_pin_write(LED_PIN, PIN_HIGH);
        rt_kprintf("led计数 : %d\r\n", count);
        rt_thread_mdelay(500);
        
        rt_pin_write(LED_PIN, PIN_LOW);
        rt_kprintf("led off\r\n");
        rt_thread_mdelay(500);
    }
    return 0;
}
MSH_CMD_EXPORT(led1, LED test);
```


## 目录

这一部分侧重开发，只用接口，理解操作系统的设计思想，并不追求背后的实现。在下一部分要去研究内核的实现。

- 基于 RTT 特性进行 MCU 开发
  - RTOS 多线程的思想
  - 线程管理
  - 线程同步
  - 线程通信

- 基于 RTT 驱动使用设备


- 已有芯片的 bsp 制作

- 已有驱动的适配

- env工具与语法








