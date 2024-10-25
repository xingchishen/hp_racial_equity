# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:36:59 2022

@author: wills
"""

#%%
import gzip
import pandas as pd
from io import BytesIO

states=['NC','SC','MD','VA','DE','PA','CT','RI','MA']

for j in range(2010,2019):
    
    with gzip.open('US_Consumer_5_File_'+str(j)+'.csv.gz', 'rb') as f: file_content = f.read()
    s=BytesIO(file_content)
    df_all=pd.read_csv(s)
    
    for i in states:
        df_state=df_all[df_all.STATE==i]
        df_state.to_csv(i+str(j)+'.csv')




