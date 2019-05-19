def draw():
    from matplotlib import pyplot as plt
    # %matplotlib inline
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = '移动支付', '非移动支付'
    explode = (0, 0.1)
    fig = []
    j = 0
    for i in Monthly:
        fig.append(plt.subplot(2, 2, j+1))
        plt.pie(
            [Monthly[i]['mobilePay'], Monthly[i]['notMobilePay']],
            labels=labels,
            explode=explode,
            autopct='%1.2f%%',
            shadow=True,
            startangle=90,
            textprops={'size': 'large'}
        )
        fig[-1].set_title(i)
        j += 1
    plt.show()
