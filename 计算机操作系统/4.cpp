#include <stdio.h>
int MA[4];       /*空闲块数组*/
int A[9][4] = {
    {3, 1, 2, 3}, {3, 4, 5, 6}, {0, 0, 0, 0}, 
    {0, 0, 0, 0}, {3, 0, 7, 8}, {0, 0, 0, 0}, 
    {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}
};               /*磁盘空间*/
int mark[9];     /*存放已分配的块*/
int No = 0;      /*已分配的块数*/
void display1()
{
    int i, j, temp, count;
    No = 0;
    if (MA[1] != 0)
    {
        i = MA[0];
        printf("\ngroup1:");
        for (j = 1; j <= i; j++)
        {
            printf("%d   ", MA[j]);
            mark[++No] = MA[j];
        }
        temp = MA[1];
        count = 2;
        while (A[temp][1] != 0)
        {
            printf("\ngroup%d:", count);
            i = A[temp][0];
            for (j = 1; j <= i; j++)
            {
                printf("%d   ", A[temp][j]);
                mark[++No] = A[temp][j];
            }
            count++;
            temp = A[temp][1];
        }
        printf("\ngroup%d:", count);
        i = A[temp][0];
        for (j = 2; j <= i + 1; j++)
            if (A[temp][j] > 0)
            {
                printf("%d   ", A[temp][j]);
                mark[++No] = A[temp][j];
            }
    }
    else
    {
        i = MA[0];
        if (i == 1)
            printf("\nThe blocks are all assigned");
        else
        {
            printf("\ngroup1:");
            for (j = 2; j <= i; j++)
            {
                printf("%d   ", MA[j]);
                mark[++No] = MA[j];
            }
        }
    }
}

void display() /*显示分组情况*/
{
    int i, j;
    if (MA[0] != 0)
        display1();
    else
    {
        i = MA[1];
        for (j = 0; j <= 3; j++)
            MA[j] = A[i][j];
        display1();
    }
}

void assign() /*分配空闲块*/
{
    int s, i;
    if (MA[0] > 1) /*若该组不止一个空闲块*/
    {
        i = MA[0];
        s = MA[i];
        MA[0]--;
        printf("\nnumber of the block:%d", s);
    }
    else if (MA[0] == 1) /*只剩一个空闲块*/
    {
        if (MA[1] != 0) /*还有其它空闲块组*/
        {
            s = MA[1];
            for (i = 0; i <= 3; i++)
                A[0][i] = A[s][i];
            MA[0]--;
            printf("\nnumber of the block:%d", s);
        }
        else /*没有其它空闲块组*/
        {
            printf("\nThere isn't any space");
            return;
        }
    }
    else /*当前组已分配完*/
    {
        for (i = 0; i <= 3; i++)
            MA[i] = A[0][i];
        assign();
    }
    display(); /*显示分组情况*/
}

void callback() /*回收空闲块*/
{
    int i, j, temp;
    printf("\ninput the No. of the block you want to callback:");
    scanf("%d", &j);
    getchar(); /*得到待回收的空闲块号*/
    for (temp = 1; temp <= No; temp++)
    {
        if (mark[temp] == j)
            break;
    }
    if (temp < No + 1) /*若该空闲块已在，退出*/
    {
        printf("\nThe block is in the disk");
        return;
    }
    if (MA[0] < 3) /*当前组不满3块*/
    {
        i = MA[0];
        MA[i + 1] = j;
        MA[0]++;
    }
    else /*已有3块*/
    {
        for (i = 0; i <= 3; i++)
            A[j][i] = MA[i];
        MA[0] = 1;
        MA[1] = j;
    }
    display(); /*显示*/
}

void menu() /*功能选择函数*/
{
    int choice;
    char judge;
    printf("\ninput your choice:(1--assign,2--callback):");
    scanf("%d", &choice);
    getchar();
    if (choice == 1)
        assign();
    else if (choice == 2)
        callback();
    else
        printf("\ninvalid command!");
    printf("\ncontinue or not?(y--Yes,n--Not):");
    scanf("%c", &judge);
    getchar();
    if (judge == 'y')
        menu();
    else
    {
        printf("\nNow the graph is:");
        display();
        printf("\npress any key to quit");
        int getch(void);
    }
}

int main(void)
{
    int i;
    for (i = 0; i <= 3; i++)
        MA[i] = A[0][i];
    display();
    menu();
    return 0;
}
