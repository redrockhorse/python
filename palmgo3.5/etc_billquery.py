# -*- coding:utf-8 -*-
# @Time : 2020/5/2 下午1:42
# @Author: kkkkibj@163.com
# @File : etc_billquery.py
# etc数据查询验证

import requests
import datetime
import time
import xlrd
import json

# 接口地址
api_url = 'https://gw.cywetc.com/api/json'
appId = '99999922'

vehicleTypeDic = {'CAR_1': 1,
                  'CAR_2': 2,
                  'CAR_3': 3,
                  'CAR_4': 4,
                  'OPERATION_CAR_1': 21,
                  'OPERATION_CAR_2': 22,
                  'OPERATION_CAR_3': 23,
                  'OPERATION_CAR_4': 24,
                  'OPERATION_CAR_5': 25,
                  'OPERATION_CAR_6': 26,
                  'WEIGHT_CAR_1': 11,
                  'WEIGHT_CAR_2': 12,
                  'WEIGHT_CAR_3': 13,
                  'WEIGHT_CAR_4': 14,
                  'WEIGHT_CAR_5': 15,
                  'WEIGHT_CAR_6': 16}

vehicleClassDic = {'PT': 0,
                   'JJ': 8,
                   'JJ1': 10,
                   'CD': 14,
                   'LTC': 21,
                   'LHSGJ': 22,
                   'QXJZ': 23,
                   'JZX': 24,
                   'DXYS': 25,
                   'YJC': 26,
                   'JZX_J2': 24,
                   'HCLC': 27}

plateColorDic = {'BLACK': 2,
                 'BLUE': 0,
                 'BLUE_WHITE': 6,
                 'GREEN': 11,
                 'GREEN_WHITE': 4,
                 'RED': 12,
                 'TEMPORARY': 9,
                 'WHITE': 3,
                 'YELLOW': 1,
                 'YELLOW_GREEN': 5}


def genParamIn(bizContent, jsonfilname):
    # filename = 'FCS_PATH_PR_REQ_99999922_20200502141436764.json'
    bizContentStr = json.dumps(bizContent, ensure_ascii=False)
    # print(bizContentStr)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17]
    # filename = 'FCS_PATH_PR_REQ_99999922_' + timestamp + '.json'
    filename = jsonfilname + timestamp + '.json'
    paramin = {
        "filename": filename,
        # "bizContent": "{\"axleCount\":0,\"mediaType\":1,\"units\":[{\"unitId\":\"S003337001000510\",\"passTime\":\"2020-04-27T16:23:06\"},{\"unitId\":\"S003337002000110\",\"passTime\":\"2020-04-27T16:36:59\"}],\"plateNum\":\"皖ZZ1515\",\"type\":2,\"plateColor\":0,\"enTollLaneId\":\"S0033370010030\",\"vehicleStatusFlag\":255,\"mediaNo\":\"10000\",\"enTime\":\"2020-04-27T20:25:10\",\"vehicleClass\":0,\"exTime\":\"2020-04-27T20:25:10\",\"exTollLaneId\":\"G00033400100402010030\",\"vehicleType\":1}",
        "bizContent": bizContentStr,
        "sign": "NONE",
        "tokenType": "USER_AUTH",
        "accessToken": "chinaetcorg",
        "version": "2.0",
        "encryptType": "NONE",
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')  # "2020-05-02T14:14:36"
    }
    # print(paramin)
    return paramin


