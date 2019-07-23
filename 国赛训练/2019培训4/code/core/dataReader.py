import xlrd
import sys
from core.timeWithoutDate import TimeWithOutDate
# from timeWithoutDate import TimeWithOutDate


def dataConverter(src: list)->list:
    res = list()
    res.append(src[0])
    for i in range(1, 4):
        res.append(src[i])
    res.append(int(src[4]))
    return res


def dataReader():
    fileName = None
    try:
        fileName = sys.argv[-1]
        print('[fileName]%s' % fileName)
    except Exception:
        print('no file name')
    data = list()
    try:
        workbook = xlrd.open_workbook(filename=fileName)
        for i in range(workbook.nsheets):
            data.append(list())
            rangeRow = workbook.sheet_by_index(i).nrows
            sheet = workbook.sheet_by_index(i)
            for x in range(rangeRow):
                temp = sheet.row_values(x)
                if temp[0] == '任务号码':
                    continue
                data[i].append(dataConverter(temp))
    except Exception as e:
        print('bad data file')
        print('\t[Exception]\t%s' % str(e))
        exit()
    # for i in data:
    #     for x in i:
    #         print(x)
    print('😀[info]\tdata fetched successfully')
    return data


def dataReader2():
    fileName = None
    try:
        fileName = sys.argv[-1]
        print('[fileName]%s' % fileName)
    except Exception:
        print('no file name')
    data = list()
    try:
        workbook = xlrd.open_workbook(filename=fileName)
        for sheet in workbook.sheets():
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                raw = sheet.row_values(i)
                proc = list()
                proc.append(raw[0])
                proc.append([float(x) for x in str.split(raw[1])])
                proc.append(int(raw[2]))
                proc.append(TimeWithOutDate(seconds=float(raw[3]) * 86400))
                proc.append(float(raw[4]))
                data.append(proc)
    except Exception as e:
        print('bad data file')
        print('\t[Exception]\t%s' % str(e))
        exit()
    # for i in data:
    #     for x in i:
    #         print(x)
    print('😀[info]\tdata fetched successfully')
    return data
