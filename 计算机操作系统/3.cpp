#include <deque>
#include <cstdio>
#include <algorithm>
using namespace std;
struct opt
{
    int value; // 值
    int time;  // 时间
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
    printf("请输入页面走向个数：");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (int i = 0; i < n; i++)
    {
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
                temp.time = 0;
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
            if (!flag) // 不存在此元素
            {
                numqueye++; // 缺页数+1
                int m = dq.front().time;
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
                printf("此时队列中所剩时间最长的元素为%d\n", (*mp).value);
                opt temp;
                temp.value = in;
                int f = 0;
                dq.erase(mp);
                temp.time = 0; // 加进来之后
                dq.push_back(temp);
            }
        }
        // 每次之后各对象的time
        for (pos = dq.begin(); pos != dq.end(); pos++)
        {
            printf("队列中的元素为 %d\n", (*pos).value);
            int f = 0;
            for (int j = i; j >= 0; j--)
                if (a[j] == (*pos).value)
                {
                    (*pos).time = i - j;
                    break;
                }
            printf("距离上次时间为%d\n", (*pos).time);
        }
    }
    printf("lru缺页次数为:%d\n", numqueye);
    printf("lru缺页中断率为：%lf\n", (double)numqueye * 1.0 / n);
}