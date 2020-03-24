# -*- coding:utf-8 -*-
# @Time : 2020/3/13 上午9:33
# @Author: kkkkibj@163.com
# @File : road_condition_survey.py
# 路况对比器
import argparse
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import math
import cv2
import matplotlib.pyplot as plt
import numpy as np

chromedriver = '/Users/hongyanma/Downloads/chromedriver'

xmin, ymin = (113.192658, 23.047543)  # 左下角
xmax, ymax = (113.403306, 23.170221)  # 右上角

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


def UTMtoGeog(x, y):  # 平面坐标转WGS84坐标系
    k0 = 0.9996
    a = 6378137
    f = 1 / 298.257222101
    b = a * (1 - f)
    e = math.sqrt(1 - (b / a) * (b / a))
    esq = (1 - (b / a) * (b / a))
    e0sq = e * e / (1 - e * e)
    zone = 49
    zcm = 3 + 6 * (zone - 1) - 180
    e1 = (1 - math.sqrt(1 - e * e)) / (1 + math.sqrt(1 - e * e))
    M0 = 0
    M = M0 + y / k0
    mu = M / (a * (1 - esq * (1 / 4 + esq * (3 / 64 + 5 * esq / 256))))
    phi1 = mu + e1 * (3 / 2 - 27 * e1 * e1 / 32) * math.sin(2 * mu) + e1 * e1 * (
            21 / 16 - 55 * e1 * e1 / 32) * math.sin(4 * mu)
    phi1 = phi1 + e1 * e1 * e1 * (math.sin(6 * mu) * 151 / 96 + e1 * math.sin(8 * mu) * 1097 / 512)
    C1 = e0sq * math.pow(math.cos(phi1), 2)
    T1 = math.pow(math.tan(phi1), 2)
    N1 = a / math.sqrt(1 - math.pow(e * math.sin(phi1), 2))
    R1 = N1 * (1 - e * e) / (1 - math.pow(e * math.sin(phi1), 2))
    D = (x - 500000) / (N1 * k0)
    phi = (D * D) * (1 / 2 - D * D * (5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * e0sq) / 24)
    phi = phi + math.pow(D, 6) * (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * e0sq - 3 * C1 * C1) / 720
    phi = phi1 - (N1 * math.tan(phi1) / R1) * phi
    lng = D * (1 + D * D * ((-1 - 2 * T1 - C1) / 6 + D * D * (
            5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * e0sq + 24 * T1 * T1) / 120)) / math.cos(phi1)
    drad = math.pi / 180
    lngd = zcm + lng / drad
    latd = phi / drad + 0.0000001
    xd = math.floor(10000000 * lngd) / 10000000
    yd = math.floor(10000000 * latd) / 10000000
    return xd, yd


def newtoold(x, y):  # 像素坐标转平面坐标
    xmin, xmax = (708040.22626217513, 788040.22626217513)
    ymin, ymax = (2417700.9535092441, 2497700.9535092441)
    scalex = (xmax - xmin) / 18480
    scaley = (ymax - ymin) / 18480
    x_old = x * scalex + xmin
    y_old = ymax - y * scaley
    return x_old, y_old


def transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (135.05 > lng > 73.66 and 53.55 > lat > 3.86)


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 扁率
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def savaBaiduMapAsPng(lon, lat, zoom, waittime):
    lon_int_str = str(int(round(float(lon), 6) * 100000))
    lat_int_str = str(int(round(float(lat), 6) * 100000))
    zoom = str(int(zoom) + 1.5)  # 百度的zoom要在搜狗的基础上+1
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.implicitly_wait(100)
    driver.get(
        'https://map.baidu.com/@' + lon_int_str + ',' + lat_int_str + ',' + zoom + 'z/maplayer%3Dtrafficrealtime')
    time.sleep(int(waittime))
    try:
        EC.presence_of_element_located((By.XPATH, '//canvas'))
        with open('cleanbaidumap.js', 'r', encoding='utf8') as fr:
            js_str = fr.read()
            driver.execute_script(js_str)
        driver.save_screenshot('/Users/hongyanma/Desktop/mapcompare/baidumap.png')
    finally:
        driver.quit()


def savaSouGoMapAsPng(lon, lat, zoom, waittime):
    lon_int_str = str(int(round(float(lon), 6) * 100000))
    lat_int_str = str(int(round(float(lat), 6) * 100000))
    zoom = str(int(zoom))
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.implicitly_wait(100)
    driver.get('http://map.sogou.com/#c=' + lon_int_str + ',' + lat_int_str + ',' + zoom + '&tf=1')
    time.sleep(int(waittime))
    try:
        EC.presence_of_element_located((By.XPATH, '//*[id=maparea]'))
        with open('cleansogoumap.js', 'r', encoding='utf8') as fr:
            js_str = fr.read()
            driver.execute_script(js_str)
        time.sleep(int(waittime))
        driver.save_screenshot('/Users/hongyanma/Desktop/mapcompare/sougoumap.png')
    finally:
        driver.quit()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--lon', type=str,
                        help='经度', default='129.49031')
    parser.add_argument('--lat', type=str,
                        help='纬度', default='48.48590')
    parser.add_argument('--zoom', type=str,
                        help='地图缩放等级', default='13')
    parser.add_argument('--waittime', type=str,
                        help='等待浏览器加载时间,单位秒', default='10')
    return parser.parse_args(argv)


