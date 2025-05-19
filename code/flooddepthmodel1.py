#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:27:34 2022

@author: kampanartpiyathamrongchai
"""

from osgeo import gdal
from osgeo import ogr
from osgeo import gdal_array
import numpy as np

def predictLevel(x,y,preX):
    res = np.polyfit(x, y, 2, rcond=None, full=False, w=None, cov=False)
    print(res)
    result = res[0]*pow(preX,2) + res[1]*preX + res[2]  
    return result


def genImage(data,stime, outfile):
    ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/bndgrd_geog.tif")
    bnd = np.array(ds.GetRasterBand(1).ReadAsArray())
    
    trans1 = ds.GetGeoTransform()
    proj1 = ds.GetProjection()
    
    #outfile11 = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Oct/demtiff/out11.tif"
    
    
    ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/dembrk_geog.tif")
    dem = np.array(ds.GetRasterBand(1).ReadAsArray())
    
    
    bnd[bnd<0.5]=np.nan
    dem[dem<0]=np.nan
    outimg = dem
    cols, rows = outimg.shape
    # print(dem)
    for w in data:
        # print(w['wlevel'][stime]-2)
        for i in range(len(dem)):
            for j in range(len(dem[i,:])):
                if bnd[i,j] != np.nan and bnd[i,j] == w['id']:
                    if dem[i,j] <= w['wlevel'][stime]-2:
                        outimg[i,j] = (w['wlevel'][stime]-2) - dem[i,j]
                    else:
                        outimg[i,j] = -9
    
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)
    outdata.GetRasterBand(1).SetNoDataValue(-9.0)
    outdata.GetRasterBand(1).WriteArray(outimg)
    outdata.SetGeoTransform(trans1)
    outdata.SetProjection(proj1)
    del(outdata)
    del(outimg)
    print('Done!')


def genPredictedImage(data,stime, outfile):
    ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/bndgrd_geog.tif")
    bnd = np.array(ds.GetRasterBand(1).ReadAsArray())
    
    trans1 = ds.GetGeoTransform()
    proj1 = ds.GetProjection()
    
    #outfile11 = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Oct/demtiff/out11.tif"
    
    
    ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/dembrk_geog.tif")
    dem = np.array(ds.GetRasterBand(1).ReadAsArray())
    
    
    bnd[bnd<0.5]=np.nan
    dem[dem<0]=np.nan
    outimg = dem
    cols, rows = outimg.shape
    # print(dem)
    for w in data:
        lev = predictLevel(w['time'], w['wlevel'], stime)
        print(lev)
        for i in range(len(dem)):
            for j in range(len(dem[i,:])):
                if bnd[i,j] != np.nan and bnd[i,j] == w['id']:
                    if dem[i,j] <= lev-2:
                    # if dem[i,j] <= w['wlevel'][11]-2:
                        outimg[i,j] = (lev-2) - dem[i,j]
                    else:
                        outimg[i,j] = -9
    
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)
    outdata.GetRasterBand(1).SetNoDataValue(-9.0)
    outdata.GetRasterBand(1).WriteArray(outimg)
    outdata.SetGeoTransform(trans1)
    outdata.SetProjection(proj1)
    del(outdata)
    del(outimg)
    print('Done!')
                        
    


data = [
        {"id" : 1, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.5,40.5,40.5,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
        {"id" : 2, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.1,40.1,40.2,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
        {"id" : 3, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.2,40.2,40.2,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
        {"id" : 4, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.1,41.3,41.4,41.5,41.8,41.9,42.1,42.5,42.8,42.9,43.1,43.2]  },
        {"id" : 5, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [39.5,39.8,40.2,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
        {"id" : 6, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.5,40.5,40.5,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
        {"id" : 7, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [39.5,39.5,39.5,39.5,39.5,40.0,40.2,40.5,40.8,41.2,41.4,41.7]  },
        {"id" : 8, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [38.0,38.0,38.1,38.5,38.8,38.9,39.1,39.5,39.8,39.9,39.9,40.1]  },
        {"id" : 9, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [39.0,39.0,39.0,39.1,39.2,39.2,39.4,39.5,39.6,39.7,39.9,40.0]  },
        {"id" : 10, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.1,40.2,40.2,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2]  },
]

data1 = [
        {"id" : 1, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.5,41.5,41.5,41.5,41.8,41.9,42.0,41.5,41.5,41.5,41.3,41.1]  },
        {"id" : 2, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.1,41.1,41.2,41.5,41.8,41.9,42.2,41.0,41.0,40.9,40.8,40.8]  },
        {"id" : 3, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.2,41.2,41.2,41.5,41.8,42.4,42.6,42.5,42.2,42.0,41.8,41.7]  },
        {"id" : 4, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [42.1,42.3,42.4,42.5,42.8,43.3,43.1,43.0,43.0,42.7,42.6,42.5]  },
        {"id" : 5, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.5,40.8,41.2,41.5,41.8,42.5,42.3,42.2,42.1,42.0,42.0,41.7]  },
        {"id" : 6, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.5,41.5,41.5,41.5,41.8,42.4,42.3,42.2,42.0,42.0,41.8,41.6]  },
        {"id" : 7, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.5,40.5,40.5,40.5,40.5,41.0,41.0,41.1,41.0,40.8,40.7,40.5]  },
        {"id" : 8, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [39.0,39.0,39.1,39.5,39.8,40.4,40.2,40.0,39.9,39.8,39.6,39.5]  },
        {"id" : 9, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.0,40.0,40.0,40.1,40.2,40.6,40.4,40.4,40.3,40.2,40.0,40.0]  },
        {"id" : 10, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [41.1,41.2,41.2,41.5,41.8,42.4,42.2,42.0,42.0,41.8,41.7,41.5]  },
]




outFile = [
    {"time": 11, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p.tif"},
    {"time": 10, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p-1.tif"},
    {"time": 9, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p-2.tif"},
    {"time": 8, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p-3.tif"},
    ]


outFile_predict = [
      {"time": 13, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p1.tif"},
      {"time": 14, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p2.tif"},
      {"time": 15, "outfile": "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p3.tif"},
    
    ]



# -- present and past 3 hours
for i in outFile:
    genImage(data,i['time'], i['outfile'])
    
#-- prediction
for i in outFile_predict:
    genPredictedImage(data, i['time'], i['outfile'])    
    




















