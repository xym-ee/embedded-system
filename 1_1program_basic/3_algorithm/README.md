
## 刷算法题


简单题，主要是基础的数据结构，比如排序，链表，队列、栈及一些字符串的算法。中等题，会涉及BFS, DFS，动态规划，树等。

ACM 模式常用的输出输入函数

C 库函数

- 字符串：3，49，30
- 线性表：86，16，27，732
- 队列：641，406，899
- 栈：946，116，117，895
- 哈希表：61，729，25，554
- dfs：105，112，98，494，547，1254
- bfs：1091，1129，102，101，752


## 一些输入输出

输入示例
3 4
11 40
输出示例
7
51

```c
#include <stdio.h>
int main()
{
    int a, b;
    while (scanf("%d %d\n", &a, &b) != EOF)
    {
        int c = a + b;
        printf("%d\n", c);
    }
}
```

## 读取一个字符串

```c
#include <stdio.h>
#include <string.h>
 
int main()
{
    char str[1000];
    int a=0, i=0;
    while(scanf("%s",str) != EOF);
    a = strlen(str);
    printf("%d",a);
}
```

到空格、换行就停止了。

要读取一行包含空格的

```c
scanf("%[^/n]", str);
```


## C 库中的一些函数

快速排序在 `stdlib.h` 中，声明如下

```c
void qsort(void *base, size_t num, size_t size, int (*compar)(const void *, const void *));
```
- base: 指向要排序的数组的指针。
- num: 数组中元素的数量。
- size: 数组中每个元素的大小（以字节为单位）。
- compar: 指向用于比较两个元素的函数的指针。该函数接受两个 const void* 类型的参数，并返回一个 int 值：
  - 如果第一个元素小于第二个元素，返回负值。
  - 如果第一个元素等于第二个元素，返回 0。
  - 如果第一个元素大于第二个元素，返回正值。

因为不知道要排序的是什么类型的值，所以都用了 void* ，需要自己实现一个两个元素比较的函数。使用示例

```c
#include <stdio.h>
#include <stdlib.h>

// 比较函数：升序排序
int compare_ints(const void *a, const void *b) {
    int int_a = *(int *)a;
    int int_b = *(int *)b;
    return (int_a > int_b) - (int_a < int_b);  // 相当于 int_a - int_b，但避免溢出问题
}

int main() {
    int values[] = { 88, 56, 100, 2, 25, 15 };
    size_t num_values = sizeof(values) / sizeof(values[0]);

    // 使用 qsort 对数组进行排序
    qsort(values, num_values, sizeof(int), compare_ints);

    // 打印排序后的结果
    for (size_t i = 0; i < num_values; i++) {
        printf("%d ", values[i]);
    }

    return 0;
}
```


## 代码测试

ACM 模式下在自己的电脑上做测试。

准备好测试用例。

```bash
diff <(cat bottle_case | ./a.out) bottle_out
```







