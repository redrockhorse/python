# -*- coding:utf-8 -*-
#@Time : 2020/12/9 下午3:26
#@Author: kkkkibj@163.com
#@File : zaihui_columname.py
dic ={}
with open('/Users/hongyanma/Desktop/zaihui_columname.txt','r') as file:
    line = file.readline()
    while line:
        if line != '\n':
            # print(line.replace('\n', '').split('\t'))
            arr = line.replace('\n', '').split('\t')
            for i in arr:
                # print(i)
                if i in dic:
                    dic[i] += 1
                else:
                    dic[i] = 1
        line = file.readline()
print(dic)
for colname in dic:
    print(colname)