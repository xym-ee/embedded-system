# ADAU1701：嵌入式视角下的音频 DSP 入门

这里记录 ADAU1701 的学习、调试和工程化使用过程。

这部分内容的重点不是从头推导音频算法，而是从嵌入式工程师熟悉的视角进入音频系统：把音频 DSP 看成一个可以配置、下载、调参和集成到产品中的专用处理器。

## 学习目标

- 建立音频 DSP 的基本概念：输入、采样、处理、输出。
- 理解 ADAU1701 在一条音频链路中的位置。
- 熟悉 SigmaStudio 的基本工作流。
- 搞清楚 MCU、EEPROM 和 ADAU1701 之间的启动与控制关系。
- 形成一套可复用的音频调试方法。

## 笔记

- [音频 DSP 的嵌入式视角](./01_audio_dsp_overview.md)
- [ADAU1701 信号链路](./02_adau1701_signal_chain.md)
- [SigmaStudio 基本工作流](./03_sigma_studio_basic.md)
- [下载、启动与存储](./04_download_and_boot.md)
- [MCU 控制 ADAU1701](./05_mcu_control_dsp.md)
- [调试记录](./06_debug_notes.md)

## 归类边界

- 具体芯片、板子、连接、启动、下载、调参和问题记录放在这里。
- 采样率、音频缓冲、增益、滤波、混响等通用音频概念，可以后续整理到 `36_network_and_iot_systems/audio-video-systems/`。
- 如果 ESP32 只是作为控制器使用，相关内容仍然优先放在这里，而不是放进 ESP32 主线。
