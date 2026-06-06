

# Hooks 系统


## 理解 hooks

Hooks 可以先理解成：Claude Code 里的事件触发器

它的作用是：当 Claude Code 里发生某个事件时，自动执行配置好的脚本。

比如：
- Claude 准备写文件前 -> 触发 PreToolUse
- Claude 写完文件后 -> 触发 PostToolUse
- 用户提交提示词后 -> 触发 UserPromptSubmit
- 会话启动时 -> 触发 SessionStart
- Claude 需要你确认时 -> 触发 Notification

为什么需要 Hooks？如果只是告诉 Claude：
- 每次改完代码后都要格式化
- 不要修改 `.env`
- 提交前先跑测试

Claude 大多数时候会照做，**但它可能忘**。Hook 的价值就是把这些“希望 AI 记住的规则”变成确定性自动化。

提示词规则：Claude 可能遵守。Hook 规则：事件发生就执行

一个最简单的例子，可以配置一个 PreToolUse Hook：
- 事件：Claude 准备调用 Write 或 Edit
- 脚本：检查文件路径
- 规则：如果路径是 .env，就拒绝
- 结果：Claude 无法修改 .env

这时它就不是“请你不要改 .env”这种软约束，而是“工具调用前被拦截”的硬约束。

Hook 的核心结构，一个 Hook 通常包含三部分：
- 触发事件：什么时候执行
- 匹配条件：哪些工具或场景会触发
- 脚本命令：触发后运行什么

比如概念上是这样：
```json
{
"hooks": {
    "PreToolUse": [
    {
        "matcher": "Write",
        "hooks": [
        {
            "type": "command",
            "command": "python .claude/hooks/protect-files.py"
        }
        ]
    }
    ]
}
}
```

意思是：当 Claude 准备使用 Write 工具时，运行 protect-files.py 这个脚本，由脚本决定是否允许继续。

比较重要的三个 Hook，

UserPromptSubmit

用户输入提交后、Claude 处理前触发。适合自动补充提示词规则，比如写作规范、任务模板、安全提醒。

PreToolUse

Claude 调用工具前触发。适合做权限检查和危险操作拦截，比如禁止改 .env、禁止执行危险 shell 命令。

PostToolUse

Claude 调用工具成功后触发。适合做后处理，比如自动格式化、自动备份、自动跑测试、写日志。

```
用户输入
↓
UserPromptSubmit Hook，可修改或增强提示词
↓
Claude 思考并决定调用工具
↓
PreToolUse Hook，可允许/拒绝/询问
↓
工具真正执行
↓
PostToolUse Hook，可执行后处理
↓
结果返回给用户
```

所以 Hooks 不是用来“让 Claude 更聪明”的，而是用来“让工作流更稳定、更安全、更自动化”的。











