---
sort: 1
---
# keil scatter 分散加载


## 生产的可执行文件

MCU 的存储空间：片内 Flash、片内 RAM。编译完成后，会看到程序占用空间的信息

```
linking...
Program Size: Code=42116 RO-data=7328 RW-data=2868 ZI-data=128204  
```

上面提到的 Program Size 包含以下几个部分：
- Code：代码段，存放程序的代码部分；
- RO-data：只读数据段，存放程序中定义的常量；
- RW-data：读写数据段，存放初始化为非 0 值的全局变量；
- ZI-data：0 数据段，存放未初始化的全局变量及初始化为 0 的变量；

编译完工程会生成一个. map 的文件，该文件说明了各个函数占用的尺寸和地址，在文件的最后几行也说明了上面几个字段的关系：

```
    Total RO  Size (Code + RO Data)                49444 (  48.29kB)
    Total RW  Size (RW Data + ZI Data)            131072 ( 128.00kB)
    Total ROM Size (Code + RO Data + RW Data)      49604 (  48.44kB)
```

程序运行之前，需要有文件实体被烧录到 Flash 中，一般是 bin 或者 hex 文件，该被烧录文件称为可执行映像文件。如下图左边部分所示，是可执行映像文件烧录到 STM32 后的内存分布，它包含 RO 段和 RW 段两个部分：其中 RO 段中保存了 Code、RO-data 的数据，RW 段保存了 RW-data 的数据，由于 ZI-data 都是 0，所以未包含在映像文件中。

STM32 在上电启动之后默认从 Flash 启动，启动之后会将 RW 段中的 RW-data（初始化的全局变量）搬运到 RAM 中，但不会搬运 RO 段，即 CPU 的执行代码从 Flash 中读取，另外根据编译器给出的 ZI 地址和大小分配出 ZI 段，并将这块 RAM 区域清零。

为什么上述的 RW-Data 既占用 Flash 又占用 RAM 呢？首先变量必先要初始化才能使用，否则初值不正确，而在 main() 函数后变量已经可以正常使用，那就是说变量的初始化是在之前完成的，查看这之前的代码只有 __main() 一个函数，除了赋初值外，都还做了什么呢？

函数__main()主要由以下两部分功能组成，如下所示:
- 1) __main()：完成代码和数据的拷贝，并把 ZI 数据区清零。代码拷贝可将代码拷贝到另外一个映射空间并执行 (例如将代码拷贝到 RAM 执行)； 数据拷贝完成 RW 段数据赋值；数据区清零完成 ZI 段数据赋值。以上的代码和分散加载文件密切相关。
- 2) _rt_entry()：进行 STACK 和 HEAP 等的初始化。最后_rt_entry跳进 main()函数入口。当 main()函数执行完后， _rt_entry 又将控制权交还给调试器。

## 分散加载文件干什么的

分散加载（scatter）文件是一个文本文件，它可以用来描述ARM连接器生成映像文件时所需要的信息。

如果不用scatter文件指定，那么ARM连接器会按照默认的方式来生成映像文件，一般情况下我们是不需要使用分散加载文件的，但在某些场合，我们希望把某些数据放在指定的地址处，那么这时候scatter文件就发挥了非常大的作用。而且scatter文件用起来非常简单好用。在分散加载文件中可以指定下列信息：
- 1）各个加载时域（load region）加载时的起始地址（load address）和最大尺寸（max size）；
- 2）各个加载时域的属性。
- 3）从每个加载时域中分割出来的运行时域。
- 4）各个运行时域（excution region）的运行起始地址（excution address）和最大尺寸（max size）。
- 5）各个运行时域的存储访问特性。
- 6）各个运行时域的属性。
- 7）各个运行时域中包含的输入段。

