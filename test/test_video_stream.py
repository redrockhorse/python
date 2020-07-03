# -*- coding:utf-8 -*-
#@Time : 2020/2/28 下午12:59
#@Author: kkkkibj@163.com
#@File : test_video_stream.py
#测试视频流地址是否可用
import requests



headers_test = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Pragma': 'no-cache'
,'TAuth': 'bc620aa68f975fa282d07bdcdc9ec9d5'
,'AppVersion': 'v1.0'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

headers_production = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Pragma': 'no-cache'
,'TAuth': 'YjQzNmQwMDQtY2EyMi00MWMxLTk0MjYtMWYzOGE1NDg3YTQ0'
,'AppVersion': 'v1.0'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

url_test = "http://36.112.134.107:9107/service/video.GetDepartmentVideoInfo?user=PT1100202001190002&currPage="
url_produciton = url = "https://spglxtapi.jchc.cn/service/video.GetDepartmentVideoInfo?user=PT1100202001110001&currPage="

url_get_flv_url_test = "http://36.112.134.107:9107/service/video.GetCameraPlayURL"
url_get_flv_url_production = "https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL"

user_pro = 'PT1100202001110001'
user_test = 'PT1100202001190002'

def getCmarelist(url=url_produciton, headers=headers_production,cpage=1):
    urlWithPageNo = url +str(cpage)+"&pageSize=500";
    r = requests.get(urlWithPageNo, headers=headers)
    result = r.json()
    return result['total'],result['videoInfo']

def videoStreamTest(streamUrl):
    flag = True
    try:
        r = requests.get(streamUrl, stream=True)
        # print(r.status_code)
        if r.status_code != 200:
            flag = False
        i = 0
        for chunk in r.iter_content(chunk_size=512):
            i = i + 1
            if i>3:
                break
        if i<2:
            flag = False
        return flag, r.status_code
    except:
        flag = False
        return flag,'ECONNRESET'

def getFlvUrl(url,cameraNum,cameraName,headers,user):
    params = {
        'user': user,
        'videotype': 0, # 0:低码流;1: 高码流
        'cameraNum':cameraNum,
        'cameraName':cameraName,
        # department: "20000320000"
    }
    r = requests.get(url,params=params,headers=headers)

    result = r.json()
    #print(result)
    if result['code'] == 200:
        return result['videoRequestUrl']['flv_url'], True
    else:
        print(result)
        return str(result['code'])+';'+result['message'], False

if __name__ == '__main__':
    ccount, tmplist = getCmarelist(url_produciton,headers_production, 1)
    #print(tmplist)
    for item in tmplist:
        # print(item['cameraNum'])
        # print(item['cameraName'])
        cameraNum = item['cameraNum']
        cameraName = item['cameraName']
        flv_url,getUrlFlag = getFlvUrl(url_get_flv_url_production,cameraNum,cameraName,headers_production,user_pro)
        if getUrlFlag == False:
            print(cameraNum + ',' + cameraName + ',' + 'get stream url failed,code and message:' + str(httpstate))
            continue
        flag,httpstate = videoStreamTest(flv_url)
        if flag == False:
            print(cameraNum+','+cameraName+','+'video stream is not available,httpstatus:'+str(httpstate))
    page = int(ccount / 500) + 1