---
sort: 3
---
# 计算机组成的一个实例：IBM5150

基于8086/8088CPU的微型计算机介绍《微机原理与接口技术》，理论性不是很强。“微机”是很古老的叫法了，微型计算机字面上包含了现在的台式机笔记本，但是提到这个词语让人想到的是一堆DIP芯片插在一块绿板上，显示屏是黑色的，闪烁着绿色字符。

<figure>
    <img src="./images/IBM5150.jpg" width=200 />
    <figcaption>真·微型计算机</figcaption>
</figure>

IBM5150用的CPU是著名的8088，许多微机原理教材里讲的古典计算机大多都是IBM5150兼容机，这里不得不讲一下Intel与IBM PC的历史了。

1971年，英特尔公司生产出它的第一个微处理器4004。

1974年，英特尔公司生产出8080型微型集成电路芯片，随之出现了以该芯片为CPU的"Altair"电脑。这个名称因电影"星际旅行"片段中的一个星系而得名，它成为业余爱好者用一套价值400美元的工具成功制造个人电脑的标志。

1975年，比尔·盖茨和保罗·艾伦建立微软公司，并开发出Altair计算机使用的BASIC语言。

1975年，IBM公司宣布以8975美元的价格启动50磅5100型便携计算机市场。

1976年，史蒂夫·沃兹尼亚克和史蒂夫·乔布斯工作室推出苹果I型电脑，这种电脑前面倾斜、放在木箱中、用螺栓连接，并以666.66美元的价格出售。

1977年，乔布斯的苹果公司推出苹果II型计算机，它以彩色图形为特色并用盒式录音磁带存储信息。

1981年8月12日，IBM推出Intel 8088作为CPU的个人电脑。**这种5150型计算机是现代PC的原形**，并运行MS-DOS。

1983年11月，苹果公司的乔布斯在Comdex大展上首次展示了令人激动不已的Macintosh计算机，从此，个人电脑千篇一律的字符界面逐渐被生动、极富个性的图形界面所取代，多媒体技术广泛应用的春天即将来临。

1985年，Intel386型芯片可进行多任务处理。微软发布Windows操作系统。

1990年，微软公司推出Windows 3.0

1993年，Intel推出奔腾处理器

1995年，Windows 95面市，并在4天内售出100多万个拷贝。此外，微软公司提出，将把因特网功能加入其所有产品。

2000年，英特尔公司推出带4200万只晶体管的奔腾4处理器，运行速度达1.5GHz，与1971年第一个英特尔芯片108千赫的速度不可同日而语。


## IBM 5150

IBM5150单独拎出来，是一个重要的时间点，是IBM公司于1981年8月12日推出的世界上首部个人电脑。IBM没有将PC设计保密，而是制作了详细的说明书作为附带的技术参考手册，宣称能够让任何一个普通消费者“在数小时内学会使用电脑”。手册里的内容成了后来电脑的行业标准。

<figure>
    <img src="./images/IBM5150TechRef.jpg" width=100 />
    <figcaption>IBM5150TechRef</figcaption>
</figure>

资料公开以后，仿造的也就出来了，兼容机基本上就是这么来的，5150的意义是重大的，兼容5150的机器也叫成了IBM PC\XT兼容机。实际上PC和XT是两个型号。这里的PC专指5150，XT指改进版5160。IBM XT使用的也是8088处理器。

## IBM PC整体结构

首先来看IBM PC的整体框图

<figure>
    <img src="./images/system_block_diagram.jpg" width=600 />
    <figcaption>system_block_diagram</figcaption>
</figure>

系统板（SYSTEM BOARD）上有微处理器8088、40KB ROM、16KB RAM（可以扩展到64KB）、DMA、定时器、中断管理芯片、输入输出设备接口等。从系统框图来看，IBM PC的设计也是模块化的，核心处理器以及外围辅助芯片设计到了一块板上作为SYSTEM BOARD，然后5 I\O EXPANSION SLOTS更像是现代的主板（不妨就叫主板好了），通过插槽的方式灵活扩展各种设备如显示器打印机游戏控制器串口通信设备等。

技术参考中也给出了SYSTEM BOARD的数据流

<figure>
    <img src="./images/system_board_data_flow.jpg" width=800 />
    <figcaption>system_board_data_flow</figcaption>
</figure>

可以看到三总线结构，除了定时器、中断管理等功能芯片，用于地址译码和数据缓冲辅助芯片主要是74系列的逻辑芯片。

此外也给出了实体图
<figure>
    <img src="./images/SYSTEM BOARD COMPONENT DIAGRAM.jpg" width=500 />
    <figcaption>SYSTEM BOARD COMPONENT DIAGRAM</figcaption>
</figure>

展示了芯片、接口位置。接下来就是研究这个8088CPU本身以及这块板上的芯片。

## 参考资料

除了各种基于8086/8088的《微机原理与接口技术》教材，还参考了一些Github上开源的IBM兼容机设计：

- [Micro 8088 - IBM XT Compatible Processor Board based on Faraday FE2010 chipset](https://github.com/skiselev/micro_8088)
- [Minimal 8088 single board computer](https://github.com/74hc595/8088sbc)

以及最重要的上古手册：
- [*IBM 5150 Technical Reference*](./references/IBM_5150_Technical_Reference.pdf)
- [*IBM 5160 Technical Reference*](./references/IBM_5160_Technical_Reference.pdf)
- [*Intel 8088 datasheet*](./references/Intel-CPU-8088.pdf)
- [*Intersil 80C88 datasheet*](./references/Intersil-CPU-80C88.pdf)

此外还有各种辅助芯片手册：

（涉及到了回来再补上）

