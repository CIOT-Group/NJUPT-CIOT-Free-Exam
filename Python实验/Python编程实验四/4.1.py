names = ['wanglin', 'liuli', 'zhangming',
         'liuli', 'zhangming', 'zhaoqiang', 'liuli']

# 初始化一个空字典用于存储姓名和对应的次数
name_counts = {}

# 遍历姓名列表
for name in names:
    # 如果姓名已经在字典中，则将次数加1
    if name in name_counts:
        name_counts[name] += 1
    # 如果姓名不在字典中，则将姓名添加到字典，并将次数设为1
    else:
        name_counts[name] = 1

# 打印结果
print(name_counts)
