#include <deque>
#include <cstdio>
#include <algorithm>
using namespace std;

int main()
{
    deque<int> dq;
    deque<int>::iterator pos;
    int numyk, numqueye = 0;
    printf("请输入物理页框块数:");
    scanf("%d", &numyk);
    int n;
    printf("\n请输入页面走向个数：");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        int in;
        scanf("%d", &in);
        if (dq.size() < numyk) // 存在空余页框
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++) // 遍历队列
                if ((*pos) == in)
                {
                    flag = 1;
                    break;
                }
            if (!flag) // 不存在此元素
            {
                numqueye++;
                dq.push_back(in); // 放入队列
            }
        }
        else // 不存在多余页框
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos) == in)
                {
                    flag = 1;
                    break;
                } // 存在该元素
            if (!flag) // 不存在此元素 则置换最先进入的项
            {
                numqueye++;       // 缺页数+1
                dq.pop_front();   // 最先进入的出队列
                dq.push_back(in); // 进队列
            }
        }
    }
    printf("fifo缺页次数为:%d\n", numqueye);
    printf("fifo缺页中断率为：%lf\n", (double)numqueye * 1.0 / n);
}
