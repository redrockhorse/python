# -*- coding:utf-8 -*-
# @Time : 2020/3/18 上午11:17
# @Author: kkkkibj@163.com
# @File : video_stream_validate_statistics.py

from rediscluster import RedisCluster

redis_nodes = [{"host": "192.168.23.90", "port": "7001", "database": 2},
               {"host": "192.168.23.82", "port": "7001", "database": 2}]
conn = RedisCluster(startup_nodes=redis_nodes, decode_responses=True)

key_prefix = 'camera_'
rc_end = conn.scan_iter(key_prefix + "*")
count_dic = {}
count_dic['total'] = 0
for k in rc_end:
    count_dic['total'] += 1
    v = conn.hget(k, "onlineStatus")
    if v not in count_dic:
        count_dic[v] = 0
    count_dic[v] += 1
print(count_dic)
