
# 命令行环境

改善 shell 及其他工具的工作流的方法，提高效率，这主要是通过定义别名或基于配置文件对其进行配置来实现的。

## 任务控制


中断正在执行的任务，比如当一个命令需要执行很长时间才能完成时（假设我们在使用 find 搜索一个非常大的目录结构）。大多数情况下，我们可以使用 Ctrl-C 来停止命令的执行。

### 结束进程

shell 使用 unix 提供的**信号机制**来和进程通信。一个进程接收到信号时，会立即处理该信号。信号是一种**软件中断**。

Ctrl + C ，shell 会发送一个 SIGINT 到进程。


## 暂停和后台执行

SIGSTOP 会让进程暂停。在终端中，键入 Ctrl-Z 会让 shell 发送 SIGTSTP 信号。

可以使用 `fg` 或 `bg` 命令恢复暂停的工作。它们分别表示在前台继续或在后台继续。

jobs 命令会列出当前终端会话中尚未完成的全部任务。

命令中的 `&` 后缀可以让命令在直接在后台运行，这使得您可以直接在 shell 中继续做其他操作，不过它此时还是会使用 shell 的标准输出。


## 终端多路复用

tmux

## 别名

shell 的别名相当于一个长命令的缩写，bash 中的语法

```bash
alias alias_name="command_to_alias arg1 arg2"
```

`=` 两边没空格，alias 是一个命令。


```bash
# 创建常用命令的缩写
alias ll="ls -lh"

# 能够少输入很多
alias gs="git status"
alias gc="git commit"
alias v="vim"

# 手误打错命令也没关系
alias sl=ls

# 重新定义一些命令行的默认行为
alias mv="mv -i"           # -i prompts before overwrite
alias mkdir="mkdir -p"     # -p make parent dirs as needed
alias df="df -h"           # -h prints human readable format

# 别名可以组合使用
alias la="ls -A"
alias lla="la -l"

# 在忽略某个别名
\ls
# 或者禁用别名
unalias la

# 获取别名的定义
alias ll
# 会打印 ll='ls -lh'
```

为了让自己的设置持续生效，可以吧配置放到 shell 的启动文件里。

## 配置文件

很多程序通过 dotfile 的配置文件来完成的（因为它们的文件名以 . 开头，例如 `~/.vimrc`。也正因为此，它们默认是隐藏文件，ls 并不会显示它们）。

shell 的配置也是通过这类文件完成的。在启动时， shell 程序会读取很多文件以加载其配置项。对于 bash 来说，可以通过编辑 `.bashrc` 或 `.bash_profile` 来进行配置。在文件中可以添加需要在启动时执行的命令，例如别名，或者是环境变量。

很多程序都要求在 shell 的配置文件中包含一行类似 `export PATH="$PATH:/path/to/program/bin"` 的命令，这样才能确保这些程序能够被 shell 找到。

一种好的管理配置文件的方式：将所有的配置文件放到一个文件夹内使用版本控制系统进行管理，用脚本将其符号链接到需要的地方。好处
- 新设备安装简单
- 可移植性，工具在任何地方都能以相同的配置工作
- 同步
- 修改追踪

## 配置文件的可移植性

配置文件的一个常见的痛点是它可能并不能在多种设备上生效。例如，操作系统或者 shell 是不同的，则配置文件是无法生效的。或者，有时仅希望特定的配置只在某些设备上生效。

有一些技巧可以轻松达成这些目的。
```bash
if [[ "$(uname)" == "Linux" ]]; then {do_something}; fi

# 使用和 shell 相关的配置时先检查当前 shell 类型
if [[ "$SHELL" == "zsh" ]]; then {do_something}; fi

# 也可以针对特定的设备进行配置
if [[ "$(hostname)" == "myServer" ]]; then {do_something}; fi
```

## 远程设备

通常的 ssh 命令 `ssh user@ip`

ssh 的一个经常被忽视的特性是它可以直接远程执行命令。 `ssh foobar@server ls` 可以直接在 foobar 执行 ls 命令。 想要配合管道来使用也可以， `ssh foobar@server ls | grep PATTERN` 会在本地查询远端 ls 的输出而 `ls | ssh foobar@server grep PATTERN` 会在远端对本地 ls 输出的结果进行查询。








