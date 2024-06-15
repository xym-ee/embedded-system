---
sort: 4
---
# NXP i.MX 应用处理器裸机开发


linux 环境下，裸机开发。工具使用和芯片熟悉

## 开发环境


### 虚拟机+ubuntu

- vmware workstation
- ubuntu
  - 安装 vmware-tools ：开源 `sudo apt install open-vm-tools-desktop`


### 网络文件系统 NFS 

主机安装

- `sudo apt install nfs-kernel-server`
- `sudo vim /etc/exports` 配置要共享的文件夹，增加配置项
  - `/home/xym/ws_linux *(rw,sync,no_root_squash)`
    - `/home/xym/ws_linux` 目录
    - `*` 所有网段，也可设置为 10.0.0.0/24 指定网段
    - `rw` 可读可写
    - `sync` 同步缓存
    - `no_root_squash` 访问者给 root 权限
- `sudo /etc/init.d/nfs-kernel-server restart` 重启一下 nfs 服务
- `showmount -e` 可以看到挂载的共享目录

开发板挂载共享文件系统
- `mount -t nfs 10.0.0.10:/home/xym/ws_linux /mnt`
- `mount -t nfs -o nolock,nfsvers=3 10.0.0.10:/home/xym/ws_linux /mnt`

### SSH

- `sudo apt install openssh-server`

### 编译器



- https://www.linaro.org/
- https://snapshots.linaro.org/components/toolchain/binaries/

下载后解压，添加路径到环境变量中

- `sudo vim /etc/profile`
- 对于 fish，可以添加到fish的配置文件中
  - set PATH $PATH /xxxxx







