import json
# infile = '/Users/hongyanma/Desktop/sonAreaSumStatic.json'#原始数据文件，要保存为utf-8编码
# with open(infile,'r') as f:
#     data_dic = json.load(f)
#     #print(data_dic)
#     print('省份,通过数量,未通过数量,总数,省份编码')
#     data = data_dic['body']
#     for i in range(len(data)):
#         #print(data[i])
#         item = data[i]
#         print(item['cityname']+','+str(item['sumpass'])+','+str(item['sumreject'])+','+str(item['sumall'])+','+str(item['dataarea']))
changeId = {}
infile = '/Users/hongyanma/Desktop/allupd.log'
with open(infile,'r') as f:
    dic ={}
    line = f.readline()
    while line:
        #print(line)
        arr = line.split(',')
        #print(arr[3],arr[5],arr[6])
        if arr[3] not in dic:
            dic[arr[3]] = arr[5]+','+arr[6]
        else:
            if dic[arr[3]]==arr[5]+','+arr[6]:
                pass
            else:
                print(arr[3]+',change')
                changeId[arr[3]] =1
        line = f.readline()
    print(dic)
result ={'msg':'',"msgcode":200,"body":[]}
outfile = '/Users/hongyanma/Desktop/test.json'
linesDic ={}
with open(infile,'r') as f,open(outfile,'w') as outf:
    line = f.readline()
    while line:
        arr = line.split(',')
        if arr[3] in changeId:
            print(line)
            result['body'].append({'x':arr[5],'y':arr[6],'corrdinate':arr[4],'id':arr[3]+'-'+arr[1]})
            if arr[3] not in linesDic:
                linesDic[arr[3]] =[]
            linesDic[arr[3]].append([arr[5],arr[6],arr[4]])
        line = f.readline()
    print(result)
    json.dump(result,outf)

result ={'msg':'',"msgcode":200,"body":[]}
outfile = '/Users/hongyanma/Desktop/testlines.json'
with open(infile,'r') as f,open(outfile,'w') as outf:
    print(linesDic)
    for id in linesDic:
        result['body'] = linesDic
    json.dump(result, outf)

