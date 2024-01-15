# 一小球从100米高度自由落下，每次落地后反跳回原高度的一半再落下，编写自定义函数cal计算小球在第n次落地时，共经过多少路程以及第n次反弹的高度。定义全局变量sn和hn分别存储小球经过的路程和第n次反弹的高度，n值由键盘输入。

sn = 0
hn = 100

def cal(n):
    global sn, hn

    for i in range(1, n + 1):
        sn += 2 * hn
        hn /= 2

    return sn - 100, hn


n = int(input("请输入 n 的值："))

s, h = cal(n)
print("第 {} 次落地时，共经过的路程为 {} 米，第 {} 次反弹的高度为 {} 米。".format(n, s, n, h))
