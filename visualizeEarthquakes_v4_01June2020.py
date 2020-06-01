import os
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH')
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from moviepy.editor import *
from datetime import datetime
from tqdm import tqdm
import natsort
from natsort import humansorted

def plotPt():
    df = pd.read_csv('eqph_csv_29May2020_noF_20lines.csv') 
    df = df.sort_values(by=['Date', 'Time_UTC'])
    crs = "epsg:32651" 
    geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry) 
    proj = ccrs.PlateCarree() 
    bounds = [116.9283371, 126.90534668, 4.58693981, 21.07014084] 
    stamen_terrain = cimgt.Stamen('terrain-background')
    with tqdm(total=df.shape[0]) as pbar: 
        for i in range(gdf.shape[0]):
            g = gdf.iloc[i].geometry
            date = gdf.iloc[i]['Date'] 
            new_date = datetime.strptime(date, '%Y-%m-%d')
            new_date = (new_date.strftime('%Y %b %d'))
            time = gdf.iloc[i]['Time_UTC'] 
            mag = gdf.iloc[i]['Magnitude']
            info = (new_date +  " --- " + time + " " + "\n" + 
                    str("Magnitude:") + str(mag))
            fig = plt.figure(figsize=(15,10))   
            ax  = fig.add_subplot(1, 1, 1, projection=proj)
            ax.set_extent(bounds)
            ax.add_image(stamen_terrain, 8)
            ax.plot(g.x, g.y, marker='o', color='red', markersize=8) 
            plt.suptitle('Earthquakes in the Philippines from 2011 to 2020' + 
                         '\n' + info, ha='left', x=0.363, y=0.95) 
            plt.savefig("exports\earthquake{0}.png".format(i))
            for i in range(1):
                pbar.update(1)               
def gif():
    os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH\exports')
    imgs = humansorted(os.listdir('.'))
    my_clip = ImageSequenceClip(imgs, fps=1)
    my_clip.write_videofile('eqph.mp4', fps=15)

plotPt()
gif()

# NEXT STEPS as of 1 June 2020
# add image number in plot
# add fault lines shp
# bigger plot
# bold plot title