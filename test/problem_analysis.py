#!/usr/bin/python
# encoding=utf-8
# 故障问题热词分析,输出一个txt文件，用逗号分隔，最后一列是故障原，如果需要分析，另存为csv格式即可
__author__ = 'kkkkibj@163.com'


infile = 'd:\\Downloads\\宽带信息.txt'#原始数据文件，要保存为utf-8编码
outfile = 'd:\\Downloads\\outputfile.txt'

with open(infile, 'r') as inputFile,open(outfile, 'w') as outputFile:
    row = 0 #处理文件的行数，其实没什么用
    sentence = ""
    while True:
        line = inputFile.readline()
        outputline="" #最终输出的，用逗号分割的数据
        if line:
            line_arr = line.split(',')
            standard = '' #规范的
            unstandard ='' #不规范的
            reason = line_arr[1] #逗号分割取第二列，故障原因所在列
            rarr = reason.split("：") #故障原因列再用分号分割
            if len(rarr) > 4: #规范的文本分割后大4列
                rlist = rarr[2].split('->')
                tmp = rlist.pop().split('[')[0]
                rlen = len(rlist)
                for i in range(3-rlen):
                    rlist.append('')
                standard = ','.join(rlist)+",0,"+tmp
                outputline=standard
            else: #不规范的文本数量较少，单独处理
                unstandard = ',,,1,'+reason
                outputline = unstandard
            line_arr.pop(1)
            outputline = ','.join(line_arr).replace('\n','').replace(' ','')+','+outputline+'\n'
            print(outputline)
            outputFile.write(outputline)
        else:
            break
        row += 1
    print('共'+str(row)+'行','执行完毕')
