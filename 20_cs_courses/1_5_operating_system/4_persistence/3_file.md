
# 文件

我们可以把设备想象成一组寄存器，以及寄存器基础上的一个设备通信协议，能够实现处理器和设备之间的数据交换：数据可以小到一个字符 (串口)，也可以大到程序和海量的数据 (GPU)。很自然的问题是，如果操作系统上的程序想要访问设备，就必须把设备抽象成一个进程可以使用系统调用访问的操作系统对象。于是我们就回到了 “文件” 和文件在操作系统中的实现。

对设备、对文件的访问本质上没有区别。


## 1.文件和文件描述符

everything is a file，终于学到 file 了。

操作系统 = 对象 + api。文件就是操作系统中有名字的对象，字节序列和字节流。

文件可以理解成一个数组指针，文件内容如果是字节序列的话，和数组并没有本质区别，那么文件名就是一个数组名，大概是这么个思路。但是并不是所有文件都可以随机寻址，`/dev/null` 这个文件就不像字节序列，终端也是，数据被读走就永远消失了。

这些东西用同一个接口来访问，**文件描述符**。

在用户空间，一个进程不能随便访问操作系统里的资源和对象。如果一个进程想访问操作系统里的对象，一定要通过指针或者类似于指针的机制，文件描述符就是。这是个数字，但是操作系统会把这个数字和进程关联起来，这个数字就有点像指针。
- 文件描述符是指向操作系统对象的指针
  - 通过指针访问任何东西
- 对象的访问都需要指针
  - open close read write

一个真实的程序也是这样的，有 strace 工具来查看，


关于文件和文件描述符更多的细节

操作系统支持 `mmap` 这个操作，把磁盘的一部分映射到地址空间，把进程地址空间的一部分和文件一一对应起来。细节问题，这个 api 的参数很多

```c
mmap(addr, length, prot, flags, fd, offset);
```

参数很多情况就很多，每种情况操作系统的设计者都要定义好其行为。就举例来说 `length` 这个参数给的大小比文件小是没问题的，如果 `length` 给的大了会怎么样呢？

写一个程序，mmap以后往下去写，linux 里会有一个 SIGBUS，信号导致了进程终止。

随着操作系统越来越复杂，东西越来越多，每个部分都在产生交互比如文件的大小、偏移量，一个人不大可能把这些所有的细节都记住。工作以后可能会被迫去搞清这些细节。

还有一个东西 lseek，read 系统调用没有没有偏移量，这个事情是操作系统在维护。read/write: 会自动维护 offset。如果要修改 offset 那么要使用 lseek 。

mmap lseek ftruncate互相交互。一个文件大小 2MB，lseek 到 3MB，会发生什么呢？或者 ftruncate 到 1MB，会怎么样？这些东西是操作系统的设计者需要考虑的东西。

问 gpt，lseek 移动到 3MB，是可以的，中间会填 0。截断文件后，又有个问题，lseek 的位置在哪里？事实上 lseek 不变。复杂性就是这么来的。

然后有了 fork，提出更多的问题。文件描述符在 fork 时会被子进程集成的，如匿名管道。问题，要不要为子进程提供一个独立的 offset 呢？linux 的方案是共用 offset。也即追加写入，如果独立的，那么父子进程想写一个 log，后写的会覆盖前面的，。

考虑到操作系统每个 api 都可能和其他 api 交互。两个线程对同一个文件有两个 offset 这个需求也是合理的。

fork 和所有操作系统 api 交互的时候都会带来复杂性。


## 2.实现文件


```c
struct file_operations {
 struct module *owner;
 loff_t (*llseek) (struct file *, loff_t, int);
 ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
 ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
 ssize_t (*read_iter) (struct kiocb *, struct iov_iter *);
 ssize_t (*write_iter) (struct kiocb *, struct iov_iter *);
 int (*iopoll)(struct kiocb *kiocb, struct io_comp_batch *, uint flags);
 int (*iterate_shared) (struct file *, struct dir_context *);
 __poll_t (*poll) (struct file *, struct poll_table_struct *);
 long (*unlocked_ioctl) (struct file *, uint, ul);
 long (*compat_ioctl) (struct file *, uint, ul);
 int (*mmap) (struct file *, struct vm_area_struct *);
 ul mmap_supported_flags;
 int (*open) (struct inode *, struct file *);
 int (*flush) (struct file *, fl_owner_t id);
 int (*release) (struct inode *, struct file *);
 int (*fsync) (struct file *, loff_t, loff_t, int datasync);
 int (*fasync) (int, struct file *, int);
 int (*lock) (struct file *, int, struct file_lock *);
 ul (*get_unmapped_area)(struct file *, ul, ul, ul, ul);
 int (*check_flags)(int);
 int (*flock) (struct file *, int, struct file_lock *);
 ssize_t (*splice_write)(struct pipe_inode_info *, struct file *, loff_t *, size_t, uint);
 ssize_t (*splice_read)(struct file *, loff_t *, struct pipe_inode_info *, size_t, uint);
 void (*splice_eof)(struct file *file);
 int (*setlease)(struct file *, int, struct file_lease **, void **);
 long (*fallocate)(struct file *file, int mode, loff_t offset, loff_t len);
 void (*show_fdinfo)(struct seq_file *m, struct file *f);
 ssize_t (*copy_file_range)(struct file *, loff_t, struct file *, loff_t, size_t, uint);
 loff_t (*remap_file_range)(struct file *file_in, loff_t pos_in, struct file *file_out,
   loff_t pos_out, loff_t len, uint remap_flags);
 int (*fadvise)(struct file *, loff_t, loff_t, int);
 int (*uring_cmd)(struct io_uring_cmd *ioucmd, uint issue_flags);
 int (*uring_cmd_iopoll)(struct io_uring_cmd *, struct io_comp_batch *,
    uint poll_flags);
} __randomize_layout;
```

只要能实现文件的一些操作，那么就能实现一个文件。

## 3.设备驱动程序

这就有了设备驱动程序。只要为一个真实的设备实现一个文件操作，就能实现一个驱动。把系统调用翻译成设备理解的数据并写到寄存器里。

devfs 里的虚拟出来的设备，如 /dev/null 。

思路：只要代码能伪装成 `struct file_operations` 认为自己可以提供文件的操作，就能正确的接入文件系统，就是文件里系统里的一个文件。


最大的问题是设备不仅仅数据，还有配置。一些思路
- 控制作为数据流的一部分，用写的接口
- 提供新接口

非数据的设备功能几乎全部依赖 `ioctl`。可设备的复杂性是无法降低的，但接口就这么一个。

设备驱动代码是整个操作系统里代码最多，质量最差的部分。


