# ESP-IDF 构建系统

ESP-IDF 的构建系统围绕 `idf.py`、CMake、Ninja、Kconfig 和 `sdkconfig` 展开。

学习构建系统的目的不是背命令，而是理解一个 ESP-IDF 工程是如何从源码变成固件镜像的。

## 常用命令

```sh
idf.py set-target esp32s3
idf.py menuconfig
idf.py build
idf.py -p COM16 flash
idf.py -p COM16 monitor
```

常用组合：

```sh
idf.py -p COM16 flash monitor
```

## 工程基本结构

一个常见 ESP-IDF 工程大致是：

```text
project/
  CMakeLists.txt
  sdkconfig
  sdkconfig.defaults
  partitions.csv
  main/
    CMakeLists.txt
    app_main.c
  components/
    xxx/
      CMakeLists.txt
      include/
      xxx.c
```

根目录 `CMakeLists.txt` 描述整个项目。

`main/` 是一个特殊组件，也可以理解为默认应用组件。

`components/` 里放自定义组件。

## idf.py

`idf.py` 是 ESP-IDF 提供的命令行入口。它本身不是编译器，而是调用底层工具完成构建、配置、烧录和监视。

可以先这样理解：

```text
idf.py
  ↓
CMake
  ↓
Ninja
  ↓
compiler / linker / objcopy
  ↓
bootloader.bin / partition-table.bin / app.bin
```

## CMake

ESP-IDF 使用 CMake 管理工程和组件。

组件通常通过 `idf_component_register` 注册：

```cmake
idf_component_register(
    SRCS "app_main.c"
    INCLUDE_DIRS "."
)
```

这里的关键不是语法，而是理解：组件向构建系统声明自己的源文件、头文件路径和依赖关系。

## Kconfig 和 sdkconfig

ESP-IDF 使用 Kconfig 管理配置项。`idf.py menuconfig` 修改后的配置会写入 `sdkconfig`。

可以把 `sdkconfig` 理解为“本工程的系统配置结果”。

常见配置包括：

- 目标芯片
- Flash 大小和模式
- PSRAM 配置
- FreeRTOS tick 频率
- 日志等级
- Wi-Fi、BLE、LWIP 等系统参数
- 分区表路径

如果要把常用配置固化到项目中，可以使用 `sdkconfig.defaults`。

## 构建产物

构建完成后，典型产物包括：

- bootloader 镜像
- partition table 镜像
- application 镜像
- map 文件
- elf 文件

`elf` 和 `map` 对理解链接、符号、内存占用很重要。后续可以结合 CSAPP 和裸机链接脚本来分析。


build 目录中的东西 三个镜像 + OTA 数据

bootloader.bin 二级 bootloader

partition-table.bin 来自 csv，描述布局

.bin 主 app

flasher_args.json 里放了所有烧录用到的信息。


## 当前要回答的问题

- 为什么 ESP-IDF 工程里有多个 `CMakeLists.txt`？
- `main` 为什么也是组件？
- `sdkconfig` 应该提交到仓库吗？
- `sdkconfig.defaults` 和 `sdkconfig` 分别适合放什么？
- 如何把自己的业务代码拆成多个组件？
- 如何从 map 文件看出固件大小和内存占用？

