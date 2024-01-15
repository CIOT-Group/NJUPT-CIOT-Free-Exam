# -*- coding:utf-8 -*-

# 提示用户从键盘上输入一个数num，判断该数num是否为回文数。（回文数：数字正序和反序是同一个数，例如输入12321，则显示12321是一个回文数。）

num = int(input("请输入一个整数："))
if num == int(str(num)[::-1]):
    print("{}是一个回文数".format(num))
else:
    print("{}不是一个回文数".format(num))
