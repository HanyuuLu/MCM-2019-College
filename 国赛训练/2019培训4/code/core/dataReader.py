import xlrd
import sys


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


if __name__ == '__main__':
    data = dataReader()
    for sheet in data:
        for x in sheet:
            print(x)
