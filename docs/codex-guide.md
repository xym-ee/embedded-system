# Codex 工作说明

## 仓库是做什么的

这是一个长期维护的学习笔记仓库，主题是计算机系统与嵌入式系统。它既包含课程笔记，也包含工程实践、项目记录和个人方法论。

整理时不要把它看成单纯的 GitBook 目录，也不要看成普通代码项目。它更像一张持续演化的知识地图：

- 课程笔记用于系统学习。
- 工程专题用于记录可复用的技术栈和系统能力。
- 项目目录用于承接具体板卡、芯片和实验。
- 世界观和五个问题目录用于沉淀抽象理解。

## 根目录约定

根目录保持轻量，只放必要入口文件：

- `AGENTS.md`：给 Codex / Agent 的仓库说明。
- `README.md`：给读者的仓库首页。
- `SUMMARY.md`：GitBook / 导航目录。

整理计划、结构调整记录、给 Codex 的工作说明、脚本说明等，都放到 `docs/`。

## 归类原则

主线目录只给长期反复使用、会持续积累的能力：

- 裸机与接口：`30_bare_metal_and_interfaces/`
- 嵌入式软件框架：`31_embedded_software_frameworks/`
- RTOS 内核：`32_rtos_kernel/`
- Linux 使用与系统编程：`33_linux_systems/`
- 嵌入式 Linux 系统构建：`34_embedded_linux_systems/`
- 网络、OpenWrt 与 IoT：`36_network_and_iot_systems/`
- AI Agent 工具链：`37_ai_agent_tools/`

接触过但不是主业的方向不要轻易升为顶层主线：

- Linux 驱动：优先作为 `34_embedded_linux_systems/linux-drivers/` 的补充主题。
- FPGA / Zynq：优先作为 `40_projects/zynq/` 的项目实践。
- 汽车电子 / AUTOSAR：优先放入 `40_projects/s32k3/` 或 `40_projects/automotive-notes/`。

## 修改注意事项

- 不要随意删除旧笔记。即使结构不完美，也先通过索引、迁移记录和 README 说明过渡。
- 大规模移动目录前，先检查 `SUMMARY.md` 和各目录 `README.md` 的链接。
- 新增内容优先放到最贴近的已有目录，不为了主题名字好看而新增顶层目录。
- `SUMMARY.md` 可以用 `docs/tools/gen_summary.py` 生成；移动脚本后，推荐从仓库根目录运行：

```bash
python docs/tools/gen_summary.py
```
