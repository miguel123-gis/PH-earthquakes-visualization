import os
os.chdir(r'path')
import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

df = pd.read_csv('emscPhilippines2008to2020.csv') 
crs = "epsg:32651" 
geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
gdf = GeoDataFrame(df, crs=crs, geometry=geometry) 
proj = ccrs.PlateCarree() 
ph = gpd.read_file('Provinces.shp') 
bounds = [117.17427453, 126.537423944, 5.58100332277, 18.5052273625] 
stamen_terrain = cimgt.Stamen('terrain-background')
for i in range(gdf.shape[0]):
    ax = plt.axes(projection=proj)
    ax.add_image(stamen_terrain, 8)
    ax.set_extent(bounds) 
    
    g = gdf.iloc[i].geometry
    ax.plot(g.x, g.y, marker='o', color='red', markersize=15) 
    
    date = gdf.iloc[i]['Date'] 
    time = gdf.iloc[i]['Time_UTC'] 
    mag = gdf.iloc[i]['Magnitude'] 
    info = (date + " " + time + " " + str("Magnitude:") + str(mag))
    plt.suptitle('Earthquakes in the Philippines from 2008 to 2020') 
    plt.title(info) 
    
    plt.show()
    #plt.savefig("earthquake{0}.png".format(i))
plt.show()

# NEXT STEPS as of 28 May 2020
# convert to GIF from via moviepy
# need to use csv module isntead of geopandas
# widen bounds
# for-loop should start from earliest (last row in csv)
