import xlrd
import sys
import datetime

def dataConverter(src: list)->list:
    res = list()
    res.append(int(src[0]))
    res.append(src[1])
    for i in range(2, 7):
        if src[i] != '/':
            res.append(xlrd.xldate_as_datetime(src[i], 0))
        else:
            res.append(None)
    return res


def dataReader():
    fileName = None
    try:
        fileName = sys.argv[-1]
        print('[fileName]%s' % fileName)
    except:
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
                if temp[0] == '序号':
                    continue
                data[i].append(dataConverter(temp))
    except:
        print('bad data file')
    # for i in data:
    #     for x in i:
    #         print(x)
    print('[data fetched successfully]')
    return data


if __name__ == '__main__':
    dataReader()
