# -*- coding:utf-8 -*-
#@Time : 2021/1/26 下午8:36
#@Author: kkkkibj@163.com
#@File : lwzx_risk_level.py
#疫情等级查询


from seleniumwire import webdriver
import json
import requests
from urllib.parse import urlencode
option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--disablegpu')
chromedriver = '/Users/hongyanma/Desktop/chromedriver87'
# chromedriver = 'd:\chromedriver'
# wsf_url = "http://192.168.220.248:8080/geoserver/wfs"
wsf_url = "http://111.205.13.109:54432/geoserver/wfs"
def getRiskLevelData():
    highcount ={}
    midcount = {}
    driver = webdriver.Chrome(chromedriver,chrome_options=option)
    driver.get('http://bmfw.www.gov.cn/yqfxdjcx/risk.html')
    for r in driver.requests:
        if r.response and r.url == 'http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson':
            reset_wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
                0) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>midcount</wfs:Name><wfs:Value>' + str(
                0) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>highcount</wfs:Name><wfs:Value>' + str(
                0) + '</wfs:Value></wfs:Property></wfs:Update></wfs:Transaction>'
            wfsresponse = requests.post(wsf_url, data=reset_wfs_xml)  # 先将数据还原
            print(wfsresponse.text)

            print(str(r.response.body,encoding="utf-8"))
            info = json.loads(str(r.response.body,encoding="utf-8"))
            data = info['data']

            print('--------------------------------')
            print('中风险地区：')
            for mid in data['middlelist']:
                province = mid['province']
                city = mid['city']
                if province == '上海市':
                    city = mid['county']
                key = province + '_' + city
                if mid['type'] == '1':
                    if key not in midcount:
                        midcount[key] = 0
                    midcount[key] += 1
                else:
                    if key not in midcount:
                        midcount[key] = 0
                    midcount[key] += len(mid['communitys'])
            print(midcount)
            for area in midcount:
                arr = area.split('_')
                # print(area)
                p = arr[0]
                c = arr[1]
                l = 1
                m = midcount[area]
                updatesql =''
                if p=='北京市' or p=='上海市':
                    updatesql = 'update public.lwzx_risk_level set risklevel='+ str(l) +',midcount='+str(m)+' where adminshe00=\''+p+'\'  and adminxiann=\''+c+'\';'

                    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
                    l) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>midcount</wfs:Name><wfs:Value>' + str(
                    m) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:And><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshe00</ogc:PropertyName><ogc:Literal>' + p + '</ogc:Literal></ogc:PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName>adminxiann</ogc:PropertyName><ogc:Literal>' + c + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:And></ogc:Filter></wfs:Update></wfs:Transaction>'
                    wfs_xml = wfs_xml.encode('utf-8')
                    print(wfs_xml)
                    wfsresponse = requests.post(wsf_url, data=wfs_xml)
                    print(wfsresponse.text)

                else:
                    updatesql = 'update public.lwzx_risk_level set risklevel=' + str(l) + ',midcount=' + str(
                    m) + ' where adminshe00=\'' + p + '\' and adminshina=\''+c+'\';'

                    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
                    l) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>midcount</wfs:Name><wfs:Value>' + str(
                    m) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:And><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshe00</ogc:PropertyName><ogc:Literal>' + p + '</ogc:Literal></ogc:PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshina</ogc:PropertyName><ogc:Literal>' + c + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:And></ogc:Filter></wfs:Update></wfs:Transaction>'
                    wfs_xml = wfs_xml.encode('utf-8')
                    wfsresponse = requests.post(wsf_url,  data=wfs_xml)
                    print(wfsresponse.text)
                print(updatesql)

            print('高风险地区：')
            for high in data['highlist']:
                province = high['province']
                city = high['city']
                if province == '上海市':
                    city = high['county']
                key = province+'_'+city
                if high['type'] == '1':
                    if key not in highcount:
                        highcount[key] = 0
                    highcount[key] += 1
                else:
                    if key not in highcount:
                        highcount[key] = 0
                    highcount[key] += len(high['communitys'])
            print(highcount)
            for area in highcount:
                arr = area.split('_')
                # print(area)
                p = arr[0]
                c = arr[1]
                l = 2
                m = highcount[area]
                updatesql =''
                if p=='北京市' or p=='上海市':
                    updatesql = 'update public.lwzx_risk_level set risklevel='+ str(l) +',highcount='+str(m)+' where adminshe00=\''+p+'\'  and adminxiann=\''+c+'\';'

                    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
                        l) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>highcount</wfs:Name><wfs:Value>' + str(
                        m) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:And><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshe00</ogc:PropertyName><ogc:Literal>' + p + '</ogc:Literal></ogc:PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName>adminxiann</ogc:PropertyName><ogc:Literal>' + c + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:And></ogc:Filter></wfs:Update></wfs:Transaction>'
                    wfs_xml = wfs_xml.encode('utf-8')
                    print(wfs_xml)
                    wfsresponse = requests.post(wsf_url,  data=wfs_xml)

                else:
                    updatesql = 'update public.lwzx_risk_level set risklevel=' + str(l) + ',highcount=' + str(
                    m) + ' where adminshe00=\'' + p + '\' and adminshina=\''+c+'\';'

                    wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
                        l) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>highcount</wfs:Name><wfs:Value>' + str(
                        m) + '</wfs:Value></wfs:Property><ogc:Filter><ogc:And><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshe00</ogc:PropertyName><ogc:Literal>' + p + '</ogc:Literal></ogc:PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName>adminshina</ogc:PropertyName><ogc:Literal>' + c + '</ogc:Literal></ogc:PropertyIsEqualTo></ogc:And></ogc:Filter></wfs:Update></wfs:Transaction>'
                    wfs_xml = wfs_xml.encode('utf-8')
                    wfsresponse = requests.post(wsf_url,  data=wfs_xml)

                print(updatesql)

# 更新WFS数据

def updateWfsStatus(highlist, midlist):
    reset_wfs_xml = '<wfs:Transaction service="WFS" version="1.0.0" xmlns:topp="http://www.openplans.org/topp" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wfs="http://www.opengis.net/wfs"><wfs:Update typeName="lwzx:lwzx_risk_level"><wfs:Property> <wfs:Name>risklevel</wfs:Name><wfs:Value>' + str(
        0) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>midcount</wfs:Name><wfs:Value>' + str(
        0) + '</wfs:Value></wfs:Property><wfs:Property> <wfs:Name>highcount</wfs:Name><wfs:Value>' + str(
        0) + '</wfs:Value></wfs:Property></wfs:Update></wfs:Transaction>'
    r = requests.post(wsf_url, data=reset_wfs_xml) #先将数据还原





if __name__ == '__main__':
    getRiskLevelData()

