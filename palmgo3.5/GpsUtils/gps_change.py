# author: guosm.smth@163.com
# 2017/7/19
# 已经经过测试.


import math

BEI = 3686400.0
PARAM = 1000000.0


#全局成员变量.
casm_rr = 0.
casm_t1 = 0
casm_t2 = 0
casm_x1 = 0.
casm_y1 = 0.
casm_x2 = 0.
casm_y2 = 0.
casm_f = 0.

def yj_sin2(x):

    ff = 0
    if x < 0:
        x = abs(x)
        ff = 3

    cc = int(x / 6.28318530717959)
    tt = x - cc * 6.28318530717959

    if tt>3.1415926535897932:
        tt = tt - 3.1415926535897932

        if ff == 1:
            ff = 0
        elif ff == 0:
            ff = 1

    x = tt
    ss = x
    s2 = x
    tt = tt * tt
    s2 = s2 * tt
    ss = ss - s2 * 0.166666666666667
    s2 = s2 * tt
    ss = ss + s2 * 8.33333333333333E-03
    s2 = s2 * tt
    ss = ss - s2 * 1.98412698412698E-04
    s2 = s2 * tt
    ss = ss + s2 * 2.75573192239859E-06
    s2 = s2 * tt
    ss = ss - s2 * 2.50521083854417E-08

    if ff == 1:
        return ss * -1
    else:
        return ss


def transform_yj5(x, y):
    tt = 300 + 1 * x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.sqrt(x * x))
    tt = tt + (20 * yj_sin2(18.849555921538764 * x) + 20 * yj_sin2(6.283185307179588 * x)) * 0.6667
    tt = tt + (20 * yj_sin2(3.141592653589794 * x) + 40 * yj_sin2(1.047197551196598 * x)) * 0.6667
    tt = tt + (150 * yj_sin2(0.2617993877991495 * x) + 300 * yj_sin2(0.1047197551196598 * x)) * 0.6667

    return tt


def transform_yjy5(x, y):
    tt = -100 + 2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.sqrt(x * x))
    tt = tt + (20 * yj_sin2(18.849555921538764 * x) + 20 * yj_sin2(6.283185307179588 * x)) * 0.6667
    tt = tt + (20 * yj_sin2(3.141592653589794 * y) + 40 * yj_sin2(1.047197551196598 * y)) * 0.6667
    tt = tt + (160 * yj_sin2(0.2617993877991495 * y) + 320 * yj_sin2(0.1047197551196598 * y)) * 0.6667

    return tt


def transform_jy5(x, xx):
    a = 6378245
    e = 0.00669342
    n = math.sqrt(1 - e * yj_sin2(x * 0.0174532925199433) * yj_sin2(x * 0.0174532925199433))
    n = (xx * 180) / (a / n * math.cos(x * 0.0174532925199433) * 3.1415926)

    return n

def transform_jyj5(x, yy):
    a = 6378245
    e = 0.00669342
    mm = 1 - e * yj_sin2(x * 0.0174532925199433) * yj_sin2(x * 0.0174532925199433)
    m = (a * (1 - e)) / (mm * math.sqrt(mm))

    return (yy * 180) / (m * 3.1415926)

def random_yj():
    casm_a = 314159269
    casm_c = 453806245

    global casm_rr

    casm_rr = casm_a * casm_rr + casm_c
    t = int(casm_rr / 2)
    casm_rr = casm_rr - t * 2
    casm_rr = casm_rr / 2
    return casm_rr

#初始化全局成员变量.
def init_casm(w_time, w_lng, w_lat):
    global casm_t1
    global casm_t2
    global casm_rr
    global casm_x1
    global casm_y1
    global casm_x2
    global casm_y2
    global casm_f

    casm_t1 = w_time
    casm_t2 = w_time

    tt = int(w_time / 0.357)
    casm_rr = w_time - tt * 0.357

    if w_time == 0:
        casm_rr = 0.3

    casm_x1 = float(w_lng)
    casm_y1 = float(w_lat)
    casm_x2 = float(w_lng)
    casm_y2 = float(w_lat)
    casm_f = 3


