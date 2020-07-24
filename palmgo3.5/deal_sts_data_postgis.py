# -*- coding:utf-8 -*-
# @Time : 2020/7/2 下午7:00
# @Author: kkkkibj@163.com
# @File : deal_sts_data.py
# 处理中科院空气污染数据
import psycopg2
import numpy as np

conn = psycopg2.connect(database="postgres", user="postgres",password="root", host="127.0.0.1", port="54321")
cursor = conn.cursor()

'''
## 执行SQL命令
cursor.execute("CREATE TABLE test_conn(id int, name text)")
cursor.execute("INSERT INTO test_conn values(1,'haha')")

## 提交SQL命令
conn.commit()

## 执行SQL SELECT命令
cursor.execute("select * from test_conn")

## 获取SELECT返回的元组
rows = cursor.fetchall()
for row in rows:
    print('id = ',row[0], 'name = ', row[1], '\n')

## 关闭游标
cursor.close()

## 关闭数据库连接
conn.close()

'''
area_arr = ['bj', 'hb', 'tj']
date_arr = ['20180415', '20180416', '20180417', '20180418', '20180419']
type_arr = ['Emission_CO', 'Emission_NOX', 'Emission_PM', 'Emission_SO2', 'Emission_VOC']
data_dir = '/Users/hongyanma/Downloads/sts_result'



def handleData(area, type, datestr):
    filecount = 0
    result = {}
    for i in range(0, 288):
        tr = str(i + 1)
        while len(tr) < 3:
            tr = '0' + tr
        filepath = data_dir + '/' + area + '/' + type + '/' + 'Track_FCD_' + datestr + '/' + 'FCD_' + datestr + '_' + tr + '.txt'
        with open(filepath, 'r') as f:
            filecount += 1
            linestr = f.readline()
            while linestr:
                linestr = f.readline()
                # print(area + ',' + type + ',' + datestr + ',' + tr + ',' + linestr.replace('\n', ''))
                if len(linestr.replace('\n', '').split(',')) > 1:
                    linkid = linestr.replace('\n', '').split(',')[0]
                    val = linestr.replace('\n', '').split(',')[1]
                    # rowdata = np.zeros(288)
                    if linkid in result:
                        rowdata = result[linkid]
                    else:
                        rowdata = np.zeros(288)
                    rowdata[i] = val
                    result[linkid] = rowdata
                else:
                    print(linestr)
            # print('filecount:'+ str(filecount))
    typeshort = type.split('_')[1]
    outdir = '/Users/hongyanma/Downloads/sts_result/total'
    outputfile = outdir + '/' + area + '_' + typeshort + '_' + datestr + '.txt'
    with open(outputfile, 'w') as outfile:
        for key in result:
            outfile.write(area + ',' + typeshort + ',' + datestr + ',' + key + ',' + ','.join(
                map(str, result[key].tolist())) + '\n')
            # print(area+','+typeshort+','+datestr+','+key+','+','.join(map(str,result[key].tolist())))
    return result


def loadDataFile2mysql(filepath):
    sql = "load data infile '" + filepath + "' into table td_ptl_air_pollution CHARACTER SET utf8 FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' (area, ptype, datestr, linkid, t001, t002, t003, t004, t005, t006, t007, t008, t009, t010, t011, t012, t013, t014, t015, t016, t017, t018, t019, t020, t021, t022, t023, t024, t025, t026, t027, t028, t029, t030, t031, t032, t033, t034, t035, t036, t037, t038, t039, t040, t041, t042, t043, t044, t045, t046, t047, t048, t049, t050, t051, t052, t053, t054, t055, t056, t057, t058, t059, t060, t061, t062, t063, t064, t065, t066, t067, t068, t069, t070, t071, t072, t073, t074, t075, t076, t077, t078, t079, t080, t081, t082, t083, t084, t085, t086, t087, t088, t089, t090, t091, t092, t093, t094, t095, t096, t097, t098, t099, t100, t101, t102, t103, t104, t105, t106, t107, t108, t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120, t121, t122, t123, t124, t125, t126, t127, t128, t129, t130, t131, t132, t133, t134, t135, t136, t137, t138, t139, t140, t141, t142, t143, t144, t145, t146, t147, t148, t149, t150, t151, t152, t153, t154, t155, t156, t157, t158, t159, t160, t161, t162, t163, t164, t165, t166, t167, t168, t169, t170, t171, t172, t173, t174, t175, t176, t177, t178, t179, t180, t181, t182, t183, t184, t185, t186, t187, t188, t189, t190, t191, t192, t193, t194, t195, t196, t197, t198, t199, t200, t201, t202, t203, t204, t205, t206, t207, t208, t209, t210, t211, t212, t213, t214, t215, t216, t217, t218, t219, t220, t221, t222, t223, t224, t225, t226, t227, t228, t229, t230, t231, t232, t233, t234, t235, t236, t237, t238, t239, t240, t241, t242, t243, t244, t245, t246, t247, t248, t249, t250, t251, t252, t253, t254, t255, t256, t257, t258, t259, t260, t261, t262, t263, t264, t265, t266, t267, t268, t269, t270, t271, t272, t273, t274, t275, t276, t277, t278, t279, t280, t281, t282, t283, t284, t285, t286, t287, t288);"
    cursor.execute(sql)


if __name__ == '__main__':
    ncount = 0
    for area in area_arr:
        for type in type_arr:
            typeshort = type.split('_')[1]
            for datestr in date_arr:
                dropsql ='drop table if exists td_ptl_air_pollution_' + area + '_' + typeshort + '_' + datestr+';'
                cursor.execute(dropsql)
                c_sql = 'create table td_ptl_air_pollution_' + area + '_' + typeshort + '_' + datestr + '(linkid varchar(14),s_vals text[]);'
                print(c_sql)

                cursor.execute(c_sql)
                # altersql = ' ALTER  TABLE td_ptl_air_pollution_' + area + '_' + typeshort + '_' + datestr + ' ADD PRIMARY KEY(`linkid`);'
                # cursor.execute(altersql)
                with open(
                        '/Users/hongyanma/Downloads/sts_result/total/' + area + '_' + typeshort + '_' + datestr + '.txt',
                        'r') as dfile:
                    linestr = dfile.readline()
                    while linestr:
                        insql = 'insert into td_ptl_air_pollution_' + area + '_' + typeshort + '_' + datestr +' values(%s,%s)'
                        # print(tuple(linestr.replace('\n', '').split(',')))
                        # print(len(linestr.replace('\n', '').split(',')))
                        linkid = linestr.split(',')[3]
                        valsarr = linestr.replace('\n', '').split(',')[4:]
                        vararrstr = ','.join(valsarr)
                        cursor.execute(insql, (linkid,'{'+vararrstr+'}'))
                        ncount += 1
                        if ncount % 1000 == 0:
                            print(ncount)
                        linestr = dfile.readline()
                conn.commit()
