__author__ = 'mahy'
import random
roadlink_file = open('E:\\ctfo\\ctfodayfile\\201612\\1100-Dti.txt','r')
json_file = open('E:\\ctfo\\ctfodayfile\\201612\\1100.json', 'w+')
try:
    # line = roadlink_file.readline()
     jsonstr=''
     for  line in roadlink_file:
        #print line
        if line.find('_') != -1:
            links = line.split('#')
            for i in range(0,len(links)):
                #print links[i]
                coor=links[i].split('|')
                x=coor[3].split('_')[0]
                y=coor[3].split('_')[1]
                if(i==0):
                    jsonstr='{start:{x:'+x+',y:'+y+'},'
                    print '0-'+jsonstr
                elif(i==len(links)-1):
                    y=y.split(',')[0]
                    jsonstr+='end:{x:'+x+',y:'+y+'},count:'+ str(random.randrange(0, 100))+'},'
                    print '1-'+jsonstr
                else:
                    jsonstr+='end:{x:'+x+',y:'+y+'},count:'+ str(random.randrange(0, 100))+'},{start:{x:'+x+',y:'+y+'},'
                    print 'x-'+jsonstr
            print jsonstr
            json_file.write('['+jsonstr+']')
finally:
     roadlink_file.close()
     json_file.close( )

