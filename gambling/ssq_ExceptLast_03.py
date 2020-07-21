#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = "select *  from jc.td_ptl_lt_data  order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
columns=[[],[],[],[],[],[],[]]
qi = len(result)
markov = {'v1':{},'v2':{},'v3':{},'v4':{},'v6':{}}
for row in result:
    rows = []
    rows.append(int(row['v1']))
    rows.append(int(row['v2']))
    rows.append(int(row['v3']))
    rows.append(int(row['v4']))
    rows.append(int(row['v5']))
    rs.append(rows)
    columns[0].append(int(row['v1']))
    columns[1].append(int(row['v2']))
    columns[2].append(int(row['v3']))
    columns[3].append(int(row['v4']))
    columns[4].append(int(row['v5']))

    columns[5].append(int(row['v6']))
    columns[6].append(int(row['v7']))

    if int(row['v1']) not in markov['v1']:
        markov['v1'][int(row['v1'])] = []
    if int(row['v2']) not in markov['v2']:
        markov['v2'][int(row['v2'])] = []
    if int(row['v3']) not in markov['v3']:
        markov['v3'][int(row['v3'])] = []
    if int(row['v4']) not in markov['v4']:
        markov['v4'][int(row['v4'])] = []
    markov['v1'][int(row['v1'])].append(int(row['v2']))
    markov['v2'][int(row['v2'])].append(int(row['v3']))
    markov['v3'][int(row['v3'])].append(int(row['v4']))
    markov['v4'][int(row['v4'])].append(int(row['v5']))

    if int(row['v6']) not in markov['v6']:
        markov['v6'][int(row['v6'])] = []
    markov['v6'][int(row['v6'])].append(int(row['v7']))

# print(rs)
# print(columns)
import collections
c0 = collections.Counter(columns[0])
c1 = collections.Counter(columns[1])
c2 = collections.Counter(columns[2])
c3 = collections.Counter(columns[3])
c4 = collections.Counter(columns[4])
print(c0)
print(c1)
print(c2)
print(c3)
print(c4)
print(qi)

print(markov)
from random import choice


from random import sample
cv0 = sample(columns[0], 5)
cv1 = []
cv2 = []
cv3 = []
cv4 = []
print(cv0)
for l1 in cv0:
    lv2 = choice(markov['v1'][l1])
    cv1.append(lv2)

for l1 in cv1:
    lv2 = choice(markov['v2'][l1])
    cv2.append(lv2)

for l1 in cv2:
    lv2 = choice(markov['v3'][l1])
    cv3.append(lv2)

for l1 in cv3:
    lv2 = choice(markov['v4'][l1])
    cv4.append(lv2)
print(cv1)
print(cv2)
print(cv3)
print(cv4)

cv5 = sample(columns[5], 5)
cv6 = []
for l1 in cv5:
    lv2 = choice(markov['v6'][l1])
    cv6.append(lv2)
print(cv5)
print(cv6)

for i in range(5):
   print(str(cv0[i]) + '，'+str(cv1[i]) + '，'+str(cv2[i]) + '，'+str(cv3[i]) + '，'+str(cv4[i]) + '-'+str(cv5[i]) + '，'+str(cv6[i]))