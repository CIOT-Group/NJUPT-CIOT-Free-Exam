#include <stdio.h>
#include <unistd.h>

void main()
{
    int pid;
    pid = fork();
    if (pid == 0)
    {
        printf("i am a son process!\n");
        printf("my process id is %d\n", pid);
    }
    else
    {
        printf("i am the father process!\n");
        printf("my process id is %d\n", pid);
    }
}