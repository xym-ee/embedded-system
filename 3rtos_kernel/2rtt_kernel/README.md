---
sort: 2
---
# rt-thread kernel

通用计算机的典型设备是鼠标、键盘、显示器。对于MCU来说，片内外设是设备。

这也很好理解，笔记本电脑把显示器和键盘都做成了一个整体，但是这些部分仍然是外设。MCU则把CPU，存储器和各种外设做到了一个硅片上，这也是“单片机”这个名字的由来。

裸机上使用设备是基于STD库或者HAL库来操作，距离寄存器是比较近的，非常靠近硬件。

操作系统的作用就是屏蔽硬件，提供接口。使得应用程序运行在不同芯片上的代码都一样。

很典型的一个游戏安装在任意一台电脑上玩起来都是一样的。

嵌入式操作系统也是要追求这个目的。因此RTT的驱动框架实际上站在了更高的角度考虑不同型号的MCU，同类不同厂家的设备，在此基础上找出共同点，做出相同的调用接口。

基于上述思路，RTT外设使用的源码的复杂也可以理解了，复杂是为了使用的简单。

## RT-Thread 启动流程

从系统通电到进入 `main()` ，来看看这期间发生了什么事情。

我们从代码推测电路系统的运行，代码离最终的机器码序列还有段距离。RT-Thread 支持不同的编译器和不同芯片，因此代码略微有差异，但是都是先从 `.s` 汇编启动文件开始运行，然后执行 RT-Thread 的启动函数 `rtthead_startup()` ，最后进入用户入口函数 `main()` ，来自官方文档的一张图：

<figure>
    <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/basic/figures/rtt_startup.png" width=1200 />
</figure>

可以看出这期间还是做了不少事情的，芯片上电后，先运行汇编代码 `startup_stm32f103xe.s` ，然后跳转到 C 代码，进行 RT-Thread 系统功能初始化，最后才执行 `main()` 。

在使用 ARM CC 编译器时，用到了 `$Sub$$` 和 `$Super$$` 语法， `$Sub$$` 的含义是在程序执行前前插入一段新程序， 有点打补丁的意思。这个 `$Sub$$main` 可以先调用一些要补充在 `main` 之前的功能函数然后调用 `$Super$$main` 正式运行 `main()` 。正好这就是系统启动的功能，很合理，很符合使用裸机的思路，只关注 `main()` 即可。

主函数在文件 `components.c` 里“打了个补丁”，
```c
int $Sub$$main(void)
{
    rt_hw_interrupt_disable();
    rtthread_startup();
    return 0;
}
```
`$Sub$$main` 里调用了 `rtthread_startup();` 的，它也定义在这个源文件里：

```c
int rtthread_startup(void)
{
    rt_hw_interrupt_disable();

    /* 板级初始化：需在该函数内部进行系统堆的初始化 */
    rt_hw_board_init();

    /* 打印 RT-Thread 版本信息 */
    rt_show_version();

    /* 定时器初始化 */
    rt_system_timer_init();

    /* 调度器初始化 */
    rt_system_scheduler_init();

#ifdef RT_USING_SIGNALS
    /* 信号初始化 */
    rt_system_signal_init();
#endif

    /* 由此创建一个用户 main 线程 */
    rt_application_init();

    /* 定时器线程初始化 */
    rt_system_timer_thread_init();

    /* 空闲线程初始化 */
    rt_thread_idle_init();

    /* 启动调度器 */
    rt_system_scheduler_start();

    /* 不会执行至此 */
    return 0;
}

```

这个函数启动了与系统相关的硬件、内核对象、系统设备、各应用线程。更细致的分为四个部分：
- 初始化与系统相关的硬件；
- 初始化系统内核对象，例如定时器、调度器、信号；
- 创建 main 线程，在 main 线程中对各类模块依次进行初始化；
- 初始化定时器线程、空闲线程，并启动调度器。

`rt_hw_board_init();` 函数里完成了系统时钟设置、串口初始化、并把终端绑定到串口。

只有在启动调度器后，创建好的线程才会根据规则运行起来。






## 程序内存分布

MCU 有的存储空间：片内 Flash 和片内 RAM ，编译完成的程序会包含几种类型的数据存放在 MCU 不同的存储区。在 Keil 里编译完成后在 Build Output 串口会哟编译输出信息：
```
linking...
Program Size: Code=48008 RO-data=5660 RW-data=604 ZI-data=2124
After Build - User command \#1: fromelf --bin.\\build\\rtthread-stm32.axf--output rtthread.bin
".\\build\\rtthread-stm32.axf" - 0 Error(s), 0 Warning(s).
Build Time Elapsed: 00:00:07
```

上面提到的 Program Size 包含以下几个部分：
- Code：代码段，存放程序的代码部分；
- RO-data：只读数据段，存放程序中定义的常量；
- RW-data：读写数据段，存放初始化为非 0 值的全局变量；
- ZI-data：0 数据段，存放未初始化的全局变量及初始化为 0 的变量；

编译完工程会生成一个 .map 的文件，该文件说明了各个函数占用的尺寸和地址，在文件的最后几行也说明了上面几个字段的关系：

