# -*- coding: utf8 -*-
# !/usr/bin/python
# 北京json数据抓取.python 版本2.5
__author__ = 'mahy'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
id_dic = {}#存储已存在的事件id

#将字符串转换为json对象
def parseJson2Object(str):
    return json.loads(str)

#解析json对象，将content字段写入文件
def writeFile(jsonObj,wfilename):
    wf = open(wfilename,'a')
    if jsonObj['status'] == 200:
            for data in jsonObj['data']:
                    wline = data['content']
                    #判断事件的id是否重复
                    if data['id'] not in id_dic:
                            wf.write(wline+'\n')
                            id_dic[data['id']]=1
    wf.close()


import glob
#第一种方式，从已下载的文件列表读入交通事件
def readFromFile(input_path,output_file):
    for filename in sorted(glob.glob(input_path+'/'+'2017*.txt')):
        f=open(filename)
        for line in f:
            obj = parseJson2Object(line)
            writeFile(obj,output_file)
        f.close()

#第二种方式，直接从http接口读取，算了，暂时不实现了
'''
def readFromHttp():
    @todo
'''
if __name__ == '__main__':
   readFromFile('/usr/local/nginx/html/bjte','/usr/local/nginx/html/bjte/content.txt')