# 编写自定义函数tax，要求可以根据输入的应纳税所得额计算出应缴纳的个人所得税。
# 年度个人所得税计算公式为：
# 应纳个人所得税税额=应纳税所得额×适用税率-速算扣除数

def tax(income):
    if income <= 36000:
        return income * 0.03 - 0
    elif income <= 144000:
        return income * 0.1 - 2520
    elif income <= 300000:
        return income * 0.2 - 16920
    elif income <= 420000:
        return income * 0.25 - 31920
    elif income <= 660000:
        return income * 0.3 - 52920
    elif income <= 960000:
        return income * 0.35 - 85920
    else:
        return income * 0.45 - 181920


income = int(input("请输入应纳税所得额："))
print("应纳税额：", tax(income))
