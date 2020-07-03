import json
grid_width = 0.8
grid_heigth = 0.8
with open('/Users/hongyanma/Desktop/1/data/aa.json','r') as f:
    # jsondata = json.load(f)
    # data = jsondata['data']
    data = json.load(f)
    print(len(data))
    maplevel ={}
    gridmap ={}
    result = []
    for i in range(len(data)):
        print(data[i])
        lng = data[i]['longitude']
        lat = data[i]['latitude']
        grid_x = int(float(lng)/grid_width)
        grid_y = int(float(lat)/grid_heigth)
        grid_no ='g'+'_' +str(grid_x)+'_'+str(grid_y)
        if grid_no in gridmap:
            pass
        else:
            gridmap[grid_no] = []
        gridmap[grid_no].append(data[i])

        # ml = data[i]['mapLevelStart']
        # if data[i]['mapLevelStart'] in maplevel:
        #     maplevel[ml] = maplevel[ml]+1
        # else:
        #     maplevel[ml] = 1
    i = 0
    for no in gridmap:
        i+=1
        result.append(gridmap[no][0])
        print(no,len(gridmap[no]))
    print(i)
    with open('/Users/hongyanma/Desktop/1/data/allmapvideo.json','w') as outf:
        json.dump(result,outf)

