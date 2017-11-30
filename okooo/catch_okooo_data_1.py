__author__ = 'Thinkpad'
# -*- coding: utf8 -*-
from lxml import etree
import httplib2
import spynner
def getBaseInfo(url):

    http = httplib2.Http(".cache")
    response, content = http.request(url, 'GET',headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    })
    tree = etree.HTML(content)
    baseInfo_list = tree.xpath(u'//div[@class="touzhu_1"]/@data-mid')
    n = len(baseInfo_list)
    print baseInfo_list
    for i in range(n-1):
        print baseInfo_list[i]

url='http://www.okooo.com/jingcai/'
if __name__=="__main__":
    getBaseInfo(url)
    browser = spynner.Browser()
    browser.load(url)
    browser.show()