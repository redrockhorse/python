# -*- coding:utf-8 -*-
#@Time : 2020/6/3 下午2:49
#@Author: kkkkibj@163.com
#@File : headless_browser.py
#无头浏览器测试

from selenium import webdriver
chromedriver = '/Users/hongyanma/Downloads/chromedriver83'
import time
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
driver.set_window_size(1920, 1080)
driver.get("http://hmrc.palmgo.cn/lwzx1/a1c64c3e6c9b76efcbccb8effd58fcad.html")
time.sleep(int(10))
driver.get_screenshot_as_file("/Users/hongyanma/Desktop/lwzx_headless.png")
driver.close()
