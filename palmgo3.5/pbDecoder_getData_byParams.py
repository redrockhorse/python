# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder_getData_byParams.py
# 解析pb gps文件,为展厅解析数据

import zipfile
import json
import os
import GPS_pb2
import coordinateSystemTransform
# import threading
import struct
import argparse
import sys
import multiprocessing
import glob

def pdZipFileDeCode(zipFilePath):
    print('start handle :'+zipFilePath)
    azip = zipfile.ZipFile(zipFilePath)
    a = azip.read(azip.namelist()[0])
    gpsmap = GPS_pb2.GpsMap()
    gpsmap.ParseFromString(a)
    hourData = {}
    result = []
    for provinceCode in gpsmap.gpsinfo:
        gpsSourceMap = gpsmap.gpsinfo[provinceCode].source
        for source in gpsSourceMap:
            gpsList = gpsSourceMap[source].gps
            for gpsSequence in gpsList:
                length = struct.unpack('<h', gpsSequence[:2])[0]

                if length + 2 != len(gpsSequence):
                    print("接收数据不完整，丢弃 gps=")
                    break
                # car_identity = struct.unpack('<Q', gpsSequence[2:10])[0]
                # if car_identity not in result:
                #     result[car_identity] = []

                # state = struct.unpack('<?', gpsSequence[10:11])[0]
                # count = struct.unpack('<b', gpsSequence[11:12])[0]

                X = struct.unpack('<l', gpsSequence[12:16])[0]

                firstX = X / 1000000.0

                Y = struct.unpack('<l', gpsSequence[16:20])[0]

                firstY = Y / 1000000.0

                # dateTimeUTC = struct.unpack('<L', gpsSequence[20:24])[0]
                #
                # speed = struct.unpack('<B', gpsSequence[24:25])[0]
                #
                # direction = struct.unpack('<h', gpsSequence[25:27])[0]
                # i = 1
                # sequencetIndex = 27
                bd_coord = coordinateSystemTransform.wgs84_to_gcj02(firstX, firstY)
                # bd_coord = [firstX, firstY]

                lng = '%.6f' % bd_coord[0]
                lat = '%.6f' % bd_coord[1]
                # grid_x = int(float(lng) / grid_width)
                # grid_y = int(float(lat) / grid_heigth)
                # grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
                if lng + '_' + lat not in hourData:
                    hourData[lng + '_' + lat] = 0
                    result.append([float(lng),float(lat)])
    return result


def saveAsRawGps(zipFilePath, output_file_dir):
    result = pdZipFileDeCode(zipFilePath)
    datajson ={}
    datajson["data"] = result
    with open(output_file_dir+'/' + zipFilePath.replace('/','_').replace('.zip','.json'),'w') as outFile:
        json.dump(datajson,outFile)
    print('Finish decoder:' + zipFilePath)



def getPbZipFiles(pb_file_dir):
    fileList = []
    # for parent, dirnames, filenames in os.walk(pb_file_dir):
    #     for filename in filenames:
    #         filePath = parent + '/' + filename
    #         fileList.append(filePath)
    for filePath in glob.glob(pb_file_dir):
        fileList.append(filePath)
    return fileList

def combination_data_by_hour(json_data_path, output_file_dir):
    for filePath in glob.glob(json_data_path):
        patharr = filePath.split('/')
        json_file_name = patharr[-1]
        arr = json_file_name.split('_')
        pcode = arr[4]
        timeId = int(arr[7].replace('.json',''))
        hour = int(timeId / 12)
        with open(filePath,'r') as tfile:
            hdata = {}
            tdata = json.load(tfile)
            out_file_path = output_file_dir+'/ph_'+str(pcode)+'_'+str(hour)+'.json'
            if os.path.exists(out_file_path):
                with open(out_file_path,'r') as ofile:
                    hdata = json.load(ofile)
                    hdata['data'] += tdata['data']
                    hdata['data'] = list(set([tuple(t) for t in hdata['data']]))
            else:
                hdata = tdata
            with open(out_file_path, 'w') as ofile:
                json.dump(hdata, ofile)



def main(argv):
    # mode = argv.mode
    pool = multiprocessing.Pool(processes=4)
    pb_file_dir = argv.pb_file_dir
    output_file_dir = argv.output_file_dir
    zipFiles = getPbZipFiles(pb_file_dir)
    print(zipFiles)
    for zipFilePath in zipFiles:
        # t = threading.Thread(target=saveAsRawGps, args=(zipFilePath, output_file_dir))
        t = pool.apply_async(saveAsRawGps, (zipFilePath, output_file_dir))
    pool.close()
    pool.join()



def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['GRID','HEAT', 'ALL'],
                        help='GRID:抽稀后的数据;HEAT:热力图数据;ALL:全部点位数据。默认ALL', default='ALL')
    parser.add_argument('--grid_width', type=str,
                        help='网格宽度', default='0.00003')
    parser.add_argument('--grid_height', type=str,
                        help='网格高度', default='0.00003')
    parser.add_argument('--output_file_dir', type=str,
                        help='结果文件输出路径.', default='./')
    parser.add_argument('--pb_file_dir', type=str,
                        help='pb 文件所在路径.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    print('start.....')
    main(parse_arguments(sys.argv[1:]))
    # saveAsRawGps('/data/pb/baidu/11/20210305/20210305_001.zip', '/baocun/outputfiles')
