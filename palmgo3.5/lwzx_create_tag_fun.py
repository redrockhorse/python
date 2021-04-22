# -*- coding:utf-8 -*-
# @Time : 2020/10/11 下午2:42
# @Author: kkkkibj@163.com
# @File : lwzx_create_tag_fun.py
# 创建元数据功能
import pymysql

# mysql 链接
mqconn = pymysql.connect(host='192.168.220.246', user='lwzx2020', passwd='lwzx2020', db='lwzx_yjjc', port=3306,
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
mqcursor = mqconn.cursor()

funarr = [{"funName": "实时数据", "funCode": "lineChart"}, {"funName": "播放", "funCode": "videoPlay"},
          {"funName": "分类占比", "funCode": "typeRatio"}, {"funName": "详情查看", "funCode": "detailInfo"},
          {"funName": "监控搜索", "funCode": "searchCamera"}, {"funName": "影响范围", "funCode": "eventCoverage"}]

'''
INSERT INTO `lwzx_yjjc`.`meta_tag_fun`
(`funId`,
`tagId`,
`funName`,
`funCode`,
`online`,
`remark`)
VALUES
(<{funId: }>,
<{tagId: }>,
<{funName: }>,
<{funCode: }>,
<{online: 1}>,
<{remark: }>);
'''

tagqrysql = 'select * from lwzx_yjjc.meta_tag;'
mqcursor.execute(tagqrysql)
result = mqcursor.fetchall()
id = 1
for row in result:
    print(row)
    insertsql = "INSERT INTO `lwzx_yjjc`.`meta_tag_fun` (`funId`,`tagId`,`funName`,`funCode`) VALUES(%s,%s,%s,%s)"
    if row['tagName'] == '省流量':
        maparr = [0, 2]
        for i in maparr:
            vals = (str(id), row['tagId'], funarr[i]['funName'], funarr[i]['funCode'])
            mqcursor.execute(insertsql,vals)
            id += 1
    if row['tagName'] == '收费站':
        maparr = [0, 2, 3, 4]
        for i in maparr:
            vals = (str(id), row['tagId'], funarr[i]['funName'], funarr[i]['funCode'])
            mqcursor.execute(insertsql,vals)
            id += 1

    if row['tagName'] == '干线公路流量':
        maparr = [0, 2]
        for i in maparr:
            vals = (str(id), row['tagId'], funarr[i]['funName'], funarr[i]['funCode'])
            mqcursor.execute(insertsql,vals)
            id += 1

    if row['tagName'] == '视频':
        maparr = [1]
        for i in maparr:
            vals = (str(id), row['tagId'], funarr[i]['funName'], funarr[i]['funCode'])
            mqcursor.execute(insertsql,vals)
            id += 1

    if row['tagName'] == '灾毁信息':
        maparr = [3, 5]
        for i in maparr:
            vals = (str(id), row['tagId'], funarr[i]['funName'], funarr[i]['funCode'])
            mqcursor.execute(insertsql,vals)
            id += 1
mqconn.commit()