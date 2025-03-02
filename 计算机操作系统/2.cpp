#include <deque>
#include <cstdio>
#include <algorithm>
using namespace std;
struct opt
{
    int value;
    int time;
};
const int maxn = 105;
int a[maxn];
int main()
{
    deque<opt> dq;
    deque<opt>::iterator pos;
    int numyk, numqueye = 0;
    printf("请输入物理页框块数:");
    scanf("%d", &numyk);
    int n;
    printf("\n请输入页面走向个数：");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (int i = 0; i < n; i++)
    {
        printf("第%d个\n", i);
        int in;
        in = a[i];
        if (dq.size() < numyk) // 存在多余页框
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos).value == in) // 存在元素和它相同
                {
                    flag = 1;
                    break;
                } // 存在该元素
            if (!flag) // 不存在此元素
            {
                numqueye++;
                opt temp;
                temp.value = in;
                int f = 0;
                for (int j = i + 1; j < n; j++)
                    if (a[j] == in)
                    {
                        f = 1;
                        temp.time = j - i;
                        break;
                    }
                if (!f)
                    temp.time = n;
                dq.push_back(temp);
            }
        }
        else // 不存在多余页框
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos).value == in)
                {
                    flag = 1;
                    break;
                } // 存在该元素
            if (!flag) // 不存在此元素 则置换time最大的项
            {
                numqueye++; // 缺页数+1
                int m = dq.front().time;
                printf("m初始值为%d\n", m);
                deque<opt>::iterator mp = dq.begin(); // 注意此处千万注意初始化 否则有可能erase找不到对象崩溃
                for (pos = dq.begin(); pos != dq.end(); pos++)
                {
                    printf("%d %d\n", (*pos).value, (*pos).time);
                    if ((*pos).time > m)
                    {
                        printf("迭代");
                        mp = pos; // 时间最大的元素的位置
                        m = (*pos).time;
                    }
                }
                opt temp;
                temp.value = in;
                int f = 0;
                dq.erase(mp);

                for (int j = i + 1; j < n; j++)
                    if (a[j] == in)
                    {
                        f = 1;
                        temp.time = j - i;
                        break;
                    }
                if (!f)
                    temp.time = n;
                dq.push_back(temp);
            }
        }
        // 每次之后重置
        for (pos = dq.begin(); pos != dq.end(); pos++)
        {
            printf("队列中的元素为 %d\n", (*pos).value);
            int f = 0;
            for (int j = i + 1; j < n; j++)
                if (a[j] == (*pos).value)
                {
                    f = 1;
                    (*pos).time = j - i;
                    break;
                }
            if (!f)
                (*pos).time = n;
        }
    }
    printf("opt缺页次数为:%d\n", numqueye);
    printf("opt缺页中断率为：%lf\n", (double)numqueye * 1.0 / n);
}
