---
sort: 3
---
# rt-thread 设备驱动



## 裸机的“驱动”

STM32 的 HAL 库，使用 GPIO 的方法。

```c
void HAL_GPIO_Init(GPIO_TypeDef  *GPIOx, GPIO_InitTypeDef *GPIO_Init);
```

然后还需要使用这些函数来操作 GPIO

```c
void HAL_GPIO_WritePin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState);
GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
```

对于 NXP 的芯片，也有自己的库



每换一个芯片，都会有一套这种东西。深度与硬件绑定。这并不好。



能不能统一起来？比如说，所有设备都要读写、控制都是用同样的函数，这样拿到一个新设备，就几乎没有了学习成本。

```c
rt_size_t rt_device_read(rt_device_t dev, rt_off_t pos,void* buffer, rt_size_t size);
rt_size_t rt_device_write(rt_device_t dev, rt_off_t pos,const void* buffer, rt_size_t size);
rt_err_t rt_device_control(rt_device_t dev, rt_uint8_t cmd, void* arg);
```

这里面的第一个参数 `rt_device_t dev`，可以猜测，接口统一了也是根据这个来区别不同设备的。那我们对驱动的关注自然也就来到了这个对象。


```c
struct rt_device
{
    struct rt_object          parent;                   /**< inherit from rt_object */

    enum rt_device_class_type type;                     /**< device type */
    rt_uint16_t               flag;                     /**< device flag */
    rt_uint16_t               open_flag;                /**< device open flag */

    rt_uint8_t                ref_count;                /**< reference count */
    rt_uint8_t                device_id;                /**< 0 - 255 */

    /* device call back */
    rt_err_t (*rx_indicate)(rt_device_t dev, rt_size_t size);
    rt_err_t (*tx_complete)(rt_device_t dev, void *buffer);

#ifdef RT_USING_DEVICE_OPS
    const struct rt_device_ops *ops;
#else
    /* common device interface */
    rt_err_t  (*init)   (rt_device_t dev);
    rt_err_t  (*open)   (rt_device_t dev, rt_uint16_t oflag);
    rt_err_t  (*close)  (rt_device_t dev);
    rt_size_t (*read)   (rt_device_t dev, rt_off_t pos, void *buffer, rt_size_t size);
    rt_size_t (*write)  (rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size);
    rt_err_t  (*control)(rt_device_t dev, int cmd, void *args);
#endif /* RT_USING_DEVICE_OPS */

#ifdef RT_USING_POSIX_DEVIO
    const struct dfs_file_ops *fops;
    struct rt_wqueue wait_queue;
#endif /* RT_USING_POSIX_DEVIO */

    void                     *user_data;                /**< device private data */
};

typedef struct rt_device *rt_device_t;
```

统一接口内部，实际上是调用了他内部自己的具体实现。

因此最核心的，我们需要这么一个结构体，并把结构体里的函数指针东西赋值。




- [STM32系列驱动介绍](https://www.rt-thread.org/document/site/#/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/STM32%E7%B3%BB%E5%88%97%E9%A9%B1%E5%8A%A8%E4%BB%8B%E7%BB%8D)


## STM32系列驱动介绍

在 RT-Thread 实时操作系统中，各种各样的设备驱动是通过一套 I/O 设备管理框架来管理的。设备管理框架给上层应用提供了一套标准的设备操作 API，开发者通过调用这些标准设备操作 API，可以高效地完成和底层硬件外设的交互。设备管理框架的结构如下图所示：

<figure>
  <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/figures/rt_device.png" width=350>
</figure>


使用 I/O 设备管理框架开发应用程序，有如下优点：

使用同一套标准的 API 开发应用程序，使应用程序具有更好的移植性
底层驱动的升级和修改不会影响到上层代码
驱动和应用程序相互独立，方便多个开发者协同开发


<figure>
  <img src="https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/tutorial/make-bsp/stm32-bsp/figures/Peripheral.png" width=420>
</figure>

