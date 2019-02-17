import re

str='国道g25阿(卡金)法快乐(手势)'
def reRoadName(str):
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    p2 =  re.compile(r'.*[a-zA-Z]')
    p3 = re.compile(r'.*[\d]')
    a = re.findall(p1,str)
    for m in a:
        str = str.replace(m,'')
    str = str.replace('(','')
    str = str.replace(')','')

    b = re.findall(p2,str)

    for m in b:
        str = str.replace(m, '')
    c = re.findall(p3,str)
    for m in c :
        str = str.replace(m, '')
    print(str)
    return str

reRoadName(str)
