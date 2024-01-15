# 采用while循环，获取给定字符串中的数字字符。要求考虑索引越界的情况，给出相应的提示。
# 【提示】
# (1) 索引越界会发生IndexError异常。
# (2) 一旦索引越界，即退出循环。

# 【输入样例】 "abc1234567def89"
# 输出样例：123456789
# It's end.

def extract(input_str):
    result = ""
    index = 0

    while True:
        try:
            char = input_str[index]
            if char.isdigit():
                result += char
            index += 1
        except IndexError:
            break

    return result


input_str = "abc1234567def89"
result = extract(input_str)

print(result)
print("It's end.")
