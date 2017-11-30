__author__ = 'Thinkpad'
# -*- coding: utf8 -*-
from lxml import etree
import httplib2
import warnings
def fxn():
    warnings.warn("deprecated", DeprecationWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
def getBaseInfo(url):

    http = httplib2.Http()
    response, content = http.request(url, 'GET',headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    })
    tree = etree.HTML(content)
    baseInfo_list = tree.xpath(u'//div[@class="touzhu_1"]/@data-mid')
    n = len(baseInfo_list)
    print baseInfo_list
    for i in range(n):
        print baseInfo_list[i]

url='http://www.okooo.com/jingcai/2016-10-26/'
if __name__=="__main__":
    getBaseInfo(url)