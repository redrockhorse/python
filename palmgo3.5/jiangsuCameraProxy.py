# -*- coding:utf-8 -*-
#@Time : 2021/1/21 下午2:58
#@Author: kkkkibj@163.com
#@File : jiangsuCameraProxy.py
#使用python代理到江苏视频的请求

import requests
from flask import request, jsonify
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('foo.txt', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)




headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Pragma': 'no-cache'
,'AppVersion': 'v1.0'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
# 跨域支持


def getToken():
    url = "https://mvpopi.jchc.cn/oc/openapi/sign"
    r = requests.post(url, json={"appKey": "ffa590e7a435458cb8b19e502fb3bea4 ",  "secret": "a9c78152c1b54335a23d0758d3b89730"})
    token = ''
    if r.json()['code'] == 200:
        token = r.json()['data']['access_token']
    return token

@app.route('/js/oc/service/video.GetCameraUrl/', methods = ["OPTIONS",'GET','POST'])
def videoPathUri():
    videoType = request.args.get('videoType')
    cameraNum= request.args.get('cameraNum')
    cameraName = request.args.get('cameraName')
    videoRate = request.args.get('videoRate')
    url = "https://mvpopi.jchc.cn/oc/service/video.GetCameraUrl?videoType="+videoType+"&cameraNum="+cameraNum+"&cameraName="+cameraName+"&videoRate="+videoRate
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
        , 'Accept-Encoding': 'gzip, deflate'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Cache-Control': 'no-cache'
        , 'Connection': 'keep-alive'
         ,'Authorization'  :    request.headers['Authorization']
        , 'Pragma': 'no-cache'
        , 'AppVersion': 'v1.0'
        ,
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    r = requests.get(url, headers=headers)
    result = r.json()
    return jsonify(result)




if __name__ == '__main__':
    app.run(port=5000,debug=True)
