# -*- coding: utf8 -*-
__author__ = 'mahongyan'
import PIL.Image as Image
import csv
import os

def drawpng(infile,outfile,xrange,yrange):
    newim=Image.new("RGBA",(xrange,yrange),(0,0,0,0))
    csvfile = file(infile, 'rb')
    reader = csv.reader(csvfile)
    y = 0
    for line in reader:
        x = 0
        if y == 0:
            pass
        else:
            for cell in line:
                if x==0:
                    pass
                else:
                    if cell == '3':
                         newim.putpixel((x,y),(0,255,0,255))
                    elif cell == '2':
                        newim.putpixel((x,y),(255,255,0,255))
                    elif cell == '1':
                        newim.putpixel((x,y),(255,0,0,255))
                    else:
                        newim.putpixel((x,y),(200,200,200,255))
                x=x+1
            #print x
        y=y+1
    #print y
    newim.save(outfile)
    csvfile.close()
    return "1000_1000.png"
if __name__ == '__main__':
    rootdir = 'E:\\ctfo\\ctfodayfile\\201706\\'
    files = os.listdir(rootdir)
    for f in files:
        if f.find(".csv") != -1:
            tempfile = file(rootdir+"\\"+f, 'rb')
            yrange = len(tempfile.readlines())
            tempfile.close()
            tempfile = file(rootdir+"\\"+f, 'rb')
            line = tempfile.readline()
            xrange = len(line.split(','))
            tempfile.close()
            drawpng(rootdir+"\\"+f,rootdir+"\\png\\"+f.split(',')[0]+".png",xrange,yrange)
    #drawpng("E:\\ctfo\\ctfodayfile\\201706\\"+"北京到上海".decode('utf-8')+"20170501.csv",1133,289)
