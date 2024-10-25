# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:36:39 2023

@author: wills
"""
#%% 

#########     by income
#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Those are the building owned by people - exclude renters
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']
age=[]
for s in states:
    building=pd.read_stata('CoreLogic/building_age_size_quality_'+s+'_curr.dta')
    building.rename(columns={'FIPSCODE':'FIPS_CODE','APNSEQUENCENUMBER':'APN_SEQUENCE_NBR', 'ONLINEFORMATTEDPARCELID':'P_ID_IRIS_FRMTD'},inplace=True)
    main=pd.read_stata('Analysis/Panel_IDaddressHeat_demographics_'+s+'.dta')
    main=main[main.ASSESSED_YEAR==2021]
    main=pd.merge(main, building, how='left', on=['FIPS_CODE', 'APN_SEQUENCE_NBR', 'P_ID_IRIS_FRMTD'])
    main=main[main.Ethnic.isin(['Black or African American','Hispanic','White'])]
    main=main[(main['PROPERTY_INDICATOR'].isin([10, 11])) & (main['OWNER_RENTER_STATUS'] == 9)]
    main['income_quantile']=pd.cut(main['FIND_DIV_1000'], bins=10,labels=['1', '2', '3', '4','5','6','7','8','9','10'])
    main['building_age']=2022-main['YEARBUILT']
    main = main.groupby(['income_quantile', 'Ethnic']).aggregate({'building_age':['mean','std']})
    main=main.reset_index()
    main.columns = main.columns.get_level_values(0)
    main.columns = ['income_quantile', 'Ethnic', 'mean','std']
    main['state']=s
    age=age+[main]

pd.concat(age).to_csv('Analysis/building_age_by_race_income.csv')

#%%
%matplotlib

#%% Plot the building age by income by race and by state

df=[]
for j in range(9):
    temp=[age[j][age[j].Ethnic==i] for i in ['Black or African American','Hispanic','White']]
    df=df+[temp]
del [j,s,temp]

#Plot
fig, ax = plt.subplots(1,9,figsize=(30,15))
width = 0.1
ax[0].errorbar(df[0][0]['mean'], np.arange(10) - width ,xerr=df[0][0]['std'] ,color='black',fmt='.', ms=10, label='Black')
ax[0].errorbar(df[0][1]['mean'], np.arange(10),xerr=df[0][1]['std'] , color='C2',fmt='.',ms=10,label='Hispanic')
ax[0].errorbar(df[0][2]['mean'], np.arange(10) + width, xerr=df[0][2]['std'], color='C3',fmt='.',ms=10,label='White')
ax[0].set_yticks([0, 1, 2, 3, 4,5,6,7,8,9])
ax[0].set_yticklabels(['10%','20%', '30%','40%', '50%','60%', '70%','80%', '90%', '100%'])
ax[0].set_xlabel('Building Age',fontsize=15)
ax[0].set_ylabel('Income intervals',fontsize=20)
ax[0].title.set_text('SC')
ax[0].title.set_size(20)
for i,s in zip(range(1,9),['NC','VA','MD','DE','PA','CT','RI','MA']):
    ax[i].errorbar(df[i][0]['mean'], np.arange(10) - width ,xerr=df[i][0]['std'] ,color='black',fmt='.',ms=10,label='Black')
    ax[i].errorbar(df[i][1]['mean'], np.arange(10),xerr=df[i][1]['std'] , color='C2',fmt='.',ms=10,label='Hispanic')
    ax[i].errorbar(df[i][2]['mean'], np.arange(10) + width, xerr=df[i][2]['std'], color='C3',fmt='.',ms=10,label='White')
    ax[i].set_yticks([])
    ax[i].set_xlabel('Building Age',fontsize=15)
    ax[i].title.set_text(s)
    ax[i].title.set_size(20)
plt.legend(bbox_to_anchor=(1,1), loc="upper left",prop={'size': 15})
plt.show()
plt.savefig('building_age_by_race_income.png',dpi=300)


#%% 

#########    by Wealth

#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Those are the building owned by people - exclude renters
states=['SC','NC','VA','MD','DE','PA','CT','RI','MA']
age=[]
for s in states:
    building=pd.read_stata('CoreLogic/building_age_size_quality_'+s+'_curr.dta')
    building.rename(columns={'FIPSCODE':'FIPS_CODE','APNSEQUENCENUMBER':'APN_SEQUENCE_NBR', 'ONLINEFORMATTEDPARCELID':'P_ID_IRIS_FRMTD'},inplace=True)
    main=pd.read_stata('Analysis/Panel_IDaddressHeat_demographics_'+s+'.dta')
    main=main[main.ASSESSED_YEAR==2021]
    main=pd.merge(main, building, how='left', on=['FIPS_CODE', 'APN_SEQUENCE_NBR', 'P_ID_IRIS_FRMTD'])
    main=main[main.Ethnic.isin(['Black or African American','Hispanic','White'])]
    main=main[(main['PROPERTY_INDICATOR'].isin([10, 11])) & (main['OWNER_RENTER_STATUS'] == 9)]
    main['wealth_quantile']=pd.cut(main['WEALTH_FINDER_SCORE'], bins=10,labels=['1', '2', '3', '4','5','6','7','8','9','10'])
    main['building_age']=2022-main['YEARBUILT']
    main = main.groupby(['wealth_quantile', 'Ethnic']).aggregate({'building_age':['mean','std']})
    main=main.reset_index()
    main.columns = main.columns.get_level_values(0)
    main.columns = ['wealth_quantile', 'Ethnic', 'mean','std']
    main['state']=s
    age=age+[main]

pd.concat(age).to_csv('Analysis/building_age_by_race_wealth.csv')

#%%
%matplotlib

#%% Plot the building age by wealth by race and by state

df=[]
for j in range(9):
    temp=[age[j][age[j].Ethnic==i] for i in ['Black or African American','Hispanic','White']]
    df=df+[temp]
del [j,s,temp]

#Plot
fig, ax = plt.subplots(1,9,figsize=(30,15))
width = 0.1
ax[0].errorbar(df[0][0]['mean'], np.arange(10) - width ,xerr=df[0][0]['std'] ,color='black',fmt='.', ms=10, label='Black')
ax[0].errorbar(df[0][1]['mean'], np.arange(10),xerr=df[0][1]['std'] , color='C2',fmt='.',ms=10,label='Hispanic')
ax[0].errorbar(df[0][2]['mean'], np.arange(10) + width, xerr=df[0][2]['std'], color='C3',fmt='.',ms=10,label='White')
ax[0].set_yticks([0, 1, 2, 3, 4,5,6,7,8,9])
ax[0].set_yticklabels(['10%','20%', '30%','40%', '50%','60%', '70%','80%', '90%', '100%'])
ax[0].set_xlabel('Building Age',fontsize=15)
ax[0].set_ylabel('Wealth quantiles',fontsize=20)
ax[0].title.set_text('SC')
ax[0].title.set_size(20)
for i,s in zip(range(1,9),['NC','VA','MD','DE','PA','CT','RI','MA']):
    ax[i].errorbar(df[i][0]['mean'], np.arange(10) - width ,xerr=df[i][0]['std'] ,color='black',fmt='.',ms=10,label='Black')
    ax[i].errorbar(df[i][1]['mean'], np.arange(10),xerr=df[i][1]['std'] , color='C2',fmt='.',ms=10,label='Hispanic')
    ax[i].errorbar(df[i][2]['mean'], np.arange(10) + width, xerr=df[i][2]['std'], color='C3',fmt='.',ms=10,label='White')
    ax[i].set_yticks([])
    ax[i].set_xlabel('Building Age',fontsize=15)
    ax[i].title.set_text(s)
    ax[i].title.set_size(20)
plt.legend(bbox_to_anchor=(1,1), loc="upper left",prop={'size': 15})
plt.show()
plt.savefig('building_age_by_race_wealth.png',dpi=300)








#%% Plot  - all states - By income  and  wealth
# See Do file for data processing
%matplotlib

#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity/data')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'Arial'

df_income=pd.read_stata('Analysis/building_age_by_race_income_all_states.dta')
df_wealth=pd.read_stata('Analysis/building_age_by_race_wealth_all_states.dta')

#Plot
fig, ax = plt.subplots(1,2,figsize=(13,15))
width = 0.1
lw=2
ax[0].errorbar(df_income[df_income.Ethnic=='White']['mean_building_age'],
               np.arange(10) + width ,xerr=df_income[df_income.Ethnic=='White']['sd_building_age']
               ,color='dodgerblue',fmt='.', ms=10, label='White',linewidth=lw)
ax[0].errorbar(df_income[df_income.Ethnic=='Hispanic']['mean_building_age'],
               np.arange(10) ,xerr=df_income[df_income.Ethnic=='Hispanic']['sd_building_age']
               ,color='crimson',fmt='.', ms=10, label='Hispanic',linewidth=lw)
ax[0].errorbar(df_income[df_income.Ethnic=='Black or African American']['mean_building_age'],
               np.arange(10) - width ,xerr=df_income[df_income.Ethnic=='Black or African American']['sd_building_age']
               ,color='black',fmt='.', ms=10, label='Black',linewidth=lw)
ax[0].set_yticks([0, 1, 2, 3, 4,5,6,7,8,9])
ax[0].set_yticklabels(['10%','20%', '30%','40%', '50%','60%', '70%','80%', '90%', '100%'])
ax[0].set_xlabel('Building Age (yrs.)',fontsize=18)
ax[0].set_ylabel('Income quantiles',fontsize=18)
ax[0].title.set_text('By income quantiles')
ax[0].title.set_size(20)

ax[1].errorbar(df_wealth[df_wealth.Ethnic=='White']['mean_building_age'],
               np.arange(10) + width ,xerr=df_wealth[df_wealth.Ethnic=='White']['sd_building_age']
               ,color='dodgerblue',fmt='.', ms=10, label='White',linewidth=lw)
ax[1].errorbar(df_wealth[df_wealth.Ethnic=='Hispanic']['mean_building_age'],
               np.arange(10) ,xerr=df_wealth[df_wealth.Ethnic=='Hispanic']['sd_building_age']
               ,color='crimson',fmt='.', ms=10, label='Hispanic',linewidth=lw)
ax[1].errorbar(df_wealth[df_wealth.Ethnic=='Black or African American']['mean_building_age'],
               np.arange(10) - width ,xerr=df_wealth[df_wealth.Ethnic=='Black or African American']['sd_building_age']
               ,color='black',fmt='.', ms=10, label='Black',linewidth=lw)
ax[1].set_yticks([0, 1, 2, 3, 4,5,6,7,8,9])
ax[1].set_yticklabels(['10%','20%', '30%','40%', '50%','60%', '70%','80%', '90%', '100%'])
ax[1].set_xlabel('Building Age (yrs.)',fontsize=18)
ax[1].set_ylabel('Wealth quantiles',fontsize=18)
ax[1].title.set_text('By wealth quantiles')
ax[1].title.set_size(20)

ax[1].legend(loc='lower left', bbox_to_anchor=(1, 0), prop={'size': 15})
#ax[1].legend(loc='lower left',prop={'size': 15})
ax[0].tick_params(axis='both', which='both', labelsize=14)
ax[1].tick_params(axis='both', which='both', labelsize=14)

plt.subplots_adjust(wspace=0.5,right=0.82)
plt.show()
plt.savefig('building_age_by_race_all_states.png',dpi=300)



#%% Plot  - all states - Just by race only
# See Do file "5e_decomposition_cross sectional - Household level.do" for data processing
%matplotlib

#%%
import os
os.chdir('C:/Users/wills/Dropbox (YSE)/xingchi.shen@yale.edu’s files/heating equity')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'Arial'
#%%
# Data
races = ['White', 'Hispanic', 'Black']
mean_building_age = [52.61, 62.17, 64.74]
std_dev_building_age = [35.14, 36.83, 33.77]

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))
width = 0.1
x_positions = np.arange(len(races))
# Error bars
ax.errorbar(x_positions, mean_building_age, yerr=std_dev_building_age, fmt='o', capsize=5, label='Building Age')
# Setting x-ticks
ax.set_xticks(x_positions)
ax.set_xticklabels(races)
ax.set_ylabel('Building Age (years)', fontsize=14)
ax.set_xlabel('Racial Groups', fontsize=14)
ax.set_title('Building Age by Race', fontsize=16)
plt.show()

# Save the plot
# plt.savefig('building_age_by_race.png', dpi=300)
