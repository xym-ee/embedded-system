
# AI Agent

这个目录记录 AI Agent、AI 工作流、编程助手和自动化工具链相关内容。

它不是“AI 应用大杂烩”，而是围绕一个问题展开：如何把 LLM、Agent 和工作流编排当成新的工程工具来理解、使用和构造。

重点包括：

- 普通用户如何使用 AI 完成写作、整理、分析和办公类任务。
- 程序员如何使用 Claude Code、Codex 等工具读代码、改代码、跑测试、管理项目。
- LLM、token、context、prompt、tool calling、MCP、skill、hooks、subagent 等基础概念。
- Claude Code / Codex 等 Agent 编程工具的使用方式和背后机制。
- Dify / n8n 等 AI 工作流工具如何把 LLM、API、知识库和业务流程编排起来。
- 自己复刻一个最简单的 mini agent，用代码理解 Agent 的基本工作循环。

## 内容边界

放在这里的内容：

- Claude Code、Codex 等 Agent 工具的使用和机制。
- Dify、n8n、LangFlow、Flowise 等 AI 工作流工具的使用和机制。
- MCP、skill、hooks、subagent、memory、tool calling 等 Agent 工程概念。
- AI 辅助工程开发流程，包括需求拆解、代码修改、测试验证、项目管理。
- harness engineering，也就是模型之外的上下文供给、执行环境、验证反馈和状态管理。

不作为本目录主线的内容：

- 嵌入式 AI 推理部署、NPU、ONNX Runtime、TensorRT、模型量化等内容，更偏向 `34_embedded_linux_systems/` 或具体项目目录。
- 关于“AI Agent 会如何改变软件、工程系统和社会组织”的世界观思考，更适合放在 `00_worldview/`。

## 学习主线

建议按下面几层理解。

### 1. 先会用

从实际任务出发，而不是一上来陷入概念。

- 单次对话：解释一个概念、改一小段文字、生成一个脚本。
- 单个小任务：整理文件、分析日志、改一个 bug、写一个 README。
- 程序员用法：读代码、定位问题、生成测试、重构局部模块。
- 非程序员用法：资料整理、表格处理、写作辅助、流程规划。
- 大项目管理：需求拆解、计划文档、任务队列、验收标准、迭代记录。

### 2. 再理解概念

这些概念不是孤立名词，而是为了理解 Agent 为什么这样工作。

- LLM：大语言模型，本质上可以先理解成一个文本到文本的函数。
- token：模型处理文本的基本单位。
- context：模型当前能看到的全部输入，包括用户问题、历史对话、工具结果和系统提示。
- prompt：给模型的任务描述和行为约束。
- tool calling：模型不能直接操作外部世界，需要通过工具完成查询、读写文件、运行命令等动作。
- MCP：一种工具接入协议，用来统一 Agent 和外部工具之间的连接方式。
- skill：把某类任务的经验、流程和格式沉淀成可复用说明。
- hooks：在 Agent 工作流程中的特定时机插入自动化动作。
- subagent：把复杂任务拆给更专门的子 Agent。
- workflow：人预先设计好的任务流，LLM 通常作为其中一个节点参与处理。

### 3. 区分 Workflow 和 Agent

Dify、n8n 这类工具比较特殊。它们可以接入 LLM，也可能带有 Agent 节点，但默认形态更像 AI 工作流搭建工具，而不是完全自主闭环的 Agent。

Workflow 更强调“人设计流程”：

```text
输入
  -> 节点 A
  -> LLM 节点
  -> 条件判断
  -> API / 数据库 / 知识库
  -> 输出
```

Agent 更强调“模型根据目标自主决定下一步”：

```text
目标
  -> 模型思考下一步
  -> 调用工具
  -> 观察结果
  -> 再决定下一步
  -> 循环直到完成
```

所以 Dify / n8n 适合单独归为 AI workflow tools。它们的核心价值是把 LLM、知识库、API、数据库、条件判断、人机交互等模块编排成可运行应用。

### 4. 用 Claude Code 实战

Claude Code 是理解 Agent 编程助手的好入口。

它既能作为日常编程工具使用，也能暴露出许多 Agent 系统本身的问题：

