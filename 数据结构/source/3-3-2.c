// 求解汉诺塔问题，要求：
// （1）给出递归和非递归算法的基本设计思想。可以选用下列方式的一种或多种进行表述：自然语言、流程图、伪代码等。
// （2）根据设计思想，采用 C / C++ 语言实现，给出注释；并给出运行及结果截图。
// （3）说明你所设计算法的时间复杂度和空间复杂度。

// 非递归算法

#include <stdio.h>
#define STACK_SIZE 100

typedef struct
{
    int n;        // 当前盘片数量
    char x, y, z; // 起始柱子、辅助柱子、目标柱子
} Task;

typedef struct stack
{
    int top;
    Task stack[STACK_SIZE];
} stack;

// 创建一个空栈
void create(stack *s)
{
    s->top = -1;
}

// 从栈中弹出元素
Task pop(stack *s)
{
    return s->stack[s->top--];
}

// 将元素压入栈中
void push(stack *s, Task task)
{
    s->stack[++s->top] = task;
}

// 打印移动盘片的操作
void move(char x, char z)
{
    printf("Move disk from %c to %c\n", x, z);
}

// 汉诺塔游戏函数
void Hanoi(int n, char x, char y, char z)
{
    // 创建一个栈
    stack s;
    create(&s);

    // 将初始任务压入栈中
    Task initialTask = {n, x, y, z};
    push(&s, initialTask);

    // 当栈不为空时，循环执行
    while (s.top >= 0)
    {
        // 从栈中弹出当前任务
        Task current = pop(&s);

        // 获取当前任务中的参数
        n = current.n;
        x = current.x;
        y = current.y;
        z = current.z;

        // 如果当前任务是最后一个任务，则直接移动盘片
        if (n == 1)
        {
            move(x, z);
        }
        else
        {
            // 将盘片从起始柱子移动到辅助柱子
            Task task3 = {n - 1, y, x, z};
            push(&s, task3);

            // 将盘片从起始柱子移动到目标柱子
            Task task2 = {1, x, y, z};
            push(&s, task2);

            // 将盘片从辅助柱子移动到目标柱子
            Task task1 = {n - 1, x, z, y};
            push(&s, task1);
        }
    }
}

int main()
{
    int n = 0; // 盘片数量
    printf("Enter the number of disks: ");
    scanf("%d", &n);
    Hanoi(n, 'A', 'B', 'C');
    return 0;
}
