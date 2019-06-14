import json

features_dic ={}#分组
with open('/Users/hongyanma/gitspace/front/front/geojson-vt/debug/1100_6_geo.json','r',encoding='gbk') as geofile:
    geoobj ={}
    geoobj=json.load(geofile)
    #json.dump(geofile)
    grid_no = '0'
    print(len(geoobj['features']))
    #124463
    j=0
    grid_nos =[]
    for i in range(len(geoobj['features'])):
        feature ={}
        name = geoobj['features'][i]['properties']['NAME']
        linkid =  geoobj['features'][i]['properties']['LINKID']
        #print(name)
        #print(linkid)
        feature["type"]= "Feature"
        feature["geometry"] = geoobj['features'][i]["geometry"]
        feature["properties"]={}
        feature["properties"]["LINKID"] = linkid

        if linkid[0:6] != grid_no:
            grid_no = linkid[0:6]
            if grid_no not in features_dic:
                features_dic[grid_no] =[]
                j += 1
                print(grid_no)
                grid_nos.append(grid_no)
        features_dic[grid_no].append(feature)

    print(grid_nos)
    #print(features_dic)
    for key in features_dic:
        with open('/Users/hongyanma/gitspace/front/front/geojson-vt/debug/bj/'+key+'.json','w') as outputfile:
            geojsonobj = {}
            geojsonobj['type'] = 'FeatureCollection'
            geojsonobj['features'] = features_dic[key]
            json.dump(geojsonobj,outputfile)




