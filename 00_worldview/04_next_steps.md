# 后续整理方式

`00-worldview` 先作为索引层存在，不急着移动原来的材料。

## 先不做大搬家

现有仓库里有两类结构：

- 按课程和技术栈组织的结构：C/C++、CSAPP、操作系统、RTOS、Linux、网络、AI。
- 按系统问题组织的结构：计算、控制、资源、连接、复杂性。

前者适合查资料，后者适合形成世界观。现在不需要立刻把所有文件迁移到新目录，否则会破坏原来的学习痕迹，也容易产生大量低价值重排。

更好的方式是：

```text
原目录保留材料
00-worldview 负责抽象、索引、重组和提炼
```

## 给每篇旧材料打一个“系统问题标签”

可以逐步在重要 README 或章节开头加一段很短的定位：

```md
本文回答的问题：
- 计算是什么：程序如何表示状态迁移。
- 控制如何建立：系统调用如何转移控制权。
```

这样不用重排文件，也能让旧材料进入新主线。

## 优先整理高价值节点

不是所有笔记都需要同等整理。优先处理那些“连接多层系统”的文章：

- `README.md`：总论和 AI/Agent 新层。
- `1/chapter2/2.md`：从 hello world 贯通系统。
- `1_5_operating_system/1_introduction/README.md`：操作系统总论。
- `1_5_operating_system/1_introduction/4_状态机应用.md`：状态机视角。
- `1_5_operating_system/3_virtualization/3_syscall_shell.md`：shell、syscall、对象/API。
- `3_2_linux_image/README.md`：从源码到跑起来的 Linux。
- `3_3_linux_driver/README.md`：设备模型与注册。
- `4_ai_develop/1_concept.md`：LLM、Tool、MCP、Agent。
- `4_ai_develop/HarnessEngineering/1.md`：Harness 五层。
- `4_ai_develop/learn_cc/*.md`：Claude Code 具体机制。

这些文章足够支撑一条主干。

## 建一个冷启动问题列表

以后整理每个大主题时，可以问同一组问题：

1. 这个系统的状态是什么？
2. 初始状态如何建立？
3. 状态迁移由谁驱动？
4. 控制权在哪里转移？
5. 资源由谁分配？
6. 边界如何跨越？
7. 失败时如何观察和恢复？
8. 哪些信息必须持久化？
9. 最小可运行模型是什么？
10. 它和真实复杂系统的差异是什么？

这组问题可以用于操作系统、RTOS、Linux 驱动、网络、Agent OS。

## Claude Code / Agent OS 这条线可以单独成卷

建议后续在 `4_ai_develop` 下继续保留实践材料，同时在 `00-worldview/03_agent_os.md` 里维护总论。

可逐步补充：

- `Agent = LLM + Harness` 的完整模型。
- Claude Code 作为 low-level harness 的结构分析。
- MCP 和设备驱动模型的对照。
- Commands/Skills 作为自然语言程序的设计原则。
- Hooks 作为确定性控制层。
- Subagent/Agent Team 作为并发和组织模型。
- 仓库作为唯一事实来源的工程规范。

## 一条可执行的整理节奏

每次只做一小步：

1. 选一篇旧材料。
2. 提炼它回答了哪个系统问题。
3. 找出里面最有代表性的 3 到 5 个观点。
4. 在 `00-worldview` 里补一段索引或总结。
5. 不急着改原文，除非原文已经明显过时。

这样能保留五年积累的自然纹理，同时慢慢长出新的主干。
