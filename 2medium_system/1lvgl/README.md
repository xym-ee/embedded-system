---
sort: 1
---
# LVGL 与 C 语言 OOP 思想


编程思想。


(2023-02-06) 我第一次接触单片机在 2018 年 4 月，51 单片机，那时我上大二。2018 年 7 月我买了第一个 STM32 开发板，在大二升大三的暑假做了一点小东西。

对于大多数电子电气、自动化的同学来说，语言和芯片只是工具，因此我们甚至并不会过多关心程序结构、编程思想，许多时候项目的软硬算法都是一个人搞，写程序的原则是能用就行。

但是当我们要实现一个更复杂的东西时，这些不好的编程习惯会成为开发路上的阻碍。

因此我个人认为电子相关专业的初学者在熟悉裸机编程，把 C 语言从书本搬到实际芯片上后，最紧要的是养成好的编程习惯，建立起软件工程的基本概念，如果从一开始就可以养成好的编程习惯，规范的命名方式，规范的编程思想，那嵌入式这条路可以走的更高更远。

因此我觉得在学完裸机编程后，可以试试使用 LVGL 做一个 UI 的项目，初步接触 C 语言里面向对象的思想。

图形库主要是学习程序结构和实现，以及模块之间的关系是如何通过指针建立的，此外图形化界面本身的思维难度不大。但是这些程序设计思想在后面的操作系统里都会遇到，在操作系统学习中的重点是操作系统本身，比如线程、驱动、协议栈之类的。


## LVGL

- [Welcome to the documentation of LVGL!](https://docs.lvgl.io/)
- [欢迎阅读百问网LVGL中文开发手册！](http://lvgl.100ask.org/8.2/index.html)



官网：https://lvgl.io/

github：https://github.com/lvgl/lvgl

手册：https://docs.lvgl.io/master/index.html

中文翻译：http://lvgl.100ask.org/8.2/examples.html

Light and Versatile Graphics Library

轻量级、多功能图形库。

在官网可以看到

这套东西可以运行在16bitCPU上，最低主频16MHz，当然越高越好，ROM最小64KB，RAM最小8KB就能跑。

显存在MCU内部、外部，或在显示控制芯片内都行。

显存分配最小为一行像素，但是1/10最好。

这是个开源项目，遵循MIT协议。

Widgets即部件，有30多个。

显示很灵活，支持各种分辨率屏幕，单色的也可以。

输入也很灵活。

画图也有比较多的功能。

也支持中文文本。


## emWin

emWin属于SEGGER公司下面的一种GUI产品，一种嵌入式GUI解决方案。业界领先的嵌入式图形库，专业的嵌入式GUI。

emWin与单任务和多任务环境兼容，可以使用专有的操作系统，也可以与任何商业RTOS兼容。它以C语言源代码提供，使其成为嵌入式市场的专业、通用GUI，可用于多种不同的场景。

## TouchGFX

TouchGFX属于Draupner Graphics公司的GUI产品，在去年（2018年7月），TouchGFX被ST收购，在STM32上可以免费使用TouchGFX。TouchGFX升级至V4.10，扩展STM32生态系统，并集成在STM32CubeMX中。

## MiniGUI

MiniGUI丰富的功能和可配置性使得它既适用于运行在30MHz CPU的低端设备，也适用于使用GPU的高端设备。为嵌入式和智能物联网设备提供一个成熟的、经过验证的跨平台GUI系统。

就在前不久（2019年9月19日），北京飞漫软件技术有限公司宣布：将在 MiniGUI 4.0.2 版本中支持国产物联网操作系统 RT-Thread！

## Qt



