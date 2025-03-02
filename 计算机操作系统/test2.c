#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int pid1, pid2;
int main()
{
    int fd[2];
    char outpipe[100], inpipe[100];
    pipe(fd); /*创建一个管道*/
    while ((pid1 = fork()) == -1);
    if (pid1 == 0)
    {
        lockf(fd[1], 1, 0);
        sprintf(outpipe, "child 1 process is sending message!");
        /*把串放入数组outpipe中*/
        write(fd[1], outpipe, 50); /*向管道写长为50字节的串*/
        sleep(5);                  /*自我阻塞5秒*/
        lockf(fd[1], 0, 0);
        exit(0);
    }
    else
    {
        while ((pid2 = fork()) == -1);
        if (pid2 == 0)
        {
            lockf(fd[1], 1, 0); /*互斥*/
            sprintf(outpipe, "child 2 process is sending message!");
            write(fd[1], outpipe, 50);
            sleep(5);
            lockf(fd[1], 0, 0);
            exit(0);
        }
        else
        {
            wait(0);                 /*同步*/
            read(fd[0], inpipe, 50); /*从管道中读长为50字节的串*/
            printf("%s\n", inpipe);
            wait(0);
            read(fd[0], inpipe, 50);
            printf("%s\n", inpipe);
            exit(0);
        }
    }
    return 0;
}
