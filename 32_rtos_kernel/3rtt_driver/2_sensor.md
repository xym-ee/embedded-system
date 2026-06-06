


# 传感器


- 应用 device_read 来读传感器数据
- 


## 传感器的使用


对于应用来说，如果底层已经实现好了一种传感器的驱动，那么一种最简单的使用方法：

```c
#define DBG_TAG     "main"
#define DBG_LVL     DBG_INFO
#include <rtdbg.h>

#define DEV_NAME "temp_v1"

int main(void)
{
    rt_device_t dev = RT_NULL;
    struct rt_sensor_data data;

    dev = rt_device_find(DEV_NAME);

    rt_device_open(dev, RT_DEVICE_FLAG_RDONLY);

    for (int i = 0; i < 10; i++)
    {
        rt_device_read(dev, 0, &data, 1);
        
        LOG_I("num:%3d, temp:%3d.%d C, timestamp:%5d", i, data.data.temp / 10, (rt_uint32_t)data.data.temp % 10, data.timestamp);
        
        rt_thread_mdelay(100);
    }
    
    rt_device_close(dev);
    
    return 0;
}
```

和其他设备的操作方法一样，但是传感器有自己的数据格式

```c
struct rt_sensor_data
{
    rt_uint32_t     timestamp;  /* The timestamp when the data was received */
    rt_uint8_t      type;       /* The sensor type of the data */
    union
    {
        struct sensor_3_axis acce;  /* Accelerometer.   unit: mG        */
        struct sensor_3_axis gyro;  /* Gyroscope.       unit: mdps      */
        /* ... */
        rt_int32_t           temp;  /* Temperature.     unit: dCelsius  */
        /* ... */

    } data;
};
```

data 中存放传感器数据，根据不同类型的传感器直接使用即可，此外还有 timestamp 时间戳，以及传感器的数据类型。


对于 MCU 的传感器来说，接的引脚可能会变，linux 驱动的解决方法是用设备树来描述硬件信息，rtthread 把这部分单独拿了出来，交给用户去配置。用户在使用前要做的就是指定传感器使用的接口，然后调用驱动层提供的初始化函数。

```c
int rt_hw_sr04_port(void)
{
    struct rt_sensor_config cfg;
    rt_base_t pins[2] = {GET_PIN(C, 4), GET_PIN(A, 4)};

    cfg.intf.dev_name = "timer15";
    cfg.intf.user_data = (void *)pins;
    rt_hw_sr04_init("sr04", &cfg);

    return RT_EOK;
}
INIT_COMPONENT_EXPORT(rt_hw_sr04_port);
```

接口这个结构体里可以指定驱动使用的通信设备的名字，以及接口的类型和其他需要传递给驱动的数据，如一些片选引脚的信息。
```c
struct rt_sensor_intf
{
    char                       *dev_name;   /* The name of the communication device */
    rt_uint8_t                  type;       /* Communication interface type */
    void                       *user_data;  /* Private data for the sensor. ex. i2c addr,spi cs,control I/O */
};

struct rt_sensor_config
{
    struct rt_sensor_intf        intf;      /* sensor interface config */
    struct rt_device_pin_mode    irq_pin;   /* Interrupt pin, The purpose of this pin is to notification read data */
    rt_uint8_t                   mode;      /* sensor work mode */
    rt_uint8_t                   power;     /* sensor power mode */
    rt_uint16_t                  odr;       /* sensor out data rate */
    rt_int32_t                   range;     /* sensor range of measurement */
};
```

此结构体中的其他配置信息都在驱动完成。`rt_hw_sr04_init` 为驱动提供给应用层提供的初始化接口。


## 传感器驱动注册

驱动开发中最核心的即实现传感器底层的 read 方法。

一个驱动开发中的常见概念，注册，即把和设备相关的数据结构或操作提交给内核。

和传感器相关的这个数据结构为 `struct rt_sensor_device`，和设备相关的操作为 `struct rt_sensor_ops`，将设备的数据结构和设备的操作联系起来的函数是 `rt_hw_sensor_register` ，所以注册前要准备的工作是实现对传感器的操作方法，以及填充传感器必要的信息。

传感器的这个数据结构为
```c
struct rt_sensor_device
{
    struct rt_device             parent;    /* The standard device */

    struct rt_sensor_info        info;      /* The sensor info data */
    struct rt_sensor_config      config;    /* The sensor config data */

    void                        *data_buf;  /* The buf of the data received */
    rt_size_t                    data_len;  /* The size of the data received */

    const struct rt_sensor_ops  *ops;       /* The sensor ops */

    struct rt_sensor_module     *module;    /* The sensor module */

    rt_err_t (*irq_handle)(rt_sensor_t sensor);             /* Called when an interrupt is generated, registered by the driver */
};
```

