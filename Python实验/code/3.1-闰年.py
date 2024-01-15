# 编写自定义函数leapyear，要求可以根据输入的年份判断该年是否是闰年。

def leapyear(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False


year = int(input("请输入年份："))
if leapyear(year):
    print("{}年是闰年".format(year))
else:
    print("{}年不是闰年".format(year))
