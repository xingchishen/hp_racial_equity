# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:41:17 2023

@author: wills
"""
#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import numpy as np

#%% 1. Count Race by ZIP in my sample for each state
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']

for i in states:
    
    # Clean DataAxle
    DataAxle=pd.read_stata('DataAxle/'+i+'2021.dta')
    DataAxle=DataAxle[DataAxle['PRIMARY_FAMILY_IND']==1]
    DataAxle=DataAxle.groupby('LOCATIONID').first()
    DataAxle=DataAxle.reset_index()
    DataAxle=DataAxle[['LOCATIONID','LOCATION_TYPE','HEAD_HH_AGE_CODE','CHILDRENHHCOUNT','WEALTH_FINDER_SCORE', 'FIND_DIV_1000', 
                       'OWNER_RENTER_STATUS','PPI_DIV_1000','Ethnicity_Code_1']]
    
    # Merge CoreID with demographics 
    Matched_Address=pd.read_stata('MatchedAddress/matches_'+i+'.dta')
    Matched_Address=pd.merge(Matched_Address,DataAxle,how='left',on=['LOCATIONID'])
    Matched_Address=pd.merge(Matched_Address,pd.read_stata('DataAxle/Race.dta'),how='left',on=['Ethnicity_Code_1'])
    
    # aggregate data since some CoreID matched to three DataAxle IDs
    Matched_Address = Matched_Address.groupby('CoreID').aggregate({'LOCATIONID':'first','LOCATION_TYPE':'first','HEAD_HH_AGE_CODE':'first',
                                                                   'CHILDRENHHCOUNT':'mean','WEALTH_FINDER_SCORE':'mean','FIND_DIV_1000':'mean',
                                                                   'OWNER_RENTER_STATUS':'mean','PPI_DIV_1000':'mean','Ethnicity_Code_1':'first',
                                                                   'Ethnicity':'first','Race':'first', 'Ethnic':'first'})
    Matched_Address=Matched_Address.reset_index()
    
    # Match to orgrinal CoreLogic IDs
    Matched_Address=pd.merge(Matched_Address,pd.read_stata('CoreLogic/housing_address_in_selected_FIPS_all_'+i+'.dta'),how='left',on=['CoreID'])
    
    # Count race by ZIP
    Matched_Address['Black'] = 0
    Matched_Address['Black'] = np.where(Matched_Address['Ethnic']=='Black or African American', 1, Matched_Address['Black'])
    Matched_Address['White'] = 0
    Matched_Address['White'] = np.where(Matched_Address['Ethnic']=='White', 1, Matched_Address['White'])
    
    ZIP_race_count=Matched_Address.groupby('ZIP').aggregate({'Black':'sum','White':'sum'})
    ZIP_race_count=ZIP_race_count.reset_index()
    ZIP_race_count.sort_values(by=['Black'])
    ZIP_race_count.to_csv('MatchedAddress/ZIP_race_count_'+i+'.csv')




#%% 2. Get the panel (ID address Heat demographics) at the household-year level
# In this panel, heating is time variant while others are time-fixed.

# Done: 'SC','NC','DE'
states=['VA','MD','PA','CT','RI','MA']

for i in states:
    
    # Clean DataAxle
    DataAxle=pd.read_stata('DataAxle/'+i+'2021.dta')
    DataAxle=DataAxle[DataAxle['PRIMARY_FAMILY_IND']==1]
    DataAxle=DataAxle.groupby('LOCATIONID').first()
    DataAxle=DataAxle.reset_index()
    DataAxle=DataAxle[['LOCATIONID','LOCATION_TYPE','HEAD_HH_AGE_CODE','CHILDRENHHCOUNT','WEALTH_FINDER_SCORE', 'FIND_DIV_1000', 
                       'OWNER_RENTER_STATUS','PPI_DIV_1000','Ethnicity_Code_1']]
    
    # Merge CoreID with demographics 
    Matched_Address=pd.read_stata('MatchedAddress/matches_'+i+'.dta')
    Matched_Address=pd.merge(Matched_Address,DataAxle,how='left',on=['LOCATIONID'])
    Matched_Address=pd.merge(Matched_Address,pd.read_stata('DataAxle/Race.dta'),how='left',on=['Ethnicity_Code_1'])
    
    # aggregate data since some CoreID matched to three DataAxle IDs
    Matched_Address = Matched_Address.groupby('CoreID').aggregate({'LOCATIONID':'first','LOCATION_TYPE':'first','HEAD_HH_AGE_CODE':'first',
                                                                   'CHILDRENHHCOUNT':'mean','WEALTH_FINDER_SCORE':'mean','FIND_DIV_1000':'mean',
                                                                   'OWNER_RENTER_STATUS':'mean','PPI_DIV_1000':'mean','Ethnicity_Code_1':'first',
                                                                   'Ethnicity':'first','Race':'first', 'Ethnic':'first'})
    Matched_Address=Matched_Address.reset_index()
    
    # Match to orgrinal CoreLogic IDs
    Matched_Address=pd.merge(Matched_Address,pd.read_stata('CoreLogic/housing_address_in_selected_FIPS_all_'+i+'.dta'),how='left',on=['CoreID'])

    # read data "tax_IDaddressHeat_all" and clean it
    Panel_IDaddressHeat=pd.read_stata('CoreLogic/tax_IDaddressHeat_all_'+i+'.dta')
    Panel_IDaddressHeat=Panel_IDaddressHeat.dropna(subset=['ASSESSED_YEAR'])
    Panel_IDaddressHeat=Panel_IDaddressHeat.loc[Panel_IDaddressHeat['PROPERTY_INDICATOR'].isin([0, 10, 11, 21, 22])]
    FIPS=pd.read_stata('CoreLogic/FIPS_'+i+'.dta') #only pick houses in selected FIPS
    FIPS['FIPS_mark']=1
    Panel_IDaddressHeat=pd.merge(Panel_IDaddressHeat,FIPS,how='left',on=['FIPS_CODE'])
    Panel_IDaddressHeat=Panel_IDaddressHeat[Panel_IDaddressHeat.FIPS_mark==1]
    Panel_IDaddressHeat=Panel_IDaddressHeat[Panel_IDaddressHeat.CITY!=""]
    Panel_IDaddressHeat=Panel_IDaddressHeat[Panel_IDaddressHeat.ZIP!="."]
    Panel_IDaddressHeat=Panel_IDaddressHeat[Panel_IDaddressHeat.ZIP!=""]
    Panel_IDaddressHeat=Panel_IDaddressHeat[Panel_IDaddressHeat.street!=""]
    Panel_IDaddressHeat=Panel_IDaddressHeat[['FIPS_CODE', 'APN_SEQUENCE_NBR', 'P_ID_IRIS_FRMTD','TAX_YEAR', 'ASSESSED_YEAR', 'HEATING']]
    
    # Merge and get the final panel at the household-year level
    Final_Panel=pd.merge(Panel_IDaddressHeat,Matched_Address,how='left',on=['FIPS_CODE', 'APN_SEQUENCE_NBR', 'P_ID_IRIS_FRMTD'])
    Final_Panel.to_csv('Analysis/Panel_IDaddressHeat_demographics_'+i+'.csv')










