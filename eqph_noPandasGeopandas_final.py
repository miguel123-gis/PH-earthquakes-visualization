# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:20:47 2020

@author: imper
"""
import os
import csv
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.feature import ShapelyFeature
from cartopy.io import shapereader
from cartopy.io.shapereader import Reader
from shapely.geometry import MultiLineString
from datetime import datetime 
from moviepy.editor import *
from tqdm import tqdm
import natsort
from natsort import humansorted
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH')

bounds = [116.9283371, 126.90534668, 4.58693981, 21.07014084]
stamen_terrain = cimgt.Stamen('terrain-background')
fault_line = ShapelyFeature(Reader('faultLines.shp').geometries(), ccrs.epsg(32651), 
                            linewidth=1, edgecolor='black', facecolor='None')
save_path = r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH\exports2\\'  
date,time,lon,lat,mag = [],[],[],[],[]
with open ('eqph_csv_29May2020_noF_5lines.csv') as file:
    reader = csv.reader(file, delimiter=',') 
    next(reader)
    date_sorted = sorted(reader, key=lambda col: datetime.strptime
                         (col[0] + ' ' + col[1], '%Y-%m-%d %H:%M:%S'))   
    for col in date_sorted:
        date.append(col[0])
        time.append(str(col[1]))
        lat.append(int(float(col[2])))
        lon.append(int(float(col[3])))
        mag.append(int(float(col[7])))
    index = range(len(date_sorted))
with tqdm(index) as pbar: 
    for d,t,x,y,m,i in zip(date,time,lon,lat,mag,index):
        fig = plt.figure(figsize=(15,10)) # frame?
        ax  = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree()) 
        d = datetime.strptime(d, '%Y-%m-%d')
        d = d.strftime('%Y %b %d')
        ax.set_extent(bounds) 
        ax.add_image(stamen_terrain, 8)
        plt.suptitle('Earthquakes in the Philippines from 2011 to 2020' + 
                     '\n' +'with active fault lines' + 
                     '\n' + str(d) + ' --- ' + str(t) +
                     '\n' + 'Magnitude: ' + str(m) +
                     ' --- ' + str(i+1) + '/' + str(len(index)),
                     ha='left', x=0.363, y=0.97)
        ax.plot(x, y, 'ro', markersize=5) 
        ax.add_feature(fault_line, zorder=1)
        plt.savefig(save_path+'earthquake{}'.format(i))
        for i in range(1):
            pbar.update(1)
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH\exports2')
imgs = humansorted(os.listdir('.'))
my_clip = ImageSequenceClip(imgs, fps=3.5)
my_clip.write_videofile('eqph.mp4', fps=15)

    
