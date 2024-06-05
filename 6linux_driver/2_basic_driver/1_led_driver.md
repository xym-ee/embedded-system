---
sort: 1
---
# led 驱动开发


- linux 模块，虚拟设备
- 字符设备驱动框架
- 常用 api


## 驱动思路，分层设计

一个关键的结构体，`linux/fs.h`

驱动的加载有两种方式，一种是直接编译到内核里去，最后就在 zImage 里。

也可以编译成模块，即 `*.ko` 调试的时候，我们可以编译成模块，测试的时候加载模块就好了。


## 模块加载与卸载


```c
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>


static int __init xxx_init(void)
{
    printk();

    return 0;
}

static void __exit xxx_exit(void)
{
    
}


module_init(xxx_init);
module_exit(xxx_exit);
```

编译后，可以使用指令 `insmod` 加载模块。`rmmod` 卸载

- modprobe 功能
- printk 函数消息级别


## 开发环境


## 设备的注册与注销



设备号 `dev_t` 是一个 u32 类型整数。高12位主设备号，低20位次设备号。

主设备号为一类设备。如 IIC 设备类型下面，挂许多具体的器件。

设备号操作的相关宏定义。
```c
#define MINORBITS	20
#define MINORMASK	((1U << MINORBITS) - 1)

#define MAJOR(dev)	((unsigned int) ((dev) >> MINORBITS))
#define MINOR(dev)	((unsigned int) ((dev) & MINORMASK))
#define MKDEV(ma,mi)	(((ma) << MINORBITS) | (mi))
```

此函数，只制定了主次设备号。比较老的函数了。需要手动去看那些号没使用。
`static inline int register_chrdev(unsigned int major, const char *name, const struct file_operations *fops)`

使用 `cat /proc/devices` 查看主设备号。


## 地址映射 api

虚拟内存到物理内存的映射。

512M DDR 挂载物理地址的 0x80000000-0x9fffffff 上，芯片里外设的寄存器也是挂在物理地址上。

但是 32 位机器跑了操作系统后，每个进程可以使用的地址空间是 4GB，0x00000000 - 0xffffffff。

想点灯，就要操作 GPIO 相关的寄存器，GPIO 的寄存器在物理地址上，但是进程里操作的都是虚拟地址，所以首先需要知道 GPIO 相关的寄存器的物理地址在虚拟地址里面是什么。

这个需求是合理的，所以内核源码里提供了这个功能，在 `arch/arm/include/asm/io.h` 中

- `#define ioremap(cookie,size) __arm_ioremap((cookie), (size), MT_DEVICE)`
  - `cookie` 需要映射到虚拟空间的起始物理地址
  - `size` 要映射的内存空间大小
  - 返回映射后虚拟空间的首地址
- `void iounmap (volatile void __iomem *addr)`
  - 驱动卸载时，要释放内存
  - `size` 要映射的内存空间大小
  - 返回映射后虚拟空间的首地址


## I/O 内存访问 api

独立编址与存储器映射IO
- x86 体系下，内存地址空间和IO地址空间独立，读写内存的指令是 `MOV` ，读写寄存器的指令是 `IN` 和 `OUT`
- ARM 体系下，全部都在内存地址空间上，即存储器映射IO，

读写映射后的内容的叫法
- 外面的寄存器或者存储器映射到 IO 地址空间，这时候叫**I/O端口**
- 外面的寄存器或者存储器映射到内存地址空间，这时候叫**I/O内存**

虽然使用 ioremap 映射后，用户空间已经可以直接使用指针来访问了，但是为了安全考虑，linux kernel 提供了一组 api 来操作映射后的内存
- 读操作
  - `u8 readb(const volatile void __iomem *addr)`
  - `u16 readw(const volatile void __iomem *addr)`
  - `u32 readl(const volatile void __iomem *addr)`
- 写操作
  - `void writeb(u8 value, volatile void __iomem *addr)`
  - `void writew(u16 value, volatile void __iomem *addr)`
  - `void writel(u32 value, volatile void __iomem *addr)`



## 硬件

参考硬件原理图与芯片寄存器手册。

LED 接在 GPIO1_IO03，需要关注的点
- 配置引脚复用为 GPIO，要关注的寄存器
  - SW_MUX_CTL_PAD_ 配置引脚复用功能
  - SW_PAD_CTL_PAD_ 配置引脚电气属性
- GPIO 时钟的使能
  - CCM 有 7 个寄存器用来开关时钟
  - GPIO1 时钟配置在 CCM_CCGR1 寄存器中 bit27-26
- 查看 Chapter 28 关于 GPIO 寄存器的介绍，需要关注的寄存器有
  - GPIO direction register (GPIO_GDIR) 配置方向
  - Data register (GPIO_DR) 数据
  
不使用引脚中断的话关注这些就够用了。

手册中，相关寄存器对应的地址
- CCM_CCGR1 
  - 0x020C406C
- SW_MUX_CTL_GPIO1_IO03
  - 0x020E0068
- SW_PAD_CTL_GPIO1_IO03
  - 0x020E02F4
- GPIO1_DR
  - 0x0209C000
- GPIO1_GDIR
  - 0x0209C004


## 字符设备驱动注册的另一种方法

前面注册用的 api 我们手动分配了主设备号，在分配前还要手动查一下哪个号没有被用掉。因此，需要一些更好用的 api。

- 自动分配一个设备号，可以用下面这个函数
  - `int alloc_chrdev_region(dev_t *dev, unsigned baseminor, unsigned count, const char *name)`
- 指定设备号，也可以使用和前面不一样的这个 api
  - `int register_chrdev_region(dev_t from, unsigned count, const char *name)`
- 设备注销，使用下面这个函数释放
  - `void unregister_chrdev_region(dev_t from, unsigned count)`

