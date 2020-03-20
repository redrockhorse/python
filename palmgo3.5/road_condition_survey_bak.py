# -*- coding:utf-8 -*-
#@Time : 2020/3/13 上午9:33
#@Author: kkkkibj@163.com
#@File : road_condition_survey.py
#路况对比器

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64
import time
driver = webdriver.Chrome('/Users/hongyanma/Downloads/chromedriver')
driver.implicitly_wait(100)
driver.get('https://map.baidu.com/@12949318,4848124,14z/maplayer%3Dtrafficrealtime')
time.sleep(5)

try:
    EC.presence_of_element_located((By.XPATH, '//canvas'))

    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//canvas'))
    # )
    # js_canvas = 'return document.querySelector("canvas")[0].toDataURL("image/png");'
    # 执行 JS 代码并拿到图片 base64 数据
    # im_info = driver.execute_script(js_canvas)  # 执行js文件得到带图片信息的图片数据
    with open('cleanbaidumap.js', 'r', encoding='utf8') as fr:
        js_str = fr.read()
        driver.execute_script(js_str)
    # print(im_info)
    # im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    # im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    # with open('bg.png', 'wb') as f:  # 保存图片到本地
    #     f.write(im_bytes)
    driver.save_screenshot('screenshot.png')


finally:
    driver.quit()


# time.sleep(10)
#下面的js代码根据canvas文档说明而来
# js_canvas = 'return document.querySelector("canvas").toDataURL("image/png");'
# # 执行 JS 代码并拿到图片 base64 数据
# im_info = driver.execute_script(js_canvas)  #执行js文件得到带图片信息的图片数据
# print(im_info)
# im_base64 = im_info.split(',')[1]  #拿到base64编码的图片信息
# im_bytes = base64.b64decode(im_base64)  #转为bytes类型
# with open('bg.png','wb') as f:  #保存图片到本地
#     f.write(im_bytes)
