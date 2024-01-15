from turtle import *


def drawcircle(cl, r):
    color(cl)
    begin_fill()
    circle(r)
    end_fill()


drawcircle("blue", 120)
goto(0, 20)
drawcircle("yellow", 100)
goto(0, 40)
drawcircle("red", 80)
goto(0, 60)
drawcircle("green", 60)
hideturtle()
done()
