---
sort: 2
---
# STM32F1微控制器结构

常用的STM32F103，属于RISC指令集，有这些特点：
- 对内存只有读写指令
- 对数据运算在CPU内部实现
- 使用RISC指令的CPU复杂度小一点容易设计

对于a=a+b操作，需要4步来实现

读a到寄存器，读b到寄存器，做运算，写a+b到RAM。

```armasm
LDR  R0, [#a]
LDR  R1, [b]
ADD  R0, R0, R1
STR  R0, [a]
```

这组指令涉及到的问题是去哪里找数据的问题，即寻址。


## 常用汇编指令

读取内存，load（加载指令）
```armasm
LDR  Rn, [Rn, #offset]
```
r3数据作为地址值，放到地址总线，数据总线读入r0。


写内存，store

```armasm
STR  R0, [Rn, #offset]
```

加法

```armasm
add 
```

减法
```armasm
sub 
```

跳转，branch and link
```armasm
bl
```

入栈
```armasm
PUSH {R0, R1}
```
push的本质是写内存。高标号寄存器写高地址。

`push r1`把r1写入地址为`sp-4`的内存，然后`sp = sp - 4`，


出栈
```armasm
pop
```

pop r1，读地址为sp的内存，然后sp=sp+4

跳转指令
```armasm
B   Label   ;跳转到Label
BX  reg     ;跳转到寄存器reg给出的地址

BL  Label   ;调用子程序，跳转到Label并且保存跳转前的下调指令地址到LR(R14)
```


## 寄存器与别名






