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
def plotPt():
    df = pd.read_csv('eqph_csv_29May2020_noF_10lines.csv') 
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
# Conversion to GIF not working, files are read wrong like 0, 10, 100 
# instead of 0, 1, 2, 3
    #image_list='exports'
    #my_clip = ImageSequenceClip(image_list, fps=0.75)
    #my_clip.write_gif('eqph_gif.gif')
plotPt()

# NEXT STEPS as of 30 May 2020
# Sort image_list properly by using natsort on the filename number