#include <deque>
#include <cstdio>
#include <algorithm>
using namespace std;
struct opt
{
    int value; // ֵ
    int time;  // ʱ��
};
const int maxn = 105;
int a[maxn];
int main()
{
    deque<opt> dq;
    deque<opt>::iterator pos;
    int numyk, numqueye = 0;
    printf("����������ҳ�����:");
    scanf("%d", &numyk);
    int n;
    printf("������ҳ�����������");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (int i = 0; i < n; i++)
    {
        int in;
        in = a[i];
        if (dq.size() < numyk) // ���ڶ���ҳ��
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos).value == in) // ����Ԫ�غ�����ͬ
                {
                    flag = 1;
                    break;
                } // ���ڸ�Ԫ��
            if (!flag) // �����ڴ�Ԫ��
            {
                numqueye++;
                opt temp;
                temp.value = in;
                temp.time = 0;
                dq.push_back(temp);
            }
        }
        else // �����ڶ���ҳ��
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos).value == in)
                {
                    flag = 1;
                    break;
                } // ���ڸ�Ԫ��
            if (!flag) // �����ڴ�Ԫ��
            {
                numqueye++; // ȱҳ��+1
                int m = dq.front().time;
                deque<opt>::iterator mp = dq.begin(); // ע��˴�ǧ��ע���ʼ�� �����п���erase�Ҳ����������
                for (pos = dq.begin(); pos != dq.end(); pos++)
                {
                    printf("%d %d\n", (*pos).value, (*pos).time);
                    if ((*pos).time > m)
                    {
                        printf("����");
                        mp = pos; // ʱ������Ԫ�ص�λ��
                        m = (*pos).time;
                    }
                }
                printf("��ʱ��������ʣʱ�����Ԫ��Ϊ%d\n", (*mp).value);
                opt temp;
                temp.value = in;
                int f = 0;
                dq.erase(mp);
                temp.time = 0; // �ӽ���֮��
                dq.push_back(temp);
            }
        }
        // ÿ��֮��������time
        for (pos = dq.begin(); pos != dq.end(); pos++)
        {
            printf("�����е�Ԫ��Ϊ %d\n", (*pos).value);
            int f = 0;
            for (int j = i; j >= 0; j--)
                if (a[j] == (*pos).value)
                {
                    (*pos).time = i - j;
                    break;
                }
            printf("�����ϴ�ʱ��Ϊ%d\n", (*pos).time);
        }
    }
    printf("lruȱҳ����Ϊ:%d\n", numqueye);
    printf("lruȱҳ�ж���Ϊ��%lf\n", (double)numqueye * 1.0 / n);
}