import os
import sys
import numpy
import dataType
import h5py
import threading
import time
import xlrd
import csv


class Saving(threading.Thread):
    def __init__(self, name, fileName):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.fileName = fileName

    def run(self):
        print("[thread %s]%s" % (self.name, self.fileName))
        with xlrd.open_workbook(self.fileName) as workBook:
            print("[info] work book %s start to read" % self.fileName)
            table = workBook.sheets()[0]
            print("[info] file %s import finished!" % self.fileName)
            # res = numpy.zeros((table.nrows, table.ncols))
            res = []
            for i in range(table.nrows):
                # res[i:] = table.row_values(i)
                res.append(table.row_values(i))
            # outputFile = h5py.File(self.fileName, 'w')
            # output = outputFile.create_dataset(self.fileName, data = res)
        with open(self.name + ".csv", 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerows(res)
            # output.write(res)
        with open(self.name + ".csv", "r") as input:
            reader = csv.reader(input)
            for line in reader:
                print(line)


def dataReader():
    ROOT = "./data"
    threadingList = []
    for currentDict, subDict, fileName in os.walk(ROOT):
        for i in fileName:
            thread = Saving(i, os.path.join(currentDict, i))
            thread.start()
            threadingList.append(thread)
    for i in threadingList:
        i.join()


if __name__ == '__main__':
    dataReader()
