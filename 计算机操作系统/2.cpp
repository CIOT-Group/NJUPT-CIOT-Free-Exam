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
    printf("����������ҳ�����:");
    scanf("%d", &numyk);
    int n;
    printf("\n������ҳ�����������");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (int i = 0; i < n; i++)
    {
        printf("��%d��\n", i);
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
        else // �����ڶ���ҳ��
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos).value == in)
                {
                    flag = 1;
                    break;
                } // ���ڸ�Ԫ��
            if (!flag) // �����ڴ�Ԫ�� ���û�time������
            {
                numqueye++; // ȱҳ��+1
                int m = dq.front().time;
                printf("m��ʼֵΪ%d\n", m);
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
        // ÿ��֮������
        for (pos = dq.begin(); pos != dq.end(); pos++)
        {
            printf("�����е�Ԫ��Ϊ %d\n", (*pos).value);
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
    printf("optȱҳ����Ϊ:%d\n", numqueye);
    printf("optȱҳ�ж���Ϊ��%lf\n", (double)numqueye * 1.0 / n);
}
