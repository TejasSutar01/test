# -*- coding: utf-8 -*-
"""
Created on Sat May 16 08:58:57 2020

@author: SONY
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_excel("E:\\TEJAS\\EXCELR ASSIGMENTS\\AIR QUALITY INDEX PROJECT\\CODE FILE\\Delhi (1).xlsx",na_values="-")

df.isnull().sum()

df.describe()


#Checking with missing dates in data as the data is from 1st Jan18 to 20th April18 then if we calculate all days it comes to 2617.

df1 = pd.DataFrame({'date': pd.date_range('2018-01-01', '2018-04-21', freq='1H', closed='left')})

df2 = df1.iloc[:2617,:]

df3 = pd.merge(df,df2,on='date',how='right')

df3.isnull().sum()
#Creating new column with all missing values

miss_val=df3.iloc[2374:,:]

#There are new 243 missing values and 80 which was before total it gets to 323.
miss_val.isnull().sum()

miss_val.set_index("date",inplace=True)


#Sorting the date column
df3=df3.sort_values(["date"])

df3=df3.reset_index()

#Final dataset with clean columns
fin_df=df3.iloc[:,1:3]

###Maximum data and Minimum data
fin_df[fin_df["pm25"]==fin_df["pm25"].max()]

fin_df[fin_df["pm25"]==fin_df["pm25"].min()]
#From max & min we can say that Maximum particle was during 2018-01-02 at 00:00:00 
#was 492.0  and Minimum was on 2018-04-12 at 17:00:00 and was 1.

##Setting date n time as index.
fin_df.set_index('date',inplace=True)

#Imputing using interpolation with different methods

fin_df["linear"] = fin_df["pm25"].interpolate(method = "linear")
fin_df["slinear"] = fin_df["pm25"].interpolate(method = "slinear")
fin_df["pm25_poly3"] = fin_df["pm25"].interpolate(method = "polynomial", order = 3)
fin_df["pm25_poly5"] = fin_df["pm25"].interpolate(method = "polynomial", order = 5)
fin_df["pm25_poly7"] = fin_df["pm25"].interpolate(method = "polynomial", order = 7)
fin_df["pm25_time"] = fin_df["pm25"].interpolate(method = "time")
fin_df["pm25_spline3"] = fin_df["pm25"].interpolate(method = "spline", order = 3)
fin_df["pm25_spline5"] = fin_df["pm25"].interpolate(method = "spline", order = 4)
fin_df["pm25_spline7"] = fin_df["pm25"].interpolate(method = "spline", order = 5)
fin_df["pm25_akima"] = fin_df["pm25"].interpolate(method = "akima")

###Graph of all interpolation methods.

columns = ["pm25",'linear', 'slinear',
       'pm25_poly3', 'pm25_poly5', 'pm25_poly7', 'pm25_time', 'pm25_spline3',
       'pm25_spline5', 'pm25_spline7', 'pm25_akima']


fig, ax = plt.subplots(11,1, figsize = (25,30), sharex = True)
i = 0
for col in columns:  
  ax[i].plot(fin_df[col])
  ax[i].set_title(col)
  i+=1








###PLot data on weekly basis
weekly=fin_df.resample("W").sum()
weekly.plot(style=[":","--","-"])

###PLot data on daily basis
daily=fin_df.resample("D").sum()
daily.plot(style=[":","--","-"])

###Plot data on time basis
time=df1.groupby(df1.index.time).mean()
hourly_ticks=4*60*60*np.arange(6)
time.plot(xticks=hourly_ticks,style=[":","--","-"])

##pm25 distribution
sns.distplot(df1["pm25"])
plt.scatter("pm25","date",color="k",data=df)

#Imputing using interpolation with different methods
df1 = df1.interpolate(method="time")

##relation between pm25 & time 
sns.lineplot(x=df1["New_Time"],y=df1["pm25"], data=df1)





