// 将n (n>1)个整数存放到一维数组R中，设计一个算法，将R中保存的序列循环左移p(0<p<n)个位置，即将R中的数据由(r0,r1,...,rn-1)变换为(rp,rp+1,...,rn-1,r0,r1,...,rp-1)。要求:
// （1）给出算法的基本设计思想。可以选用下列方式的一种或多种进行表述：自然语言、流程图、伪代码等。
// （2）根据设计思想，采用C/C++语言实现，给出注释;并给出运行及结果截图。
// （3）分析你所设计算法的时间复杂度和空间复杂度。
// （4）请举例说明你所设计的算法在工程场景中的应用。

#include <stdio.h>

// 反转数组中的一段区间
void reverse(int arr[], int start, int end)
{
    // 将数组中的元素反转
    while (start < end)
    {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}

// 将数组R中的数据左移p个位置
void Left(int arr[], int n, int p)
{
    if (p <= 0 || p >= n)
    {
        printf("Invalid rotation value.\n");
        return;
    }

    // 先反转前半部分
    reverse(arr, 0, p - 1);
    // 再反转后半部分1
    reverse(arr, p, n - 1);
    // 最后反转整个数组
    reverse(arr, 0, n - 1);
}

int main()
{
    int n, p;
    // 输入数组元素个数
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    // 如果数组元素个数小于2，则报错
    if (n <= 1)
    {
        printf("Error!\n");
        return 1;
    }

    // 定义一个数组R
    int R[n];

    // 输入数组元素
    printf("Enter the elements:\n");
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &R[i]);
    }

    // 输入要左移的位数
    printf("Enter the positions to move left (0 < p < n): ");
    scanf("%d", &p);

    // 调用函数rotateLeft，实现数组元素的左移
    Left(R, n, p);

    // 输出左移后的数组
    printf("Array after move:\n");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", R[i]);
    }
    printf("\n");

    return 0;
}