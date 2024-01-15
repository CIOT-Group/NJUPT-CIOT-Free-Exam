# -*- coding:utf-8 -*-

# BMI指数（身体质量指数，简称体质指数，又称体重指数）是国际上常用的衡量人体胖瘦程度以及是否健康的一个标准。

# 计算公式：BMI=体重（公斤）÷身高（米）的平方kg/m^2，下表列出了中国BMI分类标准。
# 表1 中国BMI分类标准
# BMI值	分类
# <18.5	体重过轻
# 18.5~23.9	正常
# 24.0~27.9	超重
# 28.0~31.9	肥胖
# >=32	重度肥胖

# 编写程序，从键盘输入一个人的体重（公斤）和身高（米），计算并输出其BMI值（保留1位小数），并根据上述标准输出其分类。
# 提示：通过round()函数可进行四舍五入。

weight = float(input("请输入体重（公斤）："))
height = float(input("请输入身高（米）："))
bmi = weight / (height * height)
bmi1 = round(bmi, 1)

print("BMI指数为：{}".format(bmi1))

if bmi < 18.5:
    print("体重过轻")
elif 18.5 <= bmi < 23.9:
    print("正常")
elif 24.0 <= bmi < 27.9:
    print("超重")
elif 28.0 <= bmi < 31.9:
    print("肥胖")
elif bmi >= 32:
    print("重度肥胖")
else:
    print("输入错误")