一般情况下，我们可以不独自编写分散加载文件，ARM连接器直接按照默认的方式来生成映像文件即可，但是在某些场合，我们希望将某些数据放在指定的位置，此时分散加载文件就发挥了非常发的作用。比如在下面几种情况就充分体现了分散加载文件的优势：
- 1）复杂内存映射：如果必须将代码和数据放在多个不同的内存区域中，则需要使用详细指令指定将哪些数据放在哪个内存空间中。
- 2）不同类型的内存：许多系统都包含多种不同的物理内存设备，如闪存、ROM、SDRAM 和快速 SRAM。分散加载描述可以将代码和数据与最适合的内存类型相匹配。例如，可以将中断代码放在快速 SRAM 中以缩短中断等待时间，而将不经常使用的配置信息放在较慢的闪存中。
- 3）位于固定位置的函数：可以将函数放在内存中的固定位置，即使已修改并重新编译周围的应用程序。
- 4）使用符号标识堆和堆栈：链接应用程序时，可以为堆和堆栈位置定义一些符号。

一些需要关注的点：
- 1）编译后输出的映像文件中各段是首尾相连的，中间没有空闲的区域，他们的先后关系是根据链接时参数的先后次序决定的armlinker -file1.o file2.o …
- 2）scatter用于将编译后的映像文件中的特定段加载到多个分散的指定内存区域。
- 3）两类域(region)：执行域(execution region)和加载域(load region)。
- 4）加载域，该映像文件开始运行前存放的区域，即当系统启动或加载时应用程序存放的区域。
- 5）执行域，映像文件运行时的区域，即系统启动后，应用程序进行执行和数据访问的存储器区域，系统在实时运行时可以有一个或多个执行块。
- 6）scatter本身并不能对映像实现“解压缩”，编译器读入scatter文件之后会根据其中的各种地址生成启动代码了，实现对映像的加载，而这一段代码就是 `*(InRoot$$Sections)` 它是 `__main()` 的一部分。这就是在汇编启动代码的最后跳转到 `__main()` 而不是跳向 `main()` 的原因之一。
- 7）起始地址与加载域重合的执行域称为root region，`*(InRootSections)` 必须放在这个执行域中，否则链接的时候会报错。`*(+RO)` 包含了 `*(InRootSections)`，所以如果在 rootregion 中用到了 `*(+RO)` 就可以不再指定 `*(InRootSections)`


## 语法

```
ROM_LOAD 0x00000000
{
  ROM 0x00000000 0x003FFFFF      
  {
      vectors.o (+RO,+FIRST)
    * (InRoot$$Sections)       ; All library sections that must be in a root region
    *(+RO)
  }

     SRAM 0x00400000 0x003FFFFF
    {
        * (+RW,+ZI)
    }

    SDRAM1 0x41000000 UNINIT
    {
         stack.o (+ZI) ; stack.s中定义了top_of_stack为长度为1的space，指定栈顶地址
    } 

    SDRAM2 +0 UNINIT
    {   
        heap.o (+ZI)
    }   
}
```

注解：
1. ROM_LOAD是加载域。这里只有一个，也可以有多个（rom地址不连续的情况）
2. ROM、SRAM、SDRAM1、SDRAM2是执行域，有多个。第一个执行域必须和加载域地址重合，因为ARM的复位地址就是加载域的起始地址（有bootstrap的话加载域址就是bootstrap执行完后的跳转地址）
3. vectors.o (+RO, +FIRST) 中断向量表放在最开头
4. ROM 0x00000000 0x003FFFFF; 加载域名 起始地址 最大允许长度；‘最大允许长度’也可以省略，但缺点是编译器不会检查段是否溢出和别的段重叠了。‘起始地址’= +0表示紧接着上一段开始的连续地址。
5. * (InRoot$$Sections)是复制代码的代码
6. UNINT关键字表示不进行初始化清零


值得注意的是：在一个scatter文件中，同一个.o文件不能出现2次，即使是在2个不同的加载域中也不可以，否则会报错：Ambiguous selectors found for *.o，错误的例子：
LOAD1 0x00000000
{
    EXE1
    {
            Init.o
     }
}

