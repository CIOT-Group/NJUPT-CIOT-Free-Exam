#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

int msgqid, pid, *pint, i;
struct msgform
{
    long mtype;
    char mtext[50];
} msg;

void client()
{
    msgqid = msgget(66, 8888);
    pid = getpid();
    pint = (int *)msg.mtext;
    *pint = pid;
    msg.mtype = 1;
    msgsnd(msgqid, &msg, sizeof(int), 0);
    msgrcv(msgqid, &msg, 50, pid, 0);
    printf("(client):receive reply from pid=%d\n", *pint);
    exit(0);
}
void server()
{
    msgqid = msgget(66, 8888 | IPC_CREAT);
    msgrcv(msgqid, &msg, 50, 1, 0);
    pint = (int *)msg.mtext;
    pid = *pint;
    printf("(server):serving for client pid=%d\n", pid);
    msg.mtype = pid;
    *pint = getpid();
    msgsnd(msgqid, &msg, sizeof(int), 0);
    exit(0);
}

int main()
{
    while ((i = fork()) == -1);
    if (!i)
        server();
    while ((i = fork()) == -1);
    if (!i)
        client();
    wait(0);
    wait(0);
    return (0);
}
