# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#安联数据增加节假日信息

'''
/*
#update td_awp_source_data set week = date_format(Case_Time,'%w');
#commit;
update td_awp_source_data set holiydayname='元旦',holiydaytotal=3,holiydayon=2
where Case_Time>='2017-01-01 00:00:00' and Case_Time<='2017-01-01 23:59:59';
commit;
update td_awp_source_data set holiydayname='元旦',holiydaytotal=3,holiydayon=3
where Case_Time>='2017-01-02 00:00:00' and Case_Time<='2017-01-02 23:59:59';
commit;
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=1
where Case_Time>='2017-01-27 00:00:00' and Case_Time<='2017-01-27 23:59:59';
commit;
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=2
where Case_Time>='2017-01-28 00:00:00' and Case_Time<='2017-01-28 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=3
where Case_Time>='2017-01-29 00:00:00' and Case_Time<='2017-01-29 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=4
where Case_Time>='2017-01-30 00:00:00' and Case_Time<='2017-01-30 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=5
where Case_Time>='2017-01-31 00:00:00' and Case_Time<='2017-01-31 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=6
where Case_Time>='2017-02-01 00:00:00' and Case_Time<='2017-02-01 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=7
where Case_Time>='2017-02-02 00:00:00' and Case_Time<='2017-02-02 23:59:59';
commit;
update td_awp_source_data set week='10'
where Case_Time>='2017-01-22 00:00:00' and Case_Time<='2017-01-22 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2017-02-04 00:00:00' and Case_Time<='2017-02-04 23:59:59';
commit;
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=1
where Case_Time>='2017-04-02 00:00:00' and Case_Time<='2017-04-02 23:59:59';
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=2
where Case_Time>='2017-04-03 00:00:00' and Case_Time<='2017-04-03 23:59:59';
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=3
where Case_Time>='2017-04-04 00:00:00' and Case_Time<='2017-04-04 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2017-04-01 00:00:00' and Case_Time<='2017-04-01 23:59:59';
commit;
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=1
where Case_Time>='2017-04-29 00:00:00' and Case_Time<='2017-04-29 23:59:59';
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=2
where Case_Time>='2017-04-30 00:00:00' and Case_Time<='2017-04-30 23:59:59';
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=3
where Case_Time>='2017-05-01 00:00:00' and Case_Time<='2017-05-01 23:59:59';
commit;
update td_awp_source_data set holiydayname='端午节',holiydaytotal=3,holiydayon=1
where Case_Time>='2017-05-28 00:00:00' and Case_Time<='2017-05-28 23:59:59';
update td_awp_source_data set holiydayname='端午节',holiydaytotal=3,holiydayon=2
where Case_Time>='2017-05-29 00:00:00' and Case_Time<='2017-05-29 23:59:59';
update td_awp_source_data set holiydayname='端午节',holiydaytotal=3,holiydayon=3
where Case_Time>='2017-05-30 00:00:00' and Case_Time<='2017-05-30 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2017-05-27 00:00:00' and Case_Time<='2017-05-27 23:59:59';
commit;
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=1
where Case_Time>='2017-10-01 00:00:00' and Case_Time<='2017-10-01 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=2
where Case_Time>='2017-10-02 00:00:00' and Case_Time<='2017-10-02 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=3
where Case_Time>='2017-10-03 00:00:00' and Case_Time<='2017-10-03 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=4
where Case_Time>='2017-10-04 00:00:00' and Case_Time<='2017-10-04 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=5
where Case_Time>='2017-10-05 00:00:00' and Case_Time<='2017-10-05 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=6
where Case_Time>='2017-10-06 00:00:00' and Case_Time<='2017-10-06 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=7
where Case_Time>='2017-10-07 00:00:00' and Case_Time<='2017-10-07 23:59:59';
update td_awp_source_data set holiydayname='国庆中秋',holiydaytotal=8,holiydayon=8
where Case_Time>='2017-10-08 00:00:00' and Case_Time<='2017-10-08 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2017-09-30 00:00:00' and Case_Time<='2017-09-30 23:59:59';
commit;
---2018---
update td_awp_source_data set holiydayname='元旦',holiydaytotal=3,holiydayon=1
where Case_Time>='2017-12-30 00:00:00' and Case_Time<='2017-12-30 23:59:59';
update td_awp_source_data set holiydayname='元旦',holiydaytotal=3,holiydayon=2
where Case_Time>='2017-12-31 00:00:00' and Case_Time<='2017-12-31 23:59:59';
update td_awp_source_data set holiydayname='元旦',holiydaytotal=3,holiydayon=3
where Case_Time>='2018-01-01 00:00:00' and Case_Time<='2018-01-01 23:59:59';
commit;
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=1
where Case_Time>='2018-02-15 00:00:00' and Case_Time<='2018-02-15 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=2
where Case_Time>='2018-02-16 00:00:00' and Case_Time<='2018-02-16 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=3
where Case_Time>='2018-02-17 00:00:00' and Case_Time<='2018-02-17 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=4
where Case_Time>='2018-02-18 00:00:00' and Case_Time<='2018-02-18 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=5
where Case_Time>='2018-02-19 00:00:00' and Case_Time<='2018-02-19 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=6
where Case_Time>='2018-02-20 00:00:00' and Case_Time<='2018-02-20 23:59:59';
update td_awp_source_data set holiydayname='春节',holiydaytotal=7,holiydayon=7
where Case_Time>='2018-02-21 00:00:00' and Case_Time<='2018-02-21 23:59:59';
update td_awp_source_data set week='10'
where Case_Time>='2018-02-11 00:00:00' and Case_Time<='2018-02-11 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2018-02-24 00:00:00' and Case_Time<='2018-02-24 23:59:59';
commit;
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=1
where Case_Time>='2018-04-05 00:00:00' and Case_Time<='2018-04-05 23:59:59';
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=2
where Case_Time>='2018-04-06 00:00:00' and Case_Time<='2018-04-06 23:59:59';
update td_awp_source_data set holiydayname='清明节',holiydaytotal=3,holiydayon=3
where Case_Time>='2018-04-07 00:00:00' and Case_Time<='2018-04-07 23:59:59';
update td_awp_source_data set week='10'
where Case_Time>='2018-04-08 00:00:00' and Case_Time<='2018-04-08 23:59:59';
commit;
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=1
where Case_Time>='2018-04-29 00:00:00' and Case_Time<='2018-04-29 23:59:59';
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=2
where Case_Time>='2018-04-30 00:00:00' and Case_Time<='2018-04-30 23:59:59';
update td_awp_source_data set holiydayname='五一劳动节',holiydaytotal=3,holiydayon=3
where Case_Time>='2018-05-01 00:00:00' and Case_Time<='2018-05-01 23:59:59';
update td_awp_source_data set week='16'
where Case_Time>='2018-04-28 00:00:00' and Case_Time<='2018-04-28 23:59:59';
commit;
*/

'''