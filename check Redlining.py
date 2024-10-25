# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:26:43 2024

@author: wills
"""
#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

#%% read redlining map data
redlining=gpd.read_file("Redlining map/mappinginequality.json")

redlining.plot()
plt.show()

redlining = redlining[redlining['state'].isin(['SC', 'NC', 'VA', 'MD', 'DE', 'PA', 'CT', 'RI', 'MA'])]
redlining = redlining[redlining['category'].isin(['Definitely Declining', 'Still Desirable', 'Hazardous', 'Best'])]

#%% read data of households 
df=pd.read_stata('Analysis/households_9ST2021_heat_building_demographics_3races.dta')
df_short=df[['APN_SEQUENCE_NBR','FIPS_CODE','P_ID_IRIS_FRMTD','LATITUDE','LONGITUDE','PPI_DIV_1000', 'WEALTH_FINDER_SCORE', 'FIND_DIV_1000', 
             'YEARBUILT', 'building_age', 'LIVING_AREA', 'SF', 'Ethnic1', 'Ethnic2', 'Ethnic3']]
df_short=df_short.dropna(subset=['LATITUDE', 'LONGITUDE']) # drop buildings without lat and lon
df_short['geometry'] = df_short.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)
df_short_gdf = gpd.GeoDataFrame(df_short, geometry='geometry')
df_short_gdf=df_short_gdf.set_crs("EPSG:4326")

#%% geo merging
redlining = redlining.to_crs("EPSG:4326")
joined_gdf = gpd.sjoin(df_short_gdf, redlining, how="left", predicate="within")
joined_gdf2=joined_gdf.dropna(subset=['category'])
joined_gdf2=joined_gdf2.drop(columns=['geometry'])
joined_gdf2.to_csv('Analysis/households_9ST2021_withinRedliningMap.csv')
