# 输入一个分钟数，输出多少年，多少天，多少时，多少分钟

def time_convert(minute):
    year = minute // 525600
    day = (minute - year * 525600) // 1440
    hour = (minute - year * 525600 - day * 1440) // 60
    minute = minute - year * 525600 - day * 1440 - hour * 60
    return year, day, hour, minute


if __name__ == "__main__":
    minute = int(input("请输入分钟数："))
    year, day, hour, minute = time_convert(minute)
    print("{}年{}天{}时{}分".format(year, day, hour, minute))
