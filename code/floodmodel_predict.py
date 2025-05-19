#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:10:29 2022

@author: kampanartpiyathamrongchai
"""

from osgeo import gdal
from osgeo import ogr
from osgeo import gdal_array
import numpy as np

def predictLevel(x,y,preX):
    res = np.polyfit(x, y, 2, rcond=None, full=False, w=None, cov=False)
    result = res[0]*pow(preX,2) + res[1]*preX + res[2]  
    return result


data = [
        {"id" : 1, "time" : [1,2,3,4,5,6,7,8,9,10,11,12], "wlevel": [40.5,40.5,40.5,40.5,40.8,40.9,41.1,41.5,41.8,41.9,42.0,42.2] },
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



ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/bndgrd_geog.tif")
bnd = np.array(ds.GetRasterBand(1).ReadAsArray())

trans1 = ds.GetGeoTransform()
proj1 = ds.GetProjection()
outfile = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/result/flood_p+3.tif"

#outfile11 = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Oct/demtiff/out11.tif"


ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Mar/data/dembrk_geog.tif")
dem = np.array(ds.GetRasterBand(1).ReadAsArray())

bnd[bnd<0.5]=np.nan
dem[dem<0]=np.nan

print(bnd)

outimg = dem
cols, rows = outimg.shape

for w in data:
    lev = predictLevel(w['time'], w['wlevel'], 15)
    print(lev)
    for i in range(len(dem)):
        for j in range(len(dem[i,:])):
            if bnd[i,j] != np.nan and bnd[i,j] == w['id']:
                if dem[i,j] <= lev-2:
                # if dem[i,j] <= w['wlevel'][11]-2:
                    outimg[i,j] = 1
                else:
                    outimg[i,j] = 0

print(outimg) 

outdriver = gdal.GetDriverByName("GTiff")
outdata   = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Byte)
outdata.GetRasterBand(1).SetNoDataValue(-9.0)
outdata.GetRasterBand(1).WriteArray(outimg)
outdata.SetGeoTransform(trans1)


#gdal.Translate(outfile11,outdata)

# Write projection information
outdata.SetProjection(proj1)