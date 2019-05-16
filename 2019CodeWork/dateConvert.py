# Excel日期类型转换函数
import datetime
__s_date = datetime.date(1899, 12, 31).toordinal()- 1
def getdate(date:float)->datetime.date:
        assert isinstance(date, float),"非浮点时间戳，输入了%s"%str(type(date))
        intDate = int(date)
        result = datetime.date.fromordinal(__s_date + intDate)
        return result
if __name__ == '__main__':
    print(getdate(42773.7131944444))
