



WPI 有一个免费的开发板试用活动，申请了一个，芯片型号 S32K312_100MQFP，记录点亮 LED 灯过程。




# 开发环境搭建

开发工具使用 NXP 官方提供的免费工具。在 [NXP® Semiconductors Official Site](https://www.nxp.com/) 注册账号，需要账号来获取软件和 Activation Code。安装包和芯片的资源都在 [S32K3 General-Purpose MCUs](https://www.nxp.com/products/S32K3) 页面中 Design Resources 的 Software 选项内 S32K3 Standard Software 中。

## 1.1 安装 S32 Design Studio

用于 S32K3xx 系列开发的最新的版本为 3.6.4（2025.10.5），S32 Design Studio 页面的 Previous 选项卡里可以看到老版本的 IDE，

全部默认就行，安装完成后，新建一个 S32DS Application Project 可以看到已经有芯片型号可以选择了，但是 SDK 列表里是空的，新建 S32DS Project form Example 中也没有我们需要的型号，需要安装 RTD 包。

安装成功后会提示 Restart Now，重启 IDE 后新建 S32DS Project from Example 就可以看到 RTD 包的例程了。







