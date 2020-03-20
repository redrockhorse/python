# -*- coding: utf8 -*-
#!/usr/bin/python


import json
dir = '/Users/hongyanma/gitspace/front/front/palmgo-bigdata-front/data/administrativeDivision/'
with open(dir+"province.json","r") as pfile:
    pcode = json.load(pfile)
#print(pcode)
for item in pcode['data']:
    # print('<MenuItem name="'+item['code']+'">'+item['name']+'</MenuItem>')
    print('"'+item['name']+'":'+item['code']+',')