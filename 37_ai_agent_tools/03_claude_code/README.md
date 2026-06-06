
# claude code



https://github.com/KimYx0207/AI-Coding-Guide-Zh




Claude Code ，24 小时在线的高级程序员。

人讲需求，然后写代码、该 bug、搜资料、运行测试。


安全，代码在本地，可以私有部署，敏感项目使用。多语言、框架支持。

全项目理解，脚本自动化，CI/CD 集成。

Cursor 或 Copilt ，实时代码补全和建议，编码还是人主导。




## 安装

windows 和 ubuntu

cc-switch 切换模型


## 使用


```sh
# 在任意目录启动
claude

# 启动流程：
# 1. 检测当前目录
# 2. 加载CLAUDE.md（如果存在）
# 3. 进入交互式对话界面
```

claude 也是一个 linux CLI 应用程序，可以将问题作为参数传入

```sh
# 带交互界面
claude "任意问题"

# 只输出一次响应
claude -p "任何问题"
```

支持 unix 的管道，可以和任意的 unix 工具结合起来使用。

```sh
cat llm.c | claude -p "这段代码实现了什么功能" > 1.md
```

解释代码，分析 log，甚至可以直接 cat elf 给模型上点强度。




```
~/.claude/                      ← 全局配置目录
├── config.json                 ← 全局配置文件
├── auth-token.json             ← 认证令牌
├── trusted-directories.json    ← 信任的目录列表
├── cache/                      ← 缓存目录
└── logs/                       ← 日志目录

项目目录/.claude/              ← 项目级配置
├── config.json                 ← 项目配置（覆盖全局）
├── commands/                   ← 自定义命令
├── skills/                     ← 自定义技能
└── hooks/                      ← 自定义钩子
```


常用启动方式
```sh
claude

# 无需权限
claude --dangerously-skip-permissions	

# 直接提问，unix 管道协作
claude -p "你的问题"
```


常用命令
```sh
claude update

claude --help
```














