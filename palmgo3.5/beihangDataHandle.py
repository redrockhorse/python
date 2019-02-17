# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#北航学生提供的数据
import json
basedir='/Users/hongyanma/Desktop/beihang'

with open(basedir + '/pathrestore.json', 'r') as prfile:
    probj = json.load(prfile)
#print(probj)
for p in probj['data']:
    print(p)
def markstation():
    nsjps=[]
    sjps=[]
    result={}
    result['data']={}
    result['data']['nsj']=[]
    result['data']['sj']=[]
    result['data']['dif']=[]
    with open(basedir+'/nsj.json','r') as nsjfile:
        nsjps = json.load(nsjfile)
        print(nsjps)

    with open(basedir+'/sj.json','r') as sjfile:
        sjps = json.load(sjfile)
        print(sjps)

    #print(set(sjps['data'])-set(nsjps['data']))
    tmpdic={}
    for nsj in nsjps['data']:
        result['data']['nsj'].append({'ID': nsj['ID'], 'coord': [nsj['LNG'], nsj['LAT']]})
        tmpdic[nsj['LNG'] + '_' + nsj['LAT']] = nsj['ID']
    for sj in sjps['data']:
        result['data']['sj'].append({'ID':sj['ID'],'coord':[sj['LNG'],sj['LAT']]})
        if sj['LNG']+'_'+sj['LAT'] not in tmpdic:
            result['data']['dif'].append({'ID':sj['ID'],'coord':[sj['LNG'],sj['LAT']]})
    print(result)

    with open(basedir+'/lablestation.json','w') as lablefile:
        json.dump(result,lablefile)



