# -*- coding:utf-8 -*-

# 随机产生100个0~100之间的整数，每行显示10个数(整数之间用逗号分隔)，并统计这100个随机整数的平均值，结果保留1位小数。

import random

sum = 0
for i in range(1, 101):
    num = random.randint(0, 100)
    print(num, end=",")
    sum += num
    if i % 10 == 0:
        print()

ave = round(sum / 100, 1)
print("平均值：", ave)
