# 环境和基本概念

C 代码是给人看的，无法直接在 CPU 上运行。可以在 CPU 上执行的是机器码，汇编指令可以和机器码一一对应起来。汇编代码也是给人看的，但是可以可机器码对应起来。



## 工具链

gcc 同样可以用于 arm cortex-m 平添，并且其他的工具如 objdump gdb 也都可以使用。
可以直接用 apt 安装，或者去 arm 官网下载，手动添加到环境变量。
- gcc-arm-none-eabi
对于更复杂的应用，可能还需要下面这两个软件包
- libnewlib-arm-none-eabi
- libstdc++-arm-none-eabi


## 链接脚本

链接器需要知道芯片的 ROM 和 RAM 的大小，此外还要一些额外信息，

```c
ENTRY(_reset);
MEMORY {
  flash(rx) : ORIGIN = 0x08000000, LENGTH = 512k
  sram(rwx) : ORIGIN = 0x20000000, LENGTH = 128k  /* remaining 64k in a separate address space */
}
_estack     = ORIGIN(sram) + LENGTH(sram);    /* stack points to end of SRAM */

SECTIONS {
  .vectors  : { KEEP(*(.vectors)) }   > flash
  .text     : { *(.text*) }           > flash
  .rodata   : { *(.rodata*) }         > flash

  .data : {
    _sdata = .;   /* .data section start */
    *(.first_data)
    *(.data SORT(.data.*))
    _edata = .;  /* .data section end */
  } > sram AT > flash
  _sidata = LOADADDR(.data);

  .bss : {
    _sbss = .;              /* .bss section start */
    *(.bss SORT(.bss.*) COMMON)
    _ebss = .;              /* .bss section end */
  } > sram

  . = ALIGN(8);
  _end = .;     /* for cmsis_gcc.h  */
}
```


## 中断向量表

mcu 的硬件中断功能需要一个向量表来存放特定中断触发时需要跳转的位置。现在只需要关心一上电时的复位中断函数的地址。

如果使用 hal 库的话，有一个汇编代码的启动代码


## 最小代码

C 语言代码

```c
int main(void)
{
    return 0;
}
```

要能在 MCU 上跑起来，需要解决这几个问题
- 设置栈指针( C 语言代码的跑起来的前提条件)
- 能够跳转到 main 的入口

STM32 通电的第一条指令的取指的地方是 `0x0000 0000`。内部存放代码的 flash 的起始地址为 `0x0800 0000`，硬件上配置了这两部分的内容相同，即存储器映射。

通电时，从 `0x0000 0000` 拿出 4 byte 放入 SP，然后从 `0x0000 0004` 取 4 byte 放入 PC。事实上从 0 地址开始的一段区域的内容是终端向量表，`0x0000 0004` 处为复位函数的指针。也就是说，设置好 SP 后，执行的就是复位函数。

因此，最起码还要有个复位函数来调用 `main`

```c
void reset(void) 
{
  main();             // Call main()
  while(1);  // Infinite loop in the case if main() returns
}
```

C 代码上的东西就这么多，接下来需要考虑编译与链接的问题。

在编译链接后生成的可执行文件中，一定要保证从 `0x0800 0000` 处开始，并且，前 4 个字节为 SP 指针，随后 4 个字节为 reset 的地址。这就需要控制链接过程。

关于编译，在 x86 架构下编译 x86 应用，使用 gcc 将 C 语言代码转换成 x86 的可执行文件。这里使用 arm-none-eabi-gcc ，用法和 gcc 一样，但是需要关注的东西比较多。

```bash
arm-none-eabi-gcc main.c -W -Wall -Wextra -Werror -Wundef -Wshadow -Wdouble-promotion -Wformat-truncation -fno-common -Wconversion -g3 -Os -ffunction-sections -fdata-sections -I. -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -o firmware.elf
```

这里参数比较多，分类来看
- 编译 warning 选项
  - `-W`: 启用基本的警告。
  - `-Wall`: 启用大多数有用的警告。
  - `-Wextra`: 启用一些额外的警告。
  - `-Werror`: 将所有警告视为错误，阻止生成目标文件。
  - `-Wundef`: 如果遇到未定义的宏，则发出警告。
  - `-Wshadow`: 如果局部变量或参数与全局变量或其他作用域的变量同名，则发出警告。
  - `-Wdouble-promotion`: 警告将 float 类型的值提升为 double 类型的操作。
  - `-Wformat-truncation`: 如果字符串格式化可能导致截断，则发出警告。
- 编译器优化和调试控制选项:
  - `-fno-common`: 避免将未初始化的全局变量放在公共区域。
  - `-Wconversion`: 启用类型转换的警告。
  - `-g3`: 包含最高级别的调试信息。
  - `-Os`: 优化代码以减小大小（而非性能）。
  - `-ffunction-sections -fdata-sections`: 将每个函数和数据对象放在自己的段中，这在链接时可以进行更有效的代码剥离。
- 包含路径:
  - `-I.`: 当前目录中的头文件路径。
- 架构与处理器选项:
  - `-mcpu=cortex-m4`: 目标处理器为 Cortex-M4。
  - `-mthumb`: 启用 Thumb 指令集。
  - `-mfloat-abi=hard`: 使用硬浮点 ABI。
  - `-mfpu=fpv4-sp-d16`: 指定使用单精度浮点单元。


## 下载

使用 stlink 

