#include <stdio.h>
int MA[4];       /*���п�����*/
int A[9][4] = {
    {3, 1, 2, 3}, {3, 4, 5, 6}, {0, 0, 0, 0}, 
    {0, 0, 0, 0}, {3, 0, 7, 8}, {0, 0, 0, 0}, 
    {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}
};               /*���̿ռ�*/
int mark[9];     /*����ѷ���Ŀ�*/
int No = 0;      /*�ѷ���Ŀ���*/
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

void display() /*��ʾ�������*/
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

void assign() /*������п�*/
{
    int s, i;
    if (MA[0] > 1) /*�����鲻ֹһ�����п�*/
    {
        i = MA[0];
        s = MA[i];
        MA[0]--;
        printf("\nnumber of the block:%d", s);
    }
    else if (MA[0] == 1) /*ֻʣһ�����п�*/
    {
        if (MA[1] != 0) /*�����������п���*/
        {
            s = MA[1];
            for (i = 0; i <= 3; i++)
                A[0][i] = A[s][i];
            MA[0]--;
            printf("\nnumber of the block:%d", s);
        }
        else /*û���������п���*/
        {
            printf("\nThere isn't any space");
            return;
        }
    }
    else /*��ǰ���ѷ�����*/
    {
        for (i = 0; i <= 3; i++)
            MA[i] = A[0][i];
        assign();
    }
    display(); /*��ʾ�������*/
}

void callback() /*���տ��п�*/
{
    int i, j, temp;
    printf("\ninput the No. of the block you want to callback:");
    scanf("%d", &j);
    getchar(); /*�õ������յĿ��п��*/
    for (temp = 1; temp <= No; temp++)
    {
        if (mark[temp] == j)
            break;
    }
    if (temp < No + 1) /*���ÿ��п����ڣ��˳�*/
    {
        printf("\nThe block is in the disk");
        return;
    }
    if (MA[0] < 3) /*��ǰ�鲻��3��*/
    {
        i = MA[0];
        MA[i + 1] = j;
        MA[0]++;
    }
    else /*����3��*/
    {
        for (i = 0; i <= 3; i++)
            A[j][i] = MA[i];
        MA[0] = 1;
        MA[1] = j;
    }
    display(); /*��ʾ*/
}

void menu() /*����ѡ����*/
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
