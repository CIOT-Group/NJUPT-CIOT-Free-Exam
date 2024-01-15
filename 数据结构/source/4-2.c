// 某图片用如下矩阵表示，
// （1）请给出其对应的压缩存储解决方案。
// （2）请设计一种高效的图片转置算法，根据设计思想，采用 C / C++ 语言实现，给出注释；并给出运行及结果截图。

#include <stdio.h>
#include <stdlib.h>
#define maxSize 100

typedef int ElemType;

typedef struct term
{
    int row;
    int col;
    ElemType value;
} Term;

typedef struct matrix
{
    int m; // 矩阵行数
    int n; // 矩阵列数
    int t; // 非零元素个数
    Term Table[maxSize];
} SparseMatrix;

// 打印稀疏矩阵
void printMatrix(SparseMatrix M)
{
    for (int i = 0; i < M.m; i++)
    {
        for (int j = 0; j < M.n; j++)
        {
            int isNonZero = 0;
            for (int k = 0; k < M.t; k++)
            {
                if (M.Table[k].row == i && M.Table[k].col == j)
                {
                    printf("%d\t", M.Table[k].value);
                    isNonZero = 1;
                    break;
                }
            }
            if (!isNonZero)
            {
                printf("0\t");
            }
        }
        printf("\n");
    }
}

// 快速转置算法
SparseMatrix transposeMatrix(SparseMatrix A)
{
    SparseMatrix B;
    B.m = A.n;
    B.n = A.m;
    B.t = A.t;

    ////数组num的元素统计稀疏矩阵A列号为j的非零元素个数
    int num[maxSize];
    // 数组k的元素k[j]统计稀疏矩阵A中列号从0到j-1的非零元素个数总和，该值也表示j列第一个非零元素在转置稀疏矩阵B的行三元组表中的位置
    int k[maxSize];

    // 计算每一列非零元素个数
    for (int j = 0; j < A.n; j++)
        num[j] = 0;
    for (int i = 0; i < A.t; i++)
        num[A.Table[i].col]++;

    // 计算每一列非零元素在B矩阵中的位置
    for (int j = 0; j < A.n; j++)
        k[j] = 0;
    for (int j = 1; j < A.n; j++)
        k[j] = k[j - 1] + num[j - 1];

    // 借助数组k完成快速转置
    for (int i = 0; i < A.t; i++)
    {
        int index = k[A.Table[i].col]++;
        B.Table[index].col = A.Table[i].row;
        B.Table[index].row = A.Table[i].col;
        B.Table[index].value = A.Table[i].value;
    }

    return B;
}

int main()
{
    SparseMatrix A;
    A.m = 6; // 6行
    A.n = 6; // 6列
    A.t = 7; // 7个非零元素

    // 行三元组表
    int nonZeroElements[7][3] = {
        {0, 0, -5},
        {0, 1, -2},
        {1, 3, -6},
        {3, 1, -3},
        {4, 0, -7},
        {4, 3, -4},
        {5, 2, -1}};

    // 将三元组表存入矩阵A中
    for (int i = 0; i < A.t; i++)
    {
        A.Table[i].row = nonZeroElements[i][0];
        A.Table[i].col = nonZeroElements[i][1];
        A.Table[i].value = nonZeroElements[i][2];
    }
    printf("Before Transposed Matrix A:\n");
    printMatrix(A);

    // 调用快速转置算法
    SparseMatrix B = transposeMatrix(A);

    printf("\n");
    printf("Aftrt Transposed Matrix B:\n");
    printMatrix(B);

    return 0;
}
