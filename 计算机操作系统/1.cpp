#include <deque>
#include <cstdio>
#include <algorithm>
using namespace std;

int main()
{
    deque<int> dq;
    deque<int>::iterator pos;
    int numyk, numqueye = 0;
    printf("����������ҳ�����:");
    scanf("%d", &numyk);
    int n;
    printf("\n������ҳ�����������");
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        int in;
        scanf("%d", &in);
        if (dq.size() < numyk) // ���ڿ���ҳ��
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++) // ��������
                if ((*pos) == in)
                {
                    flag = 1;
                    break;
                }
            if (!flag) // �����ڴ�Ԫ��
            {
                numqueye++;
                dq.push_back(in); // �������
            }
        }
        else // �����ڶ���ҳ��
        {
            int flag = 0;
            for (pos = dq.begin(); pos != dq.end(); pos++)
                if ((*pos) == in)
                {
                    flag = 1;
                    break;
                } // ���ڸ�Ԫ��
            if (!flag) // �����ڴ�Ԫ�� ���û����Ƚ������
            {
                numqueye++;       // ȱҳ��+1
                dq.pop_front();   // ���Ƚ���ĳ�����
                dq.push_back(in); // ������
            }
        }
    }
    printf("fifoȱҳ����Ϊ:%d\n", numqueye);
    printf("fifoȱҳ�ж���Ϊ��%lf\n", (double)numqueye * 1.0 / n);
}
