import requests
import time
import json
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Content-Type": "application/x-www-form-urlencoded;charset = UTF-8"
}
params = {"depOrArr": "1", "type": "1", "day": "0", "terminal": "ALL"}
params_more = {"depOrArr": "1", "type": "1", "day": "-1", "terminal": "ALL",
          "flightNo": "CZ8493", "dataTime": "2019-09-11+02:40"}
host = "http://www.baiyunairport.com/byairport-web/flight/list"
host_more = "http://www.baiyunairport.com/byairport-web/flight/loadMore"
with open('./cookie.json', 'r') as r:
    cook = json.load(r)
    cookies = requests.cookies.RequestsCookieJar()
    for i in cook:
        cookies.set(i, cook[i])
cookies = {
    "Hm_lpvt_0effb2f651854e064f7d24a159e08bd5": "1568354733",
    "Hm_lpvt_783519365e6df848bd882229527a15bc": "1568354733",
    "Hm_lvt_0effb2f651854e064f7d24a159e08bd5": "1568354733",
    "Hm_lvt_783519365e6df848bd882229527a15bc": "1568354733",
    "JSESSIONID": "5DD5847A275C3FD07224EF5193622DAE"
}


def save(no: int, text: str)-> None:
    with open('%d.html' % (no), 'wb') as w:
        w.write(text.encode('utf8'))


if __name__ == '__main__':
    count = 0
    session = requests.Session()
    session.cookies.setdefault(
        "JSESSIONID", "5DD5847A275C3FD07224EF5193622DAE")
    res = session.get(host, params=params)
    save(count, res.text)
    count += 1
    print(res.status_code)
    time.sleep(1)
    res = session.post(host_more, data=params_more, cookies=cookies,headers = headers)
    print(res.status_code)
    save(count, res.text)
