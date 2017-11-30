import math
import PIL.Image as Image

lenm = ['501','300','1200','1800']

tlist = [['1','3','3','2','1'],['2','3','2','1','0'],['3','2','1','0','3'],['4','1','0','3','2'],['5','0','3','2','1']]

intlen = [2,1,4,3]

   
newim = Image.new('RGB',(4,len(tlist)-1))
for y in range(1,len(tlist)):
    pos = 1
    for x in range(1,len(tlist[0])):
        if tlist[y][x] == '3':
            for i in range(intlen[x-1]):
                newim.putpixel((pos-1,y-1),(0,255,0))
                pos += 1
        elif tlist[y][x] == '2':
            for i in range(intlen[x-1]):
                newim.putpixel((pos-1,y-1),(255,255,0))
                pos += 1
        elif tlist[y][x] == '1':
            for i in range(intlen[x-1]):
                newim.putpixel((pos-1,y-1),(255,0,0))
                pos += 1
        else:
            for i in range(intlen[x-1]):
                newim.putpixel((pos-1,y-1),(200,200,200))
                pos += 1
newim.show()
