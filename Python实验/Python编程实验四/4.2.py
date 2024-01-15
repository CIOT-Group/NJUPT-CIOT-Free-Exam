def count_str(input_str):
    # 将字符串拆分为单词列表
    words = input_str.split()
    word_counts = {}

    # 遍历单词列表
    for word in words:
        # 如果单词已经在字典中，则将次数加1
        if word in word_counts:
            word_counts[word] += 1
        # 如果单词不在字典中，则将单词添加到字典，并将次数设为1
        else:
            word_counts[word] = 1
    # 按照键的升序顺序对字典进行排序
    sorted_word_counts = dict(sorted(word_counts.items()))
    return sorted_word_counts

input_str = "Python C++ Java PHP Python Java Go Java"
result = count_str(input_str)

for word, count in result.items():
    print(f"{word} {count}")
