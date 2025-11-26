
# 嵌入式 AI 部署


一些会涉及的知识点

硬件架构与算力基础
- ARM Cortex-A 架构（A53/A55等）
- 可选加速器：NPU、DSP、GPU（OpenCL/ CUDA for Jetson）
- 内存带宽、DDR 速度与限值
- IRQ、DMA、Cache 行为（对性能影响巨大）
- 异构系统架构：
  - i.MX93: A55 + Ethos-U65 NPU + M33
  - i.MX8MP: A53 + Vivante NPU + M7

模型能否跑、要不要量化、瓶颈在哪。

操作系统基础：Linux 嵌入式开发
- Yocto / Buildroot 基础
- 内核模块、设备节点、/dev 
- drivers → user space 的调用方式
  - sysfs、ioctl、mmap、udev


交叉编译与工具链
- aarch64 / armhf 工具链
- CMake、Make、Bazel 基本语法
- 编译带 NEON 优化的库（OpenCV、libtorch、OpenBLAS…）
- 生成 rootfs、copy 库与依赖

AI 推理引擎与框架
- TensorRT（NVIDIA）
- ONNX Runtime（通用）
- 模型转换（PyTorch → ONNX → TFLite / NPU format）
- 模型量化（INT8）
- 模型裁剪（pruning）
- 硬件加速 API

模型优化（Performance Optimization）
- INT8 静态 / 动态量化
- 模型裁剪
- 降低分辨率/通道数
- NEON SIMD 优化（A55 的必修课）
- 多核并行（pthread, OpenMP）


异构多核通信（AMP）
- RPMsg / OpenAMP
- M 核运行 RTOS（RT-Thread 或 FreeRTOS）
- A53/A55 与 M7/M33 数据交互方式





- [面向i.MX应用处理器的嵌入式Linux](https://www.nxp.com.cn/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX
)




