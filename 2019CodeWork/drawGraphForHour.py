import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def draw(data: list) -> None:
    # 中文和负号显示
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    # 绘制直方图
    xLabel = []
    for i in range(25):
        xLabel.append(str(i))
    xLabel[24] = "未知"
    # plt.hist(data, bins=40, normed=0, facecolor='blue', edgecolor='black', alpha=0.7)
    plt.xlabel("小时")
    plt.ylabel("日均出行数/人次")
    plt.title("日均出行人次数小时分布图")

    rects1 = plt.bar(x=xLabel, height=data, width=0.4,
                     alpha=0.8, color='blue', label="一部门")
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height +
                 1, str(height), ha="center", va="bottom")

    plt.show()


if __name__ == '__main__':

    # data = [2448, 638, 30, 2, 188, 898, 13733, 49587, 74256, 65315, 62844, 57405, 53875,
    #         62657, 66388, 62372, 67779, 79149, 65417, 46006, 46459, 43085, 23213, 5381, 99450]
    draw(data)
