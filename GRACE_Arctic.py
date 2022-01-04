# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:50:42 2021

@author: jason
"""


import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os
import pandas as pd
from datetime import datetime 
from numpy.polynomial.polynomial import polyfit


if os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/GRACE/Wouters/GRACE_Arctic_Wouters'

os.chdir(base_path)


th=1 
font_size=26
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = font_size
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th
plt.rcParams['axes.linewidth'] = th #set the value globally
plt.rcParams['figure.figsize'] = 17, 10
plt.rcParams["legend.framealpha"] = 0.8
plt.rcParams['figure.figsize'] = 5, 4

regions=['Iceland','Novaya_Zemlya','Greenland','Arctic_Canada_North','Svalbard','Arctic_Russia','Severnya_Zemlya','Franz_Josef_Land','Arctic_Canada_South','Alaska']



for rr,region in enumerate(regions):
    # if region=='Greenland':
    # if region=='Iceland':
    if region!='Null':
        print(region)
        fn=base_path+'/20210102/'+region+'_no_GIA_err.txt'
        df=pd.read_csv(fn, delim_whitespace=True,skiprows=1,names=['dec_year','mb','err'])

        df.dec_year=pd.to_numeric(df.dec_year)
        df.mb=pd.to_numeric(df.mb)
        df.err=pd.to_numeric(df.err)

        df[df=="NA"]=np.nan
        # df = df[df.notna()]
        df=df.dropna(axis = 0, how = 'all')
        N=len(df)


        # print(df)
        df["year"]=df.dec_year.astype(int)
        temp=((df.dec_year-df["year"])*12)+1
        df["month"]=temp.astype(int)
        df["day"]=(temp-df["month"])*30.5
        df["day"]=df["day"].astype(int)
        df["time"]=pd.to_datetime(df[['year', 'month', 'day']])
        df.index = pd.to_datetime(df.time)
        # print(df.month,df.day,temp-df.month)
        
        i_year=2002 ; f_year=2021 ; n_years=f_year-i_year+1
        
        dmdt_2d=np.zeros(N)
        dmdt_2d=np.zeros((n_years,12))

        # compute dmdt on a 2d array        
        for i in range(N-1):
            # print(df["month"][i],df["month"][i+1]-df["month"][i])
            if df["month"][i+1]-df["month"][i]==1:
                # print(df["year"][i],df["month"][i],df.mb[i+1]-df.mb[i])
                dmdt_2d[df["year"][i]-i_year,df["month"][i]]=df.mb[i+1]-df.mb[i]
            if df["month"][i+1]-df["month"][i]==-11:
                # print(df["year"][i],df["month"][i],df.mb[i+1]-df.mb[i])
                dmdt_2d[df["year"][i]-i_year,0]=df.mb[i+1]-df.mb[i]

        dmdt_2d[dmdt_2d==0]=np.nan
        # for yy in range(i_year,f_year+1):
        #     print(yy)
        
        # obtain mean dmdt for that month
        dmdt_months=np.zeros(12)
        for mm in range(12):
            dmdt_months[mm]=np.nanmean(dmdt_2d[:,mm])
            # print(mm,np.nanmean(dmdt_2d[:,mm]))
            # dmdt_2d[:,mm][~np.isfinite(dmdt_2d[:,mm])]=np.nanmean(dmdt_2d[:,mm])
        
#%% infill into 2d array the issing months
        dmdt_infilled_1d=np.zeros(n_years*12)
        dm_infilled_1d=np.zeros(n_years*12)
        year_1d=np.zeros(n_years*12)
        month_1d=np.zeros(n_years*12)
        day_1d=np.zeros(n_years*12)
        day_1d[:]=15
        
        cc=0
        temp=0.
        
        for yy in range(i_year,f_year+1):
            for mm in range(12):
                v=np.where((df.year==yy)&(df.month==mm+1))
                if np.shape(v)[1]==0:
                    # print(yy,mm,'missing')
                    dmdt_2d[yy-i_year,mm]=dmdt_months[mm]
                    dmdt_infilled_1d[cc]=dmdt_2d[yy-i_year,mm]
                else:
                    # print(yy,mm)
                    dmdt_infilled_1d[cc]=dmdt_2d[yy-i_year,mm]
                if ~np.isfinite(dmdt_2d[yy-i_year,mm]):
                    dmdt_infilled_1d[cc]=dmdt_months[mm]

                year_1d[cc]=yy
                month_1d[cc]=mm+1
                temp+=dmdt_infilled_1d[cc]
                dm_infilled_1d[cc]=temp
                # print(yy,mm,dmdt_2d[yy-i_year,mm],dmdt_infilled_1d[cc])
                cc+=1

                
#%% obtain 1 d in-filled time series

        df_infilled = pd.DataFrame(columns=['year', 'month', 'day','mb','dmdt'])
        
        df_infilled["month"]=pd.Series(month_1d)
        df_infilled["year"]=pd.Series(year_1d)
        df_infilled["day"]=pd.Series(day_1d)
        df_infilled["dmdt"]=pd.Series(dmdt_infilled_1d)
        df_infilled["mb"]=pd.Series(dm_infilled_1d)
        
        df_infilled["time"]=pd.to_datetime(df_infilled[['year', 'month','day']])
        df_infilled.index = pd.to_datetime(df_infilled.time)

                
#%%
        # plt.plot(df.month)
        
        
        # df = df.loc[df['time']>='2021-01-01',:] 
    
    
        n_rows=1
        
        fig, ax = plt.subplots(n_rows,1,figsize=(18,15))

    
        # t0=datetime(2021, 5, 15) ; t1=datetime(2021, 10, 1)
        
        plt.plot(df.mb,'-o',color='b',linewidth=th*2,label='raw')
        plt.plot(df_infilled.mb,'-o',color='r',linewidth=th*2,label='infilled')

        plt.title(region+' GRACE & GRACE-FO mass balance')
        plt.ylabel('Gt')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center' )
        plt.legend()
        
        ly='p'
        
        if ly == 'x':plt.show()
        
        plt_eps=0
        fig_path='./Figs/'
        if ly == 'p':
            plt.savefig(fig_path+region+'.png', bbox_inches='tight', dpi=250)
            # if plt_eps:
            #     plt.savefig(fig_path+site+'_'+str(i).zfill(2)+nam+'.eps', bbox_inches='tight')
