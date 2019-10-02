from pyquery import PyQuery as query
import json
with open('./to.html', 'r') as r:
    rawData = r.read()
pass
doc = query(rawData)
lisRaw = list()
lisDetail = list()
row = doc('div.row')
for i in row.items():
    lisRaw.append(i.html())
    dic = dict()
    dic['计划到达时间'] = (i('li.column.w200.bold')).text()
    dic['出发地/经停点'] = (i('li.column.w150'))[0].text
    dic['航站楼'] = (i('li.column.w80')).text()
    dic['机型'] = (i('div.item.w5p p'))[-1].text.strip('\t')
    try:
        dic['实际到达时间'] = "%s %s" % ((i('div.item.w15p p'))[4].text, (
            i('div.item.w15p p'))[5].text)
    except Exception as e:
        dic['实际到达时间'] = ""
    print(dic)
    lisDetail.append(dic)
with open('./res.json', 'w') as w:
    json.dump(lisDetail, w)
