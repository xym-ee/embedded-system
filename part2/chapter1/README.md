---
sort: 1
---
# RT-Thread 简介


学完了再来补充更多细节。


首先 RT-Thread 是国内团队开发的，一些文档都是原生中文，很好。

RT-Thread 用 C 语言实现，但是又卖你先对象的设计方法，不仅仅是 RTOS 本身，其设计思想、代码风格、系统架构也是非常值得研究学习的。

除了用于传统工业控制领域，这也是个**物联网操作系统**( IoT OS )。

感觉 IoT OS 更像是一些列技术的集合，也没有具体的教科书定义，其指的是含操作系统的、包括文件系统图形库等比较完成的中间组件，具备低功耗、链接云端能力的软件。

FreeRTOS、μC/OS 这两种 RTOS 实际上仅仅有个“内核”， RT-Thread 除了实时内核，还有特别丰富的中间层组件。


<figure>
    <img src = "https://www.rt-thread.org/document/site/rt-thread-version/rt-thread-standard/figures/02Software_framework_diagram.png" width=600 />
    <figcaption>RT-Thread 架构（官方文档）</figcaption>
</figure>

- 内核指的是多线程实现、RTOS 使用的接口、内存管理等CPU实现多任务最基础的东西。
- 组件和服务层在基于内核上，提供了上层的一些软件
- 软件包是 RT-Thread 的特色，生态的问题







