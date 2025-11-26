

正点原子 参考的软件版本
- uboot imx4.1.15_2.1.0_ga
- kernel imx4.1.15_2.1.0_ga

NXP 官网提供的版本，Linux 6.6.52_2.2.0

全新安装的 ubuntu22.04 

安装 open-ssh

i.MX 移植指南

i.MX Porting Guide


To build Kernel in a standalone environment, first, generate a development SDK, which includes the tools, toolchain, and small rootfs to compile against to put on the host machine.


## 代理设置

.bashrc 

```sh
export http_proxy="http://Clash:iLUb7CBl@192.168.1.2:7893"
export https_proxy="http://Clash:iLUb7CBl@192.168.1.2:7893"
export HTTP_PROXY="${http_proxy}"
export HTTPS_PROXY="${https_proxy}"
```








## Yocto Project, docker

NXP 官方现在推荐你使用 Docker 来构建 Yocto，而不是直接在 Ubuntu 系统里搭依赖。

[nxp-imx imx-docker](https://github.com/nxp-imx/imx-docker)


根据说明，安装 docker


```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```


解决代理问题，

容器内的代理


创建 yocto docker image
```sh
./docker-build.sh Dockerfile-Ubuntu-22.04
```

启动 docker container


## repo

Repo = 用来管理“由很多 Git 仓库组成的超大项目”的工具。

对于 i.MX BSP（Yocto）这种包含几十上百个仓库的工程，没有 Repo 会几乎无法管理。

Repo 做的事情（简单清晰）
- 用一个 manifest XML 描述“整个工程”
- 自动管理子仓库的更新
- 统一管理补丁与自定义 layer
- 保证所有仓库的版本一致性（最重要）

Repo 不是为了 Git，而是为了大型 BSP 的可维护性。

NXP 的 i.MX BSP 是典型的“几十仓库、不同 commit 组合成一个 Linux 发行版”。

Repo 的作用正是：用一个 manifest 文件，统一描述整个 BSP 所有仓库的版本与结构。只需要一个 repo sync，整个 BSP 就准备好了。



安装必要软件

```sh
sudo apt-get install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xz-utils zstd efitools
```

repo 是一个 python，安装就是添加到一个 PATH 存在的目录

```sh
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x repo
```


拉代码，需要设置终端代理，或者 git 的全局代理
```sh
mkdir imx-yocto-bsp
cd imx-yocto-bsp
repo init -u https://github.com/nxp-imx/imx-manifest -b imx-linux-walnascar -m imx-6.12.34-2.1.0.xml
repo sync
```


拉下来的东西：
```sh
m@virtual ~/imx_yocto_bsp>ls
imx-setup-release.sh@  README.md@  setup-environment@  sources/
```

- imx-setup-release.sh：该脚本用于初始化Yocto构建嵌入式Linux系统工作环境。
- setup-environment：该脚本根据运行imx-setup-release.sh脚本时输入的参数，设置Yocto工
作环境。
- sources文件夹：在该文件夹下存放了很多文件、源码以及编译工具，用于构建嵌入式Linux系
统。


DISTRO=fsl-imx-fb MACHINE=imx6ull14x14evk source imx-setup-release.sh -b build

执行完成后，自动切换到 build 下，在此文件夹下，构建嵌入式 linux 系统

bitbake imx-image-multimedia

