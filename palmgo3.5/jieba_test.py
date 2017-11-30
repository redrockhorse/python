# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import  jieba

source_string = "西直门北大街北向南方向行驶缓慢"

seg_list = jieba.cut(source_string,cut_all=True)
print("Full Mode: "+"/ ".join(seg_list))
seg_list = jieba.cut(source_string,cut_all=False)
print("Default  Mode: "+"/ ".join(seg_list))

source_string = "东六环外环方向K60马驹桥发生一辆小客车与一辆大货车追尾事故占外侧行车道和应急车道后方车多约6公里"
seg_list = jieba.cut(source_string,cut_all=True)
print("Full Mode: "+"/ ".join(seg_list))
seg_list = jieba.cut(source_string,cut_all=False)
print("Default Mode: "+"/ ".join(seg_list))

source_string = "京藏高速进京方向健翔桥以南有事故占用中间车道后车行驶缓慢目前队尾已排到清河收费站"
seg_list = jieba.cut(source_string,cut_all=True)
print("Full Mode: "+"/ ".join(seg_list))
seg_list = jieba.cut(source_string,cut_all=False)
print("Default  Mode: "+"/ ".join(seg_list))

source_string = "目前建国路、建外大街东长安街东向西方向交通压力较大建议司机朋友提前绕行"
seg_list = jieba.cut(source_string,cut_all=True)
print("Full Mode: "+"/ ".join(seg_list))
seg_list = jieba.cut(source_string,cut_all=False)
print("Default  Mode: "+"/ ".join(seg_list))

source_file='Event_new_new.txt'
target_file = 'tg.txt'
print('start !!')
with open(source_file) as sfile:
    for line in sfile:
        seg_list = jieba.cut(line,cut_all=False)
        with open(target_file,'wb') as fW:
            fW.write(' '.join(seg_list))

print('Done !!')