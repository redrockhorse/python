__author__ = 'mahy'
import PIL.Image as Image


def transparent(infile):
    #open png,covert it into 'RGBA mode',resize it,get data then make a datalist
    #datalist=list(Image.open(infile,'r').convert('RGBA').resize((1000,1000),Image.BILINEAR).getdata())
    #color(0,0,0,0) is transparent
    newim=Image.new("RGBA",(1000,1000),(0,0,0,0))
    for x in range(1000):
        for y in range(1000):
            #color(255,255,255,255) is 'white'
            #if datalist[1000*y+x]==(255,255,255,255):
            if y<500 and x<500:
                newim.putpixel((x,y),(255,0,0,255))
            else:
                pass
    newim.save("E:\\ctfo\\ctfodayfile\\201706\\png\\1000_1000.png")
    return "1000_1000.png"
transparent("E:\\ctfo\\ctfodayfile\\201706\\png\\test.png")