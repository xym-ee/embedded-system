---
sort: 1
---
# 字符设备驱动基础


## hello driver 模块


每个内核模块都有一个 `init()` 函数和一个 `exit()` 函数。`init()` 函数在驱动加载的时候执行，`exit()` 函数则在驱动移除的时候被调用。`init()` 函数让操作系统知道驱动具备什么样的能力，以及具体事件（比如，将驱动注册到总线、注册一个字符设备等）发生时应该调用驱动的哪个函数。`exit()` 函数必须释放所有 `init()` 函数请求的资源。

```c
#include <linux/module.h>

static int __init hello_init(void)
{
    pr_info("hello driver init\n");
    return 0;
}

static void __exit hello_exit(void)
{
    pr_info("hello driver exit");
}

module_init(hello_init);
module_exit(hello_exit);


MODULE_LICENSE("GPL");
MODULE_AUTHOR("xym");
MODULE_DESCRIPTION("print out \"hello driver\" ");
```

内核中常用 `printk()` 来输出信息。可以指定日志级别，级别定义在 `include/linux/kern_levels.h` 比如
- `printk(KERN_ERR "something wrong\n");`

`pr_info()` 是对 printk 的封装，定义在 `include/linux/printk.h` ，快捷调用。



驱动模块会用到一些内核的 API，因此需要使用到内核源码，makefile 里要作相应的配置

```makefile
KERNELDIR := /home/m/kernel					# 指定 kernel 所在的目录
CURRENT_PATH := $(shell pwd)				# 当前工作路径
obj-m := main.o

build: kernel_modules						# 生成目标


# -C 切换到内核目录，里面指定了交叉编译器。此外模块的源码路径也指定了，modules 为编译模块
kernel_modules:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) modules

clean:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) clean
```

直接 make 就会得到一个 `*.ko` 文件。

内核中向控制台输出内容，`printfk`


### 模块加载和卸载

linux 驱动可以编译到 kernel 中(zImage)，一般来说编译为模块 `*.ko` ，测试的时候加载就行。加载和卸载命令
- `insmod xx.ko` 最简单的模块加载命令，加载指定模块，无法解决模块依赖关系
- `modprobe xx.ko` 分析依赖关系，加载所有以来模块，此命令去 `/lib/modules/<kernel-version>` 中查找
  - 可以手动创建 `/lib/modules/4.1.15+` 然后吧模块放到此目录，执行 `modprobe`
  - 新模块使用此命令时，要向用 depmod 命令
- `rmmod  xx.ko` 卸载驱动
- `lsmod` 查看模块 
- `modinfo xx.ko` 查查看模型信息


## 带参数的模块

module_param() 来实现传入参数，S_IRUGO 表示所有人都可以从 sysfs 里读这个参数。

```c
#include <linux/module.h>

static int para = 5;

module_param(para, int, S_IRUGO);

static int __init hello_init(void)
{
    pr_info("hello driver init, parametet = %d\n", para);
    return 0;
}

static void __exit hello_exit(void)
{
    pr_info("hello driver exit");
}

module_init(hello_init);
module_exit(hello_exit);


MODULE_LICENSE("GPL");
MODULE_AUTHOR("xym");
MODULE_DESCRIPTION("print out \"hello driver\" ");

```

用法

```bash
insmod hello_para.ko
insmod hello_para.ko para=20
cat /sys/module/hello_para/parameters/para
```

## 计时模块


```c
#include <linux/module.h>
#include <linux/time.h>

static struct timeval start_time;

static int para = 5;
module_param(para, int, S_IRUGO);


static void print_hello(void)
{
    int i;
    for (i = 0; i<para; i++)
        pr_info("[%d/%d] hello\n", i, para);
}

static int __init hello_init(void)
{
    do_gettimeofday(&start_time);
    pr_info("module init\n");

    print_hello();

    return 0;
}

static void __exit hello_exit(void)
{
    struct timeval end_time;
    do_gettimeofday(&end_time);

    pr_info("time duration %ld seconds\n", end_time.tv_sec - start_time.tv_sec);

    pr_info("hello driver exit");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("xym");
MODULE_DESCRIPTION("print out \"hello driver\" ");
```


