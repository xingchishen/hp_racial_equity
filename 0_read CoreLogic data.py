# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:50:19 2022

@author: wills
"""
#%% CoreLogic

#%% read NC 2019 whole data
import os
os.chdir('Z:/YUL_mediated_data_collection-CC0737-LSSSM/CoreLogic/statedata')
import pandas as pd
df = pd.read_sas('nc_t12.sas7bdat')
df.to_csv('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data/NC_tax_2019.csv')


#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat

#%% Look at the first 1000 rows of NC_2010 TO 2018
df, meta = pyreadstat.read_sas7bdat('CoreLogic/nc.sas7bdat', row_limit=1000)
df.head()

#%% pyreadstat - read the IDs, address, heating,PRIND of NC from 2010 to 2018
cols=['P_ID_IRIS_FRMTD','APN_SEQUENCE_NBR','FIPS_CODE','HEATING','TAX_YEAR','ASSESSED_YEAR','PROPERTY_INDICATOR',
'SITUS_HOUSE_NUMBER_PREFIX','SITUS_HOUSE_NUMBER1','SITUS_HOUSE_NUMBER2','SITUS_HOUSE_NUMBER_SUFFIX','SITUS_DIRECTION','SITUS_STREET_NAME',
'SITUS_MODE','SITUS_QUADRANT','SITUS_UNIT_NUMBER','SITUS_CITY','SITUS_STATE','SITUS_ZIP_CODE','PARCEL_LEVEL_LATITUDE__2_6_',
'PARCEL_LEVEL_LONGITUDE__3_6_']
df, meta = pyreadstat.read_sas7bdat('CoreLogic/nc.sas7bdat', usecols=cols)

# read IDs, address, heating,PRIND of NC 2019, and put all years together
df1= pd.read_csv('CoreLogic/NC_tax_2019.csv', usecols=cols) 
for i in cols:
    try:
        df1[i]=df1[i].str[2:-1]  # delete the begining and end of str b' '
    except:
        pass  

df=df.append(df1,ignore_index=True)
del df1
df = df.astype({'TAX_YEAR': 'float', 'ASSESSED_YEAR': 'float'})
df.to_csv('CoreLogic/NC_tax_IDaddressHeat_2010_2019.csv')


    

#%% SC

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
YUL_path='Z:/YUL_mediated_data_collection-CC0737-LSSSM/CoreLogic/statedata/'

cols=['P_ID_IRIS_FRMTD','APN_SEQUENCE_NBR','FIPS_CODE','HEATING','TAX_YEAR','ASSESSED_YEAR','PROPERTY_INDICATOR',
'SITUS_HOUSE_NUMBER_PREFIX','SITUS_HOUSE_NUMBER1','SITUS_HOUSE_NUMBER2','SITUS_HOUSE_NUMBER_SUFFIX','SITUS_DIRECTION','SITUS_STREET_NAME',
'SITUS_MODE','SITUS_QUADRANT','SITUS_UNIT_NUMBER','SITUS_CITY','SITUS_STATE','SITUS_ZIP_CODE','PARCEL_LEVEL_LATITUDE__2_6_',
'PARCEL_LEVEL_LONGITUDE__3_6_']
df, meta = pyreadstat.read_sas7bdat(YUL_path+'sc.sas7bdat', usecols=cols)
df1, meta = pyreadstat.read_sas7bdat(YUL_path+'sc_t12.sas7bdat', usecols=cols)
df=df.append(df1,ignore_index=True)
del df1
df['ASSESSED_YEAR']=df['ASSESSED_YEAR'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
df.to_csv('CoreLogic/SC_tax_IDaddressHeat_2010_2019.csv')

#%% VA, MD, DE, PA, CT, RI, MA
# There is no DC file in YUL.../CoreLogic/statedata/

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
YUL_path='Z:/YUL_mediated_data_collection-CC0737-LSSSM/CoreLogic/statedata/'

cols=['P_ID_IRIS_FRMTD','APN_SEQUENCE_NBR','FIPS_CODE','HEATING','TAX_YEAR','ASSESSED_YEAR','PROPERTY_INDICATOR',
'SITUS_HOUSE_NUMBER_PREFIX','SITUS_HOUSE_NUMBER1','SITUS_HOUSE_NUMBER2','SITUS_HOUSE_NUMBER_SUFFIX','SITUS_DIRECTION','SITUS_STREET_NAME',
'SITUS_MODE','SITUS_QUADRANT','SITUS_UNIT_NUMBER','SITUS_CITY','SITUS_STATE','SITUS_ZIP_CODE','PARCEL_LEVEL_LATITUDE__2_6_',
'PARCEL_LEVEL_LONGITUDE__3_6_']
states=['va', 'md', 'de', 'pa', 'ct', 'ri', 'ma']

for s in states:
    df, meta = pyreadstat.read_sas7bdat(YUL_path + s +'.sas7bdat', usecols=cols)
    df1, meta = pyreadstat.read_sas7bdat(YUL_path+ s +'_t12.sas7bdat', usecols=cols)
    df=df.append(df1,ignore_index=True)
    del df1
    df['ASSESSED_YEAR']=df['ASSESSED_YEAR'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df.to_csv('CoreLogic/'+ s +'_tax_IDaddressHeat_2010_2019.csv')
    del df
    print('The state is done: ',s)







#%% read new CoreLoogic Data - hist 1 2 3
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/CoreLogic/New/'


cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID",'HEATING TYPE CODE','TAX YEAR','ASSESSED YEAR','PROPERTY INDICATOR CODE',
"SITUS HOUSE NUMBER","SITUS DIRECTION","SITUS STREET NAME","SITUS MODE","SITUS QUADRANT","SITUS UNIT NUMBER","SITUS CITY",
"SITUS STATE","SITUS ZIP CODE","PARCEL LEVEL LATITUDE","PARCEL LEVEL LONGITUDE"]

states=['SC','NC','VA', 'MD', 'DE', 'PA', 'CT', 'RI', 'MA']


for i in states:
    df2021=pd.read_csv(Google_path+'property2021/'+i+'_property_hist1.csv',usecols=cols)
    df2020=pd.read_csv(Google_path+'property2020/'+i+'_property_hist2.csv',usecols=cols)
    df2019=pd.read_csv(Google_path+'property2019/'+i+'_property_hist3.csv',usecols=cols)
    df_all=pd.concat([df2021, df2020, df2019], ignore_index=True)
    #df_all['SITUS UNIT NUMBER']=df_all['SITUS UNIT NUMBER'].astype(str)  
    df_all.to_csv('CoreLogic/New_tax_IDaddressHeat2019_2021_'+i+'.csv')


# NC SC VA - miss some parts of 2021 data. Thus, need to load corelogic current tax data to add the 2021 part, see code below
# CT MA RI - miss some parts of 2019 data. Thus, need to load new prop hist4-5-6 data to get 2019 data
# Next step: for these 3 states, load all data from hist4-5-6, combine all hist1-6 together. Merge them with old data and then delete repeted rows.


#%% read new CoreLoogic Data - hist 4 5 6
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/CoreLogic/New/'


cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID",'HEATING TYPE CODE','TAX YEAR','ASSESSED YEAR','PROPERTY INDICATOR CODE',
"SITUS HOUSE NUMBER","SITUS DIRECTION","SITUS STREET NAME","SITUS MODE","SITUS QUADRANT","SITUS UNIT NUMBER","SITUS CITY",
"SITUS STATE","SITUS ZIP CODE","PARCEL LEVEL LATITUDE","PARCEL LEVEL LONGITUDE"]

states=['CT', 'RI', 'MA']


for i in states:
    df_4=pd.read_csv(Google_path+'property_hist4/'+i+'_property_hist4.csv',usecols=cols)
    df_5=pd.read_csv(Google_path+'property_hist5/'+i+'_property_hist5.csv',usecols=cols)
    df_6=pd.read_csv(Google_path+'property_hist6/'+i+'_property_hist6.csv',usecols=cols)
    df_all=pd.concat([df_4, df_5, df_6], ignore_index=True)
    #df_all['SITUS UNIT NUMBER']=df_all['SITUS UNIT NUMBER'].astype(str)  
    df_all.to_csv('CoreLogic/New_tax_IDaddressHeat_hist456_'+i+'.csv')





#%% Read new current corelogic data

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/CoreLogic/New/'


cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID",'HEATING TYPE CODE','TAX YEAR','ASSESSED YEAR','PROPERTY INDICATOR CODE',
"SITUS HOUSE NUMBER","SITUS DIRECTION","SITUS STREET NAME","SITUS MODE","SITUS QUADRANT","SITUS UNIT NUMBER","SITUS CITY",
"SITUS STATE","SITUS ZIP CODE","PARCEL LEVEL LATITUDE","PARCEL LEVEL LONGITUDE"]

states=['SC','NC','VA','MD','DE','PA','RI']


for i in states:
    df=pd.read_csv(Google_path+'property2022/'+i+'_property2022.csv',usecols=cols) 
    #df.to_csv('New_tax_IDaddressHeat_curr_'+i+'.csv')

#df['SITUS HOUSE NUMBER']=df['SITUS HOUSE NUMBER'].astype(str)
#df.to_stata('New_tax_IDaddressHeat_2022_RI.dta')

#%% Read new current corelogic data -MA only

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/Data/CoreLogic/New/'


cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID",'HEATING TYPE CODE','TAX YEAR','ASSESSED YEAR','PROPERTY INDICATOR CODE',
"SITUS HOUSE NUMBER","SITUS DIRECTION","SITUS STREET NAME","SITUS MODE","SITUS QUADRANT","SITUS UNIT NUMBER","SITUS CITY",
"SITUS STATE","SITUS ZIP CODE","PARCEL LEVEL LATITUDE","PARCEL LEVEL LONGITUDE"]

df=pd.read_csv(Google_path+'property2022/'+'MA'+'_property2022.csv',usecols=cols) 
df=df.loc[df['PROPERTY INDICATOR CODE'].isin([0,10,11,21,22])]
df.to_csv('New_tax_IDaddressHeat_curr_MA.csv')


#%% To get more building info. - size and age - SC NC VA MD DE PA CT RI MA - current period

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/Data/CoreLogic/New/'
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']
cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID","YEAR BUILT","BEDROOMS - ALL BUILDINGS","TOTAL ROOMS - ALL BUILDINGS",
      "UNIVERSAL BUILDING SQUARE FEET","LIVING SQUARE FEET - ALL BUILDINGS","PROPERTY INDICATOR CODE","BUILDING QUALITY CODE"]

for i in states:
    df=pd.read_csv(Google_path+'property2022/'+i+'_property2022.csv',usecols=cols) 
    df=df.loc[df['PROPERTY INDICATOR CODE'].isin([0,10,11,21,22])]
    df.to_csv('CoreLogic/building_age_size_quality_'+i+'_curr.csv')



#%% Get building info. - size and age - SC hist5 - in which most are 2016 assessed year
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/Data/CoreLogic/New/'
states=['SC']
cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID","YEAR BUILT","BEDROOMS - ALL BUILDINGS","TOTAL ROOMS - ALL BUILDINGS",
      "UNIVERSAL BUILDING SQUARE FEET","LIVING SQUARE FEET - ALL BUILDINGS","PROPERTY INDICATOR CODE","BUILDING QUALITY CODE"]

for i in states:
    df=pd.read_csv(Google_path+'property_hist5/'+i+'_property_hist5.csv',usecols=cols) 
    df=df.loc[df['PROPERTY INDICATOR CODE'].isin([0,10,11,21,22])]
    df.to_csv('CoreLogic/building_age_size_quality_'+i+'_hist5.csv')


#%% To get more building info. - assessed value - SC NC VA MD DE PA CT RI MA - current period

import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/Data/CoreLogic/New/'
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']
cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID","PROPERTY INDICATOR CODE","TOTAL VALUE CALCULATED","LAND VALUE CALCULATED",
      "IMPROVEMENT VALUE CALCULATED","ASSESSED TOTAL VALUE","ASSESSED LAND VALUE","ASSESSED IMPROVEMENT VALUE"]

for i in states:
    df=pd.read_csv(Google_path+'property2022/'+i+'_property2022.csv',usecols=cols) 
    df=df.loc[df['PROPERTY INDICATOR CODE'].isin([0,10,11,21,22])]
    df.to_csv('CoreLogic/building_value_'+i+'_curr.csv')

#%% To get more building info. - assessed value - SC ONLY hist5 - in which most are 2016 assessed year
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import pyreadstat
Google_path='G:/Shared drives/BIG/Data/CoreLogic/New/'
states=['SC']
cols=["FIPS CODE","APN SEQUENCE NUMBER","ONLINE FORMATTED PARCEL ID","PROPERTY INDICATOR CODE","TOTAL VALUE CALCULATED","LAND VALUE CALCULATED",
      "IMPROVEMENT VALUE CALCULATED","ASSESSED TOTAL VALUE","ASSESSED LAND VALUE","ASSESSED IMPROVEMENT VALUE"]

for i in states:
    df=pd.read_csv(Google_path+'property_hist5/'+i+'_property_hist5.csv',usecols=cols) 
    df=df.loc[df['PROPERTY INDICATOR CODE'].isin([0,10,11,21,22])]
    df.to_csv('CoreLogic/building_value_'+i+'_hist5.csv')