def handelETCData():
    resultdata = {}
    ds = xlrd.open_workbook('/Users/hongyanma/Desktop/etctestdata.xlsx')
    st = ds.sheet_by_index(0)
    nrows = st.nrows
    # print(nrows)
    tableheader = st.row(0)
    # print(len(tableheader))
    for i in range(len(tableheader)):
        print(str(i) + " : " + tableheader[i].value)

    for j in range(1, nrows):
        row = st.row(j)
        passid = row[2].value
        axleCount = row[12].value
        mediaType = row[16].value
        plateNum = row[21].value
        type = 2
        plateColor = row[22].value
        if plateColor in plateColorDic:
            plateColor = plateColorDic[plateColor]
        enTollLaneId = row[10].value
        vehicleStatusFlag = 255
        mediaNo = row[17].value
        enTime = row[11].value.replace('.0', '').replace(' ', 'T')
        vehicleClass = row[15].value
        if vehicleClass in vehicleClassDic:
            vehicleClass = vehicleClassDic[vehicleClass]
        exTime = row[19].value.replace('.0', '').replace(' ', 'T')
        exTollLaneId = row[18].value
        vehicleType = row[14].value
        if vehicleType in vehicleTypeDic:
            vehicleType = vehicleTypeDic[vehicleType]
        unitId = row[6].value
        passTime = row[13].value.replace('.0', '').replace(' ', 'T')

        available = len(enTollLaneId) >= 14 and len(exTollLaneId) >= 14 and len(row[6].value) == 19
        # print(available)
        unit = {"unitId": unitId[0:16], "passTime": passTime}
        if available:
            if passid not in resultdata:
                resultdata[passid] = {}
                resultdata[passid] = resultdata[passid]
                resultdata[passid]['axleCount'] = axleCount
                resultdata[passid]['mediaType'] = mediaType
                resultdata[passid]['units'] = []
                resultdata[passid]['plateNum'] = plateNum
                resultdata[passid]['type'] = type
                resultdata[passid]['plateColor'] = plateColor
                resultdata[passid]['enTollLaneId'] = enTollLaneId
                resultdata[passid]['vehicleStatusFlag'] = vehicleStatusFlag
                resultdata[passid]['mediaNo'] = mediaNo
                resultdata[passid]['enTime'] = enTime
                resultdata[passid]['exTollLaneId'] = exTollLaneId
                resultdata[passid]['vehicleClass'] = vehicleClass
                resultdata[passid]['exTime'] = exTime
                resultdata[passid]['vehicleType'] = vehicleType
            resultdata[passid]['units'].append(unit)
        # print(resultdata)
    return resultdata
    # bizContent = "{\"axleCount\":0,\"mediaType\":1,\"units\":[{\"unitId\":\"S003337001000510\",\"passTime\":\"2020-04-27T16:23:06\"},{\"unitId\":\"S003337002000110\",\"passTime\":\"2020-04-27T16:36:59\"}],\"plateNum\":\"皖ZZ1515\",\"type\":2,\"plateColor\":0,\"enTollLaneId\":\"S0033370010030\",\"vehicleStatusFlag\":255,\"mediaNo\":\"10000\",\"enTime\":\"2020-04-27T20:25:10\",\"vehicleClass\":0,\"exTime\":\"2020-04-27T20:25:10\",\"exTollLaneId\":\"G00033400100402010030\",\"vehicleType\":1}",


# 路径还原api
def pathPlanApi(param):
    # print(param)
    ts = time.time()
    rp = requests.post(api_url, None, param)
    print(rp.json())
    print("path_api use time: " + str(time.time() - ts))
    return rp.json()


# 费用api
def etcFeeApi(param):
    ts = time.time()
    rp = requests.post(api_url, None, param)
    # print("fee_api use time: " + str(time.time() - ts))
    # print(rp.json())
    return json.loads(rp.text)


