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
regionsx=['ACN','ACS']

# regions=['Arctic_Canada_North']

ver=''
ver=''

vers=['2022','2023']

vers=['v_Wouters_20220102','v_WoutersGlambie_202309']

month_names=['J','F','M','A','M','June','July','August','S','O','N','D']
n_rows=1

fig, ax = plt.subplots(n_rows,1,figsize=(18,15))

t0=datetime(2016, 9, 15) ; t1=datetime(2021, 12, 15)

colors=['b','r']
lines=['-','--']

rates_raw=[]
regions_list=[]
version_list=[]
    
for rr,region in enumerate(regions):
    # if region=='Greenland':
    # if region=='Alaska':
    # if region=='Svalbard':
    # if region=='Iceland':
    # if region=='Arctic_Canada_South':
    # if region=='Arctic_Canada_North':
    if region!='Null':
        for vv,ver in enumerate(vers):
            print(region.lower())
            fn=f'/Users/jason/Dropbox/GRACE/Wouters/GRACE_Arctic_Wouters/output/reformatted/{region}_{ver}.csv'
            df=pd.read_csv(fn)
                
            df.index = pd.to_datetime(df.time)
            t0=datetime(2002, 9, 15)
            df.mb[t0:t1]-=np.nanmean(df.mb[t0:datetime(2015, 9, 15)])

            # print(df.month,df.day,temp-df.month)
            
            # plt.plot(df.month)
            # df = df.loc[df['time']>='2021-01-01',:] 

            
            # df.mb-=df.mb[0]
            # df_infilled.mb-=df_infilled.mb[0]
            
            t0=datetime(2002, 9, 15) ; t1=datetime(2015, 9, 15)
            # x=df_infilled["jt"][t0:t1].values
            # y=df_infilled.mb[t0:t1].values
            # b, m = polyfit(x, y, 1)
            # rates_infilled.append(m)
    
            x=df["jt"][t0:t1].values
            y=df.mb[t0:t1].values
            b, m = polyfit(x, y, 1)
            rates_raw.append(m)
            regions_list.append(region)
            version_list.append(ver)
            xx=[x[0],x[-1]]
            yy=[xx[0]*m+b,xx[1]*m+b]
            # plt.plot([datetime(2002, 9, 15),datetime(2015, 9, 15)],yy,color=colors[vv],linewidth=th*4,linestyle=lines[rr])
            
            t0=datetime(2002, 9, 15) ; t1=datetime(2015, 12, 15)
            plt.plot(df.mb[t0:t1],color=colors[vv],linewidth=th*2,linestyle=lines[rr],label=region+', '+ver+",  trend: %.1f" % m+' Gt/y')
            # df_infilled.mb[t0:t1]-=np.nanmean(df_infilled.mb[t0:datetime(2003, 9, 15)])
            # plt.plot(df_infilled.mb[t0:t1],'-o',color='r',linewidth=th*2,label='infilled')
            # plt.plot(df_infilled.mb[t0:t1],'-o',color='r',linewidth=th*2,label='gap-filled')
            # plt.title(ver)

        tit=region.replace('_','-')
        fn=f'/Users/jason/Dropbox/Glaciers_of_the_Arctic/GOA-2023/output/ArcticInSituvGRACE_{tit}_mass_balance_1971-2022.csv'
        df_scaled=pd.read_csv(fn)
        df_scaled['month']=6
        df_scaled['day']=15
        df_scaled["time"]=pd.to_datetime(df_scaled[['year', 'month', 'day']])

        df_scaled['cumu']=np.nan
        temp=0
        for i in range(len(df_scaled)):
            temp+=df_scaled.mass_balance[i]
            df_scaled['cumu'][i]=temp

        df_scaled.index = pd.to_datetime(df_scaled.time)
        
        osy=np.mean(df_scaled.cumu[datetime(2002, 6, 15):datetime(2015, 6, 15)].values)
        # df_scaled.index = pd.to_datetime(df_scaled['year'], format='%Y-%m-%d').year

        
        plt.plot(df_scaled.cumu-osy,'o',color=colors[rr],label=f'{regionsx[rr]} reconstruction after Box et al 2018')
        
            # plt.title(region+' GRACE & GRACE-FO mass change')
# plt.title(region+' satellite-derived mass change')
# plt.title('regional gravimetric mass changes')
plt.ylabel('cumulative mass change relative to 2002-2015, Gt')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center' )
plt.legend()


out=pd.DataFrame({'region':np.array(regions_list),
      'mb':np.array(rates_raw),
      'version':np.array(version_list),
      # 'mb_infilled':np.array(rates_infilled),
      })

vals=['mb']

for val in vals:
    out[val] = out[val].map(lambda x: '%.1f' % x)
    
print(ver,out)

out.to_csv('/Users/jason/Dropbox/GRACE/Wouters/GRACE_Arctic_Wouters/output/v'+ver+'_2003-2015_mb.csv',index=None)
ly='x'

if ly == 'x':plt.show()

plt_eps=0
fig_path='./Figs/'
if ly == 'p':
    plt.savefig(fig_path+region+'_2017-2021_'+ver+'.png', bbox_inches='tight', dpi=72)
    # if plt_eps:
    #     plt.savefig(fig_path+site+'_'+str(i).zfill(2)+nam+'.eps', bbox_inches='tight')
    
