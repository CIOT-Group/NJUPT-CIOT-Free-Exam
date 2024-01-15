// 设计算法，将一个带头结点的单链表A分解为两个带头结点的单链表A和B，使得A表中含有原表中序号为奇数的元素，而B表中含有原表中序号为偶数的元素，且保持其相对顺序不变。要求:
// （1）给出算法的基本设计思想。可以选用下列方式的一种或多种进行表述：自然语言、流程图、伪代码等。
// （2）根据设计思想，采用C/C++语言实现，给出注释；并给出运行及结果截图。
// （3）说明你所设计算法的时间复杂度和空间复杂度。
// （4）请举例说明你所设计的算法在工程场景中的应用。

#include <stdio.h>
#include <stdlib.h>

// 初始化链表
struct List
{
    int data;
    struct List *next;
};

// 分解链表为一个奇数项链表A和偶数项链表B
void splitLinkedList(struct List *head, struct List **A, struct List **B)
{
    struct List *oddHead = NULL;  // 奇数序号链表的头结点
    struct List *evenHead = NULL; // 偶数序号链表的头结点
    struct List *current = head;  // 当前节点

    int index = 1; // 记录当前节点的序号

    while (current != NULL) // 当前节点不为空
    {
        struct List *newNode = (struct List *)malloc(sizeof(struct List));
        newNode->data = current->data;
        newNode->next = NULL;

        if (index % 2 == 1)
        { // 奇数序号节点
            if (oddHead == NULL)
            {
                // 链表为空，直接将新节点作为头节点
                oddHead = newNode;
                *A = oddHead;
            }
            else
            {
                // 将新节点作为头节点，并将头节点指向下一个节点
                oddHead->next = newNode;
                oddHead = oddHead->next;
            }
        }
        else
        { // 偶数序号节点
            if (evenHead == NULL)
            {
                // 链表为空，直接将新节点作为头节点
                evenHead = newNode;
                *B = evenHead;
            }
            else
            {
                // 将新节点作为头节点，并将头节点指向下一个节点
                evenHead->next = newNode;
                evenHead = evenHead->next;
            }
        }

        current = current->next;
        index++;
    }
}

// 打印链表
void printLinkedList(struct List *head)
{
    struct List *current = head;
    while (current != NULL)
    {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("END\n");
}

int main()
{
    // 创建带头结点的原始链表
    struct List *head = (struct List *)malloc(sizeof(struct List));
    head->next = NULL;
    struct List *current = head;

    // 添加数据
    for (int i = 1; i <= 20; i++)
    {
        struct List *newNode = (struct List *)malloc(sizeof(struct List));
        newNode->data = i;
        newNode->next = NULL;
        current->next = newNode;
        current = current->next;
    }

    struct List *A = NULL; // 奇数项链表
    struct List *B = NULL; // 偶数项链表

    // 分解链表
    splitLinkedList(head->next, &A, &B);

    // 打印分解后的链表A和B
    printf("OddListA: ");
    printLinkedList(A);
    printf("EvenListB: ");
    printLinkedList(B);

    return 0;
}