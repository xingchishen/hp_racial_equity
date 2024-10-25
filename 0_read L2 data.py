# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:43:36 2023

@author: wills
"""
#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data/L2')
import pandas as pd
import numpy as np


#%% get eduction information 
# 8 states except for VA
files=['VM2--SC--2022-08-18-DEMOGRAPHIC.tab','VM2--NC--2022-08-23-DEMOGRAPHIC.tab','VM2Uniform--VA--2022-09-07.tab'
       'VM2--MD--2022-08-27-DEMOGRAPHIC.tab',
       'VM2--DE--2022-08-24-DEMOGRAPHIC.tab','VM2--PA--2022-08-30-DEMOGRAPHIC.tab','VM2--CT--2022-08-17-DEMOGRAPHIC.tab',
       'VM2--RI--2022-08-25-DEMOGRAPHIC.tab','VM2--MA--2022-08-19-DEMOGRAPHIC.tab']
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']


for j,s in zip(files,states):
    
    cols=['Residence_Addresses_Zip','EthnicGroups_EthnicGroup1Desc','CommercialData_Education']
    df=pd.read_csv(j,sep='\t',usecols=cols,encoding= 'unicode_escape')
    df_B=df[df.EthnicGroups_EthnicGroup1Desc=="Likely African-American"]
    df_A=df[df.EthnicGroups_EthnicGroup1Desc== "East and South Asian"]
    df_H=df[df.EthnicGroups_EthnicGroup1Desc== "Hispanic and Portuguese"]
    df_W=df[df.EthnicGroups_EthnicGroup1Desc== "European"]
    df_M=df[(df.EthnicGroups_EthnicGroup1Desc=="Likely African-American")|(df.EthnicGroups_EthnicGroup1Desc== "Hispanic and Portuguese")]
    
    conditions=(df.CommercialData_Education=="Bach Degree - Extremely Likely")|(df.CommercialData_Education=="Bach Degree - Likely")|(df.CommercialData_Education=="Grad Degree - Extremely Likely")|(df.CommercialData_Education=="Grad Degree - Likely")            
    df['N_AboveBach']=0
    df['N_AboveBach'] = np.where(conditions, 1, df['N_AboveBach'] )
    df['count']=1
    
    conditions=(df_B.CommercialData_Education=="Bach Degree - Extremely Likely")|(df_B.CommercialData_Education=="Bach Degree - Likely")|(df_B.CommercialData_Education=="Grad Degree - Extremely Likely")|(df_B.CommercialData_Education=="Grad Degree - Likely")            
    df_B['N_AboveBach']=0
    df_B['N_AboveBach'] = np.where(conditions, 1, df_B['N_AboveBach'] )
    df_B['count']=1
    
    conditions=(df_A.CommercialData_Education=="Bach Degree - Extremely Likely")|(df_A.CommercialData_Education=="Bach Degree - Likely")|(df_A.CommercialData_Education=="Grad Degree - Extremely Likely")|(df_A.CommercialData_Education=="Grad Degree - Likely")            
    df_A['N_AboveBach']=0
    df_A['N_AboveBach'] = np.where(conditions, 1, df_A['N_AboveBach'] )
    df_A['count']=1
    
    conditions=(df_H.CommercialData_Education=="Bach Degree - Extremely Likely")|(df_H.CommercialData_Education=="Bach Degree - Likely")|(df_H.CommercialData_Education=="Grad Degree - Extremely Likely")|(df_H.CommercialData_Education=="Grad Degree - Likely")            
    df_H['N_AboveBach']=0
    df_H['N_AboveBach'] = np.where(conditions, 1, df_H['N_AboveBach'] )
    df_H['count']=1
    
    conditions=(df_W.CommercialData_Education=="Bach Degree - Extremely Likely")|(df_W.CommercialData_Education=="Bach Degree - Likely")|(df_W.CommercialData_Education=="Grad Degree - Extremely Likely")|(df_W.CommercialData_Education=="Grad Degree - Likely")            
    df_W['N_AboveBach']=0
    df_W['N_AboveBach'] = np.where(conditions, 1, df_W['N_AboveBach'] )
    df_W['count']=1
    
    conditions=(df_M.CommercialData_Education=="Bach Degree - Extremely Likely")|(df_M.CommercialData_Education=="Bach Degree - Likely")|(df_M.CommercialData_Education=="Grad Degree - Extremely Likely")|(df_M.CommercialData_Education=="Grad Degree - Likely")            
    df_M['N_AboveBach']=0
    df_M['N_AboveBach'] = np.where(conditions, 1, df_M['N_AboveBach'] )
    df_M['count']=1
    
    df = df.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df=df.reset_index()
    df_B = df_B.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df_B=df_B.reset_index()
    df_A = df_A.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df_A=df_A.reset_index()
    df_H = df_H.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df_H=df_H.reset_index()
    df_W = df_W.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df_W=df_W.reset_index()
    df_M = df_M.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_AboveBach':'sum'})
    df_M=df_M.reset_index()
    
    
    df['Ratio_AboveBach']=df['N_AboveBach']/df['count']
    df=df[['Residence_Addresses_Zip','Ratio_AboveBach']]
    df_B['Ratio_AboveBach_B']=df_B['N_AboveBach']/df_B['count']
    df_B=df_B[['Residence_Addresses_Zip','Ratio_AboveBach_B']]
    df_A['Ratio_AboveBach_A']=df_A['N_AboveBach']/df_A['count']
    df_A=df_A[['Residence_Addresses_Zip','Ratio_AboveBach_A']]
    df_H['Ratio_AboveBach_H']=df_H['N_AboveBach']/df_H['count']
    df_H=df_H[['Residence_Addresses_Zip','Ratio_AboveBach_H']]
    df_W['Ratio_AboveBach_W']=df_W['N_AboveBach']/df_W['count']
    df_W=df_W[['Residence_Addresses_Zip','Ratio_AboveBach_W']]
    df_M['Ratio_AboveBach_M']=df_M['N_AboveBach']/df_M['count']
    df_M=df_M[['Residence_Addresses_Zip','Ratio_AboveBach_M']]
    
    for i in [df_B, df_A, df_H, df_W, df_M]:
        df=pd.merge(df,i,how='left',on=['Residence_Addresses_Zip'])
    
    df.to_csv(s+'.csv')

#%%
df=pd.concat([pd.read_csv(i+'.csv') for i in states],ignore_index=True)
df.to_csv('Education_byRace_ZIP2022.csv')











#%% Get %Democratic information  -- HAVE NOT RUN YET

files=['VM2--SC--2022-08-18-DEMOGRAPHIC.tab','VM2--NC--2022-08-23-DEMOGRAPHIC.tab','VM2Uniform--VA--2022-09-07.tab'
       'VM2--MD--2022-08-27-DEMOGRAPHIC.tab',
       'VM2--DE--2022-08-24-DEMOGRAPHIC.tab','VM2--PA--2022-08-30-DEMOGRAPHIC.tab','VM2--CT--2022-08-17-DEMOGRAPHIC.tab',
       'VM2--RI--2022-08-25-DEMOGRAPHIC.tab','VM2--MA--2022-08-19-DEMOGRAPHIC.tab']
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']


for j,s in zip(files,states):
    
    cols=['Residence_Addresses_Zip','EthnicGroups_EthnicGroup1Desc','Parties_Description']
    df=pd.read_csv(j,sep='\t',usecols=cols,encoding= 'unicode_escape')
    df_B=df[df.EthnicGroups_EthnicGroup1Desc=="Likely African-American"]
    df_A=df[df.EthnicGroups_EthnicGroup1Desc== "East and South Asian"]
    df_H=df[df.EthnicGroups_EthnicGroup1Desc== "Hispanic and Portuguese"]
    df_W=df[df.EthnicGroups_EthnicGroup1Desc== "European"]
    df_M=df[(df.EthnicGroups_EthnicGroup1Desc=="Likely African-American")|(df.EthnicGroups_EthnicGroup1Desc== "Hispanic and Portuguese")]
    
    conditions=(df.Parties_Description=="Democratic")       
    df['N_Dem']=0
    df['N_Dem'] = np.where(conditions, 1, df['N_Dem'] )
    df['count']=1
    
    conditions=(df_B.Parties_Description=="Democratic")       
    df_B['N_Dem']=0
    df_B['N_Dem'] = np.where(conditions, 1, df_B['N_Dem'] )
    df_B['count']=1

    conditions=(df_A.Parties_Description=="Democratic")       
    df_A['N_Dem']=0
    df_A['N_Dem'] = np.where(conditions, 1, df_A['N_Dem'] )
    df_A['count']=1

    conditions=(df_H.Parties_Description=="Democratic")       
    df_H['N_Dem']=0
    df_H['N_Dem'] = np.where(conditions, 1, df_H['N_Dem'] )
    df_H['count']=1
    
    conditions=(df_W.Parties_Description=="Democratic")       
    df_W['N_Dem']=0
    df_W['N_Dem'] = np.where(conditions, 1, df_W['N_Dem'] )
    df_W['count']=1

    conditions=(df_M.Parties_Description=="Democratic")       
    df_M['N_Dem']=0
    df_M['N_Dem'] = np.where(conditions, 1, df_M['N_Dem'] )
    df_M['count']=1
    
    df = df.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df=df.reset_index()
    df_B = df_B.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df_B=df_B.reset_index()
    df_A = df_A.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df_A=df_A.reset_index()
    df_H = df_H.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df_H=df_H.reset_index()
    df_W = df_W.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df_W=df_W.reset_index()
    df_M = df_M.groupby(['Residence_Addresses_Zip']).aggregate({'count':'sum','N_Dem':'sum'})
    df_M=df_M.reset_index()
    
    
    df['Ratio_Dem']=df['N_Dem']/df['count']
    df=df[['Residence_Addresses_Zip','Ratio_Dem']]
    df_B['Ratio_Dem_B']=df_B['N_Dem']/df_B['count']
    df_B=df_B[['Residence_Addresses_Zip','Ratio_Dem_B']]
    df_A['Ratio_Dem_A']=df_A['N_Dem']/df_A['count']
    df_A=df_A[['Residence_Addresses_Zip','Ratio_Dem_A']]
    df_H['Ratio_Dem_H']=df_H['N_Dem']/df_H['count']
    df_H=df_H[['Residence_Addresses_Zip','Ratio_Dem_H']]
    df_W['Ratio_Dem_W']=df_W['N_Dem']/df_W['count']
    df_W=df_W[['Residence_Addresses_Zip','Ratio_Dem_W']]
    df_M['Ratio_Dem_M']=df_M['N_Dem']/df_M['count']
    df_M=df_M[['Residence_Addresses_Zip','Ratio_Dem_M']]
    
    for i in [df_B, df_A, df_H, df_W, df_M]:
        df=pd.merge(df,i,how='left',on=['Residence_Addresses_Zip'])
    
    df.to_csv(s+'.csv')

#%%
df=pd.concat([pd.read_csv(i+'.csv') for i in states],ignore_index=True)
df.to_csv('Dem_share_byRace_ZIP2022.csv')