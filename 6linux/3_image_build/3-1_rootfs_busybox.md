---
sort: 9
---
# rootfs : busybox




nfs 挂载

```
root=/dev/nfs nfsroot=10.0.0.10:/home/xym/ws_linux/rootfs,proto=tcp rw
ip=10.0.0.11:10.0.0.10:10.0.0.1:255.255.255.0::eth0:off
```

启动参数
```
setenv bootargs 'console=ttymxc0,115200 root=/dev/nfs nfsroot=10.0.0.10:/home/xym/ws_linux/rootfs,proto=tcp,nfsvers=3 rw ip=10.0.0.11:10.0.0.10:10.0.0.1:255.255.255.0::eth0:off' 
```


uboot 有比较强的容错能力，可能首选非从 nfs 挂载，遇到这种情况，手动写死 bootcmd

```
setenv bootcmd 'tftp 80800000 zImage; tftp 83000000 imx6ull-mini.dtb; bootz 80800000 - 83000000;'
```

```
setenv bootcmd 'mmc dev 1; fatload mmc 1:1 80800000 zImage; fatload mmc 1:1 83000000 imx6ull-14x14-emmc-4.3-800x480-c.dtb; bootz 80800000 - 83000000;'
```


## 测试和完善

系统启动后

```
[    8.622515] VFS: Mounted root (nfs filesystem) on device 0:14.
[    8.630672] devtmpfs: mounted
[    8.634627] Freeing unused kernel memory: 528K (80b48000 - 80bcc000)
can't run '/etc/init.d/rcS': No such file or directory

Please press Enter to activate this console. 
```


提示 kernel(先笼统的这么讲) 想运行一个东西，但是没有。事实上这是个脚本，我们自己创建就好了。

kernel 启动后需要启动一些服务， `/etc/init.d/rcS` 脚本里启动了一些东西。


