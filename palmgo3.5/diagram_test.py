## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)

import xml.etree.ElementTree as ET
# from PIL import Image
import os
import os.path
# import cairosvg
# from skimage import io

# 参考文献：
# 1、http://blog.csdn.net/q_l_s/article/details/71629804 使用 Python ElementTree 生成 xml
# 2、http://blog.csdn.net/a102111/article/details/50806550 Python xml解析记录
# 3、http://www.jb51.net/article/79494.htm 深入解读Python解析XML的几种方式
# 4、http://blog.csdn.net/oatnehc/article/details/45537415 使用Python批量转换SVG文件为PNG或PDF文件
# 5、http://blog.csdn.net/einsteinlike/article/details/41803193 png图片结构分析与加密解密原理
# 6、http://www.jb51.net/article/62526.htm Python通过PIL获取图片主要颜色并和颜色库进行对比的方法
# 7、http://www.sioe.cn/yingyong/yanse-rgb-16/ RGB调色工具.

# 生成标准对比模板.
# 读取SVG模板的xml文件，提取“traffic”层的fill属性，修改后输出到新的.svg文件中.

def cal_dis_of_pixels(pixel1, pixel2):

    r = abs(pixel1[0] - pixel2[0])
    g = abs(pixel1[1] - pixel2[1])
    b = abs(pixel1[2] - pixel2[2])

    return int((r * r + g * g + b * b) / 3)

