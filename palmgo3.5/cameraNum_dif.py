# -*- coding:utf-8 -*-
# @Time : 2020/3/19 上午10:24
# @Author: kkkkibj@163.com
# @File : cameraNum_dif.py

import requests
import json

# 前置查询条件
request_param_pre = {
    'TEST': {
        'httpHeader': {'Accept': 'application/json, text/javascript, */*; q=0.01'
            , 'Accept-Encoding': 'gzip, deflate'
            , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            , 'Cache-Control': 'no-cache'
            , 'Connection': 'keep-alive'
            , 'Pragma': 'no-cache'
            , 'TAuth': 'bc620aa68f975fa282d07bdcdc9ec9d5'
            , 'AppVersion': 'v1.0'
            ,
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                       },

        'cameraListApi': "http://36.112.134.107:9107/service/video.GetDepartmentVideoInfo?user=PT1100202001190002&currPage=",
        'videoStreamApi': "http://36.112.134.107:9107/service/video.GetCameraPlayURL?user=PT1100202001190002",
        'getCameraStatusApi': "http://36.112.134.107:9107/service/video.GetCameraStatus?user=PT1100202001190002&currPage="
    },
    'PRO': {
        'httpHeader': {'Accept': 'application/json, text/javascript, */*; q=0.01'
            , 'Accept-Encoding': 'gzip, deflate'
            , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            , 'Cache-Control': 'no-cache'
            , 'Connection': 'keep-alive'
            , 'Pragma': 'no-cache'
            , 'TAuth': 'YjQzNmQwMDQtY2EyMi00MWMxLTk0MjYtMWYzOGE1NDg3YTQ0'
            , 'AppVersion': 'v1.0'
            ,
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                       },

        'cameraListApi': "https://spglxtapi.jchc.cn/service/video.GetDepartmentVideoInfo?user=PT1100202001110001&currPage=",
        'videoStreamApi': "https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001",
        'getCameraStatusApi': "https://spglxtapi.jchc.cn/service/video.GetCameraStatus?user=PT1100202001190002&currPage="
    }

}


# 获取视频流地址
def getVideoStreamUrl(mode, cameraNum, cameraName):
    params = {
        'videotype': 0,  # 0:低码流;1: 高码流
        'cameraNum': cameraNum,
        'cameraName': cameraName,
    }
    try:
        r = requests.get(request_param_pre[mode]['videoStreamApi'], params=params,
                         headers=request_param_pre[mode]['httpHeader'], timeout=45)

        result = r.json()
        if result['code'] == 200:
            return result['videoRequestUrl']['flv_url'], True
        else:
            print(str(result['code']) + ';' + result['msg'])
            return str(result['code']) + ';' + result['msg'], False
    except Exception as e:
        print(str(e))
        return e, False


# wsf_url = "http://hmrc.palmgo.cn/geoserver/wfs"
wsf_url = "http://192.168.23.82:8060/geoserver/wfs"


# 更新WFS数据
def updateWfsStatus(cameraNum, onlineStatus):
    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="sf:toll_bd09_line_point"><wfs:Property> <wfs:Name>onlineStat</wfs:Name><wfs:Value>' + str(
        onlineStatus) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>cameraNum</ogc:PropertyName><ogc:Literal>' + cameraNum + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter></wfs:Update></wfs:Transaction>'
    r = requests.post(wsf_url, data=wfs_xml)
    # logger.info(r.text)


if __name__ == '__main__':
    wfs_full_data = 'http://192.168.23.82:8060/geoserver/sf/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sf:toll_bd09_line_point&maxFeatures=25000&outputFormat=application%2Fjson&bbox=30.00941270901087,10.69485909762269,150.41800606835588,69.65606727035105,EPSG:4326&_=1584580305916'
    # wfs_full_data = 'http://hmrc.palmgo.cn/geoserver/sf/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sf:toll_bd09_line_point&maxFeatures=25000&outputFormat=application%2Fjson&bbox=30.00941270901087,10.69485909762269,150.41800606835588,69.65606727035105,EPSG:4326&_=1584580305916'

    r = requests.get(wfs_full_data)
    jdata = r.json()
    # jobj = json.loads(jdata)
    features = jdata['features']
    i = 0
    t = 0
    for ft in features:
        t += 1
        onlineStat = ft['properties']['onlineStat']
        cameraNum = ft['properties']['cameraNum']
        msg, flag = getVideoStreamUrl(mode, cameraNum, '')
        if int(onlineStat) == 11:
            i += 1
            online = ft['properties']['online']
            mode = 'PRO'
            if int(online) == 0:
                mode = 'TEST'
            if flag is False:
                # print(cameraNum)
                updateWfsStatus(cameraNum, 0)
        if int(onlineStat) != 11:  # 上线
            if flag is True:
                updateWfsStatus(cameraNum, 11)

    print(i)
    print(t)
