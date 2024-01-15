from turtle import *


def Draw(n):
    color("blue")
    d = 180-((180*(n-2))/n)
    for i in range(n):
        forward(50)
        right(d)


def main():
    n = input("请输入一个正整数:")
    n = int(n)
    if (n < 3):
        print("输入的n应大于等于3")
        return 0
    else:
        Draw(n)
        hideturtle()
        done()


if __name__ == "__main__":
    main()
