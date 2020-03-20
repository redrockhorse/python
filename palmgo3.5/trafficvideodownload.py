# -*- coding:utf-8 -*-
#@Time : 2020/1/20 上午8:27
#@Author: kkkkibj@163.com
#@File : trafficvideodownload.py

import sys
import you_get
import requests
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
,'Accept-Encoding': 'gzip, deflate, br'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Cookie': 'acw_tc=2f624a5d15795264267093767e0ec1eebcc28ef0a7105ba80ddc9a54412e6f'
,'Host': 'spglxtapi.jchc.cn'
,'Pragma': 'no-cache'
,'Sec-Fetch-Mode': 'navigate'
,'Sec-Fetch-Site': 'none'
,'Sec-Fetch-User': '?1'
,'Upgrade-Insecure-Requests': 1
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def getFlvUrl(cameraNum,cameraName):
    url = "https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL";
    # https: // spglxtapi.jchc.cn / service / video.GetCameraPlayURL?user = PT1100202001110001 & videotype = 0 & cameraNum = sxjgl_shhungs_310000011011001001416 & cameraName = % E6 % B1 % BD % E8 % BD % A6 % E5 % 9F % 8E % E7 % AB % 8B % E4 % BA % A4 & _ = 1579521074466
    params = {
        'user': 'PT1100202001110001',
        'videotype': 1, # 0:低码流;1: 高码流
        'cameraNum':cameraNum,
        'cameraName':cameraName,
    # department: "20000320000"
    }
    #print(params)
    r = requests.get(url,params=params,headers=headers)
    #print(r)
    #print(r.url)
    result = r.json()
    print(result)
    return result['videoRequestUrl']['flv_url']
    #print(result)

def download(url, path):
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()


def dowloadVideo(cameraNum,cameraName,dir):
    flvurl = getFlvUrl(cameraNum, cameraName)
    print(flvurl)
    with open(dir+'/'+cameraNum+'.flv', 'wb+') as f:
        r = requests.get(flvurl,stream=True)
        print(r.status_code)
        i = 0
        for chunk in r.iter_content(chunk_size=512):
            if chunk and i < 30000:#1000*512大约2分05秒长度
                f.write(chunk)
                i = i+1
                if i % 500 == 0:
                    print(i)
            else:
                print('download complate!')
                break

if __name__ == '__main__':
    # 视频网站的地址
    #url = 'https://www.bilibili.com/bangumi/play/ep118488?from=search&seid=5050973611974373611'
    # 视频输出的位置
    # path = '/Users/hongyanma/Downloads/trafficvideo/test.flv'
    # download(url, path)
    #https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001&videotype=0&cameraNum=sxjgl_nhugs_320500011011001001028&cameraName=AK1147%2B800(N)%E4%B8%80&_=1580874301046
    #https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001&videotype=0&cameraNum=sxjgl_gjxcgs_320206011101001015007&cameraName=S19%E5%8D%97%E7%A1%95K141-260&_=1580874301054
    #http://36.112.134.107:9107/service/video.GetCameraPlayURL?user=PT1100202001190002&videotype=0&cameraNum=628358c0b50c422fa18b09166ba635b6&cameraName=G1(%E4%BA%AC%E5%93%88%E9%AB%98%E9%80%9F)%E5%A4%A9%E6%B4%A5%E6%AE%B5%E5%A4%A9%E6%98%82%E5%85%AC%E5%8F%B8K77%2B600&_=1580874869596
    #https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001&videotype=0&cameraNum=03c59a0a-055c-468a-86a3-08d2d9585b0a&cameraName=G4%E4%BA%AC%E7%9F%B3K171%2B790%E4%B8%8A%E8%A1%8C%E7%AC%AC271%E5%8F%B7&_=1580874869620
    #https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001&videotype=0&cameraNum=d96e4e0a-7eb4-4bef-99fc-1422c21ddbc8&cameraName=G4%E4%BA%AC%E7%9F%B3K261%2B155&_=1580874869648
    #https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001&videotype=0&cameraNum=sxjgl_nhugs_320500011011001001063&cameraName=AK1189%2B050(N)%E9%AB%98%E8%81%9A&_=1580974059648
    # flvurl = getFlvUrl('sxjgl_lxgs_320300011050204007475', 'G30_K189%2B180东行枪机HD')
    # print(flvurl)
    #download(flvurl, path)
    # with open('/Users/hongyanma/Desktop/downloadvide.flv', 'wb+') as f:
    #     r = requests.get(flvurl,stream=True)
    #     i = 0
    #     for chunk in r.iter_content(chunk_size=512):
    #         if chunk and i<1000:
    #             #print(chunk)
    #             f.write(chunk)
    #             i = i+1
    #             if i%100==0:
    #                 print(i)
    #         else:
    #             print('download complate!')
    #             break
    dir = '/Users/hongyanma/Downloads/trafficvideo'
    # dowloadVideo('d96e4e0a-7eb4-4bef-99fc-1422c21ddbc8', 'G4%E4%BA%AC%E7%9F%B3K261%2B155', dir)
    # dowloadVideo('03c59a0a-055c-468a-86a3-08d2d9585b0a', 'G4%E4%BA%AC%E7%9F%B3K171%2B790%E4%B8%8A%E8%A1%8C%E7%AC%AC271%E5%8F%B7', dir)
    # dowloadVideo('sxjgl_nhugs_320500011011001001028', 'AK1147%2B800(N)%E4%B8%80', dir)
    # dowloadVideo('sxjgl_gjxcgs_320206011101001015007','S19%E5%8D%97%E7%A1%95K141-260', dir)
    # dowloadVideo('4dc4ccfa-5447-4963-b7ee-a12873b401ba', 'G4(京港澳高速)河南高速公路发展有限责任公司安新K580%2B029', dir)
    dowloadVideo('0962fc52-a5af-4900-bb93-c9485ab0b353', 'CCTV37', dir)