```
==============================================================================

    Total RO  Size (Code + RO Data)                 9352 (   9.13kB)
    Total RW  Size (RW Data + ZI Data)              2048 (   2.00kB)
    Total ROM Size (Code + RO Data + RW Data)       9404 (   9.18kB)

==============================================================================
```

RO 表示程序占用 Flash 的大小， RW 表示了程序运行时占用 RAM 的大小， ROM 表示烧写程序占用的 Flash 大小。

烧录到 STM32 为 bin 或者 hex 文件，称为**可执行映像文件**，映像文件在 Flash 里的内存分布和 MCU 上电后在 RAM 里的内存分布略有区别：

<figure>
    <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/basic/figures/03Memory_distribution.png" width=550 />
</figure>

可执行映像文件包含了 RO 和 RW 两部分，未初始化或者初始化为 0 的变量不占用映像存储空间。

STM32 默认上电后从 Flash 启动，启动后有个把 RW 段数据搬到 RAM 的过程，RO 段的数据不会动，也就是说 CPU 可以直接在 Flash 上读代码。此外对于 ZI 数据，根据编译器给出的地址和大小分配 ZI 段，并清零。


```
Flash 只读不写， RAM 断电丢失数据。可以直接原地执行代码的设备称为XiP设备，比如 NOR Flash，直接挂在数据总线上。

此外还有 SPI Flash ，SPI 接口显然和总线接口不一样，因此需要把里面的内容搬到一个可以被数据总线读取的地方，大概是这么个思路。
```

剩下的没使用的 RAM 内存空间就是**动态内存堆**，在向操作系统请求内存时，分配的都是这一部分的。比如说一个小李子：
```c
rt_uint8_t *msg_ptr;
msg_ptr = (rt_uint8_t*)rt_malloc(128);
rt_memset(msg_ptr, 0, 128);
```
指针 `msg_ptr` 指向了一个 128 Byte 的内存堆，并把值全部设置为0。

RW 段存放有初值的全局变量，ZI 段存放初值为0的全局变量。

## RT-Thread 自动初始化机制

自动初始化指的是初始化函数不需要被显式调用，只需要通过一个宏定义方式进行声明，就会在系统启动过程中被执行。

举个例子：
```c
int rt_hw_usart_init(void)  /* 串口初始化函数 */
{
     ... ...
     /* 注册串口 1 设备 */
     rt_hw_serial_register(&serial1, "uart1",
                        RT_DEVICE_FLAG_RDWR | RT_DEVICE_FLAG_INT_RX,
                        uart);
     return 0;
}
INIT_BOARD_EXPORT(rt_hw_usart_init);    /* 使用组件自动初始化机制 */
```

`INIT_BOARD_EXPORT(rt_hw_usart_init)` 就可以实现在系统启动时自动运行这个函数。

这种声明的函数是被 `rt_components_board_init()` 与 `rt_components_init()`，调用的。


rt_components_board_init() 函数执行的比较早，主要初始化相关硬件环境，执行这个函数时将会遍历通过 INIT_BOARD_EXPORT(fn) 申明的初始化函数表，并调用各个函数。

rt_components_init() 函数会在操作系统运行起来之后创建的 main 线程里被调用执行，这个时候硬件环境和操作系统已经初始化完成，可以执行应用相关代码。rt_components_init() 函数会遍历通过剩下的其他几个宏申明的初始化函数表。


## 内核对象模型

内核对象实际就是内核里面这些东西，这些东西是如何实现出来的，实现的时候用了面向对象的思想。

<figure>
    <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/programming-manual/basic/figures/03kernel_object2.png
" width=600 />
</figure>

这个图表示了内核里这些东西的关系，他们都需要名字，因此有个基类，在基类上扩展自己的属性。

上图中由对象控制块 rt_object 派生出来的有：线程对象、内存池对象、定时器对象、设备对象和 IPC 对象（IPC：Inter-Process Communication，进程间通信。在 RT-Thread 实时操作系统中，IPC 对象的作用是进行线程间同步与通信）；由 IPC 对象派生出信号量、互斥量、事件、邮箱与消息队列、信号等对象。

对象控制块 rt_object 的数据结构：
```c
struct rt_object
{
    /* 内核对象名称     */
    char      name[RT_NAME_MAX];
    /* 内核对象类型     */
    rt_uint8_t  type;
    /* 内核对象的参数   */
    rt_uint8_t  flag;
    /* 内核对象管理链表 */
    rt_list_t   list;
};

```

内核对象容器的数据结构
```c
struct rt_object_information
{
    /* 对象类型 */
    enum rt_object_class_type type;
    /* 对象链表 */
    rt_list_t object_list;
    /* 对象大小 */
    rt_size_t object_size;
};
```

一类对象由一个 rt_object_information 结构体来管理，每一个这类对象的具体实例都通过链表的形式挂接在 object_list 上。而这一类对象的内存块尺寸由 object_size 标识出来（每一类对象的具体实例，他们占有的内存块大小都是相同的）。







