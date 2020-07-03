# -*- coding:utf-8 -*-
#@Time : 2020/1/17 下午5:28
#@Author: kkkkibj@163.com
#@File : camareInfoList.py

import json
import requests
import time

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
# ,'Host': 'testqxsj.txffp.com'
# ,'Origin': 'http://127.0.0.1:2500'
,'Pragma': 'no-cache'
#,'TAuth': 'YjQzNmQwMDQtY2EyMi00MWMxLTk0MjYtMWYzOGE1NDg3YTQ0'
,'TAuth': 'bc620aa68f975fa282d07bdcdc9ec9d5'
,'AppVersion': 'v1.0'
# ,'Referer': 'http://127.0.0.1:2500/layerdata/collectPage?tbfid=79b22d4324614ce5a9f44ab570d7a1f2'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
import numpy as np

def getCmarelist(cpage=1,clist =[]):
    # url = "https://spglxtapi.jchc.cn/service/video.GetDepartmentVideoInfo?user=PT1100202001110001&currPage="+str(cpage)+"&pageSize=500";
    url = "http://36.112.134.107:9107/service/video.GetDepartmentVideoInfo?user=PT1100202001190002&currPage=" + str(cpage) + "&pageSize=500";
    print(url)
    r = requests.get(url, headers=headers)
    result = r.json()

    while result['code'] != 200:
        r = requests.get(url, headers=headers)
        result = r.json()


    return result['total'],result['videoInfo']



if __name__ == '__main__':
    videolist = []
    ccount,tmplist = getCmarelist(1,videolist)
    videolist = tmplist
    page = int(ccount/500)+1
    #print(page)
    for i in range(2,page+1):
        # time.sleep(3)
        print(i)
        ccount, tmplist = getCmarelist(i, videolist)
        a = np.array(videolist)
        b = np.array(tmplist)
        a_list = list(a)
        b_list = list(b)
        a_list.extend(b_list)
        videolist = a_list

    print(len(videolist))
    # with open('/Users/hongyanma/Desktop/videolist'+str(ccount)+'.json','w') as f:
    #     json.dump(videolist,f,ensure_ascii=False),
    with open('/Users/hongyanma/Desktop/videolisttest'+str(ccount)+'.json','w') as f:
        json.dump(videolist,f,ensure_ascii=False),
