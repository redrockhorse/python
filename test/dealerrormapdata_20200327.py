import json
import requests
import math
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='datacapture_rest', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def fecthData():
    tmparr = []
    tmpdic = {}
    sql = "select a.f57826e008444f3486df2a6ebdbc8967, a.9969d53562034211be860e22031a7f89,a.26762f6e885d4458b76e755cb2f92933," + "a.fca58197ecd3428d8c8a93783af7c64d,a.1d2eb9b9d3d54d3aa51c7e7c1debd12e from layer_tollplaza a  where a.f57826e008444f3486df2a6ebdbc8967 in " + " (select b.f57826e008444f3486df2a6ebdbc8967 from  " + "layer_tollplaza b where b.9969d53562034211be860e22031a7f89='NoName' and b.state=1)" + " and a.9969d53562034211be860e22031a7f89 <>'NoName' and LENGTH(trim(a.9969d53562034211be860e22031a7f89)) >0 and LENGTH(trim(a.26762f6e885d4458b76e755cb2f92933))>0 and " + " LENGTH(trim(a.fca58197ecd3428d8c8a93783af7c64d)) > 0 and LENGTH(trim(a.1d2eb9b9d3d54d3aa51c7e7c1debd12e))  >0;"
    # print(sql)
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    for i in range(len(sqlresult)):
        # if i > 10:
        #     break
        item = sqlresult[i]
        # print(item)
        tmpdic[item['f57826e008444f3486df2a6ebdbc8967']] = item
        tmparr.append(item['f57826e008444f3486df2a6ebdbc8967'])
    # print(len(tmparr))
    return tmpdic

def fecthData_1():
    tmparr = []
    tmpdic = {}
    sql = "select f57826e008444f3486df2a6ebdbc8967 from  layer_tollplaza where 9969d53562034211be860e22031a7f89='NoName' and state=1  and LENGTH(trim(9969d53562034211be860e22031a7f89)) >0 and LENGTH(trim(26762f6e885d4458b76e755cb2f92933))>0 and  LENGTH(trim(fca58197ecd3428d8c8a93783af7c64d)) > 0 and LENGTH(trim(1d2eb9b9d3d54d3aa51c7e7c1debd12e))  >0;"
    # print(sql)
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    for i in range(len(sqlresult)):
        # if i > 10:
        #     break
        item = sqlresult[i]
        # print(item)
        tmpdic[item['f57826e008444f3486df2a6ebdbc8967']] = item
        tmparr.append(item['f57826e008444f3486df2a6ebdbc8967'])
    # print(len(tmparr))
    return tmpdic

def repair(rightdic):
    sql = "select id,f57826e008444f3486df2a6ebdbc8967 from  layer_tollplaza where 9969d53562034211be860e22031a7f89='NoName' and state=1;"
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    for i in range(len(sqlresult)):
        item = sqlresult[i]
        # print(item)
        id = item['id']
        key = item['f57826e008444f3486df2a6ebdbc8967']
        if key in rightdic:
            val = rightdic[key]
            # print(rightdic[key])
            update_sql = "update layer_tollplaza set 9969d53562034211be860e22031a7f89 = '"+val['9969d53562034211be860e22031a7f89']+"' ,"+ " 26762f6e885d4458b76e755cb2f92933='"+val['26762f6e885d4458b76e755cb2f92933']+"',"+"fca58197ecd3428d8c8a93783af7c64d='"+val['fca58197ecd3428d8c8a93783af7c64d']+"',"+"1d2eb9b9d3d54d3aa51c7e7c1debd12e='"+val['1d2eb9b9d3d54d3aa51c7e7c1debd12e']+"' where id='"+id+"' and 9969d53562034211be860e22031a7f89='NoName' and state=1;"

            print(update_sql)



if __name__ == '__main__':
    rdic = fecthData()
    i = 0
    for key in rdic:
        i += 1
    print(i)

    rdic1 = fecthData_1()
    i = 0
    n = 0
    for key in rdic1:
        if key not in rdic:
            # print(key)
            n += 1
        i += 1
    print(i)
    print(n)
    repair(rdic)

