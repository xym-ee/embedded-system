
# imx8mp

快速构建


终端设置代理

```sh
export http_proxy=http://192.168.1.181:7890
export https_proxy=http://192.168.1.181:7890
```


安装依赖工具

```sh
sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xzutils zstd efitools
```


```sh
sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget zstd efitools
```

安装 repo 工具

```sh
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
# 放到 /bin 或某个环境变量的目录里
```


`imx-manifest` 是 NXP 官方用于管理 i.MX Linux BSP（Board Support Package）源码的“入口仓库”。它本身不包含代码，而是通过多个 `.xml` manifest 文件来描述 所有需要拉取的子仓库，并用 repo 工具统一管理。

NXP 的 BSP 依赖几十个仓库，且版本组合高度固定，如果用 submodule 会非常难管理。

```sh
mkdir imx-yocto-bsp

# 可能需要代理
# 初始化 repo 仓库，获得依赖关系
repo init -u https://github.com/nxp-imx/imx-manifest -b imx-linux-kirkstone -m imx-5.15.71-2.2.2.xml 

# 拉取所有源码
repo sync
```

```sh
# 执行后，自动切换到了 build 目录
DISTRO=fsl-imx-xwayland MACHINE=imx8mp-ddr4-evk source imx-setup-release.sh -b build

# 在 build 目录下构建
bitbake imx-image-multimedia
```






烧镜像，






