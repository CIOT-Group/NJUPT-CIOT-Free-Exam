#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>

#define SHMKEY 75 /*定义共享区关键词*/

void CLIENT()
{
    int shmid, i;
    int *addr;
    shmid = shmget(SHMKEY, 1024, 0777 | IPC_CREAT);

    /*获取共享区，长度1024，关键词SHMKEY*/
    addr = shmat(shmid, 0, 0); /*共享区起始地址为addr*/
    for (i = 9; i >= 0; i--)
    {
        while (*addr != -1);
        printf("(client)sent\n");
        *addr = i; /*把i赋给addr*/
    }
    exit(0);
}

void SERVER()
{
    int shmid;
    int *addr;

    shmid = shmget(SHMKEY, 1024, 0777 | IPC_CREAT);
    /*创建共享区*/
    addr = shmat(shmid, 0, 0); /*共享区起始地址为addr*/
    *addr = -1;
    do
    {
        while (*addr == -1);
        printf("(server)received\n%d", *addr);
        if (*addr != 0)
            *addr = -1;
    } while (*addr != 0);

    wait(0);
    shmctl(shmid, IPC_RMID, 0);
}

void main()
{
    if (fork())
    {
        SERVER();
    }
    else
    {
        CLIENT();
    }
}