传感器类继承自 `struct rt_device` 类，用户的操作就是用的 device 类中的方法，此外还增加了传感器独有的数据和操作。

传感器信息中包括
```c
struct rt_sensor_info
{
    rt_uint8_t     type;                    /* The sensor type */
    rt_uint8_t     vendor;                  /* Vendor of sensors */
    const char    *model;                   /* model name of sensor */
    rt_uint8_t     unit;                    /* unit of measurement */
    rt_uint8_t     intf_type;               /* Communication interface type */
    rt_int32_t     range_max;               /* maximum range of this sensor's value. unit is 'unit' */
    rt_int32_t     range_min;               /* minimum range of this sensor's value. unit is 'unit' */
    rt_uint32_t    period_min;              /* Minimum measurement period,unit:ms. zero = not a constant rate */
    rt_uint8_t     fifo_max;
};
```

驱动开发时，如 type vendor 这些都是枚举类型，和做选择题一样，直接填充就行。`struct rt_sensor_config` 也是一样的，有一部分是用户层配置的，有一些和驱动相关的在这里配置。


用户调用的传感器初始化的函数的实现：
```c
int rt_hw_sr04_init(const char *name, struct rt_sensor_config *cfg)
{
    rt_int8_t result;
    rt_sensor_t sensor_sr04 = RT_NULL;

    sr04_dev = _sr04_init(cfg);
    /* sr04 sensor register */
    sensor_sr04 = rt_calloc(1, sizeof(struct rt_sensor_device));
    if (sensor_sr04 == RT_NULL) {
        return -1;
    }

    sensor_sr04->info.type       = RT_SENSOR_CLASS_PROXIMITY;
    sensor_sr04->info.vendor     = RT_SENSOR_VENDOR_UNKNOWN;
    sensor_sr04->info.model      = "sr04";
    sensor_sr04->info.unit       = RT_SENSOR_UNIT_CM;
    sensor_sr04->info.intf_type  = RT_SENSOR_INTF_ONEWIRE;
    sensor_sr04->info.range_max  = SENSOR_DISTANCE_RANGE_MAX;
    sensor_sr04->info.range_min  = SENSOR_DISTANCE_RANGE_MIN;
    sensor_sr04->info.period_min = 5;

    rt_memcpy(&sensor_sr04->config, cfg, sizeof(struct rt_sensor_config));
    sensor_sr04->ops = &sensor_ops;

    result = rt_hw_sensor_register(sensor_sr04, name, RT_DEVICE_FLAG_RDONLY, RT_NULL);
    if (result != RT_EOK) {
        LOG_E("device register err code: %d", result);
        goto __exit;
    }

    return RT_EOK;

__exit:
    if (sensor_sr04)
        rt_free(sensor_sr04);
    return -RT_ERROR;
}

```

这个驱动初始化函数中调用了 `rt_hw_sensor_register` 来完成**注册**，即把传感器名字、描述传感器的数据结构、等信息告诉内核，由内核关联起来。


## 驱动的实现

传感器类中，有个 `struct rt_sensor_ops` ，驱动开发的核心即实现此结构体中的操作。rtthread 的传感器操作方法比较少，相对 linux 来说要容易不少。

```c
struct rt_sensor_ops
{
    rt_size_t (*fetch_data)(struct rt_sensor_device *sensor, void *buf, rt_size_t len);
    rt_err_t (*control)(struct rt_sensor_device *sensor, int cmd, void *arg);
};
```

在传感器使用时，rt_device_read 最终调用的就是 fetch_data 指向的函数。实现的时候关注传入的参数以及返回值。

```c
static rt_size_t temp_sensor_fetch_data(struct rt_sensor_device* sensor, void* buf, rt_size_t size)
{
    struct rt_sensor_data* data = buf;
    rt_int16_t max_range = 0;

    if (size < 1)
    {
        LOG_E("%s:read size err! size=%d", __func__, size);
        return 0;
    }

    if (buf == RT_NULL)
    {
        LOG_E("%s:read buf is NULL!", __func__);
        return 0;
    }

    max_range = temp_info_tbl[SENS_TEMP_01].range_max - temp_info_tbl[SENS_TEMP_01].range_min;

    for (int i = 0; i < size; i++)
    {
        data->type = RT_SENSOR_CLASS_TEMP;
        data->data.temp = rand() % max_range + temp_info_tbl[SENS_TEMP_01].range_min;
        data->timestamp = rt_sensor_get_ts();
        LOG_D("%s:%d", __func__, data->data.temp);
        data++;
    }

    return size;
}

```


这些东西实现以后，就已经可以用了，

