# -*- coding:utf-8 -*-
# @Time : 2020/10/7 下午6:07
# @Author: kkkkibj@163.com
# @File : postgres2mysql.py
import pymysql
import psycopg2

# mysql 链接
mqconn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='lwzx_yjjc', port=3786,
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
mqcursor = mqconn.cursor()
# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="root", host="127.0.0.1", port="54321")
pgcursor = pgconn.cursor()


def putData2Myql():
    sql = 'select lxbm,lxmc from public.lwzx_71118_links group by lxmc,lxbm;'
    pgcursor.execute(sql)
    result = pgcursor.fetchall()
    for row in result:
        insertsql = 'INSERT INTO `lwzx_yjjc`.`roads` (`lxbm`,`lxmc`) VALUES (%s,%s);'
        mqcursor.execute(insertsql, list(row))
        print(row)
    mqconn.commit()


if __name__ == '__main__':
    putData2Myql()
