import os
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.feature import ShapelyFeature
from cartopy.io import shapereader
from cartopy.io.shapereader import Reader
from shapely.geometry import MultiLineString
from moviepy.editor import *
from datetime import datetime
from tqdm import tqdm
import natsort
from natsort import humansorted

def plotPt():
    df = pd.read_csv('eqph_csv_29May2020_noF_20lines.csv') 
    df = df.sort_values(by=['Date', 'Time_UTC'])
    geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
    gdf = GeoDataFrame(df, crs='epsg:32651', geometry=geometry) 
    proj = ccrs.PlateCarree() 
    bounds = [116.9283371, 126.90534668, 4.58693981, 21.07014084]
    save_path = r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH\exports\\'
    stamen_terrain = cimgt.Stamen('terrain-background')
    fault_line = ShapelyFeature(Reader('faultLines.shp').geometries(), ccrs.epsg(32651), 
                                 linewidth=1, edgecolor='black', facecolor='None')
    with tqdm(total=df.shape[0]) as pbar:     
        for i in range(gdf.shape[0]):
            g = gdf.iloc[i].geometry
            date = gdf.iloc[i]['Date'] 
            new_date = datetime.strptime(date, '%Y-%m-%d')
            new_date = new_date.strftime('%Y %b %d')
            time = gdf.iloc[i]['Time_UTC'] 
            mag = gdf.iloc[i]['Magnitude']  
            info = (new_date +  ' --- ' + time + ' ' + '\n' + 
                    str('Magnitude:') + str(mag) + ' --- ' + str(i+1) + '/' + str(len(df)))
            plt.suptitle('Earthquakes in the Philippines from 2011 to 2020' + 
                        '\n'+ 'with active fault lines' + '\n' + info, ha='left', 
                        x=0.363, y=0.97)             
            fig = plt.figure(figsize=(15,10))   
            ax  = fig.add_subplot(1, 1, 1, projection=proj)
            ax.set_extent(bounds)
            ax.add_image(stamen_terrain, 8)
            ax.plot(g.x, g.y, marker='o', color='red', markersize=8) 
            ax.add_feature(fault_line, zorder=1)
            plt.suptitle('Earthquakes in the Philippines from 2011 to 2020' + 
                         '\n'+ 'with active fault lines' + '\n' + info, ha='left', 
                         x=0.363, y=0.97) 
            fault_line_legend = mlines.Line2D([1], [1], color='black')
            ax.legend([fault_line_legend], ['Fault lines'], loc='lower left', fancybox='True')
            #plt.show()
            plt.savefig(save_path+'earthquake{}.png'.format(i))
            for i in range(1):
                pbar.update(1)               
def gif():
    os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH\exports')
    imgs = humansorted(os.listdir('.'))
    my_clip = ImageSequenceClip(imgs, fps=3.5)
    my_clip.write_videofile('eqph.mp4', fps=15)

plotPt()
gif()