baidu_jam_levev_4 = [[0, 150, 28], [4, 255, 255]]
baidu_jam_levev_3 = [[0, 196, 198], [4, 216, 219]]
baidu_jam_levev_2 = [[13, 150, 230], [33, 170, 255]]
baidu_jam_levev_1 = [[57, 90, 200], [80, 168, 220]]

sogou_jam_levev_4 = [[0, 200, 158], [4, 232, 178]]
sogou_jam_levev_3 = [[0, 150, 198], [4, 255, 255]]
sogou_jam_levev_2 = [[13, 150, 200], [36, 255, 255]]
sogou_jam_levev_1 = [[50, 90, 100], [80, 255, 255]]


# 抽取路况线
def extractTf(img_path):
    result_img = []
    dark_red = np.uint8([[[163, 0, 4]]])
    hsv_dark_red = cv2.cvtColor(dark_red, cv2.COLOR_BGR2HSV)
    print(hsv_dark_red)

    red = np.uint8([[[233, 0, 15]]])
    hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
    print(hsv_red)

    yellow = np.uint8([[[253, 250, 56]]])
    hsv_yellow = cv2.cvtColor(yellow, cv2.COLOR_BGR2HSV)
    print(hsv_yellow)

    green = np.uint8([[[68, 204, 106]]])
    hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    print(hsv_green)

    img = cv2.imread('/Users/hongyanma/Desktop/mapcompare/sougoumap.png')
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower_darkred = np.array([0, 120, 46])
    # upper_darkred = np.array([10, 255, 200])
    lower_darkred = np.array(baidu_jam_levev_4[0])
    upper_darkred = np.array(baidu_jam_levev_4[1])
    mask = cv2.inRange(hsv, lower_darkred, upper_darkred)
    darkred_things = cv2.bitwise_and(img, img, mask=mask)

    lower_red = np.array([0, 100, 46])
    upper_red = np.array([10, 200, 255])
    lower_red = np.array(baidu_jam_levev_3[0])
    upper_red = np.array(baidu_jam_levev_3[1])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    red_things = cv2.bitwise_and(img, img, mask=mask)

    lower_yellow = np.array([11, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    lower_yellow = np.array(sogou_jam_levev_2[0])
    upper_yellow = np.array(sogou_jam_levev_2[1])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_things = cv2.bitwise_and(img, img, mask=mask)

    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    lower_green = np.array(sogou_jam_levev_1[0])
    upper_green = np.array(sogou_jam_levev_1[1])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_things = cv2.bitwise_and(img, img, mask=mask)

    tf_img = cv2.bitwise_or(green_things, yellow_things)
    tf_img = cv2.bitwise_or(red_things, tf_img)
    tf_img = cv2.bitwise_or(darkred_things, tf_img)
    # cv2.imshow('source', cv2.cvtColor(tf_img, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    cv2.namedWindow("tfimge", 0);
    cv2.resizeWindow("tfimge", 640, 480);
    cv2.imshow("tfimge", tf_img)
    cv2.waitKey(0)
    cv2.imwrite('/Users/hongyanma/Desktop/mapcompare/sogou_tf.png',tf_img)
    # cv2.imshow('source', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    # cv2.imshow('source', cv2.cvtColor(darkred_things, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    # cv2.imshow('source', cv2.cvtColor(red_things, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    # cv2.imshow('source', cv2.cvtColor(yellow_things, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)
    # cv2.imshow('source', cv2.cvtColor(green_things, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)

    # result_img.append(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # result_img.append(cv2.cvtColor(darkred_things, cv2.COLOR_RGB2BGR))
    # result_img.append(cv2.cvtColor(red_things, cv2.COLOR_RGB2BGR))
    # result_img.append(cv2.cvtColor(yellow_things, cv2.COLOR_RGB2BGR))
    # result_img.append(cv2.cvtColor(green_things, cv2.COLOR_RGB2BGR))
    #
    # plt.figure(1)
    # i_c = len(result_img)
    # for i in range(i_c):
    #     plt.subplot(1, i_c, i + 1)
    #     plt.imshow(result_img[i])
    #     plt.axis('off')
    #     plt.title('tf' + str(i), fontsize=8)
    #     # plt.pause(1)
    # plt.show(1)


def hougthLinesMap():
    img = cv2.imread('/Users/hongyanma/Desktop/mapcompare/baidumap.png')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    cv2.imshow('soure', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('gray', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.imshow('gray1', gray1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    gray = cv2.bilateralFilter(gray, 3, 15, 75)
    cv2.imshow('bf-gray', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.MORPH_RECT
    # cv2.MORPH_ELLIPSE
    gray = cv2.erode(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 3)), iterations=2)
    # gray = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 2)), iterations=2)

    cv2.imshow('oc-gray', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    gray = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))
    cv2.imshow('cv-gray', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    edges = cv2.Canny(gray, 50, 150)
    # cv2.imshow("edges", edges)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 38)
    # for line in lines:
    #     rho, theta = line[0]
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * a)
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * a)
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
    # cv2.imshow("houghLine", img)

    # plt.figure()
    cv2.imshow('edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(argv):
    lon = argv.lon
    lat = argv.lat
    zoom = argv.zoom
    waittime = argv.waittime
    savaBaiduMapAsPng(lon, lat, zoom, waittime)
    coordinate = bd09_to_gcj02(float(lon), float(lat))
    savaSouGoMapAsPng(coordinate[0], coordinate[1], zoom, waittime)


if __name__ == '__main__':
    # main(parse_arguments(sys.argv[1:]))
    extractTf('')
    # hougthLinesMap()
