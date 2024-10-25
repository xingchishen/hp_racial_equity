# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:36:59 2022

@author: wills
"""

#%%
import gzip
import pandas as pd
from io import BytesIO

states=['NC','SC','WV','MD','VA','PA','OH','IN','KY']

for j in range(2010,2019):
    
    with gzip.open('US_Consumer_5_File_'+str(j)+'.csv.gz', 'rb') as f: file_content = f.read()
    s=BytesIO(file_content)
    df_all=pd.read_csv(s)
    
    for i in states:
        df_state=df_all[df_all.STATE==i]
        df_state.to_csv(i+str(j)+'.csv')




#%% 
# creat a gz file
import gzip
import shutil
with open('test.csv', 'rb') as f_in:
    with gzip.open('test.csv.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        
        
df=pd.read_csv('test.csv.gz',compression='gzip',chunksize=1000000)
pd_df = pd.concat(df)



from dask import dataframe as dd
dask_df = dd.read_csv('test.csv.gz',compression='gz')

#%%
import os
os.chdir('C:/Users/wills/Documents/DataAxle')
import pandas as pd
import numpy as np

df=pd.read_csv('US_Consumer_5_File_2010.csv',nrows=10000)
