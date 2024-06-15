---
sort: 1
---
# task

在 FreeRTOS 中，每个执行线程都被称为”任务”。从以前的经验来看，线程具有
更多的特定含义。


```c
void ATaskFunction(void *pvParameters)
{
    int iVaribale = 0;

    for(;;)
    {

    }

    vTaskDelete(NULL);
}
```
- 必须返回 void
- 带有一个 void 指针参数
- 觉不允许有 return 语句，即不可以从任务中返回，也不可以执行到 }

一个任务函数可以创建许多个任务，每个任务都是独立的执行实例，有自己的栈空间。


任务创建
```c
BaseType_t xTaskCreate(	TaskFunction_t pxTaskCode,
                        const char * const pcName,
                        const uint16_t usStackDepth,
                        void * const pvParameters,
                        UBaseType_t uxPriority,
                        TaskHandle_t * const pxCreatedTask );
```
- 参数说明
  - pxTaskCode 一个永不退出的 C 函数
  - pcName 任务名字
  - usStackDepth 栈大小，单位为 word 非 byte
  - pvParameters 给任务函数的一个函数
  - uxPriority 优先级
  - pxCreatedTask 指向任务控制句柄，如果不控制可以设为 NULL
- 返回值
  - pdPASS
  - errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY


一个例子

```c
void vTaskFunction( void *pvParameters )
{
    char *pcTaskName;
    volatile unsigned long ul;   

    pcTaskName = ( char * ) pvParameters;

    for(;;)
    {
        vPrintString(pcTaskNake);

        for(ul = 0; ul<mainDELAY_LOOP_COUNT; ul++)
        {

        }
    }
}

static const char *pcTextForTask1 = “Task 1 is running\r\n”;
static const char *pcTextForTask2 = “Task 2 is running\t\n”;

int main()
{
    /* Create one of the two tasks. */
    xTaskCreate(    vTaskFunction,          /* 指向任务函数的指针. */
                    "Task 1",               /* 任务名. */
                    1000,                   /* 栈深度. */
                    (void*)pcTextForTask1,  /* 通过任务参数传入需要打印输出的文本. */
                    1,                      /* 此任务运行在优先级1上. */
                    NULL );                 /* 不会用到此任务的句柄. */   
    xTaskCreate( vTaskFunction, "Task 2", 1000, (void*)pcTextForTask2, 1, NULL );

    vTaskStartScheduler();

    for( ;; );
}
```

使用一个任务函数创建两个任务实例输出不同内容，降低代码的重复性。

对于单核 CPU 可以现象的到，经管有两个任务，但是在一个时刻，仅可能有一个任务占用 CPU，因此一个任务最基本的有两个状态：运行态和非运行态。在抢占式内核中，两个任务相同优先级下，会按时间片调度。如果两个任务优先级不同，上面的代码会出现“饿死”低优先级任务的情况。换句话说，任务循环没有等待。

这时候就需要扩充任务状态了。
- 阻塞态：等待某事事情，是非运行态的一个子状态
  - 定时：阻塞延时
  - 同步：队列、信号量、互斥量

循环延迟改成阻塞延迟，使用 `vTaskDelay()` 函数，此外还有用于实现一个固定执行周期的 `vTaskDelayUntil()`




