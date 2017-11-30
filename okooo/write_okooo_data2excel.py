__author__ = 'mahy'
# -*- coding: utf8 -*-
import xlwt
import MySQLdb
import time
import re
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
style_default = xlwt.XFStyle()
style_red = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
def create_excel_bysql(sql):
    cur.execute(sql)
    results = cur.fetchall()
    write_excel(results)

def set_style(resultflag,gameresult):#name,height,bold=False
  '''
  style = xlwt.XFStyle()
  font = xlwt.Font()
  font.name = name # 'Times New Roman'
  font.bold = bold
  font.color_index = 4
  font.height = height
  style.font = font
  '''
  style = style_default
  if(gameresult==resultflag):
    style = style_red
  return style

def write_excel(data):
    pattern = re.compile(r'\d*\.+\d*')
    excelfile = xlwt.Workbook()
    sheet1 = excelfile.add_sheet(u'sheet1',cell_overwrite_ok=True)
    columnames =["时间".decode('utf-8'),'联赛'.decode('utf-8'),'球队'.decode('utf-8'),'必发赔率'.decode('utf-8'),'必发交易量'.decode('utf-8'),'必发系数'.decode('utf-8'),'竞彩赔率'.decode('utf-8'),'竞彩交易量'.decode('utf-8'),'竞彩系数'.decode('utf-8'),'赛果'.decode('utf-8'),'比分'.decode('utf-8'),'净胜球'.decode('utf-8')]

    for i in range(0,len(columnames)):
        sheet1.write(0,i,columnames[i],set_style(1,2))
    l=0
    for rs in data:
        l+=1
        #print rs[0]
        #sheet1.write_merge(l,l+2,0,0,rs[0].strftime("%Y-%m-%d"),set_style('Times New Roman',220,True))
        sheet1.write_merge(l,l+2,0,0,rs[0].strftime("%Y-%m-%d"))
        sheet1.write_merge(l,l+2,1,1,rs[1])
        sheet1.write_merge(l,l,2,2,rs[2])
        sheet1.write_merge(l+1,l+1,2,2,'VS')
        sheet1.write_merge(l+2,l+2,2,2,rs[3])

        bf_3=0.0
        bf_1=0.0
        bf_0=0.0
        sl_3=0.0
        sl_1=0.0
        sl_0=0.0
        sheet1.write(l,3,rs[4])
        sheet1.write(l,4,rs[5])
        sheet1.write(l+1,3,rs[6])
        sheet1.write(l+1,4,rs[7])
        sheet1.write(l+2,3,rs[8])
        sheet1.write(l+2,4,rs[9])
        gameresult=rs[16]
        if(rs[4]!=None and rs[5]!=None and rs[6]!=None and rs[7]!=None and rs[8]!=None and rs[9]!=None):
            sum = int(rs[5])+int(rs[7])+int(rs[9])
            sheet1.write(l,5,float(rs[4])*int(rs[5])/sum,set_style(3,gameresult))
            sheet1.write(l+1,5,float(rs[6])*int(rs[7])/sum,set_style(1,gameresult))
            sheet1.write(l+2,5,float(rs[8])*int(rs[9])/sum,set_style(0,gameresult))
            #sheet1.write(l,5,float(rs[4])*int(rs[5])/sum)
            #sheet1.write(l+1,5,float(rs[6])*int(rs[7])/sum)
            #sheet1.write(l+2,5,float(rs[8])*int(rs[9])/sum)
            bf_3=float(rs[4])*int(rs[5])/sum
            bf_1=float(rs[6])*int(rs[7])/sum
            bf_0=float(rs[8])*int(rs[9])/sum

        sheet1.write(l,6,rs[10])
        sheet1.write(l,7,rs[11])
        sheet1.write(l+1,6,rs[12])
        sheet1.write(l+1,7,rs[13])
        sheet1.write(l+2,6,rs[14])
        sheet1.write(l+2,7,rs[15])
        if(rs[10]!=None and rs[11]!=None and rs[12]!=None and rs[13]!=None and rs[14]!=None and rs[15]!=None):
            sheet1.write(l,8,float(rs[10])*float(pattern.match(rs[11]).group())/100,set_style(3,gameresult))
            sheet1.write(l+1,8,float(rs[12])*float(pattern.match(rs[13]).group())/100,set_style(1,gameresult))
            sheet1.write(l+2,8,float(rs[14])*float(pattern.match(rs[15]).group())/100,set_style(0,gameresult))
            #sheet1.write(l,8,float(rs[10])*float(pattern.match(rs[11]).group())/100)
            #sheet1.write(l+1,8,float(rs[12])*float(pattern.match(rs[13]).group())/100)
            #sheet1.write(l+2,8,float(rs[14])*float(pattern.match(rs[15]).group())/100)
            sl_3=float(rs[10])*float(pattern.match(rs[11]).group())/100
            sl_1=float(rs[12])*float(pattern.match(rs[13]).group())/100
            sl_0=float(rs[14])*float(pattern.match(rs[15]).group())/100
        sheet1.write_merge(l,l+2,9,9,rs[16])
        sheet1.write_merge(l,l+2,10,10,rs[17])
        sheet1.write_merge(l,l+2,11,11,rs[18])
        bf_3='%f' %bf_3
        bf_1='%f' %bf_1
        bf_0='%f' %bf_0
        sl_3='%f' %sl_3
        sl_1='%f' %sl_1
        sl_0='%f' %sl_0
        update(rs[0].strftime("%Y-%m-%d"),rs[1],rs[2],rs[3],bf_3,bf_1,bf_0,sl_3,sl_1,sl_0)
        l+=2
    fliename='okooo_'+time.strftime('%Y-%m-%d')
    defatul_f = r'E:\1579\excel'       # 默认路径
    #f = raw_input(u'请选择保存文件的路径：按回车跳过：')
    f=''
    f_name = r'\%s.xls' % fliename
    filepath = [defatul_f+f_name, f+f_name][f != '']
    excelfile.save(filepath)
    return True

def update(pdate,lg,hname,aname,bf_3,bf_1,bf_0,sl_3,sl_1,sl_0):
    update_sql='update td_ptl_okooo_data SET bf_coefficient_3='+bf_3+',bf_coefficient_1='+bf_1+',bf_coefficient_0='+bf_0+',sl_coefficient_3='+sl_3+',sl_coefficient_1='+sl_1+',sl_coefficient_0='+sl_0+' where pdate="'+pdate+'" and lg="'+lg+'" and hname="'+hname+'" and aname="'+aname+'"'
    print update_sql
    cur.execute(update_sql)
    conn.commit()

if __name__ == '__main__':
    sql="select pdate,lg,hname,aname,deal_bf_price_3,deal_bf_volume_3,deal_bf_price_1,deal_bf_volume_1,deal_bf_price_0,deal_bf_volume_0,sl_odds_3,sl_percent_3,sl_odds_1,sl_percent_1,sl_odds_0,sl_percent_0,gameresult,score,score_dif from td_ptl_okooo_data where pdate>='"+time.strftime('%Y-%m-%d')+"' order by id asc;"
    create_excel_bysql(sql)
    cur.close()
    conn.close()