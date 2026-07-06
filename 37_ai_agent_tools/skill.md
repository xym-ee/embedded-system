
# Agent 使用与原理


早期，提升 claude 在特定任务的表现。

但是发现很好用。


后来全都跟上了，2025/12/18 Anthropic 将其发布为开放标准，支持跨平台

Agent skill 超越了单一 claude 产品范畴，成为通用的设计


概念 - 基本用法 - 高级用法(reference script)


## 基础用法

一个说明文档 + 各种资源



`SKILL.md` 本身，一个说明文档。


用户，claude code，大模型。

使用一个 skill 的时候，

用户发送 请求，claude code 把请求和 skill 名称及描述一同送给大模型。

大模型判断是否可以使用 skill，把信息告诉 claude code，然后 claude code 把 SKILL.md 内容完整发送给 大模型。

然后大模型按照 SKILL.md 的流程继续。

核心机制，按需加载，


## reference

我们希望不仅仅是简单复述，有更完善的内容。

reference，按需加载的按需加载。

头文件引用。



## script

动手做事情。

## 区别


reference 会全部塞进上下文

script 执行，影响不大。


## 渐进式披露

元数据层，名称 描述，始终加载

指令层，SKILL.md 中除名称和描述之外的内容，按需加载

资源层，reference script，按需加载的按需加载。

reference 被读取，放入上下文回答参考。Script 被执行，claude 不会去看代码内容。

但是如果没说清楚，claude 还是有可能看 script 里的内容的。指示是否清晰的问题，看script就占用上下文了。


## MCP

本质上都是让模型连接和操作外部世界。

MCP 

MCP connects Claude to data.

Skills teach Claude what to do with that data.

skill 也能连数据，通用约定？适合的场景？  复杂度上去以后区别会慢慢体现出来，实践出来的。目前是这样，以后可能还会变。



## 