LOAD2 0xFFFF0000
{
    EXE2
    {
            Init.o
     }
}




## 结构

分散加载文件一般由1个加载时域和1到多个运行时域组成（当然也可以包含2个以上的加载时域）

<figure>
  <img src="https://img-blog.csdnimg.cn/2021022414391748.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0tYdWUwNzAz,size_16,color_FFFFFF,t_70#pic_center" width = 350>
</figure>

<figure>
  <img src="http://hiphotos.baidu.com/chenxing263/pic/item/87ac2edc789d8ceecc11661a.jpg" width=400>
</figure>

具体来说，在scatter文件中可以指定下列信息：
- 各个加载时域的加载时起始地址、最大尺寸和属性；
- 每个加载时域包含的输出段；
- 各个输出段的运行时起始地址、最大尺寸、存储访问特性和属性；
- 各个输出段中包含的输入段。

### 加载时域

```
load_region_name  [#start_address + #offset] [attribute] [#max_size]
{
  ; execution_region_description
}
```

- `load_region_name`：加载时域的名称，名称可以按照用户意愿自己定义，该名称中只有前 31 个字符有意义。它仅仅用来唯一的标识一个加载时域，而不像运行时域的名称除了唯一的标识一个运行时域外，还用来构成连接器连接生成的连接符号。
- `#start_address + #offset`：用来表示本加载时域的起始地址
  - `start_address`：表示本加载时域中的对象在连接时的起始地址，地址必须是字对齐的；
  - `offset`：连接时的起始地址相对于上一加载时域的偏移地址，4 Byte 对齐。本加载时域是第一个加载时域，则它的起始地址即为 offset。
