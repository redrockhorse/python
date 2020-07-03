import json
import requests
import math
headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Host': 'testqxsj.txffp.com'
,'Origin': 'http://127.0.0.1:2500'
,'Pragma': 'no-cache'
,'Referer': 'http://127.0.0.1:2500/layerdata/collectPage?tbfid=79b22d4324614ce5a9f44ab570d7a1f2'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


with open('/Users/hongyanma/Desktop/q202001091200.json','r') as f1,open('/Users/hongyanma/Desktop/20200109.txt','r') as f2:
    jdata = json.load(f1)
    data = jdata['data']
    jdic =[]
    n = 0
    for i in range(len(data)):
        if data[i]['jamMaxlen'] >= 500:
            # jdic[data[i]['key']]=1
            jdic.append(data[i]['key'])
            n=n+1
    print(n)

    fdic = []
    line = f2.readline()
    while line:
        linearr = line.split(',')
        fdic.append(linearr[1])
        line = f2.readline()

    b = set(fdic)
    a = set(jdic)
    print(b - a)

