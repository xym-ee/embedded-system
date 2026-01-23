
# nrf5340 


https://docs.nordicsemi.com/category/nrf5340-category


## 硬件架构

[产品介绍](https://docs.nordicsemi.com/bundle/ps_nrf5340/page/keyfeatures_html5.html)


nRF5340拥有两个核心，一个是应用处理器（Cortex-M33），另一个是网络处理器（Cortex-M33），分别处理不同的任务。

- 应用内核
  - 128/64 MHz Arm Cortex-M33
  - 1 MB Flash + 512 KB RAM
    - 256 kB CPU single-cycle RAM
    - 256 kB of additional RAM
- 网络内核
  - 64 MHz Arm Cortex-M33
  - 256 KB Flash + 512 KB RAM


<img src="https://docs-be.nordicsemi.com/bundle/ps_nrf5340/page/chapters/soc_overview/doc/image/soc_overview.svg?_LANG=enus" >



## 内存映射

<img src="https://docs-be.nordicsemi.com/bundle/ps_nrf5340/page/chapters/soc_overview/doc/image/memorymap.svg?_LANG=enus">


- 所有的内存和寄存器都位于 同一地址空间，这意味着应用核心和网络核心都可以访问相同的内存资源。
- 两个256 KB的RAM块被映射为 一个连续的512 KB RAM块，但它们有不同的访问特性：
  - 第一个256 KB块：CPU可以 单周期 访问，这意味着它可以非常快速地访问（一个CPU周期）。
  - 第二个256 KB块：访问时需要 额外最多四个CPU周期，这会引入一些小的延迟。

一些点
- 内存访问：所有内存位于一个地址空间中，但第二个256 KB RAM块的访问延迟更高。
- 共享内存：应用核心和网络核心可以共享内存，通过共同的地址空间进行通信，并通过保护机制进行配置。
- 安全性：使用TrustZone技术，当网络核心处于非安全模式时，限制其访问安全内存，从而保护应用核心的安全内存。
- 系统保护：SPU确保内存区域的安全性和访问控制，特别是在双核心架构中，增强了系统的隔离性和保护性。


app core 内存映射

https://docs.nordicsemi.com/bundle/ps_nrf5340/page/chapters/memory/appmem.html



## 开发环境


[nRF Connect for Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-Desktop)


下载安装后，有 QUICK START 页面，里面有详细的引导。以及简单的试用，验证开发板的基本功能。以及提供了开发资料的页面

- [Nordic Developer Academy](https://academy.nordicsemi.com/)
- [Application development](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/app_dev.html)
- [Developing with nRF53 Series](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/app_dev/device_guides/nrf53/index.html)


Develop 页面里，有开发环境方式，vscode 和 command line 方式。


## 参考资料


- [nRF Connect SDK](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/index.html)
- [nRF5340 DK Hardware](https://docs.nordicsemi.com/bundle/ug_nrf5340_dk/page/UG/dk/intro.html)


- [Nordic Developer Academy](https://academy.nordicsemi.com/)
- [Application development](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/app_dev.html)
- [Developing with nRF53 Series](https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/app_dev/device_guides/nrf53/index.html)








