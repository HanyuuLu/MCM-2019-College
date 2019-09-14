import requests
import json
a = dict()
a['phonenumber'] = 2308947
a['password'] = 230748
with open('./headers.json', 'r') as r:
    headers = json.load(r)['headers']
    rs = dict()
    for i in headers:
        rs[i['name']] = i['value']
print(rs)
res = requests.post('http://hanyuu.top:8080/user/login', data=a, headers=rs)
print(res.status_code)
print(res.text)
