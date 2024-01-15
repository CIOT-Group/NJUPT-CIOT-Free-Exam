# 编写程序找出前5个默尼森数。所谓默尼森数是指P是素数且M也是素数，并且满足等式M=2^P-1，则称M为默尼森数。例如P=5，M=2^P-1=31，5和31都是素数，因此31是默尼森数。

from math import sqrt, ceil


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(ceil(sqrt(n))) + 1):
        if n % i == 0:
            return False
    return True


def is_mns():
    index = 0
    num = 0
    while True:
        num += 1
        if is_prime(num) and is_prime(2 ** num - 1):
            print(2 ** num - 1)
            index += 1
            if index == 5:
                break


is_mns()
