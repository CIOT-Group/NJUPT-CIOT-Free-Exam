# -*- coding:utf-8 -*-

# 某自然数除它本身以外的所有因子之和等于该数，这个数就称为“完数”。例如，6的因子为1,2,3，6=1+2+3，因此6是一个完数。编写程序找出1000之内的所有完数。

def is_perfect(n):
    sum = 0
    for i in range(1, n):
        if n % i == 0:
            sum += i
    if sum == n:
        return n


def main():
    for i in range(1, 1000):
        if is_perfect(i):
            print(i)


if __name__ == '__main__':
    main()
