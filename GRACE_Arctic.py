#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 06:18:04 2023

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
regions=['Arctic_Canada_North','Arctic_Canada_South']

ver=''
ver=''

vers=['2022','2023']

vers=['v_Wouters_20220102','v_WoutersGlambie_202309']

for ver in vers:
    rates_raw=[]
    rates_infilled=[]
    regions_list=[]
    
    for rr,region in enumerate(regions):
        # if region=='Greenland':
        # if region=='Alaska':
        # if region=='Svalbard':
        # if region=='Iceland':
        # if region=='Arctic_Canada_South':
        # if region=='Arctic_Canada_North':
        if region!='Null':
            print(region.lower())
            if ver=='v_WoutersGlambie_202309':
                fn=f"/Users/jason/Dropbox/Glaciers_of_the_Arctic/Wouters_gravimetry_Glambie_submission 2/Wouters_{region.lower()}.csv"
                df=pd.read_csv(fn)
                df["year"]=df.end_dates.astype(int)
                temp=((df.end_dates-df["year"])*12)+1
                # df["mb"]=df.changes
            else:
                fn=base_path+'/20220102/'+region+'_no_GIA_err.txt'
                df=pd.read_csv(fn, delim_whitespace=True,skiprows=1,names=['dec_year','mb','err'])
        
                df.dec_year=pd.to_numeric(df.dec_year)
                df.mb=pd.to_numeric(df.mb)
                df.err=pd.to_numeric(df.err)
        
                df[df=="NA"]=np.nan
                # df = df[df.notna()]
                df=df.dropna(axis = 0, how = 'all')
        
        
                # print(df)
                df["year"]=df.dec_year.astype(int)
                temp=((df.dec_year-df["year"])*12)+1
    
            N=len(df)
    
            # plt.plot(df["month"])
            df["month"]=temp.astype(int)
            df["day"]=(temp-df["month"])*30.5
            df["day"]=df["day"].astype(int)
            df["day"][df["day"]==0]=1
            df["time"]=pd.to_datetime(df[['year', 'month', 'day']])
            df["jt"]=df["time"].dt.year+df["time"].dt.dayofyear/366
            df.index = pd.to_datetime(df.time)
            
            # print(df.month,df.day,temp-df.month)
            
            i_year=2002 ; f_year=2021 ; n_years=f_year-i_year+1
            
            dmdt_2d=np.zeros(N)
            dmdt_2d=np.zeros((n_years,12))
            dmdt_2d_raw=np.zeros((n_years,12))
            dmdt_2d_fill_indexes=np.zeros((n_years,12))
    
            if ver=='v_Wouters_20220102':
                # compute dmdt on a 2d array        
                for i in range(N-1):
                    # print(df["month"][i],df["month"][i+1]-df["month"][i])
                    if df["month"][i+1]-df["month"][i]==1:
                        # print(df["year"][i],df["month"][i],df.mb[i+1]-df.mb[i])
                        dmdt_2d[df["year"][i]-i_year,df["month"][i]]=df.mb[i+1]-df.mb[i]
                        dmdt_2d_raw[df["year"][i]-i_year,df["month"][i]]=df.mb[i+1]-df.mb[i]
                    if df["month"][i+1]-df["month"][i]==-11:
                        # print(df["year"][i],df["month"][i],df.mb[i+1]-df.mb[i])
                        dmdt_2d[df["year"][i]-i_year,0]=df.mb[i+1]-df.mb[i]
                        dmdt_2d_raw[df["year"][i]-i_year,0]=df.mb[i+1]-df.mb[i]
            else:
                # compute dmdt on a 2d array
                df['mb']=np.nan
                temp=0.
                for i in range(N-1):
                    temp+=df.changes[i]
                    df.mb[i]=temp
                    # print(df["month"][i],df["month"][i+1]-df["month"][i])
                    if df["month"][i+1]-df["month"][i]==1:
                        dmdt_2d[df["year"][i]-i_year,df["month"][i]]=df.changes[i]
                        dmdt_2d_raw[df["year"][i]-i_year,df["month"][i]]=df.changes[i]
                    if df["month"][i+1]-df["month"][i]==-11:
                        # print(df["year"][i],df["month"][i],df.mb[i+1]-df.mb[i])
                        dmdt_2d[df["year"][i]-i_year,0]=df.changes[i]
                        dmdt_2d_raw[df["year"][i]-i_year,0]=df.changes[i]

            df.to_csv(f'/Users/jason/Dropbox/GRACE/Wouters/GRACE_Arctic_Wouters/output/reformatted/{region}_{ver}.csv')

                
            dmdt_2d[dmdt_2d==0]=np.nan
            dmdt_2d_raw[dmdt_2d_raw==0]=np.nan
            # for yy in range(i_year,f_year+1):
            #     print(yy)
            
            # obtain mean dmdt for that month
            dmdt_months=np.zeros(12)
            for mm in range(12):
                dmdt_months[mm]=np.nanmean(dmdt_2d[:,mm])
                # print(mm,np.nanmean(dmdt_2d[:,mm]))
    
    
            for mm in range(12):
                dmdt_2d_fill_indexes[:,mm][~np.isfinite(dmdt_2d[:,mm])]=1
                dmdt_2d[:,mm][~np.isfinite(dmdt_2d[:,mm])]=dmdt_months[mm]
            
            # plt.plot(dmdt_months,'-o')
    
            months_index=np.arange(12)
            plt_2d_annual=1
            if plt_2d_annual:
                n_rows=1; fig, ax = plt.subplots(n_rows,1,figsize=(18,15))
                for yy in range(i_year,f_year+1):
                    if yy==2017:
                        plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                        v=np.where(dmdt_2d_fill_indexes[yy-i_year,:]==1)
                        plt.plot(v[0],dmdt_2d[yy-i_year,:][dmdt_2d_fill_indexes[yy-i_year,:]==1],
                                 's',markersize=10,color='g',label='in-filled '+str(yy))
                    # if yy==2010:plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                    if yy==2012:
                        plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                        print(dmdt_2d[yy-i_year,:])
                        v=np.where(dmdt_2d_fill_indexes[yy-i_year,:]==1)
                        plt.plot(v[0],dmdt_2d[yy-i_year,:][dmdt_2d_fill_indexes[yy-i_year,:]==1],
                                 '*',markersize=20,color='C0',label='in-filled '+str(yy))
                        print(v[0],dmdt_2d[yy-i_year,:][dmdt_2d_fill_indexes[yy-i_year,:]==1])
                    if yy==2016:plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                    if yy==2019:plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                        
                    if yy==2021:plt.plot(dmdt_2d[yy-i_year,:],'-o',label=yy)
                plt.legend()
                
    #%% infill into 2d array the missing months
            dmdt_infilled_1d=np.zeros(n_years*12)
            dm_infilled_1d_cum=np.zeros(n_years*12)
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
                        # dmdt_2d[yy-i_year,mm]=dmdt_months[mm]
    
                    if ~np.isfinite(dmdt_2d[yy-i_year,mm]):
                        dmdt_infilled_1d[cc]=dmdt_months[mm]
    
                    year_1d[cc]=yy
                    month_1d[cc]=mm+1
                    # temp+=dmdt_infilled_1d[cc]
                    if np.isfinite(dmdt_2d_raw[yy-i_year,mm]):temp+=dmdt_2d_raw[yy-i_year,mm]
                    if ~np.isfinite(dmdt_2d_raw[yy-i_year,mm]):temp+=dmdt_2d[yy-i_year,mm]
                    dm_infilled_1d_cum[cc]=temp
                    # print(yy,mm,dmdt_2d[yy-i_year,mm],dmdt_infilled_1d[cc])
                    cc+=1
    
                    
    #%% obtain 1 d in-filled time series
    
            df_infilled = pd.DataFrame(columns=['year', 'month', 'day','mb','dmdt'])
            
            df_infilled["month"]=pd.Series(month_1d)
            df_infilled["year"]=pd.Series(year_1d)
            df_infilled["day"]=pd.Series(day_1d)
            df_infilled["dmdt"]=pd.Series(dmdt_infilled_1d)
            df_infilled["mb"]=pd.Series(dm_infilled_1d_cum)
            
            # from datetime import datetime, timedelta
    
            df_infilled["time"]=pd.to_datetime(df_infilled[['year', 'month','day']])
            df_infilled["jt"]=df_infilled["time"].dt.year+df_infilled["time"].dt.dayofyear/366
            
            df_infilled.index = pd.to_datetime(df_infilled.time)
    
            df_infilled.to_csv('./output/'+region+'_gap-filled'+ver+'.csv')
                    
    #%%
            # plt.plot(df.month)
            # df = df.loc[df['time']>='2021-01-01',:] 
            month_names=['J','F','M','A','M','June','July','August','S','O','N','D']
            n_rows=1
            
            fig, ax = plt.subplots(n_rows,1,figsize=(18,15))
        
            t0=datetime(2016, 9, 15) ; t1=datetime(2021, 12, 15)
            t0=datetime(2002, 9, 15) ; t1=datetime(2021, 12, 15)
            
            # df.mb-=df.mb[0]
            df_infilled.mb-=df_infilled.mb[0]
            df.mb[t0:t1]-=np.nanmean(df.mb[t0:datetime(2003, 9, 15)])
            plt.plot(df.mb[t0:t1],'-o',color='b',linewidth=th*2,label='raw')
            df_infilled.mb[t0:t1]-=np.nanmean(df_infilled.mb[t0:datetime(2003, 9, 15)])
            # plt.plot(df_infilled.mb[t0:t1],'-o',color='r',linewidth=th*2,label='infilled')
            # plt.plot(df_infilled.mb[t0:t1],'-o',color='r',linewidth=th*2,label='gap-filled')
            # plt.title(ver)
    
            t0=datetime(2002, 9, 15) ; t1=datetime(2015, 9, 15)
            x=df_infilled["jt"][t0:t1].values
            y=df_infilled.mb[t0:t1].values
            b, m = polyfit(x, y, 1)
            rates_infilled.append(m)
    
            x=df["jt"][t0:t1].values
            y=df.mb[t0:t1].values
            b, m = polyfit(x, y, 1)
            rates_raw.append(m)
    
            regions_list.append(region)
    
            mb_annual_hydrological=np.zeros(n_years)
            years=np.zeros(n_years)
            
            # cc=0
            # mult=0.6
            # for yy in range(i_year+1,f_year+1):
            #     years[yy-i_year]=yy
            #     for mm in range(12):
            #         if df_infilled.year[cc]>2016:
            #             # plt.text(datetime(df_infilled.year[cc].astype(int),
            #             #         df_infilled.month[cc].astype(int),df_infilled.day[cc].astype(int)),
            #             #           df_infilled.mb[cc],
            #             #           "{:.0f}".format(mm+1),c='k',ha='center',va='center',
            #             #           fontsize=font_size*mult)
            #             plt.text(datetime(df_infilled.year[cc].astype(int),
            #                     df_infilled.month[cc].astype(int),df_infilled.day[cc].astype(int)),
            #                       df_infilled.mb[cc],
            #                       month_names[mm],c='k',ha='center',va='center',
            #                       fontsize=font_size*mult)                
            #         cc+=1
    
            #     v=np.where((df_infilled.year==yy)&(df_infilled.month==9))
            #     mb_annual_hydrological[yy-i_year]=df_infilled.mb[v[0][0]]-df_infilled.mb[v[0][0]-12]
                
            #     if df_infilled.year[v[0][0]]>2016:
            #         plt.plot([datetime(yy,9,15),datetime(yy-1,9,15)],[df_infilled.mb[v[0][0]],df_infilled.mb[v[0][0]-12]],c='r',linestyle='--')
            #         mx=(df_infilled.mb[v[0][0]]+df_infilled.mb[v[0][0]-12])/2
            #         yx=(df_infilled.mb[v[0][0]]-df_infilled.mb[v[0][0]-12])
            #         plt.text(datetime(yy,1,1),mx,"{:.0f}".format(yx),c='r')
    
                # print(yy,df_infilled.mb[v[0][0]],df_infilled.mb[v[0][0]-12],mb_annual_hydrological[yy-i_year])
    
            # plt.title(region+' GRACE & GRACE-FO mass change')
            plt.title(ver+' '+region+' satellite-derived mass change')
            plt.ylabel('Gt')
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center' )
            plt.legend()
            
            ly='p'
            
            if ly == 'x':plt.show()
            
            plt_eps=0
            fig_path='./Figs/'
            if ly == 'p':
                plt.savefig(fig_path+region+'_'+ver+'.png', bbox_inches='tight', dpi=72)
                # if plt_eps:
                #     plt.savefig(fig_path+site+'_'+str(i).zfill(2)+nam+'.eps', bbox_inches='tight')
    
            # data=[[years],[means],[stds]]
            df2 = pd.DataFrame(columns = ['year', 'mass_balance_sept_to_sept_Gt']) 
            df2.index.name = 'index'
            df2["year"]=pd.Series(years)
            df2["mass_balance_sept_to_sept_Gt"]=pd.Series(mb_annual_hydrological)
            df2 = df2.drop(df2.index[0])
            # df2["std"]=pd.Series(stds)
            # df2["n"]=pd.Series(n)
            
            # df2 = df2.loc[:, ~df2.columns.str.contains('^Unnamed')]
            df2.to_csv('./output/'+region+'_hydrological_year_'+ver+'.csv')
            
    # out=pd.DataFrame({'region':np.array(regions_list),
    #       'mb':np.array(rates_raw),
    #       'mb_infilled':np.array(rates_infilled),
    #       })
    # print(ver,out)
    
    # out.to_csv('/Users/jason/Dropbox/GRACE/Wouters/GRACE_Arctic_Wouters/output/v'+ver+'_2003-2015_mb.csv',index=None)