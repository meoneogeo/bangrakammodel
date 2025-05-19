#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 12:52:09 2022

@author: kampanartpiyathamrongchai
"""

from osgeo import gdal
from osgeo import ogr
from osgeo import gdal_array
import numpy as np


ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Aug2022/data/aug22/brk_bnd_sm_geo.tif")
bnd = np.array(ds.GetRasterBand(1).ReadAsArray())

trans1 = ds.GetGeoTransform()
proj1 = ds.GetProjection()

#outfile11 = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Oct/demtiff/out11.tif"


ds = gdal.Open("/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Aug2022/data/aug22/brk_dem_fill_adj_geo.tif")
dem = np.array(ds.GetRasterBand(1).ReadAsArray())

#station = ['st001', 'st002', 'st003', 'st004', 'st005', 'st006', 'st007', 'st008', 'st009', 'st010']
# flevel = ['40.695', '41.023', '40.663', '40.167','43.208', '40.073', '42.123', '40.642', '40.288', '42.601']
flevel = ['40.69', '40.59', '40.26', '40.49','42.80', '40.07', '39.88', '40.06', '42.02', '42.60']

outfile = "/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/Aug2022/data/demadjust_geo7.tif"


bnd[bnd<0.5]=np.nan
dem[dem<0]=np.nan
outimg = dem
cols, rows = outimg.shape
# print(dem)
for w in flevel:
    # print(w['wlevel'][stime]-2)
    for i in range(len(dem)):
        for j in range(len(dem[i,:])):
            if bnd[i,j] != np.nan and bnd[i,j] == flevel.index(w) + 1:
                if dem[i,j] <= float(w):
                    outimg[i,j] = round(float(w),2)
                else:
                    outimg[i,j] = dem[i,j]

outdriver = gdal.GetDriverByName("GTiff")
outdata = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)
outdata.GetRasterBand(1).SetNoDataValue(-9.0)
outdata.GetRasterBand(1).WriteArray(outimg)
outdata.SetGeoTransform(trans1)
outdata.SetProjection(proj1)
del(outdata)
del(outimg)
print('Done!')