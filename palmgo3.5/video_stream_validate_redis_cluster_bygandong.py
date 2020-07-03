# -*- coding:utf-8 -*-
# @Time : 2020/3/11 下午12:41
# @Author: kkkkibj@163.com
# @File : video_stream_validate.py
# 视频地址验证
import argparse
import requests
import threading
import logging
from datetime import datetime
import time
import redis
import sys
from redis import ConnectionPool
from rediscluster import RedisCluster
redis_nodes = [{"host":"192.168.23.90","port":"7001","database":2},{"host":"192.168.23.82","port":"7001","database":2}]
#POOL = ConnectionPool(host='127.0.0.1', port=6379, max_connections=500, decode_responses=True)
#conn = redis.Redis(connection_pool=POOL)
conn = RedisCluster(startup_nodes=redis_nodes,decode_responses=True)
# 采用redis hashmap存储视频状态
# key= 'camera_'+cameraNum
# fields:
#   onlineStatus:0不在线 1在线 2异常;我们检查状态为1的,如果可用更新为11，不可用更新为10
#   updateTime: 更新时间
#   reason: 不可用的原因
#   mode: PRO生产 TEST测试

key_prefix = 'camera_'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
error_num = 0
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
        'getCameraStatusApi': "https://spglxtapi.jchc.cn/service/video.GetCameraStatus?user=PT1100202001110001&currPage="
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
            return str(result['code']) + ';' + result['msg'], False
    except Exception as e:
        logger.error(str(e))
        return e, False


wsf_url = "http://192.168.23.82:8060/geoserver/wfs"


# 更新WFS数据
def updateWfsStatus(cameraNum, onlineStatus):
    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="sf:toll_bd09_line_point"><wfs:Property> <wfs:Name>onlineStat</wfs:Name><wfs:Value>' + str(
        onlineStatus) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>cameraNum</ogc:PropertyName><ogc:Literal>' + cameraNum + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter></wfs:Update></wfs:Transaction>'
    r = requests.post(wsf_url, data=wfs_xml)
    # logger.info(r.text)
tmp_dic = {}


#直接根据感动的状态更新数据
def videoStreamTestRedis(mode, cameraNum,gandongstat):
    if cameraNum in tmp_dic:
        print('cameraNum 有重复的 :' + cameraNum)
    else:
        tmp_dic[cameraNum] = 1
    global error_num
    key_str = key_prefix + cameraNum
    onlineStatus = 11
    if gandongstat != "1" and gandongstat != 1:
        onlineStatus = 10
    conn.hset(key_str, 'onlineStatus', gandongstat)
    conn.hset(key_str, 'updateTime', time.time())
    conn.hset(key_str, 'reason', '')
    conn.hset(key_str, 'mode', mode)
    updateWfsStatus(cameraNum, onlineStatus)





# 从第三方厂家获取视频状态
def fetchVideoStatus(mode, page_no):
    try:
        url_with_page_no = request_param_pre[mode]['getCameraStatusApi'] + str(page_no) + "&pageSize=500"
        logging.info(url_with_page_no)
        r = requests.get(url_with_page_no, headers=request_param_pre[mode]['httpHeader'])
        result = r.json()
        logging.info(result)
        return result['total'], result['cameraStatus']
    except Exception as e:
        logging.error(str(e))
        return 0, []


def dealPageListDataRedis(status_data, mode):
    i = 0
    tmp_len = len(status_data)
    for item in status_data:
        i += 1
        if i % 10 == 0 or i == tmp_len:
            logging.info('当前条数 %s / %s' % (i, tmp_len))
        cameraNum = item['cameraNum']
        onlineStatus = item['onlineStatus']
        t = threading.Thread(target=videoStreamTestRedis, args=(mode, cameraNum, onlineStatus))
        t.start()
        thread_num = len(threading.enumerate())
        logger.info('当前线程数:' + str(thread_num))
        while thread_num > 50:
            time.sleep(1)
            thread_num = len(threading.enumerate())
            logger.info('休息1下:' + str(thread_num))



def updateVideoStatus(mode):
    cpage = 1
    logging.info('当前模式:' + mode)
    logging.info('当前进度 %s/%s' % (cpage, 'unknow'))
    total_list_num, status_data = fetchVideoStatus(mode, cpage)
    conn.set("c_" + mode + "_total", total_list_num)
    #dealPageListDataRedis(status_data, mode)
    totalpage = int(total_list_num / 500) + 1
    logging.info('视频总条数：%s' % total_list_num)
    logging.info('数据总页数（每页500条）%s' % totalpage)
    while cpage <= totalpage:
        total_list_num, status_data = fetchVideoStatus(mode, cpage)
        if total_list_num > 0:
            cpage += 1
            dealPageListDataRedis(status_data, mode)
        else:
            logging.error('获取摄像头列表失败 %s/%s' % (cpage, totalpage))
        logging.info('当前进度 %s/%s' % (cpage, totalpage))


def main(argv):
    mode = argv.mode
    # with open(argv.output_file_name, 'w+') as data_file:
    data_file = open(argv.output_file_name, 'w+')
    if mode == 'ALL':
        updateVideoStatus('TEST')
        updateVideoStatus('PRO')
    else:
        updateVideoStatus(mode)


def parse_arguments(argv):
    dt = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['TEST', 'PRO', 'ALL'],
                        help='TEST:测试地址;PRO:生产地址;ALL:全部。默认全部', default='ALL')
    parser.add_argument('--output_file_dir', type=str,
                        help='结果文件输出路径.', default='./')
    parser.add_argument('--output_file_name', type=str,
                        help='结果文件名称.', default='video_validate_result%s.txt' % dt.strftime('%Y%m%d%H%M%S'))
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
    # cm = '11949D31-4D39-47C4-9767-AD62F2DFE998'
    # updateWfsStatus(cm, 1)
    # updateVideoStatus('TEST')
    # total_list_num = conn.get("c_" + 'PRO' + "_total")
    # print(total_list_num)
    # keys = conn.scan(0, 'camera_*', 100)
    # i = 0
    # while int(keys[0]) != 0:
    #     for item in keys[1]:
    #         i += 1
    #         if i % 100 == 0:
    #             print(i)
    #         status = conn.hget(item, "onlineStatus")
    #     keys = conn.scan(keys[0], 'camera_*', 100)
    # print(i)
