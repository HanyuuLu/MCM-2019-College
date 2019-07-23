# vip map
# 会员地理分布信息
import sys
sys.path.append('.\\')
from core.dataReader import dataReader2
if __name__ == '__main__':
    data = dataReader2()
    print(data)