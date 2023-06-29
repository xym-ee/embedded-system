---
sort: 4
---
# uboot 中远程挂载



## uboot 环境变量

```
setenv ipaddr 10.0.0.11
setenv ethaddr 88:b2:77:40:8e:48
setenv gatewayip 10.0.0.1
setenv netmask 255.255.255.0
setenv serverip 10.0.0.10
```


设置环境变量 bootcmd 来挂载 tftp 目录下的内核、设备树文件到开发板内存中。


- `tftp 80800000 zImage` 加载内核
- `tftp 83000000 imx6ull-alientek-emmc.dtb` 加载设备树
- `bootz 80800000 - 83000000`

使用 bootcmd 参数挂载

- `setenv bootcmd 'tftp 80800000 zImage;tftp 83000000 imx6ull-alientek-emmc.dtb;bootz 80800000 - 83000000'`
- `saveenv`

相当于启动脚本了。

nfs 挂载根文件系统，通过修改 bootargs 参数实现。

```
setenv bootargs 'console=ttymxc0,115200 root=/dev/nfs \
nfsroot=10.0.0.10:/home/xym/tftp/rootfs,proto=tcp rw \ 
ip=10.0.0.11:10.0.0.10:10.0.0.1:255.255.255.0::eth0:off'
```



