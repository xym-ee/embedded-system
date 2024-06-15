---
sort: 2
---
# C语言开发


准备工作，汇编代码为C语言创造环境

- 设置CPU为 SVC 模式，特权模式，超级管理员，可以操作芯片的任何东西
  - CPSR 寄存器，bit4-0 10011 即可
- 设置 C 语言的栈指针
  - 设置 SP 指向 DDR，裸机程序设置为 2MB，大小为 0x200000，A7为满减栈，DDR起始地址 `0x80000000` SP 设置为 `0x80200000`
- 跳转到 C 语言函数的入口地址
  - 使用 `B` 指令，一般为 `main` 函数


两个文件 start.s 和 main.c

```
arm-linux-gnueabihf-gcc -Wall -nostdlib -c -O0 -o start.o start.s
arm-linux-gnueabihf-gcc -Wall -nostdlib -c -O0 -o main.o main.c

arm-linux-gnueabihf-ld -Ttext 0x87800000 -o ledc.elf start.o main.o
arm-linux-gnueabihf-objcopy -O binary -S ledc.elf ledc.bin
```

-O2 优化会出问题，_start 的指令没有放到指定的起始地址。所以为了让程序各模块能够按照设想的方式组合，需要控制链接地址以及链接顺序。

我们需要指定链接的区域，或者叫段。需要自己定义一些段，这些段的起始地址也要能自己指定。

```
SECTIONS{
	. = 0X87800000;
	.text :
	{
		start.o 
		main.o 
		*(.text)
	}
	.rodata ALIGN(4) : {*(.rodata*)}     
	.data ALIGN(4)   : { *(.data) }    
	__bss_start = .;    
	.bss ALIGN(4)  : { *(.bss)  *(COMMON) }    
	__bss_end = .;
}
```

链接脚本里的 bss 段前后记录了开始地址和结束地址，可以在代码里直接使用，对内存做一些操作。

bss 在程序内是定义时没给过值的变量，程序设计的不严谨直接用可能会出问题，因此清 bss 段也是一个常规操作，需要知道段的前后位置。












