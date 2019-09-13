import requests
import json


def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


def initialize():
    headers = dict()
    data = dict()
    with open('./headers.json', 'r') as r:
        temp = json.loads(r.read())
        for i in temp['headers']:
            headers[i['name']] = i['value']
    with open('./conf.json', 'r') as r:
        data = json.loads(r.read())
    return headers, data


if __name__ == '__main__':
    headers, data = initialize()
    session = requests.Session()
    host_name = "http://www.njiairport.com/flightInformation1.aspx"
    resget = session.get(host_name, headers=headers)
    print(resget.status_code)
    with open('./get.html', 'wb') as w:
        w.write(resget.text.encode('utf8'))
    respost = session.post(host_name, headers=headers, data=data)
    print(resget.status_code)
    with open('./post.html', 'wb') as w:
        w.write(respost.text.encode('utf8'))
