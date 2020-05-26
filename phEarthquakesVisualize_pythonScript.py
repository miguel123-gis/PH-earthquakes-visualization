import os
os.chdir(r'C:\Users\imper\Documents\new_GISfiles\earthquakesPH')
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
os.environ['PROJ_LIB'] = r'C:\Users\imper\miniconda3\envs\eq\Library\share\basemap'
from mpl_toolkits.basemap import Basemap

def plotPoint():
    df = pd.read_csv('emscPhilippines2008to2020_5lines.csv')
    prov  = gpd.read_file('Provinces.shp')
    crs = "epsg:32651"
    geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    for d in df['Date'].values:
        date = d
    for t in df['Time_UTC'].values:
        time = t
    for i in range(gdf.shape[0]): 
        ax = prov.plot(figsize=(15,10)) 
        ax.axis('off')
        g = gdf.iloc[i].geometry
        date = gdf.iloc[i]['Date']
        time = gdf.iloc[i]['Time_UTC']       
        info = (date + " " + time)
        plt.plot(g.x, g.y, marker='o', color='red', markersize=15)
        plt.suptitle('Earthquakes in the Philippines from 2008 to 2020')
        plt.title(info)
        plt.show()
        plt.savefig("earthquake{1}.png".format(i))
        
plotPoint()

# End product are photos that will be converted into GIF via the moviepy package