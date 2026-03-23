


# claude code 基础

## 基本命令

基本命令，

/clear 清空上下文

/compact 压缩对话，

/cost 花费

/logout /login

/model 模型切换，opus 的模型，

/status 状态

/doctor 检测安装状态

如果知道解决思路，那么问题可以更高效的被 AI 解决。


## 几种模式

shift + tab

默认，规划，自动

规划模式里，有 todo list

通常也是先做顶层设计，提需求，规划技术方案。可以要求把计划输出到 plan.md 

做完计划后，可以要求按照计划去实现。

claude 给的 todos 基本上也是软件开发的一个流程。

全权放手干，不需要任何授权。

`claude --dangerously-skip-permissions`

此模式启动后会看到 bypass permissions on


网页游戏测试功能，或者一个网页应用如 todo 之类的。

## 记忆

CLAUDE.md

典型工作流程

CLAUDE.md -> 对话直到长度溢出 -> 运行 /compact -> 达到一个可交付的程度 -> 更新 CLAUDE.md 

CLAUDE.md ，一个持续发挥作用的全局变量。保留关键信息。


一个新项目，可以使用 /init，直接生成总结信息。

一开始提需求时，要求生成 plan.md，项目规划输出到 CLAUDE.md

>我需要设计一个电商网站，使用 java 开发，创建一个单独的文件夹：shop-demo。首先需要项目需求和技术方案到 plan.md，然后将项目规划输出到 CLAUDE.md，最后根据 plan.md 中的计划实现代码，参考 CLAUDE.md 中的规划。

任何内容都可以放进去，但是看情况。


## 会话管理

随时暂停和回滚，

esc 暂停，两次 esc 回退历史节点。

暂停也可以继续运行，历史信息都是在的。

/resume

make CLI great again

## 资源监控，批量任务

查看 token 消耗量，按天

npx ccusage@latest

查看实时消耗量

npx ccusage blocks --live

TASK.md

cat TASK.md | while IFS= 

按行传递给 claude 去运行。

## 一些使用技巧








