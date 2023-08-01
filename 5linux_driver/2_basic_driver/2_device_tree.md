---
sort: 2
---
# 设备树

新版本的 Linux 中，ARM 相关的驱动全部采用了设备树。

uboot 启动时，加载了 zImage 和 dtb 到 DDR 里。用 `bootz 80800000 - 83000000` 启动。其中 `83000000` 存放的就是设备树。

设备树是嵌入式 linux 驱动工程师掌握的必备技能。

描述设备树的文件叫做 DTS(Device Tree Source)，这个 DTS 文件采用树形结构描述板级设备。设备数的存在也是为了把硬件相关的东西剥离出内核本身。

在现在的 linux 源码中，`arch/arm/mach-xxxx` 或者 `arch/arm/plat-xxxx` 下的 .c 文件都是用来描述板级的却区别的。用 C 语言来描述整个板上的设备信息。

单片机的驱动，直接写死，绝对有代码，可以用在所有芯片上。

然而，一款 CPU 可以设计出来的开发板太多了，如果每个开发板都用 .c 写死，带来的问题是，如果硬件上的改变，必须要编译整个内核。当然这不是最主要的问题，最关键的，linux 本身提供的功能上的东西，对于这种板级的描述信息，硬编码进内核，是不合适的。这也是 dts 引入 arm 的原因。

设备树源文件为 `*.dts`，编译出来的设备树二进制文件为 `*.dtb`，编译工具为 `dtc` 工具。

dtc 工具在 scripts 中，由 gcc 编译器编译出 dtc 工具。

编译设备树的命令为

`make dtbs`

或者编译指定的设备树

`make imx6ull_mini.dtb`

`arch/arm/boot/dts` 里的 makefile 根据架构型号，确定编译对应架构的开发板的设备树。因此，新增开发板对应的设备树，要记得在此文件中新增。


## 基本语法

设备树的头文件为 `.dtsi`，设备树也可以引用 `.h` 头文件，也可以引用 `.dts` 文件。在行为上，只是相当于把整个文件的内容复制过去，本质上都是文本文件，后缀只是给人看的。

这个设计也很好理解，设备树不仅仅描述了芯片外面挂的设备，也描述了 CPU 里的信息，因此，这部分是公共的，这些只写一次就好了。`imx6ull.dtsi` 就描述了 imx6ull 芯片的所有信息。

设备树语法很简单，几乎没啥学习成本，对着 imx6ull 看看就能明白的个大概。

源码在 `arch/arm/boot/dts/imx6ull.dtsi` 中，


开发板的 dts 中，先去包含一些东西
```
/dts-v1/;

#include <*.h>
#include "*.dtsi"

/ {
    属性1 = "字符串";
    属性2 = "字符串";

    结点1 {
        属性 = ;
    };

    结点2 {
        属性 = ;
    };
};

&cpu0 {
    arm-supply = <&reg_arm>;
    soc-supply = <&reg_soc>;
    dc-supply = <&reg_gpio_dvfs>;
};
```

设备树也是由 `/` 根节点开始，用树的方式描述设备信息。根节点之外，`&` 来引用前面的结点，修改属性。

在 dtsi 里也有根结点，在这个文件引用的 `skeleton.dtsi` 里也有根节点，这几个根节点是同一个根节点，里面的内容都会一同拼接起来。设备树里的内容可以在另外一个文件中对一个东西赋值，就修改了设备树里的内容。

三个文件拼接起来的设备树：

```
/ {
    #address-cells = <1>;       /* skeleton.dtsi */
    #size-cells = <1>;          /* skeleton.dtsi */
    model = "Freescale i.MX6 ULL 14x14 EVK Board";          /* board.dts */
    compatible = "fsl,imx6ull-14x14-evk", "fsl,imx6ull";    /* board.dts */

    chosen {                    /* skeleton.dtsi 定义 */
        stdout-path = &uart1;   /* board.dts新增属性 */
    };

    aliases {                   /* skeleton.dtsi */
        gpio0 = &gpio1;         /* imx6ull.dtsi 新增属性*/
        i2c0 = &i2c1;           /* imx6ull.dtsi 新增属性*/
        mmc0 = &usdhc1;         /* imx6ull.dtsi 新增属性*/
        serial0 = &uart1;       /* imx6ull.dtsi 新增属性*/
        spi0 = &ecspi1;         /* imx6ull.dtsi 新增属性*/
        usbphy0 = &usbphy1;     /* imx6ull.dtsi 新增属性*/
    };

    memory {                    /* skeleton.dtsi */
        device_type = "memory"; /* skeleton.dtsi */
        reg = <0 0>;            /* skeleton.dtsi */
        reg = <0x80000000 0x20000000>;  /* board.dts 修改属性 */
    };

    cpus {
        #address-cells = <1>;
        #size-cells = <0>;
    }

	intc: interrupt-controller@00a01000 {

	};

    clocks {

    };

    soc {

    };
};
```

这里只给出了一级结点。结点的命名也是有要求的，参考 PAPR 文档，完整的命名为 `label:node-name@address`，

后面的地址对于外设来说，一般是起始地址。对于具体的挂载总线上的设备，一般就是设备地址。

