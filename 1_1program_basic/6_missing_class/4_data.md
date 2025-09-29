
# 数据整理

当使用管道运算符的时候，其实就是在进行某种形式的数据整理。

例如这样一条命令 journalctl | grep -i intel，它会找到所有包含 intel（不区分大小写）的系统日志。您可能并不认为这是数据整理，但是它确实将某种形式的数据（全部系统日志）转换成了另外一种形式的数据（仅包含 intel 的日志）。大多数情况下，数据整理需要您能够明确哪些工具可以被用来达成特定数据整理的目的，并且明白如何组合使用这些工具。

日志处理是典型的需要做数据处理的场景。

比如查看哪些人什么时候登陆过服务器。

```bash
journalctl | grep sshd
journalctl | grep sshd | grep 'Disconnected' > ssg.log
```

还是有很多无关的数据，可以删除掉，使用 sed 工具

最常用的替换 `sed 's/被替换的/替换内容/'`

一些特殊的符号
- `.` 除换行符之外的 “任意单个字符”
- `*` 匹配前面字符零次或多次
- `+` 匹配前面字符一次或多次
- `[abc]` 匹配 a, b 和 c 中的任意一个
- `(RX1|RX2)` 任何能够匹配 RX1 或 RX2 的结果
- `^` 行首
- `$` 行尾

`journalctl | grep sshd | grep 'Disconnected' | sed 's/.*Disconnected from //'`

匹配任何开头的内容和 Disconnected from ，然后替换成什么都没有。

这是 sed 常用的使用方法。还有更多的功能。

想做更复杂的事情，可以使用在线的正则表达式工具调试，或者直接询问 gpt。

为了完成某种匹配，最终可能会写出非常复杂的正则表达式。关于如何匹配电子邮箱地址一点也不简单。

sed 还有更多的功能，如文本注入，打印特定行。

sort 会对其输入数据进行排序。uniq -c 会把连续出现的行折叠为一行并使用出现次数作为前缀。我们希望按照出现次数排序，过滤出最常出现的用户名：


```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | awk '{print $2}' | paste -sd,
```

awk 是另外一种编辑器。其实是一种编程语言。只看看最基本的用法就好。

awk 一个代码块。在代码块中，`$0` 表示整行的内容，`$1` 到 `$n` 为一行中的 n 个区域，区域的分割基于 awk 的域分隔符（默认是空格，可以通过 -F 来修改）。在这个例子中，我们的代码意思是：对于每一行文本，打印其第二个部分，也就是用户名。

此外还可以分析数据，统计数据，甚至画图