def format_svg_comp_sample(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    for child_root in root:

        if child_root.tag != '{http://www.w3.org/2000/svg}g':
            continue

        if '{http://www.inkscape.org/namespaces/inkscape}label' in child_root.attrib.keys():
            if child_root.attrib['{http://www.inkscape.org/namespaces/inkscape}label'] != 'Traffic':
                continue

        for cc_child in child_root:
            if cc_child.tag == '{http://www.w3.org/2000/svg}path':

                if 'style' in cc_child.attrib.keys():
                    style_value = cc_child.attrib['style']
                    color_str = style_value[5:12]
                    stype_new_value = style_value.replace(color_str, '#cccccc')
                    cc_child.attrib['style'] = stype_new_value

    tree.write(output_path, encoding='utf-8')


# 将SVG转换为png图片.
def convert_svg_to_png(svg_path, png_path):
    # svg = open(svg_path).read()
    # cairosvg.svg2pdf(bytestring=svg, write_to=png_path)
    pass


def png_from_d32_to_d8(input_path, output_path):
    im = Image.open(input_path)

    # PIL complains if you don't load explicitly
    im.load()

    # Get the alpha band
    alpha = im.split()[-1]

    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255,
    # and the rest to 0
    # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    # im.paste(255, mask)

    # The transparency index is 255
    # im.save(output_path, transparency=255)

    im.save(output_path, color=255)

# 比较两幅png图片（第一种方法）.
def comp1_png_with_sample(sample_path, png_path):
    output1 = open('C:\\Users\\Guo Shengmin\\Desktop\\图\\0001-sample-0128-data.csv', 'w')
    output2 = open('C:\\Users\\Guo Shengmin\\Desktop\\图\\0001-png-0128-data.csv', 'w')

    png1 = Image.open(sample_path)
    png1_colors = png1.getcolors() # 读取调色板索引.

    dict_png1_colors = {}
    for pc1 in png1_colors:
        dict_png1_colors[pc1[1]] = pc1[0]

    png2 = Image.open(png_path)
    png2_colors = png2.getcolors()

    dict_png2_colors = {}
    for pc2 in png2_colors:
        dict_png2_colors[pc2[1]] = pc2[0]

    png1_width = png1.size[0]
    png1_height = png1.size[1]

    png2_width = png2.size[0]
    png2_height = png2.size[1]

    if png1_width != png2_width or png1_height != png2_height:
        return -1

    for h in range(png1_height):
        str = ''
        for w in range(png1_width):
            pixel1 = png1.getpixel((w, h))
            str = str + '{:d}'.format(dict_png1_colors[pixel1]) + ','           # 基于像素到调色板中查颜色.

        output1.write(str + '\n')

    for h in range(png2_height):
        str = ''
        for w in range(png2_width):
            pixel2 = png2.getpixel((w, h))
            str = str + '{:d}'.format(dict_png2_colors[pixel2]) + ','

        output2.write(str + '\n')

    output1.close()
    output2.close()

# 打印在png中使用过的像素值.
def print_used_pixel(input_path_list, output_path):


    dict_pixel_rgb = {}

    for i in range(len(input_path_list)):
        input_path = input_path_list[i]

        print('proc: ' + input_path)
        png1 = Image.open(input_path).convert('RGB')

        png1_width = png1.size[0]
        png1_height = png1.size[1]

        for h in range(png1_height):
            for w in range(png1_width):
                pixel1 = png1.getpixel((w, h))
                pixel_rgb_str = '{:d}'.format(pixel1[0]) + '_' + '{:d}'.format(pixel1[1]) + '_' + '{:d}'.format(pixel1[2])

                if pixel_rgb_str in dict_pixel_rgb.keys():
                    dict_pixel_rgb[pixel_rgb_str] = dict_pixel_rgb[pixel_rgb_str] + 1
                else:
                    dict_pixel_rgb[pixel_rgb_str] = 1


    output = open(output_path, 'w')
    for pixel_rgb_key in dict_pixel_rgb.keys():
        output.write(pixel_rgb_key + ',' + '{:d}'.format(dict_pixel_rgb[pixel_rgb_key]) + '\n')
    output.close()

# 比较两幅png图片（第二种方法，还原成RGB像素，通过像素值来比较）.
def comp2_png_with_sample(sample_path, png_path):
    output1 = open('C:\\Users\\Guo Shengmin\\Desktop\\图\\0001-sample-0128-data.csv', 'w')
    output2 = open('C:\\Users\\Guo Shengmin\\Desktop\\图\\0001-png-0128-data.csv', 'w')

    print_pixel = False

    bg_err_pixel_cnt = 0
    bg_pixel_cnt = 0
    fg_red_pixel_cnt = 0
    fg_yellow_pixel_cnt = 0
    fg_green_pixel_cnt = 0
    fg_gray_pixel_cnt = 0
    fg_other_pixel_cnt = 0

    RGB_THRESHOLD = 0

    # 还原成RGB像素.
    png1 = Image.open(sample_path).convert('RGB')
    png2 = Image.open(png_path).convert('RGB')

    png1_width = png1.size[0]
    png1_height = png1.size[1]

    png2_width = png2.size[0]
    png2_height = png2.size[1]

    if png1_width != png2_width or png1_height != png2_height:
        return -1

    for h in range(png1_height):
        str1 = ''
        str2 = ''
        for w in range(png1_width):
            pixel1 = png1.getpixel((w, h))
            pixel2 = png2.getpixel((w, h))

            if print_pixel == True:
                pixel1_str = '{:d}'.format(pixel1[0]) + '_' + '{:d}'.format(pixel1[1]) + '_' + '{:d}'.format(pixel1[2])
                pixel2_str = '{:d}'.format(pixel2[0]) + '_' + '{:d}'.format(pixel2[1]) + '_' + '{:d}'.format(pixel2[2])

                str1 = str1 + pixel1_str + ','
                str2 = str2 + pixel2_str + ','

            if pixel1 != (153, 153, 153):   # back_ground. not #999999.
                if pixel1 != pixel2 and cal_dis_of_pixels(pixel1, pixel2) > 100:
                    bg_err_pixel_cnt = bg_err_pixel_cnt + 1
                    print('err bg ' + '{:d}'.format(h) + ', {:d}'.format(w))
                    print('pixel1 = (' + '{:d}'.format(pixel1[0]) + ',' + '{:d}'.format(pixel1[1]) + 

',' + '{:d}'.format(pixel1[2]) + ')')
                    print('pixel2 = (' + '{:d}'.format(pixel2[0]) + ',' + '{:d}'.format(pixel2[1]) + 

',' + '{:d}'.format(pixel2[2]) + ')')

                bg_pixel_cnt = bg_pixel_cnt + 1

            else:
                if pixel2 == (0, 255, 0):
                    fg_green_pixel_cnt = fg_green_pixel_cnt + 1
                elif pixel2 == (255, 255, 0):
                    fg_yellow_pixel_cnt = fg_yellow_pixel_cnt + 1
                elif pixel2 == (255, 0, 0):
                    fg_red_pixel_cnt = fg_red_pixel_cnt + 1
                elif pixel2 == (192, 192, 192) or pixel2 == (153, 153, 153):
                    fg_gray_pixel_cnt = fg_gray_pixel_cnt + 1
                else:

                    # if cal_dis_of_pixels(pixel1, pixel2) > 100:
                    fg_other_pixel_cnt = fg_other_pixel_cnt + 1
                    print('other fg ' + '{:d}'.format(h) + ', {:d}'.format(w))
                    print('pixel fg = (' + '{:d}'.format(pixel2[0]) + ',' + '{:d}'.format(pixel2[1]) + 

',' + '{:d}'.format(pixel2[2]) + ')')


        if print_pixel:
            output1.write(str1 + '\n')
            output2.write(str2 + '\n')

    output1.close()
    output2.close()
    bg_err_rate = bg_err_pixel_cnt / bg_pixel_cnt
    return (bg_err_pixel_cnt, bg_pixel_cnt, fg_red_pixel_cnt, fg_yellow_pixel_cnt, fg_green_pixel_cnt, 

\
            fg_gray_pixel_cnt, fg_other_pixel_cnt)



# svg_input_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\0001.svg'
# svg_output_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\0001-1.svg'
# # format_svg_comp_sample(svg_input_path, svg_output_path)
#
# svg_png_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\0001-sample---1.png'
#
# svg_png_path32 = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\0001-sample.png'
# svg_png_path8 = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\0001-sample8.png'
# png_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图示模板\\1100-0001.png'
# #comp1_png_with_sample(svg_png_path8, png_path)
#
#
# svg_png_path8 = 'C:\\Users\\Guo Shengmin\\Desktop\\图\\0128.png'
# png_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图\\0128-1740.png'
# # comp1_png_with_sample(svg_png_path8, png_path)
# svg_png_path8 = 'C:\\Users\\Guo Shengmin\\Desktop\\图\\0016.png'
# png_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图\\1100-0016.png'

# (bg_err, bg_cnt, red_cnt, yellow_cnt, green_cnt, gray_cnt, other_cnt) = comp2_png_with_sample(svg_png_path8, png_path)
#
# bg_rate = bg_err / bg_cnt
#
# print('bg_err = ' + '{:d}'.format(bg_err))
# print('bg_cnt = ' + '{:d}'.format(bg_cnt))
# print('bg_rate = ' + '{:.2f}'.format(bg_rate))
#
# print('red_cnt = ' + '{:d}'.format(red_cnt))
# print('yellow_cnt = ' + '{:d}'.format(yellow_cnt))
# print('green_cnt = ' + '{:d}'.format(green_cnt))
# print('gray_cnt = ' + '{:d}'.format(gray_cnt))
# print('other_cnt = ' + '{:d}'.format(other_cnt))



png_path_list = []
png_dir = 'C:\\Users\\Guo Shengmin\\Desktop\\图'
pixel_used_path = 'C:\\Users\\Guo Shengmin\\Desktop\\图\\pixel_count.csv'

# 扫描 match_table_dir 下的所有文件.
for parent,dirnames,filenames in os.walk(png_dir):
    for filename in filenames:
        if filename[-3:] == 'png':
            png_path_list.append(os.path.join(parent, filename))

print_used_pixel(png_path_list, pixel_used_path)

print('process ok.')