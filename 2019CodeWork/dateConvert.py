# Excel日期类型转换函数
# Excel 日期浮点数
# 时间起点 1900/01/00 00:00:00
# 单位1=1day
# Python time时间浮点数
# 时间起点 1970/01/01 08:00:00
# 单位1=1second
from datetime import datetime
from xlrd import xldate_as_tuple as conv


def getDateTime(date: float, **exception: bool) -> datetime.date:
    try:
        res = conv(float(date), 0)
        return datetime(res[0], res[1], res[2], res[3], res[4], res[5])
    except Exception:
        if exception:
            raise Exception("invaild date input")
        else:
            return None


if __name__ == '__main__':
        print(getDateTime(42773.41667))