一个追加内容的例子，imx6ull 中 soc 节点下的 aips2 结点下的 i2c1

```
i2c1: i2c@021a0000 {
    #address-cells = <1>;
    #size-cells = <0>;
    compatible = "fsl,imx6ul-i2c", "fsl,imx21-i2c";
    reg = <0x021a0000 0x4000>;
    interrupts = <GIC_SPI 36 IRQ_TYPE_LEVEL_HIGH>;
    clocks = <&clks IMX6UL_CLK_I2C1>;
    status = "disabled";
}
```

在不同的开发板上，如果挂了外设，就需要新增子节点，使用引用的方式

```
&i2c1 {
	clock-frequency = <100000>;
	pinctrl-names = "default";
	pinctrl-0 = <&pinctrl_i2c1>;
	status = "okay";

	mag3110@0e {
		compatible = "fsl,mag3110";
		reg = <0x0e>;
		position = <2>;
	};

	fxls8471@1e {
		compatible = "fsl,fxls8471";
		reg = <0x1e>;
		position = <0>;
		interrupt-parent = <&gpio5>;
		interrupts = <0 8>;
	};
};
```

可以看出，这块板的 i2c1 上挂了两个芯片。

## linux 中的设备树

在 `proc/device-tree` 中，能看到设备树的所有东西。结点以文件夹的形式给出来，属性以文件的形式给出。

内核启动时，是知道设备树的地址的，内核解析设备树，然后在 `/proc/device-tree` 里呈现出来。

可以在根结点下面随便新增一个设备树做测试。

在设备树中添加一个硬件对应的结点时，可以参考文档。

## 特殊设备结点

```
/ {
    chosen {
        stdout-path = &uart1;
    };

    aliases {

    };
}
```

单词 aliases 的意思是“别名”，因此 aliases 节点的主要功能就是定义别名，定义别名的目的就是为了方便访问节点。不过我们一般会在节点命名的时候会加上 label，然后通过&label来访问节点，这样也很方便，而且设备树里面大量的使用&label 的形式来访问节点。

chosen 并不是一个真实的设备，chosen 节点主要是为了 uboot 向 Linux 内核传递数据，重点是 bootargs 参数。一般 `.dts` 文件中 chosen 节点通常为空或者内容很少，imx6ull-alientek-emmc.dts 中 chosen 节点内容如下所示：

但是进入 `/proc/device-tree/chosen` 会看到有 `bootargs` 这个属性。

uboot 将 bootargs 参数传递给 linux 内核，设备树中我们也未设置此参数，显然 uboot 增加了这一属性。

uboot 是知道 dtb 在 DDR 中的位置的，在 uboot 源码的 `common/fdt_support.c` 中有 `fdt_chosen()` 函数，此函数调用了 `fdt_find_or_add_subnode()` 从设备树中找 chosen 结点，没有的话就自己创建一个。然后把 bootargs 用 `fdt_setprop()` 函数写入设备树。



## kernel api

在驱动开发中，需要获得设备树里的属性值。内核提供了许多 api 方便驱动开发，这些函数都放在 `include/linux/of.h` 中，并且都用 `of_` 开头。

内核中，使用一个结构体来描述结点，定义为

```c
struct device_node {
	const char *name;                   /* 节点名字 */
	const char *type;
	phandle phandle;
	const char *full_name;
	struct fwnode_handle fwnode;

	struct	property *properties;
	struct	property *deadprops;	/* removed properties */
	struct	device_node *parent;
	struct	device_node *child;
	struct	device_node *sibling;
	struct	kobject kobj;
	unsigned long _flags;
	void	*data;
#if defined(CONFIG_SPARC)
	const char *path_component_name;
	unsigned int unique_id;
	struct of_irq_controller *irq_trans;
#endif
};
```

属性也用要给结构体来描述

```c
struct property {
	char	                *name;      /* 属性名字 */
	int	                    length;     /* 属性长度 */
	void	                *value;     /* 属性值 */
	struct property         *next;      /* 下一个属性 */
	unsigned long           _flags;
	unsigned int            unique_id;
	struct bin_attribute    attr;
};
```

### 查找结点

```c
/* 通过名字查找 */
struct device_node *of_find_node_by_name(struct device_node *from, const char *name);

struct device_node *of_find_node_by_type(struct device_node *from, const char *type)

struct device_node *of_find_compatible_node(struct device_node *from,
                                            const char *type,
                                            const char *compatible)

struct device_node *of_find_matching_node_and_match(struct device_node  *from,
                                                    const struct of_device_id *matches,
                                                    const struct of_device_id **match)


inline struct device_node *of_find_node_by_path(const char *path)
```

### 查找父子结点


```c
struct device_node *of_get_parent(const struct device_node *node)

struct device_node *of_get_next_child(const struct device_node *node,
                                      struct device_node *prev)
```

### 提取属性


```c
property *of_find_property( const struct device_node *np,
                            const char *name,
                            int *lenp)

int of_property_count_elems_of_size(const struct device_node *np,
                                    const char *propname,
                                    int elem_size)
```


## 参考资料

- [Power_ePAPR_APPROVED](https://elinux.org/images/c/cf/Power_ePAPR_APPROVED_v1.1.pdf)


