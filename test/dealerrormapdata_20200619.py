import json
import requests
import math
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='datacapture', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


sql1='select * from  datacapture.layer_video where 392ae76344cc4a2786ec55d983dda79f in (\'1\',\'4\') and state = 1'
cursor.execute(sql1)
sqlresult = cursor.fetchall()
n =0
for i in range(len(sqlresult)):
    item = sqlresult[i]
    #print(item)
    str1 = ''
    str2 = ''
    if item['d945f4bd47dd48d1b4d59e64560c483b'].find('（') != -1:
        str1 = item['d945f4bd47dd48d1b4d59e64560c483b'].split('（')[0]
        str2 = item['d945f4bd47dd48d1b4d59e64560c483b'].split('（')[1].split('）')[0]
    else:
        str1 = item['d945f4bd47dd48d1b4d59e64560c483b'].split('(')[0]
        str2 = item['d945f4bd47dd48d1b4d59e64560c483b'].split('(')[1].split('）')[0]
    upsql = 'update datacapture.layer_video set 392ae76344cc4a2786ec55d983dda79f=\'' + str1 + '\',548b90a9189a4ab4b7760acb36c6433b=\'' + str2 + '\' where id = \'' + item['id'] + '\';'
    print(upsql)
    # sql2 = 'select * from datacapture.layer_video  where d945f4bd47dd48d1b4d59e64560c483b = \'G4(京港澳高速)湖南衡阳耒宜段衡阳管理处K1732+670(公平主线收费站)\' and 392ae76344cc4a2786ec55d983dda79f not in (\'1\',\'4\')  limit 1'
    sql2 = 'select id,392ae76344cc4a2786ec55d983dda79f,548b90a9189a4ab4b7760acb36c6433b from datacapture.layer_video  where d945f4bd47dd48d1b4d59e64560c483b = \''+item['d945f4bd47dd48d1b4d59e64560c483b']+'\' and 392ae76344cc4a2786ec55d983dda79f not in (\'1\',\'4\') order by lastupd desc limit 1'
    #print(sql2)
    cursor.execute(sql2)
    result = cursor.fetchone()
    if result is not None:
        n += 1
        #print(item['id'],result)
        upsql = 'update datacapture.layer_video set 392ae76344cc4a2786ec55d983dda79f=\''+ result['392ae76344cc4a2786ec55d983dda79f'] + '\',548b90a9189a4ab4b7760acb36c6433b=\''+result['548b90a9189a4ab4b7760acb36c6433b'] +'\' where id = \'' + item['id'] +'\';'
        print(upsql)
print(n)



