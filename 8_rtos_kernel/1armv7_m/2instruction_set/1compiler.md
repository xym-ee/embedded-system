---
sort: 1
---
# 编译器

- GCC （GNU Compiler Collection）是GNU开发的编译器，许可证为GPL的自由软件；
- armcc 是 arm 公司开发的一款编译器，集成在 KEIL 以及 ARM DS IDE 里面，于 5.06 版本后停滞（AC5），不继续维护，其前端基于 Edison Design Group 。
- armclang 集成于 armcc，基于新的架构 clang 和 LLVM，作为 arm 的第六代编译器，AC6，成为今后主推的编译器。

```note
GCC 原来只能处理C，现在可以处理C++、Pascal、Object-C、Java等。

苹果公司之前一直使用GCC作为编译器，但是GCC对Objective-C支持一直不怎么好，好多新特性没有增加，所以苹果公司开始寻求编译器的替代品。

这个时候LLVM就出现了，是Chris Lattner在硕士和博士时提出和形成的编译器，不过其是采用GCC的前端进行语义分析，然后LLVM做优化和生成目标代码，可以叫做LLVM-GCC。

后来苹果公司直接计划绕开GCC，于是招募了Chris Lattner 博士开发编译器，Clang就这样诞生了，其基于LLVM开发的C/C++/Obj-C编译器，实际上其是一个编译器前端，来取代GCC或者超越GCC
```



## armcc(AC5)

armcc,armasm,armlink,armar


## armclang (AC6)

- armclang
  - 基于现代LLVM和Clang技术构建
  - 支持GNU语法汇编
  - 与最初为GCC编写的源代码高度兼容
  - 实现规范，包括ANSI / ISO C和C ++，用于Arm架构的ABI，用于64位Arm架构的ABI以及Arm C语言扩展（ACLE）




## 参考资料

- [熟悉又陌生的arm 编译器详解（armcc/armclang）](https://mp.weixin.qq.com/s/HW2_cNK0ajOGIzBk_y_wrA)

