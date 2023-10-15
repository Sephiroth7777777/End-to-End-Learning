#usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# @Time    : 2019/6/27 19:45
# @Author  : Yang Yuan
# @State   : 读取地图csv数据，导入mapbox生成轨迹,同时叠加多个坐标框
# @FileName: csv_to_mapbox_2.py
# @Software: vscode,python3
"""
from bottle import template
import webbrowser
import pandas as pd
import numpy as np

# articles = ['[121.69775466666667,31.276067333333336]','[121.79775466666667,31.376067333333336]']

def read_csv(file_name):
    csv_data = pd.read_csv(file_name)
    csv_data_new = csv_data[['latitude','longtitude']]
    articles = []
    for i in range(csv_data.shape[0]):
        articles_one = []
        articles_one.append(csv_data['longtitude'][i])
        articles_one.append(csv_data['latitude'][i])
        # print (str(articles_one))
        # articles.append(str(articles_one))
        articles.append(articles_one)
        # print (articles)
    return articles

def generate(title,file_name):
    #定义想要生成的Html的基本格式
    #使用%来插入python代码
    template_demo="""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8' />
        %
        <title>{{title}}</title>
        %
        <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
        <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet' />
        <style>
            body { margin:0; padding:0; }
            #map { position:absolute; top:0; bottom:0; width:100%; }
        </style>
        <script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
        <script src="./papaparse.min.js"></script>

    </head>
    <body>
    
    <div id='map'></div>

    <script>
    //read csv file
    

    mapboxgl.accessToken = 'pk.eyJ1Ijoic2VwaGlyb3RoIiwiYSI6ImNqd3pxOW9vZDBocWIzeXM4MGM3NTM3a2YifQ.NeOB39h4oWH0fxHs9Z4PXw';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [121.59775466666667, 31.176067333333336],
        zoom: 16
    });

    map.on('load', function () {    
        map.addLayer({
            "id": "route",
            "type": "line",
            "source": {
                "type": "geojson",
                "data": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            % for link in items:
                            {{link}},
                            %end
                        ]
                    }
                }
            },
            "layout": {
                "line-join": "round",
                "line-cap": "round"
            },
            "paint": {
                "line-color": "#000000",
                "line-width": 8
            }
        });

        % for link in itemNew:
        map.addLayer({
            "id": "{{link.index}}",
            "type": "line",
            "source": {
                "type": "geojson",
                "data": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "LineString",
                        "coordinates":
                                    {{link}},
                    }
                }
            },
            "layout": {
                "line-join": "round",
                "line-cap": "round"
            },
            "paint": {
                "line-color": "#ff0000",
                "line-width": 3
            }
        });
        %end

    });
    </script>
    """

    articles = read_csv(file_name)
    # v1 = [21, 34, 45]
    # v2 = [55, 25, 77]
    # v = list(map(lambda x: x[0]-x[1], zip(v2, v1)))
    # print (v)
    margin = 0.00030
    margin1 = 0.00027
    arctileNew = []
    arctileNumber = []
    j = 1
    for i in range(len(articles)):
        if i%50 == 0:
            arctile_1 = []
            arctile_2 = []
            arctile_3 = []
            arctile_4 = []
            arctile_5 = []
            arctile_6 = []
            # print (articles[i])
            arctile_1.append(articles[i][0]+margin)
            arctile_1.append(articles[i][1]-margin1)
            arctile_2.append(articles[i][0]+margin)
            arctile_2.append(articles[i][1]+margin1)
            arctile_3.append(articles[i][0]-margin)
            arctile_3.append(articles[i][1]+margin1)
            arctile_4.append(articles[i][0]-margin)
            arctile_4.append(articles[i][1]-margin1)
            arctile_5.append(articles[i][0]+margin)
            arctile_5.append(articles[i][1]-margin1)
            arctile_6.append(arctile_1)
            arctile_6.append(arctile_2)
            arctile_6.append(arctile_3)
            arctile_6.append(arctile_4)
            arctile_6.append(arctile_5)
            arctileNew.append(arctile_6)
            arctileNumber.append(j)
            j += 1
            print (arctileNumber)

    html = template(template_demo,title=title,items=articles,itemNew=arctileNew,itemNumber=arctileNumber)
    # print (articles)
    # print (arctileNew)

    with open("test3.html",'wb') as f:
        f.write(html.encode('utf-8'))

def main():
    title = "Add a GeoJSON line"
    file_name = "match.csv"
    generate(title,file_name)

if __name__ == '__main__':
    main()
    webbrowser.open("test3.html")    #使用浏览器打开html

