# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:54:53 2022

@author: wills
"""
#%%
import os
from glob import glob
import pandas as pd
import numpy as np
import recordlinkage
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')

#%%
Core_all=pd.read_stata(glob('CoreLogic/housing_address_in_selected_FIPS*.dta')[0],index_col='CoreID')
Axle_all=pd.read_stata(glob('DataAxle/NC*_primaryHH_address.dta')[0],index_col='LOCATIONID')

#%%
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

#%%
#Core=Core_all[Core_all['ZIP'].astype(int)<=27100]
#Axle=Axle_all[Axle_all['ZIP'].astype(int)<=27100]

#Core_block=Core_all[(Core_all['ZIP'].astype(int)==27009)|(Core_all['ZIP'].astype(int)==27024)]
#Axle_block=Axle_all[(Axle_all['ZIP'].astype(int)==27009)|(Axle_all['ZIP'].astype(int)==27024)]

ZIP_all=Core_all.ZIP.unique().tolist()
ZIP_all.sort()
ZIP_list=chunkIt(ZIP_all, 6)

#%%
final_final_matched=pd.DataFrame([],columns=['CoreID', 'LOCATIONID', 'house_num', 'street', 'Score', 'Group','coordinate'])
ZIP_error=[]

for i in ZIP_list[0]:
    try:
        Core=Core_all[Core_all.ZIP==i]
        Axle=Axle_all[Axle_all.ZIP==i]
        
        # Compare full address
        indexer = recordlinkage.Index()
        indexer.block(left_on='ZIP', right_on='ZIP')
        
        candidates = indexer.index(Core, Axle)
        
        compare = recordlinkage.Compare()
        compare.numeric('house_num','house_num',offset=2,label='house_num')
        compare.string('street','street',label='street')
        features = compare.compute(candidates,Core,Axle)
        
        # Get matches
        potential_matches = features[features.house_num>=0.5][features.street>=0.8]
        potential_matches=potential_matches.reset_index()
        potential_matches['Score'] = potential_matches['house_num']*0.2+potential_matches['street']*0.8
        
        best_matches=potential_matches.loc[potential_matches.groupby('CoreID').Score.idxmax()][['CoreID', 'LOCATIONID', 'house_num', 'street', 'Score']]
        best_matches['Group']="best_matches"
        
        # Check the matched records
        #merge = pd.merge(best_matches,Core[['house_num','street']],on=['CoreID'],how='left')
        #Axle2=Axle[['house_num','street']]
        #Axle2.rename(columns={'house_num': 'house_num2','street':'street2'},inplace=True)
        #merge = pd.merge(merge,Axle2,on=['LOCATIONID'],how='left')
        
        
        # Get the left CoreID with Lon and Lat
        Core_leftwithLonLat=Core[~Core.index.isin(best_matches['CoreID'])] 
        Core_leftwithLonLat=Core_leftwithLonLat[Core_leftwithLonLat.LATITUDE>0]
        
        # Compare lon and lat
        indexer = recordlinkage.Index()
        indexer.block(left_on='ZIP', right_on='ZIP')
        
        candidates = indexer.index(Core_leftwithLonLat, Axle)
        
        del compare
        compare = recordlinkage.Compare()
        compare.geo('LATITUDE','LONGITUDE','LATITUDE','LONGITUDE',method='linear',label='coordinate')
        
        features = compare.compute(candidates,Core_leftwithLonLat,Axle)
        potential_matches = features[features.coordinate>0]
        potential_matches=potential_matches.reset_index()
        
        knn_lonlat=potential_matches.sort_values(['CoreID','coordinate'],ascending=False).groupby('CoreID').head(3) #keep 3 closest
        knn_lonlat['Group']='KNN_lon_lat'
        
        # Last part - not matched on full address; withoug lat lon
        # match only on street name and ZIP
        
        Core_finalleft=Core[~Core.index.isin(best_matches['CoreID'])] 
        Core_finalleft=Core_finalleft[~Core_finalleft.index.isin(knn_lonlat['CoreID'])]
        
        indexer = recordlinkage.Index()
        indexer.block(left_on='ZIP', right_on='ZIP')
        
        candidates = indexer.index(Core_finalleft, Axle)
        
        del compare
        compare = recordlinkage.Compare()
        compare.numeric('house_num','house_num',method='exp',offset=2,label='house_num')
        compare.string('street','street',label='street')
        features = compare.compute(candidates,Core_finalleft,Axle)
        
        features=features.reset_index()
        features['Score'] = features['house_num']*0.2+features['street']*0.8
        
        knn_address=features.sort_values(['CoreID','Score'],ascending=False).groupby('CoreID').head(3) # keep the three most similar
        knn_address['Group']='KNN_address'
        
        del compare
        
        # Put all matched group together
        final_matched=pd.concat([best_matches, knn_lonlat, knn_address], ignore_index=True)
        del best_matches
        del knn_lonlat
        del knn_address
        
        final_final_matched=pd.concat([final_final_matched, final_matched], ignore_index=True)
        #final_final_matched.append(final_matched,ignore_index=True)
        
    except:
        ZIP_error=ZIP_error+[i]

#%%
final_final_matched.to_csv('matches.csv')
ZIP_error = pd.DataFrame(ZIP_error)
ZIP_error.to_csv('ZIP_error.csv')