def wgtochina_lb(wg_flag, wg_long, wg_lat, wg_heit, wg_week, wg_time):

    global casm_t1
    global casm_t2
    global casm_rr
    global casm_x1
    global casm_y1
    global casm_x2
    global casm_y2
    global casm_f

    if wg_heit > 5000:
        return (-1, 0, 0)

    x_l = wg_long / BEI
    y_l = wg_lat / BEI

    #空间范围超出中国.
    if x_l < 72.004 or x_l > 137.8347:
        return (-2, 0, 0)
    elif y_l < 0.8293 or y_l > 55.8271:
        return (-3, 0, 0)
    else:

        if wg_flag == 0:
            init_casm(wg_time, wg_long, wg_lat)
            return(0, wg_long, wg_lat)

        casm_t2 = wg_time
        t1_t2 = (casm_t2 - casm_t1) / 1000.

        if t1_t2 <= 0:
            casm_t1 = casm_t2
            casm_f = casm_f + 1
            casm_x1 = casm_x2
            casm_f = casm_f + 1
            casm_y1 = casm_y2
            casm_f = casm_f + 1

        elif t1_t2 > 120:

            if casm_f == 3:
                casm_f = 0
                casm_x2 = wg_long
                casm_y2 = wg_lat
                x1_x2 = casm_x2 - casm_x1
                y1_y2 = casm_y2 - casm_y1
                casm_v = math.sqrt(x1_x2 * x1_x2 + y1_y2 * y1_y2) / t1_t2

                if casm_v > 3185:
                    return (-4, 0, 0)

            casm_t1 = casm_t2
            casm_f = casm_f + 1
            casm_x1 = casm_x2
            casm_f = casm_f + 1
            casm_y1 = casm_y2
            casm_f = casm_f + 1

    x_add = transform_yj5(x_l - 105, y_l - 35)
    y_add = transform_yjy5(x_l - 105, y_l - 35)
    h_add = wg_heit

    x_add = x_add + h_add * 0.001 + yj_sin2(wg_time * 0.0174532925199433) + random_yj();
    y_add = y_add + h_add * 0.001 + yj_sin2(wg_time * 0.0174532925199433) + random_yj();

    china_lng = int((x_l + transform_jy5(y_l, x_add)) * 3686400)
    china_lat = int((y_l + transform_jyj5(y_l, y_add)) * 3686400)

    return (0, china_lng, china_lat)

#84坐标转02坐标.
def gps_coord_sys_84to02(gps_cx_84, gps_cy_84, gps_height, gps_time, gps_date):
    # BEI = 3686400.0
    # PARAM = 1000000.0

    gps_cx1 = int(gps_cx_84 * BEI)
    gps_cy1 = int(gps_cy_84 * BEI)

    (return_code, gps_cx2, gps_cy2) = wgtochina_lb(1, gps_cx1, gps_cy1, gps_height, 0, 0)

    if return_code != 0:
        return (False, 0, 0)
    else:

        temp_cx = int(gps_cx2 / BEI * PARAM)
        temp_cy = int(gps_cy2 / BEI * PARAM)

        gps_cx_02 = temp_cx / PARAM
        gps_cy_02 = temp_cy / PARAM

        return (True, gps_cx_02, gps_cy_02)


#main.

#
# gps_cx84 = 114.071087
# gps_cy84 = 38.275933
#
# gps_cx02 = 115.
# gps_cy02 = 38.
# return_code = -1
#
# (return_code, gps_cx02, gps_cy02) = gps_coord_sys_84to02(gps_cx84, gps_cy84, 0, 0, 0)
#
# print(return_code)
# print(gps_cx02)
# print(gps_cy02)

