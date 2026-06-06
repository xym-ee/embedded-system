---
sort: 3
---
# rt-thread 中的外设


## “设备”的层次

关于设备的层次，有一些设备直接接到MCU的对应接口上就能工作，比如基于UART的传感器，可以认为这个传感器的驱动就是串口驱动。当然再对接一层sensor驱动统一接口也没有任何问题。

<figure>
    <img src="./images/设备层次.png" width=280 >
</figure>

设备驱动层次：
- 片内外设驱动
- 板载模块驱动

有时候板载模块并不止使用一个片内外设，如spi芯片有时还需要普通io做片选信号。

对于设备使用，知道这些也就够了，下面关注如何使用。

## 设备的使用

不管任何设备，和业务关系最密切的就是**读**和**写**。

在基于rtt进行开发时，可以使用如下函数进行读一个设备
```c
rt_size_t rt_device_read(rt_device_t dev, rt_off_t pos,void* buffer, rt_size_t size);
```
- `dev` : 设备句柄
- `pos` : 读取数据偏移量
- `buffer` : 读取数据的存储地址
- `size` : 读取数据长度

对于任何一个设备，都可以使用这个函数来读取，这就是在操作系统使用设备的方式。

同样地，写一个设备也有通用的函数：
```c
rt_size_t rt_device_write(rt_device_t dev, rt_off_t pos,const void* buffer, rt_size_t size);
```
- `dev` : 设备句柄
- `pos` : 写入数据偏移量
- `buffer` : 写入数据的存储地址
- `size` : 写入数据长度
- return : 实际写入的大小


对于随机向MCU发送数据的设备，可以设置一个回调函数，在回调函数中通知数据到达
```c
rt_err_t rt_device_set_rx_indicate(rt_device_t dev, rt_err_t (*rx_ind)(rt_device_t dev,rt_size_t size));
```
- `dev` : 设备句柄
- `rx_ind` : 函数指针
- return : `RT_ROK`设置成功

这个函数的可读性其实差了一点，写成这样会对人类更友好：
```c
typedef rt_err_t (*rx_ind_t)(rt_device_t dev,rt_size_t size);

rt_err_t rt_device_set_rx_indicate(rt_device_t dev, rx_ind_t rx_ind);
```


这几个函数就是使用设备的接口。







