---
sort: 3
---
# sdk 

有点像是单片机的用法了。

STM32 HAL 库或者早年的 STD 库，底层的本质是操作寄存器。但是应用处理器里外设多，寄存器也多，可以自己写，但没必要。

SDK 里的一些封装也是为了让芯片使用起来更容易。

makefile 也可以做的让适配度更广泛一些。


```makefile
CROSS_COMPILE ?= arm-linux-gnueabihf-
NAME		  ?= ledc

CC 		:= $(CROSS_COMPILE)gcc
LD		:= $(CROSS_COMPILE)ld
OBJCOPY := $(CROSS_COMPILE)objcopy
OBJDUMP := $(CROSS_COMPILE)objdump

OBJS 	:= start.o main.o

$(NAME).bin:$(OBJS)
	$(LD) -Timx6ul.lds -o $(NAME).elf $^
	$(OBJCOPY) -O binary -S $(NAME).elf $@
	$(OBJDUMP) -D -m arm $(NAME).elf > $(NAME).dis

%.o:%.s
	$(CC) -Wall -nostdlib -c -O2 -o $@ $<
	
%.o:%.S
	$(CC) -Wall -nostdlib -c -O2 -o $@ $<
	
%.o:%.c
	$(CC) -Wall -nostdlib -c -O2 -o $@ $<
	
clean:
	rm -rf *.o $(NAME).bin $(NAME).elf $(NAME).dis
	

```

linux 内核的 makefile 就是类似的写法。