- 如何管理上下文。
- 如何给工具授权。
- 如何规划长任务。
- 如何使用 `CLAUDE.md` 保存项目记忆。
- 如何通过 MCP 扩展能力。
- 如何通过 hooks、skills、subagent 定制工作流。

### 5. 复刻 mini agent

当基本概念和工具使用都熟悉以后，可以自己写一个最小 Agent。

最小循环大概是：

```text
用户输入
  -> 构造 context
  -> 调用 LLM
  -> 判断是否需要调用工具
  -> 执行工具
  -> 工具结果写回 context
  -> 继续调用 LLM
  -> 得到最终回答
```

这个过程跑通以后，Claude Code、Codex、Dify、MCP、skill、hooks 都可以放回同一个系统框架里理解。

### 6. 再看 harness engineering

当 Agent 不只是玩具，而是要稳定完成真实任务时，模型之外的工程设施会变得很重要。

需要关心：

- 任务如何被规范描述。
- 上下文如何供给。
- 执行环境如何隔离。
- 工具权限如何控制。
- 结果如何验证。
- 失败如何回滚。
- 长期状态如何管理。

## 建议目录结构

后续可以逐步整理成下面的结构，不需要一次性搬完。

```text
37_ai_agent_tools/
  README.md

  01_concepts/
    01_llm_token_context.md
    02_prompt_and_messages.md
    03_tool_calling.md
    04_mcp.md
    05_memory_skill_hooks.md
    06_agent_patterns.md
    07_workflow_vs_agent.md

  02_usage_patterns/
    01_single_chat_task.md
    02_non_programmer_usage.md
    03_programmer_usage.md
    04_file_and_knowledge_work.md
    05_project_management.md

  03_claude_code/
    01_basic_usage.md
    02_context_and_memory.md
    03_permissions_and_terminal.md
    04_mcp.md
    05_hooks.md
    06_subagent.md
    07_skills.md
    08_project_workflow.md

  04_codex/

  05_ai_workflow_tools/
    dify/
    n8n/
    langflow.md
    flowise.md

  06_mini_agent/
    01_agent_loop.md
    02_minimal_llm_call.md
    03_context_loop.md
    04_tool_calling.md
    05_file_tools.md
    06_permissions.md
    07_mcp_client.md

  07_harness_engineering/
```

## 当前内容索引

### 概念与总论

- [概念](./1_concept.md)：LLM、token、context、prompt、tool、MCP、Agent、skill 等基础概念。
- [AI 开发](./1.md)：早期 AI 开发相关记录。

### Claude Code

- [claude code 总览](./learn_cc/README.md)
- [基础使用](./learn_cc/1基础使用.md)
- [MCP 集成](./learn_cc/2mcp.md)
- [Hooks 系统](./learn_cc/3hooks.md)
- [subagent](./learn_cc/4subagent.md)
- [s01](./learn_cc/s01.md)

零散旧笔记：

- [claude code](./2_claude_code.md)
- [claude code 基础](./3_basic_cmd.md)
- [cc](./4_cc_.md)
- [claude code](./222.md)

### Codex

- [codex](./codex/README.md)

### AI 工作流工具

- [AI 应用开发](./dify/README.md)
- [本地部署](./dify/1.md)

后续可以补充：

- n8n：偏通用自动化流程编排，可把 LLM 节点接入业务流程。
- LangFlow / Flowise：偏 LLM 应用和链式流程可视化搭建。

### Harness Engineering

- [Harness Engineering](./harness-engineering/README.md)
- [L01 02](./harness-engineering/1.md)
- [代码仓库作为唯一事实来源](./harness-engineering/2.md)
- [prj1](./harness-engineering/prj1.md)

### 边界内容

嵌入式 AI 部署、NPU、推理运行时、Yocto / Buildroot 构建环境等内容不作为本目录主线，已经放到 `34_embedded_linux_systems/` 下的新主题：

- [嵌入式 AI 部署](../34_embedded_linux_systems/ai-deployment/README.md)

## 参考资料

- [Claude Code: A Highly Agentic Coding Assistant](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/)
- [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering)
- [vibe-coding-cn](https://github.com/2025Emma/vibe-coding-cn)
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code/blob/main/README-zh.md)
