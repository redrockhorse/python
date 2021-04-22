# -*- coding:utf-8 -*-
#@Time : 2021/4/1 下午4:03
#@Author: kkkkibj@163.com
#@File : province_code.py
case_sql = "CASE 'province'"
with open('/Users/hongyanma/Desktop/provincecode.txt') as f:
    line = f.readline()
    while line:
        print(line)
        arr = line.split(":")
        pname = arr[0]
        pcode = arr[1].replace("\n",'')
        case_sql += " when " + "'"+str(pcode)+"' then "  + "'"+ pname +"' "
        line = f.readline()
print(case_sql)
