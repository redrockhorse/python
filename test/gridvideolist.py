import json
import  requests
grid_width = 0.03
grid_heigth = 0.03
# wfs_full_data = 'http://hmrc.palmgo.cn/geoserver/sf/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sf:toll_bd09_line_point&maxFeatures=25000&outputFormat=application%2Fjson&bbox=30.00941270901087,10.69485909762269,150.41800606835588,69.65606727035105,EPSG:4326&_=1584580305916'
wfs_full_data = 'http://92.168.23.82:8060/geoserver/sf/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sf:toll_bd09_line_point&maxFeatures=25000&outputFormat=application%2Fjson&bbox=30.00941270901087,10.69485909762269,150.41800606835588,69.65606727035105,EPSG:4326&_=1584580305916'

# with open('/Users/hongyanma/Desktop/1/data/geoserver-GetFeature.json','r') as f:
with requests.get(wfs_full_data) as r:
    # jsondata = json.load(f)
    # data = jsondata['data']
    # jsondata = json.load(f)
    jsondata = r.json()
    data = jsondata['features']
    print(len(data))
    maplevel ={}
    gridmap ={}
    result = {"type":"FeatureCollection","totalFeatures":100,"features":[]}
    for i in range(len(data)):
        print(data[i])
        lng = data[i]['properties']['longitude']
        lat = data[i]['properties']['latitude']
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
        result["features"].append(gridmap[no][0])
        print(no,len(gridmap[no]))
    print(i)
    result['totalFeatures'] = i
    with open('/Users/hongyanma/Desktop/1/data/allmapvideo.json','w') as outf:
        json.dump(result,outf)

