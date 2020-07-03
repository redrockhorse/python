# -*- coding:utf-8 -*-
# @Time : 2020/3/11 下午12:41
# @Author: kkkkibj@163.com
# @File : video_stream_validate.py
# 视频地址验证
import argparse
import requests
import sys
import threading
import logging
from datetime import datetime

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
        'videoStreamApi': "http://36.112.134.107:9107/service/video.GetCameraPlayURL?user=PT1100202001190002"
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
        'videoStreamApi': "https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL?user=PT1100202001110001"
    }

}


# 获取摄像头列表数据
def getCmarelist():
    try:
        # url_with_page_no = request_param_pre[mode]['cameraListApi'] + str(page_no) + "&pageSize=500"
        r = requests.get('http://hmrc.palmgo.cn/geoserver/sf/ows?service=WFS&version=1.0.0&request=GetFeature&MAXFEATURES=500000&typeName=sf:toll_bd09_line_point&CQL_FILTER=onlinestat%20=%2011&outputFormat=application%2Fjson')
        result = r.json()
        # print(url_with_page_no)
        print(result['totalFeatures'])
        return result['totalFeatures'], result['features']
    except:
        return 0, []


# 获取视频流地址
def getVideoStreamUrl(mode, cameraNum, cameraName):
    params = {
        'videotype': 0,  # 0:低码流;1: 高码流
        'cameraNum': cameraNum,
        'cameraName': cameraName,
    }
    try:
        r = requests.get(request_param_pre[mode]['videoStreamApi'], params=params,
                         headers=request_param_pre[mode]['httpHeader'])

        result = r.json()
        if result['code'] == 200:
            return result['videoRequestUrl']['flv_url'], True
        else:
            return str(result['code']) + ';' + result['msg'], False
    except Exception as e:
        return e, False


def videoStreamTest(mode, cameraNum, cameraName, data_file):
    global error_num
    flag = True
    message = ''
    flv_url, getUrlFlag = getVideoStreamUrl(mode, cameraNum, cameraName)
    if getUrlFlag == False:
        # logging.info(cameraNum + ',' + cameraName + ',' + 'get stream url failed,code and message:' + str(flv_url))
        message = mode + ',' + cameraNum + ',' + cameraName + ',' + 'get stream url failed,code and message:' + str(
            flv_url)
        logging.info(message)
        data_file.writelines('%s\n' % message)
        error_num += 1
        return flag, message
    try:
        r = requests.get(flv_url, stream=True)
        if r.status_code != 200:
            flag = False
            message = mode + ',' + cameraNum + ',' + cameraName + ',' + 'video stream is not available,httpstatus:' + str(
                r.status_code)
            # logging.info(flv_url)
            logging.info(message)
            data_file.writelines('%s\n' % message)
            error_num += 1
            return flag, message
        i = 0
        for chunk in r.iter_content(chunk_size=512):
            i = i + 1
            if i > 3:
                break
        if i < 2:
            flag = False
            message = mode + ',' + cameraNum + ',' + cameraName + ',' + 'video stream is not available,httpstatus:can\'t download video stream data'
            logging.info(message)
            data_file.writelines('%s\n' % message)
        else:
            flag = True
            message = mode + ',' + cameraNum + ',' + cameraName + ',' + 'success,success'
            logging.info(message)
            data_file.writelines('%s\n' % message)
        return flag, message
    except Exception as e:
        flag = False
        if cameraName is None:
            cameraName = ''
        message = mode + ',' + cameraNum + ',' + cameraName + ',' + 'video stream is not available,httpstatus:' + str(e)
        logging.info(message)
        data_file.writelines('%s\n' % message)
        error_num += 1
        return flag, message


def dealPageListData(mode, cpage, data_file):
    logging.info('当前页码 %s' % cpage)
    total_list_num, tmplist = getCmarelist(mode, cpage)
    if total_list_num > 0:
        tmp_len = len(tmplist)
        i = 0
        for item in tmplist:
            i += 1
            if i % 10 == 0 or i == tmp_len:
                logging.info('当前条数 %s / %s' % (i, tmp_len))
            cameraNum = item['cameraNum']
            cameraName = item['cameraName'].replace('\r', '').replace('\n', '')
            # videoStreamTest(mode, cameraNum, cameraName)
            t = threading.Thread(target=videoStreamTest, args=(mode, cameraNum, cameraName, data_file,))
            t.start()
    return total_list_num


def doValidate(mode, data_file):
    cpage = 1
    logging.info('当前模式:' + mode)
    logging.info('当前进度 %s/%s' % (cpage, 'unknow'))
    total_list_num = dealPageListData(mode, cpage, data_file)
    totalpage = int(total_list_num / 500) + 1
    logging.info('视频总条数：%s' % total_list_num)
    logging.info('数据总页数（每页500条）%s' % totalpage)
    while cpage < totalpage:
        total_list_num = dealPageListData(mode, cpage, data_file)
        if total_list_num > 0:
            cpage += 1
        else:
            logging.error('获取摄像头列表失败 %s/%s' % (cpage, totalpage))
        logging.info('当前进度 %s/%s' % (cpage, totalpage))


def main(argv):
    # mode = argv.mode
    data_file = open(argv.output_file_name, 'w+')
    # if mode == 'ALL':
    #     doValidate('TEST', data_file)
    #     doValidate('PRO', data_file)
    # else:
    #     doValidate(mode, data_file)
    totalFeatures,features = getCmarelist()
    for item in features:
        # print(item)
        mode = 'PRO'
        cameraNum = item['properties']['cameranum']
        cameraName = item['properties']['cameraname']
        if int(item['properties']['online']) == 0:
            mode = 'TEST'
        else:
            mode = 'PRO'
            print('onlinename:'+cameraName)

        # videoStreamTest(mode, cameraNum, cameraName, data_file)
        t = threading.Thread(target=videoStreamTest, args=(mode, cameraNum, cameraName, data_file,))
        t.start()


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
