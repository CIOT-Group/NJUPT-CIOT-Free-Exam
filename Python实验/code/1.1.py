from turtle import *


def draw_star(size, cl):
    color(cl)
    begin_fill()
    for i in range(5):
        forward(size)
        right(144)
    end_fill()


def main():
    draw_star(100, "red")
    up()
    forward(150)
    down()
    draw_star(100, "yellow")
    hideturtle()
    done()


if __name__ == "__main__":
    main()