def main():
    tabletestdata ={"data":[]}
    # pathparam = {"filename": "FCS_FEE_COMPUTE_REQ_99999922_20200108150154581.json", "encryptType": "NONE", "version": "2.0",
    #          "signType": "NONE", "sign": "NONE", "timestamp": "2020-01-08T15:01:54", "tokenType": "USER_AUTH",
    #          "accessToken": "chinaetcorg",
    #          "bizContent": "{\"axleCount\":2,\"enTime\":\"2020-04-27T16:19:49\",\"enTollLaneId\":\"S0033370010030\",\"exTime\":\"2020-04-27T20:25:10\",\"exTollLaneId\":\"G00033400100402010030\",\"mediaNo\":null,\"mediaType\":1,\"plateColor\":0,\"plateNum\":\"皖ZZ1515\",\"units\":[{\"passTime\":\"2020-04-27T16:22:36\",\"unitId\":\"S003337001000510\",\"unitType\":4},{\"passTime\":\"2020-04-27T16:32:38\",\"unitId\":\"G151137003001620\",\"unitType\":4},{\"passTime\":\"2020-04-27T16:40:54\",\"unitId\":\"G151137003001720\",\"unitType\":4},{\"passTime\":\"2020-04-27T16:49:17\",\"unitId\":\"G151137003001820\",\"unitType\":4},{\"passTime\":\"2020-04-27T17:00:11\",\"unitId\":\"G151137003001920\",\"unitType\":4},{\"passTime\":\"2020-04-27T17:02:58\",\"unitId\":\"G151137003002020\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:20:56\",\"unitId\":\"G000337008000610\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:22:28\",\"unitId\":\"G000332001000110\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:26:49\",\"unitId\":\"G000332001000210\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:42:41\",\"unitId\":\"G251332004000110\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:43:57\",\"unitId\":\"G251332004000210\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:51:29\",\"unitId\":\"G003032001001610\",\"unitType\":4},{\"passTime\":\"2020-04-27T18:59:11\",\"unitId\":\"G003032001001710\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:00:33\",\"unitId\":\"G003032001001810\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:03:45\",\"unitId\":\"G000332004000110\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:06:00\",\"unitId\":\"G003034001000110\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:27:47\",\"unitId\":\"G000334001000110\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:30:17\",\"unitId\":\"G000334001000310\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:46:18\",\"unitId\":\"G000334001000410\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:54:09\",\"unitId\":\"G000334001000510\",\"unitType\":4},{\"passTime\":\"2020-04-27T19:57:03\",\"unitId\":\"G000334001000610\",\"unitType\":4}],\"vehicleClass\":0,\"vehicleStatusFlag\":0,\"vehicleType\":1}}"}
    #
    # pathPlanApi(pathparam)
    #
    #
    # feeparam = {"filename":"FCS_PATH_PR_REQ_99999922_20200502141436764.json","bizContent":"{\"axleCount\":0,\"mediaType\":1,\"units\":[{\"unitId\":\"S003337001000510\",\"passTime\":\"2020-04-27T16:23:06\"},{\"unitId\":\"S003337002000110\",\"passTime\":\"2020-04-27T16:36:59\"}],\"plateNum\":\"皖ZZ1515\",\"type\":2,\"plateColor\":0,\"enTollLaneId\":\"S0033370010030\",\"vehicleStatusFlag\":255,\"mediaNo\":\"10000\",\"enTime\":\"2020-04-27T20:25:10\",\"vehicleClass\":0,\"exTime\":\"2020-04-27T20:25:10\",\"exTollLaneId\":\"G00033400100402010030\",\"vehicleType\":1}","sign":"NONE","tokenType":"USER_AUTH","accessToken":"chinaetcorg","version":"2.0","encryptType":"NONE","timestamp":"2020-05-02T14:14:36"}
    # etcFeeApi(feeparam)

    print('main')
    initData = handelETCData()
    print(initData)
    i = 0
    p = 0
    f = 0
    for passid in initData:
        print(passid)
        paramin = genParamIn(initData[passid], 'FCS_PATH_PR_REQ_99999922_')
        pathOutParam = pathPlanApi(paramin)
        if 'statusCode' in pathOutParam and pathOutParam['statusCode'] == 0:
            p += 1
            feeParamIn = initData[passid]
            bizContent = json.loads(pathOutParam['bizContent'])
            feeParamIn['pathId'] = bizContent['paths'][0]['pathId']
            feeParamIn['units'] = bizContent['paths'][0]['units']
            feeParamIn['enTollStationId'] = feeParamIn['enTollLaneId'][0:14]
            feeParamIn['exTollStationId'] = feeParamIn['exTollLaneId'][0:14]
            # feeParamIn['filename'] = feeParamIn['filename'].replace('FCS_PATH_PR_REQ_99999922_',
            #                                                         'FCS_FEE_COMPUTE_REQ_99999922_')
            feeparamin = genParamIn(feeParamIn, 'FCS_FEE_COMPUTE_REQ_99999922_')
            feeoutparame = etcFeeApi(feeparamin)
            if 'statusCode' in feeoutparame and  feeoutparame['statusCode'] == 0:
                tabletestdata['data'].append(initData[passid])
                f += 1

        i += 1
        # if i > 10:
        #     break
    print(i)
    print(p)
    print(f)
    # with open('/Users/hongyanma/Desktop/etc_original_data.json','w+') as outf:
    #     json.dump(tabletestdata,outf)

    # rquest_param_in = genParamIn()
    # pathPlanApi(rquest_param_in)


if __name__ == '__main__':
    main()
    # print(datetime.datetime.strptime('2020-04-29 09:25:00.0'.replace('.0',''), '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%dT%H:%M:%S'))
    # print('2020-04-29 09:25:00.0'.replace('.0', '').replace(' ', 'T'))
