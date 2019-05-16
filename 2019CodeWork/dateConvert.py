# Excel日期类型转换函数
# Excel 日期浮点数
# 时间起点 1900/01/00 00:00:00
# 单位1=1day
# Python time时间浮点数
# 时间起点 1970/01/01 08:00:00
# 单位1=1second
from datetime import datetime
from xlrd import xldate_as_tuple as conv
# __s_date = datetime.date(1899, 12, 31).toordinal() - 1


# def getdatestr(date: str) -> datetime.date:
#         try:
#                 return getDateTime(float(date))
#         except Exception as e:
#                 # print(str(e))
#                 return None


def getDateTime(date: float) -> datetime.date:
        try:
                res = conv(float(date),0)
                return datetime(res[0], res[1], res[2], res[3], res[4], res[5])
        except Exception as e:
                return None
        # print(date)
        # stamp = -70 * 3600 * 24 * 365 + 3600 * 24 * 4 - 8 * 3600
        # stamp += 3600*24*date
        # # +3600*365*date
        # return datetime.fromtimestamp(stamp)


        # # global __s_time
        # # intDate = int(date)
        # # result = datetime.date.fromordinal(__s_date + intDate)
        # # print(result.float())
        # # print(__s_date)
        # # floatTime = float(date)
        # # floatTime = time.localtime(int(floatTime*3600))
        # # return [result,floatTime]
if __name__ == '__main__':
        print(getDateTime(42773.41667))
#     res = conv(42773.41667, 0)
#     date = datetime(res[0], res[1], res[2], res[3], res[4], res[5])
#     print(date.weekday())
    # a = getDateTime(float(20 * 3600 * 24 * 365+3600*24*4-18*3600))
    # print(a+timedelta(hours = 10))
    # from datetime import datetime
    # t = 1429417200.0
    # print(datetime.fromtimestamp(t))
    # a = datetime(1900, 1, 1, 0, 0, 0)
    # a + datetime.timedelta(days=t)
    # b=datetime(1970, 1, 1, 8, 0, 0)
    # pass
