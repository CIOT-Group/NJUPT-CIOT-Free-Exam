// 求解汉诺塔问题，要求：
// （1）给出递归和非递归算法的基本设计思想。可以选用下列方式的一种或多种进行表述：自然语言、流程图、伪代码等。
// （2）根据设计思想，采用 C / C++ 语言实现，给出注释；并给出运行及结果截图。
// （3）说明你所设计算法的时间复杂度和空间复杂度。

// 递归算法

#include <stdio.h>

// 函数hanoi求解汉诺塔问题
void hanoi(int n, char X, char Y, char Z)
{
    // 如果盘子数量为1，则直接从X移动到Z
    if (n == 1)
    {
        printf("Move disk 1 from %c to %c\n", X, Z);
        return;
    }
    // 否则，先将n-1个盘子从X移动到Y，然后将第n个盘子从X移动到Z，最后将n-1个盘子从Y移动到Z
    else
    {
        hanoi(n - 1, X, Z, Y);
        printf("Move disk %d from %c to %c\n", n, X, Z);
        hanoi(n - 1, Y, X, Z);
    }
}

int main()
{
    int n = 0;
    printf("Enter the number of disks: ");
    scanf("%d", &n);
    // 调用函数hanoi求解问题
    hanoi(n, 'A', 'B', 'C');
    return 0;
}