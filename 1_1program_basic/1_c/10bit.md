
# 位操作

- 运算符 ~ & | ^ << >> &= |= ^= <<= >>=
- 回顾 二进制、八进制、十六进制计数法
- 处理一个值中的位：位运算符和位字段

C 语言中可以单独操作变量中的 bit，在控制硬件设备时，通常每个 bit 都有特定的含义。与文件相关的操作系统信息在存储时也会通过 bit 表明特定项。许多压缩和加密操作都是直接处理 bit 的。

更高级的语言通常不会处理这个级别的细节，C 在比汇编高级的同时，保留了一些汇编级别的操作，因此 C 成为编写设备驱动和嵌入式代码的首选。

## 背景知识，二进制，bit byte

1 Byte = 8 bit

有符号整数，原码，反码和补码，

二进制浮点数，IEEE754 

## 按位运算符

~ & | ^


### 用法：掩码

常用用法，掩码(mask)，掩码指的是一些设置为开(1)或关(0)的 bit 组合。

```c
#define MASK 2  //0b0000 0010
flags = flags & MASK;   //除 bit1 外都清除
```

相当于把 0 都覆盖上去，1 的位置保持原样。

### 用法：打开位(设置位)

打开一个 bit 同时其他 bit 保持不变

```c
#define MASK 2          //0b0000 0010
flags = flags | MASK;   //bit1 置位
flags |= MASK;
```

### 用法：关闭位(清空位)

打开一个 bit 同时其他 bit 保持不变

```c
#define MASK 2          //0b0000 0010
flags = flags & ~MASK;   //bit1 置位
flags &= ~MASK;
```

### 用法：切换位

打开已经关闭的，关闭已经打开的

```c
#define MASK 0b1011 0110 
flags = flags ^ MASK;
flags ^= MASK;
```

### 用法：检查bit

```c
#define MASK 2          //0b0000 0010

if ((flags & MASK) == MASK)
{

}
```

### 移位运算符



## 位字段(位域) bit field

```c
struct field {
    unsigned char a : 1;
    unsigned char b : 1;
    unsigned char c : 1;
    unsigned char d : 1;
    unsigned char e : 1;
    unsigned char f : 1;
    unsigned char g : 1;
    unsigned char h : 1;
};
```

位字段提供了一种记录设置的方便的方式，有些设置是简单的二选一，只需要使用 1bit，包含位字段的结构允许在一个存储单元内保存多个设置。

```c
struct prcode {
    unsigned char code1 : 2;
    unsigned char code1 : 2;
    unsigned char code1 : 8;
};
```

可以使用宽度为 0 的字段是下一字段域下一整数对齐。

关于字段的存储，和机器相关，因此不好移植，但是有些情况确实使用字段更方便。









