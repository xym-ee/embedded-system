---
sort: 2
---
# makefile



## 核心思路

vim 的设置
- set nu   # 行号
- set ts=4 # tab 为 4 个空格
- set noexpandtab # tab 不要用空格代替


makefile 
- 描述了文件的依赖关系，一个工程只修改了一个文件时，只重新编译依赖这个被修改文件的文件。
- 描述了生成目标的指令

```
目标：依赖文件1 依赖文件2
    命令1
    命令2
依赖文件1：...
```


举例，main.c, fun1.c, fun2.c

```makefile

# 第一个出现的为默认生成目标
main: main.o fun1.o fun2.o
    gcc -o main fun1.o fun2.o
fun1.o: fun1.c
    gcc -c fun1.c
fun2.o: fun2.c
    gcc -c fun2.c

```










