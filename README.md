
![GitHub last commit](https://badgen.net/github/last-commit/xym-ee/embedded-system/main)
![Github commits](https://badgen.net/github/commits/xym-ee/embedded-system/main)
![no problems](https://badgen.net/badge/no%20problem/(maybe)/red)

嵌入式系统学习。

[如何学习嵌入式系统？ - 知乎](https://www.zhihu.com/question/19688487/answer/32217959)

这个回答下面还有个回答：

如果是学计算机的，那么学嵌入式不会有门槛。

如果不是学计算机的，那么忘了嵌入式，先学习计算机。


## 这个笔记的框架


- [ ] MCU 裸机开发，8051、MSP430、arm 内核的 STM32、NXP i.mx rt 等
  - [ ] 通信接口
  - [ ] 8bit、16bit mcu
  - [ ] arm 芯片开发，芯片本身，外设，固件库的使用等
  - [ ] 软件框架，系统架构，(状态机、订阅发布、事件触发、任务调度)
- [ ] 中等规模系统开发，编程思维(C 语言 OOP 思想)
  - [ ] 裸机 LVGL 图形库
  - [ ] 基于 rtos 开发 (rt-thread 和 freeRTOS)
- [ ] ARMv7-M 架构与 RTOS 原理
  - [ ] Cortex-M3 内核，指令集、中断、体系结构等
  - [ ] rt-thread 内核、驱动
- [ ] linux 应用开发(系统编程+GUI)
  - [ ] ubuntu 相关、linux 使用、
  - [ ] shell 编程、vim、gcc、makefile
  - [ ] 网络编程、多线程
- [ ] Linux 驱动开发
  - [ ] linux 系统构建：bootloader、kernel、device tree、root filesystem
  - [ ] 各种驱动框架





## 嵌入式系统

(2023.7)

嵌入式的几个阶段

裸机，直接使用芯片，猛糙快，非常靠近寄存器，不会太细致的区分层次。

项目大到一定程度以后，出现了代码维护上的困难，编码规范和思想。

为了更容易处理更多的事情，开始基于 RTOS 去实现一些东西。

出于性能的考虑(更快的芯片)，或者安全性、通用性的考虑，或者更大的项目的分工，需要一套更成熟、更标准化、提供更多基础设施的框架：linux。

更严格的要求：fpga

(2023.4)

MCU 裸机开发、LVGL 以及基于 rt-thread 开发是在面向应用，现称为一个东西的熟练使用者，在去看背后的原理以及实现。个人觉得从刚开始接触 MCU 比如 STM32，到能做出一个简单的电子系统，这个过程有个两三个月足够了，基于 ST 库开发，不同的外设的操作方式实际上是类似的，可能学习GPIO的时候，会跟着教程去细致的看外设内部的原理图，但是一旦用代码操作起来，都是模式化的东西。在能自己独立设计出一个不是那么小的电子系统后，我认为应该再往上走一个层次，去注意软件工程，或者说编码思想方面的东西了，先不着急去做更大的系统。

搞MCU大多是学电气电子或者自动化的同学，写代码很多时候都是猛糙快，讲究个能用就行，如果在熟练使用MCU后停留在这个阶段，对职业发展是不利的。因此我觉得在觉得自己玩熟了MCU，了解了大多数外设后，可以尝试去玩玩一些与外设耦合不那么紧密的代码，比如 LVGL，显示框架本身是硬件无关的，再比如rtthread本身也是，这些大一些的 C 语言项目都是有一套自己的思想以及设计方法在里面的，而且这些东西不仅仅适用于 MCU 平台，举个例子，机器人仿真用的 webots，可以使用 C 语言开发算法，里面的程序表达

```c
WbDeviceTag left_front_motor = wb_robot_get_device("left_front_motor");
wb_motor_set_position(left_front_motor,INFINITY);
wb_motor_set_velocity(left_front_motor,0);
```

对比 lvgl 里的程序表达

```c
/*Create a screen*/
lv_obj_t * scr = lv_obj_create(NULL, NULL);
lv_scr_load(scr);          /*Load the screen*/

/*Create 2 buttons*/
lv_obj_t * btn1 = lv_btn_create(scr, NULL);         /*Create a button on the screen*/
lv_btn_set_fit(btn1, true, true);                   /*Enable automatically setting the size according to content*/
lv_obj_set_pos(btn1, 60, 40);              	   /*Set the position of the button*/

lv_obj_t * btn2 = lv_btn_create(scr, btn1);         /*Copy the first button*/
lv_obj_set_pos(btn2, 180, 80);                    /*Set the position of the button*/

/*Add labels to the buttons*/
lv_obj_t * label1 = lv_label_create(btn1, NULL);	/*Create a label on the first button*/
lv_label_set_text(label1, "Button 1");          	/*Set the text of the label*/

lv_obj_t * label2 = lv_label_create(btn2, NULL);  	/*Create a label on the second button*/
lv_label_set_text(label2, "Button 2");            	/*Set the text of the label*/

/*Delete the second label*/
lv_obj_del(label2);
```

还有 rtthread 里线程创建的

```c
/* 线程示例 */
int thread_sample(void)
{
    /* 创建线程 1，名称是 thread1，入口是 thread1_entry*/
    static rt_thread_t tid1 = rt_thread_create("thread1",
                            thread1_entry, RT_NULL,
                            THREAD_STACK_SIZE,
                            THREAD_PRIORITY, THREAD_TIMESLICE);

    /* 如果获得线程控制块，启动这个线程 */
    if (tid1 != RT_NULL)
        rt_thread_startup(tid1);

    return 0;
}

/* 导出到 msh 命令列表中 */
MSH_CMD_EXPORT(thread_sample, thread sample);
```

甚至 Linux 环境下 socket 编程

```c
int main(){
    //创建套接字
    int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    //将套接字和IP、端口绑定
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));  //每个字节都用0填充
    serv_addr.sin_family = AF_INET;  //使用IPv4地址
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  //具体的IP地址
    serv_addr.sin_port = htons(1234);  //端口
    bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    //进入监听状态，等待用户发起请求
    listen(serv_sock, 20);
    //接收客户端请求
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);
    int clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);
    //向客户端发送数据
    char str[] = "http://c.biancheng.net/socket/";
    write(clnt_sock, str, sizeof(str));
   
    //关闭套接字
    close(clnt_sock);
    close(serv_sock);
    return 0;
}
```
这些代码都是类似的，都是定义一个东西等于一个函数的返回值，然后用不同方法操作这个东西。HAL 库里有些东西也是这样，但是 HAL 库还是和STM32硬件本身耦合的比较紧。

在学习使用 LVGL 时会熟悉 C 的一些编程方法和思想，比如 C 中继承，这种思想在 gui 上是可视化的，很容易理解。如果自己写过网站的话，css 样式控制代码里更是如此。在此基础上去使用 rt-thread 的成本就比较低了，只需要稍稍理解一下线程的概念，就能轻松的让多任务跑起来，而且手册中的 OOP 思想也因为有 lgvl 的对比理解，不那么抽象了。

熟练使用 rtos 大约也要花个几个月的时间，这时候应该可以很容易的实现出更大规模的系统。

熟练的基于 rtos 开发后，一方面可以去试着基于 linux 去开发对运算要求更高的应用，也可以去看看 linux 驱动开发，也可以在 linux 上玩玩，有了前面的基础，玩linux 也不困难。同时也可以去看看 rtthread 的实现原理，这是一个中等规模的 C 语言项目，同时也能学习操作系统的一些知识，rtt 里面好多东西在 linux 里都能找到影子 比如 menuconfig 工具，自动初始化机制的宏定义，甚至驱动框架都有借鉴的地方。



(2022.6)

嵌入式的领域过于宽广，洗衣机控制系统、手机、甚至树莓派都可以叫做嵌入式平台，Nvidia 把自己推出的小型 AI 计算机也叫做嵌入式边缘计算平台，所以我用一句话总结嵌入式：除了日常使用的通用电脑之外其他的可以跑代码的、有 CPU 、需要写程序的计算设备。

<figure>
  <img src="./assets/images/nvdia.png" width=300 >
  <figcaption>
  NVIDIA 官网对 Jetson 的介绍
  </figcaption>
</figure>

<figure>
  <img src="./assets/images/jetson.png" width=400 >
  <figcaption>
  Jetson NANO 开发套件，工控造型的nano
  </figcaption>
</figure>

除了这些比较贵的，像一台电脑可以运行 Linux 的嵌入式设备，也有结构简单，偏底层应用的芯片。

<figure>
  <img src="./assets/images/arm.png" width=500 >
  <figcaption>
  arm cortex-m 内核，ST、GD、NXP的芯片
  </figcaption>
</figure>

这些芯片的内核，或者叫 CPU 都是 ARM 公司设计的，通用 PC 一般来讲都是 x86 架构（Mac 上用的 M1 是个例外），这也是嵌入式系统的一个特征。




## 一些想法

- 2022/10/18
  - 嵌入式软件。程序设计。最近在学抽象数学，数学的发展在一步步抽象，在学习矩阵分析的时候，会发现微积分里的运算、函数，线性代数中的欧几里得空间居然都变成了矩阵分析里的实例，矩阵分析像是一个类，各种东西抽象出一个通用的思想，共性的东西。程序设计也是在一步步从底层向上抽象，这两种不同的东西是否有一些联系呢？思维上相同的东西。比如C++的类和对象，线性代数本身像是一个抽象的类，实例化后有欧几里得空间、状态空间，各种空间。甚至矩阵分析里的各种运算符，要格外的关注其含义，即运算的空间，+的含义是不同的(抽象空间的+或数域的+)，这一点C++有运算符重载这个特性，居然可以直接去实现出来矩阵分析里的一些思想，抽象类相加的含义。
