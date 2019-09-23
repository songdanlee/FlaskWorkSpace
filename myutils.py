import datetime


class Calender:

    # 如果一号周周一那么第一行1-7号   0
    # 如果一号周周二那么第一行empty*1+1-6号  1
    # 如果一号周周三那么第一行empty*2+1-5号  2
    # 如果一号周周四那么第一行empty*3+1-4号  3
    # 如果一号周周五那么第一行empyt*4+1-3号  4
    # 如果一号周周六那么第一行empty*5+1-2号  5
    # 如果一号周日那么第一行empty*6+1号   6
    # 输入 1月
    # 得到1月1号是周几
    # [] 填充7个元素 索引0对应周一
    # 返回列表
    def __init__(self):
        # 接受所有的日期，需要是一个嵌套列表，列表当中嵌套的是7元素列表
        self.result = []

        # 月份分类
        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        now = datetime.datetime.now()
        month = now.month
        # 年 月 日 时 分
        first_date = datetime.datetime(now.year, now.month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)  # 指定月份的总天数
        elif month in small_month:
            day_range = range(1, 31)
        else:
            if not self.leep_year(now.year):
                day_range = range(1, 29)
            else:  # 闰年29天
                day_range = range(1, 30)
        # 获取指定月天数
        day_range = list(day_range)

        # python的日期当中 星期范围 0-6 0代表周一
        first_week = first_date.weekday()

        # 第一行数据
        line1 = ["empty" for e in range(first_week)]

        for d in range(7 - first_week):
            flag = 0 # 标记和当天的状态，0 小于今天，1 等于今天 ，2 大于今天
            if day_range[0] > now.day:
                flag = 2
            elif day_range[0] == now.day:
                flag = 1
            line1.append(
                {"day":str(day_range.pop(0)),"course":["数据分析"],"flag":flag}
            )
        self.result.append(line1)

        # 添加第二行到最后一行
        while day_range:  # 如果总天数列表有值，就接着循环
            line = []  # 每个子列表
            for i in range(7):
                if len(line) < 7 and day_range:
                    flag = 0  # 标记和当天的状态，0 小于今天，1 等于今天 ，2 大于今天
                    if day_range[0] > now.day:
                        flag = 2
                    elif day_range[0] == now.day:
                        flag = 1
                    line.append(
                        {"day":str(day_range.pop(0)),"course":["数据分析"],"flag":flag}
                    )
                else:
                    line.append("empty")
            self.result.append(line)


    # 返回当月的日历
    def calenda_month(self):
        return self.result

    # 计算闰年，闰年返回1
    def leep_year(self,year):
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 == 0)

    def print_result(self):
        # 只是为了展示效果
        print("星期一  星期二  星期三  星期四  星期五  星期六  星期日")
        for line in self.result:
            for day in line:
                print(day, end=" ")
            print()

if __name__ == '__main__':

    Calender().print_result()