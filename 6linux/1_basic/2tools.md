---
sort: 2
---
# 系统编程开发环境


- ubuntu 和 windows 文件传输
- ubuntu nfs 和 ssh
- 交叉编译工具链
- 代码编辑软件
- 串口调试工具



## 开发主机


物理机安装 ubuntu，或者虚拟机安装ubuntu，性能可能有一些损失。但是在使用上没什么区别。

关注网络设置，virtual box 里。

- 网络地址转换器(NAT)
  - 只能满足虚拟机最基础的上网需求
  - 虚拟机之间无法 ping 通
  - 虚拟机可以 ping 通主机(虚拟机的网关就是主机)
  - 主机不能 ping 通虚拟机
- 桥接网卡
  - 完全模拟一台网络上的实体机
  - 通过主机网卡直连网络，IP 由 DHCP 分配
  - 所以如果主机无法上网，功能就全没了
- 仅主机网络(Host only)
  - 主机无法上网的情况下，模拟一个局域网，虚拟机互联
- 内部网络
  - 虚拟机互联，隔离主机

在虚拟机安装时，一般使用桥接网卡的模式，这样在网络上，虚拟机和物理机有一样的地位，可以分配一个固定的 IP，方便后面通过网络做更多的事情。



## 远程终端工具

在 ubuntu 主机中，可以直接在终端中使用 ssh，开发板已经安装并启动了 ssh 工具。

windows中，
- MobaXterm
- vscode 安装 ssh 插件
  - remote explorer

ssh 主机需要安装功能

```bash

```

## 代码编辑器

在 Ubuntu 中，可以直接用 vim，现代化一点的可以用 clion，也可以用 linux 版的 vscode。

或者使用 windows 版本的 vscode 远程工具。


## NFS

1.主机安装
```bash
sudo apt install nfs-kernel-server
```

2.配置 nfs 共享的目录，配置文件为 `/etc/exports`

```
/home/xym/ws_linux 10.0.0.10/24(rw,sync,all_squash,no_subtree_check)
```


3.重启NFS服务

```bash
sudo /etc/init.d/nfs-kernel-server restart

#可以查看当前共享的目录
showmount -e
```

开发板上的操作


```
mount 10.0.0.10:/home/xym/ws_linux /mount

#查看挂载的目录
df
```