`struct timeval` 结构体定义

```c
struct timespec {
	__kernel_time_t	tv_sec;			/* seconds */
	long		tv_nsec;		/* nanoseconds */
};
```

使用 `kernel/time/keeping.c` 中的 `do_gettimeofday()` 来获取时间信息。


## 字符设备驱动简介

操作系统被设计为对用户应用隐藏底层硬件细节。

但是，应用程序也有访问外设数据的需求，也需要向外设输出数据的需求。

外设的寄存器只能由 Linux 内核访问，因此 Linux 需要一种能够将数据从内核态传给用户态的机制。

这种数据的传输通过**设备节点**来处理，这些设备节点也称作**虚拟文件**。

设备节点存在于根文件系统中，尽管它们并不是真正的文件。当用户读取设备节点时，内核将底层驱动捕获的数据流拷贝到应用程序的内存空间。当用户写设备节点时，内核将应用程序提供的数据流拷贝到驱动程序的数据缓冲区，这些数据最终向底层硬件输出。

这些虚拟文件可以被用户应用程序通过标准的系统调用方式打开、读取或者写入。

用户应用程序的请求最终被送往驱动核心，每个设备都有专门的驱动来处理这些请求。Linux支持三种类型的设备：字符设备、块设备以及网络设备。

每种设备在驱动上的差异主要体现在文件的打开、读取和写入行为上。

字符设备是最常见的设备，这种设备的读写直接进行而无须经由缓冲区，比如键盘、显示器、打印机、串口等。块设备的读写以块大小为单位，一次读写整数倍的块大小，块大小一般为512或者1024字节。它们可以被随机读取，任何块都可以被读取，不管它们在设备的什么位置。一个典型的块设备的例子就是硬盘驱动器。网络设备则通过BSD套接字接口和网络子系统来访问。

比如在终端 `ls -l` 就可以看到设备类型。

从应用程序的角度看，一个字符设备本质上就是一个文件。进程只知道一个 `/dev` 文件路径。进程通过 `open()` 系统调用打开文件，通过 `read()` 和 `write()` 来执行标准的文件操作。

了实现上述目标，字符设备驱动必实现 `file_operations` 数据结构中描述的各种操作并注册它们。`file_operations` 数据结构定义在 `include/linux/fs.h` 中。

Linux 文件系统层负责确保调用驱动相关的操作，这些操作在用户态应用程序执行相应的系统调用时被触发（在内核部分，驱动负责实现并注册这些回调操作）。

内核驱动通过 `copy_from_user()` 和 `copy_to_user()` 这两个特定的函数与用户态应用程序交换数据。


在Linux中，设备通过两个设备号来标识：一个主设备号和一个从设备号。这些设备号可以通过调用 `ls -l/dev` 查看。设备驱动将自己的主设备号注册到内核并负责管理从设备号。当访问一个设备文件时，主设备号决定了执行输入/输出操作时调用哪个设备驱动。访问设备时，内核使用主设备号来识别正确的设备驱动。从设备号的使用则取决于具体设备，由驱动负责。比如，i.MX7D 有多个物理 UART 端口。同样的驱动被用于控制所有的 UART 设备。但是每个物理 UART 需要自己的设备节点，因此这些UART设备节点具有相同的主设备号，但从设备号
各不相同。

## hello 字符设备模块

传统上，Linux系统一般使用静态设备创建方式。不管对应的物理设备是否存在，/dev目录下创建了大量的设备节点（有时多达上千个）。通常这项工作由MAKEDEV脚本完成。对于可能存在的每一个设备，该脚本根据对应的主从设备号调用 `mknod` 程序来创建设备节点。

现在处于学习目的这么做。


