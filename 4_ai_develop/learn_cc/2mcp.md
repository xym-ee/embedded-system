
# MCP 集成


配置常用 MCP 服务器。

理解协议和自定义开发。

MCP 集成的目标：让 cc 不止会读写当前项目，还能通过标准接口调用外部系统。



## 基本概念

MCP 的基本模型

MCP 不是某个具体工具，而是协议。结构是：

Claude Code = MCP Client
外部能力 = MCP Server
具体可调用函数 = Tools
只读数据 = Resources
提示模板 = Prompts

最重要的是分清：

MCP Server 不是 AI
MCP Server 是 AI 可以调用的工具服务

比如 GitHub MCP Server 提供 create_issue、list_prs 这类工具；SQLite MCP Server
提供查询数据库的工具。


常用 MCP Server

对实际使用最有价值的是：

filesystem  文件系统访问
github      Issue / PR / repo 操作
sqlite / postgres / mysql  数据库查询
context7    查最新技术文档
brave / search 类工具  网络搜索
puppeteer / browser 类工具  浏览器自动化


MCP 的配置使用 json 

```json
{
"mcpServers": {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    }
}
}
```

和 unix 里定义 services 类似，cmd + agrs + env


不用一开始就写 MCP server，但可以理解
- STDIO：本地子进程通信，最常见，像命令行程序通过 stdin/stdout 说话
- HTTP：远程服务通信，适合团队或服务器部署
- JSON-RPC：请求/响应格式

一个模型：Claude Code 启动一个 MCP Server 子进程，通过 JSON-RPC 问它“你有哪些工具”， 然后在需要时调用这些工具


MCP 也是解决 claude 对接 AI 工具的问题

```raw
Claude Desktop → [自定义代码] → GitHub
Claude Desktop → [自定义代码] → 数据库
Claude Desktop → [自定义代码] → 文件系统

VS Code + AI → [另一套代码] → GitHub
VS Code + AI → [另一套代码] → 数据库

```

解决方案：统一接口，一次开发到处使用
```raw
Claude Desktop ──┐
VS Code + AI ────┼── MCP协议 ── GitHub MCP Server
Cursor ──────────┤              数据库 MCP Server
任何AI工具 ───────┘              文件系统 MCP Server
```

2024.11 Anthropic 发布 1.0

2025.12 捐赠给 Linux 基金会，成为行业标准




## 接入

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```











