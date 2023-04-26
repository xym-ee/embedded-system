---
sort: 1
---
# 编程模型

## CPU 模式和特权

处理器模式：线程模式、异常模式。


## 寄存器

<figure>
    <img src="./images/1-1.png" width=550>
</figure>

- R0 - R12 通用寄存器，复位值为 unknown
- SP(stack pointer) 为栈指针寄存器，实际上有两个MSP(main SP)、PSP(process SP)
  - SP 就是 R13，在 thread mode 下，CONTROL 寄存器的 bit1 位控制具体的使用：0为MSP(复位默认)，1为PSP
  - MSP 的值为地址 0x0000 0000 处的值，也即CPU第一件事就是从0地址搬运4byte数据到MSP
  - PSP 复位值为 unknown
- LR(link register) 存放函数返回地址，复位值为 0xFFFF FFFF
- PC(program counter) 为程序计数器，R15，bit0 永远是0，即地址 2byte 对齐。复位时，值为地址 0x00000004 的值，此处为复位函数的入口地址。

由此，m3内核芯片的启动流程：上电后，0x00000000 处的 4byte 加载到 MSP，然后 0x00000004 处的值加载到 PC，这里是复位程序的首地址，这些行为是电路自动完成，不需要程序控制，也是硬件和软件约定好的入口。

```note
STM32 内部 flash 的起始地址为 0x0800 0000，那么芯片的0x00000000处是什么呢？

实际上 0x00000000 被映射到了 0x08000000，使用 keil 调试时可以看到这两部分存储空间的内容完全一致。
```


程序状态状态寄存器(program status register)也可以写成 xPSR，有 3 个寄存器：ASPR、ISRP、ESPR，application、interrupt、execution。




