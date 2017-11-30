__author__ = 'Thinkpad'
import re
import datetime
date_pattern = re.compile(r'\d*-\d*-\d*')
time_pattern = re.compile(r'\d*:\d*')
num_pattern = re.compile(r'\d*')
str ='16-11-06&nbsp;12:00'
ptime='20'+date_pattern.search(str).group()
timestr=time_pattern.search(str).group()
print ptime+" "+timestr
#a=int('')
score='2:1'
hs=num_pattern.match(score).group()
datestr = datetime.datetime.strptime('2016-11-07', "%Y-%m-%d").date()
for i in range(10):
    print datestr-datetime.timedelta(days=i)

print hs
