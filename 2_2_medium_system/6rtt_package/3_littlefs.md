

spi flash



SFUD (Serial Flash Universal Driver) 


CubeMX 配置 spi 模式和引脚

Kconfig 中增加 spi 选项

```
        config BSP_USING_SPI_FLASH
            bool "Enable SPI FLASH (W25Q128 spi2)"
            select BSP_USING_SPI
            select BSP_USING_SPI2
            select RT_USING_SFUD
            select RT_SFUD_USING_SFDP
            default n
```

在外设中打开此选项，并在 Components 下的 Device Drivers 中打开 Using SPI Bus，并勾选 SFUD 功能



需要手动挂在

```c
#include <rtthread.h>
#include "spi_flash.h"
#include "spi_flash_sfud.h"
#include <drv_spi.h>
#include <drv_gpio.h>

#if defined(BSP_USING_SPI_FLASH)

static int rt_hw_spi_flash_init(void)
{
    __HAL_RCC_GPIOB_CLK_ENABLE();
    rt_hw_spi_device_attach("spi2", "spi20", GET_PIN(B, 12));

    if (RT_NULL == rt_sfud_flash_probe("W25Q128", "spi20"))
    {
        return -RT_ERROR;
    }

    return RT_EOK;
}
INIT_COMPONENT_EXPORT(rt_hw_spi_flash_init);
#endif
```


日志提示

```log
[I/SFUD] Warning: Read SFDP parameter header information failed. The W25Q128 does not support JEDEC SFDP.
[I/SFUD] Warning: This flash device is not found or not supported.
[I/SFUD] Error: W25Q128 flash device initialization failed.
[E/SFUD] ERROR: SPI flash probe failed by SPI device spi20.
```

CubeMX 配置问题，软件片选，NSS 引脚设置为 GPIO_Output ，SFUD 可以了。





参考资料

[在 STM32L4 上应用 littlefs 文件系统](https://www.rt-thread.org/document/site/#/rt-thread-version/rt-thread-standard/application-note/components/dfs/an0027-littlefs?id=%e5%9c%a8-stm32l4-%e4%b8%8a%e5%ba%94%e7%94%a8-littlefs-%e6%96%87%e4%bb%b6%e7%b3%bb%e7%bb%9f)


