import xlrd
import os
DIR = r'.\code'
FILE_LIST = \
    [
        'data (1).xls',
        'data (2).xlsx',
        'data (3).xlsx'
    ]


def fetchData(no: int) -> map:
    assert no >= 0 and no < len(FILE_LIST), "[ERROR] × 无效数据编号"
    fileName = os.path.join(DIR, FILE_LIST[no])
    print("▶[info] reading %s" % fileName)
    try:
        resData = dict()
        # workbook = xlrd.open_workbook(fileName)
        with xlrd.open_workbook(fileName) as workbook:
            sheetNames = workbook.sheet_names()
            for sheetName in sheetNames:
                sheet = workbook.sheet_by_name(sheetName)
                resData[sheetName] = list()
                for i in range(sheet.nrows):
                    rawRow = rawConverterList[no](sheet.row(i))
                    if rawRow is not None:
                        resData[sheetName].append(rawRow)
        print("√[info] read %s finished." % fileName)
        return resData
    except Exception as e:
        print('×[ERROR] when reading %s \n %s' % (fileName, str(e)))


def rawConverter_1(src: list):
    if src is not None and src[0].value is not None and isinstance(src[0].value, (int, float, str)):
        try:
            if float(src[0].value):
                return [i.value for i in src]
            return src
        except Exception:
            return None
    else:
        return None


def rawConverter_2(src: list):
    if src is not None and src[0].value is not None and isinstance(src[0].value, (int, float, str)):
        try:
            if src[0].value != None and src[0].value != "代码" and src[0].value != '':
                return [i.value for i in src]
        except Exception:
            return None
    else:
        return None


rawConverterList = (rawConverter_1, rawConverter_2)

if __name__ == '__main__':
    res = fetchData(0)
    res2 = fetchData(1)
    pass
