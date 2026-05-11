
# subagent

怎么把一个复杂任务拆给多个独立上下文的 AI 子代理去做。

Subagent 的关键价值是：把主会话不适合亲自做的、边界清晰的子任务，委派给独立 agent

例如：请开一个 reviewer subagent，检查这次改动的回归风险和缺失测试。

并行开两个 subagent：
- 1. 一个检查后端接口变更
- 2. 一个检查前端样式回归

主代理负责协调，子代理负责专项分析或执行。

管理 agents，/agents


.claude/agents/

  项目级子代理定义目录，适合当前仓库专用的 reviewer、tester、doc-writer 等。

~/.claude/agents/

  用户级子代理定义目录，适合你跨项目复用的个人代理。



什么时候适合用 Subagent，适合：
- 代码审查
- 安全审计
- 测试缺口分析
- 大型项目里并行阅读不同模块
- 让一个代理只负责前端，另一个只负责后端
- 让一个代理专门检查方案风险

不适合：
- 很小的单步任务
- 需要和 Claude 高频来回确认的任务
- 边界不清楚的探索性任务
- 所有代理都要同时改同一批文件的任务

任务能被清楚切开，就适合 Subagent；切不开，就先别拆。


---

claude code 快速上手，subagent，指派一个 agent 专家去干活。

了解 agent team 的概念，一个项目组分工合作。

任务拆分的判断力。



Agent Team，
- Team Lead 分配任务，协调进度
- Teammate 执行任务与汇报
- Task List 共享任务列表，成员进度和状态，看板
- Send Message ，agent通信，直接消息或广播，


sub agent 为一对一，子 agent 返回结果给主 agent。


## 快速体验

agent team 需要启用。

启用
```sh
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

claude code，

```md
我正在设计一个agent专注于空间智能场景里的物联网设备交互。或者叫做 Agent OS。确定最终的架构和技术方案。

创建一个 agent team 包含以下角色
- 架构设计师
- 物联网工程师
- LLM 应用工程师
- Agent 专家
- 架构抨击者，找出设计中的不合理之处

保存关键的决定信息。
```
claude 作为 team lead 创建，分配，汇总结果。

结束时清理

一些 demo

### 脑暴

官方文档 agent team 入门场景

```sh
我正在设计一个命令行界面（CLI）工具，基于 LLM api 实现终端 AI 能力集成。

组建一支由3名队友组成的代理团队：
- 用户体验设计师：设计命令界面和用户流程
- 技术架构师：提出实现架构
- 唱反调：抨击这个想法，并找出其失败模式

让他们进行辩论，然后制定一份最终产品规格说明，内容包括：
1. 目标用户
2. CLI 命令
3. 工具功能
4. 最小可行产品（MVP）的范围
请勿编辑文件。保留关键决策信息
```


### 并行代码审查


```md
组一个 Agent Team 来审查这个仓库

3 个评审员
- 逻辑正确性层次：看代码能不能正确完成需求。
- 可维护性层次：看代码是否规范、清晰、容易读，能不能方便修改这段代码。
- 设计层次：看整体方案是否合理。

每位评审者应独立进行检查，然后对彼此的发现提出质疑。
返回一份包含严重性、文件路径和建议修复方法的最终报告。
请勿编辑文件。
```






## 入门


到这里，基本理解了 claude 的工作流。

选一个真实小项目
写一份 CLAUDE.md
做一个 /dev:code-review command
接一个最简单的 MCP
试一次 researcher + implementer + reviewer 的 Agent Team
最后让 reviewer 审查结果












