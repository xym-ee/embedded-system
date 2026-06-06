# 嵌入式 AI 部署

这个主题记录在嵌入式 Linux 平台上部署 AI 应用会遇到的系统问题。

它和 `37_ai_agent_tools/` 的区别是：这里关注模型如何在板子、镜像、运行时和异构硬件上跑起来；`37_ai_agent_tools/` 关注 Agent、AI 工作流、编程助手和工具链本身。

## 关注问题

一些会涉及的知识点：

硬件架构与算力基础：

- ARM Cortex-A 架构，如 A53、A55。
- 可选加速器：NPU、DSP、GPU，例如 OpenCL / CUDA for Jetson。
- 内存带宽、DDR 速度与限值。
- IRQ、DMA、Cache 行为，这些对性能影响很大。
- 异构系统架构：
  - i.MX93: A55 + Ethos-U65 NPU + M33
  - i.MX8MP: A53 + Vivante NPU + M7

核心问题是：模型能否跑、要不要量化、瓶颈在哪里。

操作系统基础：

- Yocto / Buildroot 基础。
- 内核模块、设备节点、`/dev`。
- drivers 到 user space 的调用方式：
  - sysfs
  - ioctl
  - mmap
  - udev

交叉编译与工具链：

- aarch64 / armhf 工具链。
- CMake、Make、Bazel 基本语法。
- 编译带 NEON 优化的库，如 OpenCV、libtorch、OpenBLAS。
- 生成 rootfs，复制库与依赖。

AI 推理引擎与框架：

- TensorRT，主要用于 NVIDIA 平台。
- ONNX Runtime，通用推理运行时。
- 模型转换：PyTorch -> ONNX -> TFLite / NPU format。
- 模型量化：INT8。
- 模型裁剪：pruning。
- 硬件加速 API。

模型优化：

- INT8 静态 / 动态量化。
- 模型裁剪。
- 降低分辨率 / 通道数。
- NEON SIMD 优化。
- 多核并行，如 pthread、OpenMP。

异构多核通信：

- RPMsg / OpenAMP。
- M 核运行 RTOS，如 RT-Thread 或 FreeRTOS。
- A53 / A55 与 M7 / M33 的数据交互方式。

## 当前笔记

- [Docker](./docker.md)：容器、镜像和构建环境隔离的基础概念。
- [im6ull](./im6ull.md)：i.MX6ULL、Yocto、NXP BSP 和 Docker 构建环境记录。
- [linux_app](./linux_app.md)：嵌入式 Linux 应用工程环境的早期记录。

## 参考资料

- [面向 i.MX 应用处理器的嵌入式 Linux](https://www.nxp.com.cn/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX)