```c
#include <linux/module.h>       /* 内核模块相关 */
#include <linux/cdev.h>         /* 字符设备相关 */
#include <linux/fs.h>           /* 文件操作 */

#define MYDEV_MAJOR_NUM     202     /* 主设备号 */

static struct cdev mydev;   /* 字符设备定义 */

static int mydev_open(struct inode *inode, struct file *file)
{
    pr_info("mydev open\n");
    return 0;
}

static int mydev_close(struct inode *inode, struct file *file)
{
    pr_info("mydev close\n");
    return 0;
}

static long mydev_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    pr_info("ioctl is called, cmd=%d, arg=%ld\n", cmd, arg);
    return 0;
}

/* 设备操作 */
static const struct file_operations mydev_fops = {
    .owner          = THIS_MODULE,
    .open           = mydev_open,
    .release        = mydev_close,
    .unlocked_ioctl = mydev_ioctl,
};

static int __init mydev_init(void)
{
    int ret;

    dev_t mydev_num = MKDEV(MYDEV_MAJOR_NUM, 0);          /* 设备表示信息，主设备号和从设备号，第一个设备表示 */

    pr_info("module init\n");

    ret = register_chrdev_region(mydev_num, 1, "mydev_name"); /* 设备号静态分配 */

    if (ret<0)
    {
        pr_info("major number allocate error\n");
        return ret;
    }

    cdev_init(&mydev, &mydev_fops);         /* 初始化字符设备 */
    ret = cdev_add(&mydev, mydev_num, 1);             /* 向内核注册 */

    if (ret < 0)
    {
        unregister_chrdev_region(mydev_num, 1);
        pr_info("add cdev error\n");
        return ret;
    }
    
    return 0;
}

static void __exit mydev_exit(void)
{
    pr_info("module exit\n");
    cdev_del(&mydev);
    unregister_chrdev_region(MKDEV(MYDEV_MAJOR_NUM, 0), 1);
}

module_init(mydev_init);
module_exit(mydev_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("xym");
MODULE_DESCRIPTION("this module interact with the system call ioctl()");
```

模块手动加载到内核 `insmod mydev.ko` 然后需要手动创建设备节点 `mknod /dev/mydev_test` ，之后就可以在 /dev 下面看到设备文件了。


此程序中用 `register_chrdev_region` 静态分配和释放设备号。使用 `alloc_chrdev_region()` 函数可以动态分配。函数声明

```c
int alloc_chrdev_region(dev_t *)
```



## 模块添加到内核镜像

前面的驱动都是用 `insmod` 手动加载，还可以把模块直接和内核一起打包成镜像，在内核启动时一同启动。

在内核源码根目录下，所有的字符设备驱动都在 `driver/char/` 下，将调试好的驱动源码放在此目录，打开此目录的 Kconfig 文件，添加配置

```
config HELLO_DEVICE
    tristate "hello driver test"
    default n
```

打开 makefile 文件，添加
```
obj-$(CONFIG_HELLO_DEVICE) += hello_driver.o
```

在 menucofing 内选中，保存配置后，就可以在 .config 里看到了。然后编译镜像。

用新镜像启动后，还需要手动 mknod 一下。


## class字符设备 模块


### 设备文件系统创建设备文件

前面都在用 mknod 手动创建设备文件，现在的内核有一个名为 sysfs 的虚拟文件系统。

sysfs 方便用户态进程查看系统硬件配置。

当内核检测到设备时，编译到内核的 linux 驱动通过 sysfs 将设备注册。编译成模块的驱动的注册过程发生在模块加载。


### class 字符设备

还是之前的字符设备，但是设备节点使用设备文件系统创建。


## misc字符设备 模块


杂项框架是 linux 内核提供的一个接口，此框架允许模块注册其各自的从设备号。

通过杂项设备实现的字符设备驱动使用 linux 内核为杂项设备分配的主设备号。这样能少用一个主设备号。

对于一个新杂项设备，系统内动态分配一个从设备编号，设备也会以目录的形式出现在 sysfs 的 `sys/class/misc` 下。

系统给杂项驱动的主设备号是 10，对于一些小型设备，模块可以通过杂项设备驱动注册从设备号并管理。