- `attribute`：指定本加载时域的属性，默认加载时域的属性是ABSOLUTE。
  - PI – 位置无关属性。
  - RELOC – 重定位。
  - OVERLAY – 覆盖。
  - ABSOLUTE – 起始地址由[#start_address + #offset]
- `max_size`：指定本加载时域的最大尺寸。如果本加载时域的实际尺寸超过了该值，连接器将报告错误，默认取值为  `0xFFFFFFFF`。
- execution_region_description：运行时域，可以有多个运行时域。

### 运行时域

```
execution_region_name  [#start_address + #offset]  [attribute] [max_size]
{
  ; input_section_description
}
```

- `execution_region_name`：为运行时域的名称，名称可以按照用户意愿自己定义，该名称中只有前 31 个字符有意义。它除了唯一的标识一个运行时域外，还用来构成连接器生成的连接符号。
- `#start_address + #offset`：用来表示本运行时域的起始地址：
  - `start_address`：表示本运行时域中的对象在连接时的起始地址，地址必须是字对齐的；
  - `offset`：表示本运行时域相对前一个运行时域结束地址的偏移量。
- `attribute`：指定本加载时域内容的属性，包含以下几种， 默认加载时域的属性是ABSOLUTE。
  - PI – 位置无关属性。
  - RELOC – 重定位。
  - OVERLAY – 覆盖。
  - ABSOLUTE – 起始地址由 start_address 指定（默认属性）。
  - FIXED – 固定地址。此时该域加载时域地址和运行时域地址是相同的，而且都是通过 start_address 指定的，而且 start_address 必须是绝对地址或者 offset 为 0 。
- `max_size`：指定本运行时域的最大尺寸。如果本运行时域的实际尺寸超过了该值，连接器将报告错误，默认取值为 0xFFFFFFFF。
- `length`：如果指定的长度为负值，则将 start_address 作为区结束地址。它通常与 EMPTY 一起使用，以表示在内存中变小的堆栈。

### 输入段描述

```
    module_select_pattern  (
      (+input_section_attr | input_section_pattern)
      ([","] +input_section_attr | "," input_section_pattern))
                            
```

- `module_select_pattern`：目标文件滤波器，支持使用通配符 `*` 与 `?` 
  - `*` 匹配任意字符，`*`，`.ANY`
  - `?` 匹配单个字符
  - 进行匹配时所有字符不区分大小写。
- `input_section_attr`：属性选择器与输入段属性相匹配。每个 input_section_attr 的前面有一个“+”号。如果指定一个模式以匹配输入段名称，名称前面必须有一个“+”号。可以省略紧靠“+”号前面的任何逗号。 选择器不区分大小写（可以识别的为属性First、Last）。
  - 通过使用特殊模块选择器模式.ANY ，可以将输入段分配给执行区，而无需考虑其父模块。可以使用一个或多个.ANY 模式以任意分配方式填充运行时域。在大多数情况下，使用单个.ANY 等效于使用*模块选择器。

## 应用举例

### 1

以 ST 的 Cortex-M4 核的低功耗 STM32L476VC 芯片为例，其资源如下：
- Flash 基地址：0x08000000，小为 256kB(0x00040000)
- RAM 基地址：0x20000000，大小为 96kB(0x00018000)

```
; 定义一个加载时域，域基址：0x08000000，域大小为 0x00040000
LR_IROM1 0x08000000 0x00040000  {

  ; 定义一个运行时域，第一个运行时域必须和加载时域起始地址相同，
  ; 其域大小一般也和加载时域大小相同。将 RESET 段最先加载到本域的起始地址，即
  ; RESET 的起始地址为 0， RESET 存储的是向量表
  ER_IROM1 0x08000000 0x00040000  {
   *.o (RESET, +First)
  }

  ; 自定义的应用程序信息（软硬件版本、发布时间、升级信息等）
  ; 将其固定的放在中断向量表之后，便于通过.bin文件查看程序的信息
  ER_IROM2 + 0 {
   *.o (SECTION_APP_INFO, +First)
  }
  
  ; 初始化相关代码
  ; 加载所有匹配目标文件的只读属性数据，包含：Code、 RW-Code、 RO-Data。
  ER_IROM3 + 0 {
   *(InRoot$$Sections)
   .ANY (+RO)
  }

  ; 定义一个运行时域，域基址： 0x20000000 ，域大
  ; 小为 0x00018000 ，对应实际 RAM 大小
  RW_IRAM1 0x20000000 0x00018000  {
   .ANY (+RW +ZI)					; 这里也可以用 * 号替代 .ANY
  }
}
```

如上分散加载文件所示：它包含1个加载时域，3个运行时域。其第一个运行时域与加载时域的基地址一致（在嵌入式系统中，必须首先加载中断向量表，且必须与加载时域的基地址保持一致，否则编译时会报错）。

SECTION_APP_INFO：用户自定义的一块区域，记录终端的版本、升级等相关信息，它是一块固定的位置，紧随中断向量变之后。它为一个结构体形式。

类型声明为：
```c
/**
  * @brief 应用程序信息(必须为4字节对齐。同时用于IAP和APP)
  */
typedef struct
{
    UINT8   ucFactory[FACTORY_LENGTH];        /* 厂商标志 */
    UINT8   ucProduct[PRODUCT_LENGTH];        /* 产品标志 */
    UINT8   ucProtocol[PROTOCOL_LENGTH];      /* 规约标志 */
    UINT8   ucVerSW[VER_SW_LENGTH];           /* 软件版本 */
    UINT8   ucVerDateSW[DATE_SW_LENGTH];      /* 软件发布日期 */
    UINT8   ucVerHW[VER_SW_LENGTH];           /* 硬件版本 */
    UINT8   ucVerDateHW[DATE_HW_LENGTH];      /* 硬件发布日期 */
    UINT64  udwUpGradeFlag;                   /* 升级标志。主要存放升级方式。该值在升级完成后，改为 以上定义的各种值，以指示升级方式 */
    UINT64  udwAppFlag;                       /* 应用程序标志。该值在升级中动态改变。升级完成后必为APP_FLAG_UPGRADED */
    UINT64  udwCRC;                           /* 程序本身的 CRC。用来保证数据的完整性 */
    UINT64  udwLength;                        /* 程序本身的长度。仅指计算 CRC 的长度 */
} APP_INFO, IAP_INFO;
```

实现为
```c
const APP_INFO stAppInfo __attribute__((section("SECTION_IAP_INFO"))) =
{
    FACTORY,		/* 厂商标识，宏值 */
    PRODUCT,		/* 产品标识，宏值 */
    PROTOCOL,		/* 规约标识，宏值 */
    VER_SW,			/* 软件版本，宏值 */
    DATE_SW,		/* 软件版本发布日期，宏值 */
    VER_HW,			/* 硬件版本，宏值 */
    DATE_HW,		/* 硬件版本发布日期，宏值 */
    UPDATE_FLAG,	/* 升级标志，宏值 */
    APP_FLAG,		/* 应用程序标识，宏值 */
};
```


以属性FIXED实现一个加载域多个执行域的情况

下面的这种情况是对中分散加载文件的略微修改，它将第 2 个加载时域 (ER_IROM2) 的基地址固定为了0x08000400 。这样为中断向量表预留的空间大小为 0x400 字节，冗余的部分以 0x00 填充（这样写会导致生成的映像文件变大）。对应的 .bin 文件如下图所示：

```
LR_IROM1 0x08000000 0x00040000  {         ; load region size_region
  ER_IROM1 0x08000000 0x400  {            ; load address = execution address
   *.o (RESET, +First)
  }
  
  ER_IROM2 0x08000400  FIXED 0x0003C000 { ; 应用程序信息
   *.o (SECTION_APP_INFO, +First)         ;First标识该输入段是运行该运行时域的第一个输入段
  }
  
  ER_IROM3 + 0 {                          ; 初始化相关代码
   *(InRoot$$Sections)
   .ANY (+RO)
  }
  
  RW_IRAM1 0x20000000 0x00018000  {  		  ; RW data
   .ANY (+RW +ZI)
  }
}
```


下面的这种情况也是是对6.1中分散加载文件的略微修改，它将第2个加载时（ER_IROM2 ）的基地址固定为了0x08000400 ，第3个加载域（ER_IROM23）的基地址固定为了0x08000800，这样为中断向量表和SECTION_APP_INFO均预留的空间大小为0x400字节，冗余的部分以0x00填充。

```
LR_IROM1 0x08000000 0x00040000  {    		; load region size_region
  ER_IROM1 0x08000000 0x400  {  			; load address = execution address
   *.o (RESET, +First)
  }
  
  ER_IROM2 0x08000400  FIXED 0x0003C000 {	; 应用程序信息
   *.o (SECTION_APP_INFO, +First)
  }
  
  ER_IROM3 0x08000800  FIXED 0x00038000 {	; 初始化相关代码
   *(InRoot$$Sections)
   .ANY (+RO)
  }
  
  RW_IRAM1 0x20000000 0x00018000  {  		; RW data
   .ANY (+RW +ZI)
  }
}
```

## 多块 RAM 的分散加载文件配置

还是上述的 MCU，假设其增加了另外一块 RAM，其资源如下：
- 1）Flash基地址：0x08000000，小为256KB
- 2）RAM基地址：0x10000000，大小为24KB(0x6000)
- 3）RAM基地址：0x20000000，大小为24KB(0x6000)

若想将两块RAM都使用起来（可使用48KB），那么分散加载文件的写法应该如下：

```
LR_IROM1 0x08000000 0x00040000  {         ; load region size_region
  ER_IROM1 0x08000000 0x400  {            ; load address = execution address
    *.o (RESET, +First)
  }
  ER_IROM2 0x08000400  FIXED 0x0003C000 { ; 应用程序信息
    *.o (SECTION_APP_INFO, +First)        ;First标识该输入段是运行该运行时域的第一个输入段
  }
  ER_IROM3 + 0 {                          ; 初始化相关代码
    *(InRoot$$Sections)
    .ANY (+RO)
  }

  ; 定义的 RAM1 的运行时域，使用 .ANY 进行随意分配变量，这里不能使用*号替代
  ; *表示匹配有所有的目标文件，这样变量就无法分配到第二块 RAM 空间了
  RW_IRAM1 0x100000000 0x6000 {
   .ANY (+RW +ZI)
  }

  ; 定义的RAM2的运行时域，同样使用.ANY 随意分配变量的方式
  ; 如果还有另多的 RAM 块，在这里增加新的运行时域即可，格式和 RAM2 的定义相同
  RW_IRAM2 0x200000000 0x6000  {
   .ANY (+RW +ZI)
  }
}
```

以上的分散加载机制确实可以使两个RAM空间（48KB）都使用起来，但是它并不等同于一个48KB的RAM。在实际应用中定义一个30KB 的数组 `unsigned char test[30*1024];` ，编译会出错，提示没有足够空间。

改成在同一个文件内定义两个 15KB 的数组，任会出错，因为.ANY 是按文件名匹配的。

解决方法，定义在两个文件内，或指定段。

```c
#pragma arm section zidata = "SRAM" // 在 C 文件中定义新的段
unsigned char Test1[15 * 1024];     // 定义第一个15KB数组
#pragma arm section                 // 恢复原有的段
unsigned char Test2[15 * 1024];     // 定义第二个15KB数组，这20KB数组不会和
```

## 多块 Flash 分散加载文件配置

假设有一个MCU，它有两块独立的Flash，一个RAM，资源分配如下：
- （1）Flash1 基址： 0x00000000，大小：256 KB(0x00040000)；
- （2）Flash2 基址： 0x20000000，大小：2048 KB(0x00200000)；
- （3）RAM 基址： 0x10000000，大小：32 KB(0x00008000)；

如果这么写会出错
```
LR_IROM1 0x00000000 0x00040000 {

	ER_IROM1 0x00000000 0x00040000 {  ; 定义 Flash1 运行时域
		*.o (RESET, +First)             ; 先加载向量表
		*(InRoot$$Sections)
		.ANY (+RO)                      ; 随意分配只读数据
	}

	ER_IROM2 0x20000000 0x00200000 {  ; 定义 Flash2 运行时域
		.ANY (+RO)                      ; 随意分配只读数据
	}

	RW_IRAM1 0x10000000 0x00008000 {
		.ANY (+RW +ZI)
	}
}
```

正确的编写方式应该如下：
```
LR_IROM1 0x00000000 0x00040000 {    ; 定义 Flash1 的加载域

	ER_IROM1 0x00000000 0x00040000 {
		*.o (RESET, +First)
		*(InRoot$$Sections)
		.ANY (+RO)                      ; 随机分配只读数据
	}

	RW_IRAM1 0x10000000 0x00008000 {
		.ANY (+RW +ZI)
	}
}

LR_IROM2 0x20000000 0x00200000 {    ; 定义 Flash2 的加载域
	ER_IROM2 0x20000000 0x00200000 {
		.ANY (+RO)                      ; 随机分配只读数据，代码不会进行拷贝
	}
}
```

这样写能够解决双Flash加载的问题，但是同样有一个问题，那就是，编译时会生成2份bin文件，需要分别两次烧录代码。

## 一些补充

- 第一个运行时域存放的代码不会进行额外拷贝
  - 因为分散加载文件有一项很强大的功能，就是可以将 Flash 的代码拷贝到 RAM 中运行，这一段拷贝代码就存在于 `__main()` 函数中，但**拷贝代码不能拷贝自身**，所以必须规定有一个运行时域中存放的代码是不会被拷贝的，这个指的就是第一个运行时域。
  - 一段代码必须先完成拷贝，才能被执行。换句理解就是拷贝代码前包括自身的所
有代码都不能拷贝，也就是说这些代码全部都必须放在第一个运行时域中。
- 规定其余运行时域中存放的代码均会被拷贝
  - 一个加载时域，只需要一个不拷贝的运行时域即可。所以规定其余所有的运行时域中的代码均会被拷贝。
- 第一个运行时域的基址必须与加载域基址相同
  - 为了保证第一个运行时域的代码能够被正确存储和执行，因此要求第一个运行时域的基址必须和加载时域的基址相同。

关于 `__main()` 做的事情：此函数为编译器自动创建，编译器发现定义了 `main()` 就会自动创建 `__main()`，此函数为 C 库函数。程序 reset 运行后，执行到这里，主要有两个比较大的行为
- `__scatterload()` 负责把 RW/RO 段从装载域地址复制到运行域地址，并完成 ZI 运行域的初始化工作
- `__rt_entry()` 负责初始化堆栈，完成库函数初始化，最后自动跳转 `main()` 函数


## 一个实际的例子

```
#define m_flash_config_start           0x60000000
#define m_flash_config_size            0x00001000

#define m_ivt_start                    0x60001000
#define m_ivt_size                     0x00001000

#define m_interrupts_start             0x60002000
#define m_interrupts_size              0x00000400

#define m_text_start                   0x60002400
#define m_text_size                    0x007FDC00

#define m_data_start                   0x20000000
#define m_data_size                    0x00020000

#define m_data2_start                  0x20200000
#define m_data2_size                   0x000C0000

/* Sizes */
#if (defined(__stack_size__))
  #define Stack_Size                   __stack_size__
#else
  #define Stack_Size                   0x0400
#endif

#if (defined(__heap_size__))
  #define Heap_Size                    __heap_size__
#else
  #define Heap_Size                    0x0400
#endif

#if defined(XIP_BOOT_HEADER_ENABLE) && (XIP_BOOT_HEADER_ENABLE == 1)
LR_m_text m_flash_config_start m_text_start+m_text_size-m_flash_config_start {   ; load region size_region
  
  RW_m_config_text m_flash_config_start FIXED m_flash_config_size { ; load address = execution address
    * (.boot_hdr.conf, +FIRST)
  }

  RW_m_ivt_text m_ivt_start FIXED m_ivt_size { ; load address = execution address
    * (.boot_hdr.ivt, +FIRST)
    * (.boot_hdr.boot_data)
    * (.boot_hdr.dcd_data)
  }
#else
LR_m_text m_interrupts_start m_text_start+m_text_size-m_interrupts_start {   ; load region size_region
#endif
  VECTOR_ROM m_interrupts_start FIXED m_interrupts_size { ; load address = execution address
    * (RESET,+FIRST)
  }
  ER_m_text m_text_start FIXED m_text_size { ; load address = execution address
    * (InRoot$$Sections)
    .ANY (+RO)
  }
  RW_m_data m_data_start m_data_size-Stack_Size-Heap_Size { ; RW data
    .ANY (+RW +ZI)
    * (NonCacheable.init)
    * (NonCacheable)
  }
  ARM_LIB_HEAP +0 EMPTY Heap_Size {    ; Heap region growing up
  }
  ARM_LIB_STACK m_data_start+m_data_size EMPTY -Stack_Size { ; Stack region growing down
  }
}
```


## 参考资料

- [ARM之一 分散加载文件（scatter）详述](https://blog.csdn.net/KXue0703/article/details/114018759)
- [Scatter文件的编写及分析](https://blog.csdn.net/nolatin/article/details/8545606?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-8545606-blog-114018759.235%5Ev35%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-8545606-blog-114018759.235%5Ev35%5Epc_relevant_default_base3&utm_relevant_index=1)

