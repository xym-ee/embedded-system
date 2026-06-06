
# imx6ull_5.15.71_2.2.2


ubuntu 20.04


安装依赖工具

```sh
sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget zstd efitools
```


安装 repo 工具

```sh
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
# 放到 /bin 或某个环境变量的目录里
```


```sh
# 创建工作目录
mkdir imx-yocto-bsp
cd imx-yocto-bsp

# 可能需要代理
# 初始化 repo 仓库，获得依赖关系
repo init -u https://github.com/nxp-imx/imx-manifest -b imx-linux-kirkstone -m imx-5.15.71-2.2.2.xml

# 拉取 yocto 工程源码，poky meta-imx kernel uboot
repo sync
```


```sh
# 执行后，自动切换到了 build 目录
DISTRO=fsl-imx-fb MACHINE=imx6ull14x14evk source imx-setup-release.sh -b build-imx6ull

# 在 build 目录下构建
bitbake core-image-base
```


从 yocto 项目拿到工具链 源码。像老的代码一样，就可以直接去移植了。

poky 工具链需要 source 自动配置一下环境，然后 ARM CROSS_COMPILE 都在环境变量中设置好了，可以直接使用 make 指令

```sh
make clean
make mx6ull_14x14_evk_defconfig
make -j32
```

编译 uboot 直接烧到 正点原子 的开发板做测试：

```sh
U-Boot 2022.04-lf_v2022.04+g181859317bf (Nov 29 2025 - 14:21:07 +0800)

CPU:   i.MX6ULL rev1.1 792 MHz (running at 396 MHz)
CPU:   Industrial temperature grade (-40C to 105C) at 32C
Reset cause: POR
Model: i.MX6 ULL 14x14 EVK Board
Board: MX6ULL 14x14 EVK
DRAM:  512 MiB
Core:  65 devices, 18 uclasses, devicetree: separate
MMC:   FSL_SDHC: 0, FSL_SDHC: 1
Loading Environment from MMC... *** Warning - bad CRC, using default environment

[*]-Video Link 0 (480 x 272)
        [0] lcdif@21c8000, video
In:    serial
Out:   serial
Err:   serial
switch to partitions #0, OK
mmc0 is current device
flash target is MMC:0
Net:
Error: ethernet@20b4000 address not set.

Error: ethernet@20b4000 address not set.

Error: ethernet@20b4000 address not set.

Error: ethernet@20b4000 address not set.
Could not get PHY for FEC0: addr 2

Error: ethernet@20b4000 address not set.

Error: ethernet@20b4000 address not set.
Could not get PHY for FEC0: addr 2
No ethernet found.

Fastboot: Normal
Normal Boot
Hit any key to stop autoboot:  0
=>
```



UART DDR ，

uboot 启动正常，DRAM 识别正确，SD 卡和 EMMC 驱动正常。

uboot 里面的 LCD 驱动默认是给 4.3 寸 480x272 分辨率的，如果使用的其他分辨率的屏幕需要修改驱动。

网络不能工作，识别不出来网络信息，需要修改驱动。







