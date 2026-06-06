---
sort: 7
---
# (附加)socket 编程


在 UNIX/Linux 系统中不同的硬件设备都被看成一个文件。对硬件的操作，等同于对磁盘上普通文件的操作。

一切都是文件！

为了表示和区分已经打开的文件，UNIX/Linux 会给每个文件分配一个 ID，这个 ID 就是一个整数，被称为**文件描述符**（File Descriptor）。例如：通常用 0 来表示标准输入文件（stdin），它对应的硬件设备就是键盘；通常用 1 来表示标准输出文件（stdout），它对应的硬件设备就是显示器。

UNIX/Linux 程序在执行任何形式的 I/O 操作时，都是在读取或者写入一个文件描述符。一个文件描述符只是一个和打开的文件相关联的整数，它的背后可能是一个硬盘上的普通文件、FIFO、管道、终端、键盘、显示器，甚至是一个*网络连接*。

**网络连接也是一个文件，它也有文件描述符**。


Socket是提供网络服务的库，socket本意为“插座”，插在插座上，就能获得数据。socket就是计算机用来获得网络数据的工具。

socket在计算机领域翻译为“套接字”。

Socket 是“程序可用的通信端点”，TCP / UDP 是两种最常用的传输方式。


## socket 基本分类

socket 创建时指定的东西

```c
socket(domain, type, protocol);
```





TCP 流式套接字。SOCK_STREAM ，可靠，双向，通讯流。
- 先建立连接
- 数据保证送达
- 顺序保证
- 像一条“管道”



UDP 数据报套接字。SOCK_DGRAM 无连接的套接字，快速传输但无序、传输的数据可能丢失也可能损坏，限制每次传输的数据大小、数据的发送和接收是同步的。



## 

一条连接由 4 个东西决定

```
(src_ip, src_port, dst_ip, dst_port)
```

写一个 tcp 通信的程序

```c
/* server.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{
    /* raw socket */
    int listen_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    /* listen socket */
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;                         //使用IPv4地址
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");     //具体的IP地址
    serv_addr.sin_port = htons(9999);                       //端口

    bind(listen_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    listen(listen_fd, 20);

    /* connected socket */
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);
    int fd = accept(listen_fd, (struct sockaddr*)&clnt_addr, &clnt_addr_size);

    /* write fd */
    char str[] = "This is a socket message.";
    write(fd, str, sizeof(str));
   
    close(fd);
    close(listen_fd);

    return 0;
}
```


```c
/* client.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main()
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));  //每个字节都用0填充
    serv_addr.sin_family = AF_INET;  //使用IPv4地址
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  //具体的IP地址
    serv_addr.sin_port = htons(9999);  //端口
    connect(fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
   
    char buffer[40];
    read(fd, buffer, sizeof(buffer)-1);
    printf("Message form server: %s\n", buffer);
    close(fd);
    return 0;
}
```











