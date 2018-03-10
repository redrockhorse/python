
#Author: guosm.smth@163.com
#Date: 2017/7/19
# cal_dis 函数经过测试．


import math

# 将经纬度转换成米制平面坐标.
def sub_guss_fuc(cx1, cy1, loc):

    # 高斯投影分带.
    zone_num = 0

    if loc == 0:
        zone_num = int(cy1 / 6) + 1
        loc = zone_num * 6 - 3
    else:
        zone_num = int(loc / 6) + 1

    #以弧度为单位的经纬度数值.

    cir_cx1 = cx1 / 180 * 3.1415926
    cir_cy1 = (cy1 - loc) / 180 * 3.1415926 # 同时计算了中央经线

    #1980 坐标系参数.
    a = 6378245.00 # 椭圆长轴.
    b = 6356863.50 # 椭圆短轴.
    sqre1 = (a * a - b * b) / (a * a) #第一偏心率平方.

    sinb = math.sin(cir_cx1)
    cosb = math.cos(cir_cx1)

    #子午圈曲率半径.
    M = a * (1 - sqre1) / (1 - sqre1 * sinb * sinb) / math.sqrt(1 - sqre1 * sinb * sinb)
    #卯酉圈曲率半径.
    N = a / math.sqrt(1 - sqre1 * sinb * sinb)
    sqrita = N / M - 1

    #该纬度点到赤道的子午线弧长
    s = a * (1 - sqre1) * (1.00505117739 * cir_cx1 - 0.00506237764 / 2 * math.sin(2 * cir_cx1) \
                           + 0.0000106245 / 4 * math.sin(4 * cir_cx1) - 0.00000002081 / 6 * math.sin(6 * cir_cx1))

    tanb = math.tan(cir_cx1)

    x1 = s + cir_cy1 * cir_cy1 * N / 2 * sinb * cosb \
         + cir_cy1 * cir_cy1 * cir_cy1 * cir_cy1 * N / 24 * sinb * cosb * cosb * cosb \
           * (5 - tanb * tanb + 9 * sqrita * sqrita + 4 * sqrita)

    y1 = cir_cy1 * N * cosb + cir_cy1 * cir_cy1 * cir_cy1 * N / 6 * cosb * cosb * cosb * (1 - tanb * tanb + sqrita) \
         + cir_cy1 * cir_cy1 * cir_cy1 * cir_cy1 * cir_cy1 \
         * N / 120 * cosb * cosb * cosb * cosb * cosb * (5 - 18 * tanb * tanb + tanb * tanb * tanb * tanb)

    y1 = y1 + 500000 + zone_num * 1.0e+6

    return (x1, y1)

# 将经纬度转换成米制平面坐标的主调函数，目的是参数调用是将经纬度互换一下.
def cal_guass_from_lb(cx1, cy1, loc):
    (x1, y1) = sub_guss_fuc(cy1, cx1, loc)

    return (x1, y1)

#计算2个经纬度之间的距离.
def cal_dis(cx1, cy1, cx2, cy2):

    # 中心位置标识.
    center_loc = (int(cx1 / 6) + 1) * 6 - 3

    #球面坐标转平面坐标.
    (x1, y1) = cal_guass_from_lb(cx1, cy1, center_loc)
    (x2, y2) = cal_guass_from_lb(cx2, cy2, center_loc)

    dis = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    return dis

# 计算2个经纬度之间的向量夹角.
def cal_angle(cx1, cy1, cx2, cy2):

    # 计算向量.
    vec_x = cx2 - cx1
    vec_y = cy2 - cy1

    # 相同坐标输入或离的太近.
    if math.fabs(vec_x) < 1e-8 and math.fabs(vec_y) < 1e-8:
        return -1

    #  x=0 y>0 经度相同且纬度增大
    elif math.fabs(vec_x) < 1e-8 and vec_y > 1e-8:
        return 0

    # x>0 y=0 经度增大且纬度相同.
    elif vec_x > 1e-8 and math.fabs(vec_y) < 1e-8:
        return 90

    # x=0 y<0 经度相同且纬度减小.
    elif math.fabs(vec_x) < 1e-8 and -1 * vec_y > 1e-8:
        return 180

    # x<0 y=0 经度减小且纬度相同.
    elif -1 * vec_x > 1e-8 and math.fabs(vec_y) < 1e-8:
        return 270

    else:
        # 1或2 象限.
        if vec_x > 1e-8:
            return 90 - int(math.atan(vec_y / vec_x) * 180 / 3.1415926)
        else:
            return 270 - int(math.atan(vec_y / vec_x) * 180 / 3.1415926)

# 计算2个向量角的夹角.
def cal_inc_angle(ang1, ang2):

    if ang1 == -1 or ang2 == -1:
        return -1

    inc_angle = abs(ang1 - ang2)

    if inc_angle <= 180:
        return inc_angle
    else:
        return 360 - inc_angle

# 计算2个向量角的平分线的角度.
def cal_bisection(ang1, ang2):

    max_ang = ang1
    min_ang = ang2

    if ang2 > ang1:
        max_ang = ang2
        min_ang = ang1


    bis_angle = max_ang - int((max_ang - min_ang) / 2)
    return bis_angle


# test main.

# gps_cx1 = 114.071087
# gps_cy1 = 38.275933
#
# gps_cx2 = 115.
# gps_cy2 = 38.
#
# dis = cal_dis(gps_cx1, gps_cy1, gps_cx2, gps_cy2)
# angle = cal_angle(gps_cx1, gps_cy1, gps_cx2, gps_cy2)
# print(angle)