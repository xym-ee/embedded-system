
# AGENTS.md

## 仓库定位

这个仓库是个人的“计算机与嵌入式系统”学习笔记。它不是单一项目源码仓库，而是一份长期演化的知识地图，用来整理计算机系统、嵌入式软件、RTOS、Linux、网络系统、AI Agent 工具链等学习内容。

仓库的核心目标是：从课程知识、工程实践和个人思考中，逐步沉淀出对系统构造的理解。

## 内容主线

- `00_worldview/`：跨学科世界观、系统观、AI Agent 与工程系统思考。
- `10_five_questions_of_computer_systems/`：用五个问题组织计算机系统理解。
- `20_cs_courses/`：本科计算机课程、经典教材和系统化学习笔记。
- `30_bare_metal_and_interfaces/` 到 `37_ai_agent_tools/`：当前主要工程专题。
- `40_projects/`：具体板卡、芯片、实验和项目实践。

## 给 Codex 的工作约定

- 先读 `README.md`、`SUMMARY.md` 和 `docs/README.md`，再判断内容应该放在哪里。
- 根目录保持轻量，只保留 `AGENTS.md`、`README.md`、`SUMMARY.md` 这类入口文件；结构说明、迁移记录、工具说明放入 `docs/`。
- 不要为了编号连续而新增顶层主线目录。Linux 驱动、FPGA / Zynq、汽车电子 / AUTOSAR 当前按接触型补充内容处理，具体规则见 `docs/structure-adjustment-record.md`。
- 修改笔记时尽量保持原有中文表达风格，只做必要的结构化、补充和纠错。
- 移动或重命名大量笔记前，先更新说明文档或迁移计划，避免破坏 `SUMMARY.md` 中的链接。
