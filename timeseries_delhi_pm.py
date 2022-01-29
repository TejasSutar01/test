

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose

#--------------------Run this cell to mount your Google Drive-------------------
from google.colab import drive
drive.mount('/content/drive')

data = pd.read_excel('/content/drive/My Drive/Timeseries_Delhi/Delhi.xlsx', sheet_name = "Delhi")

sns.set_style("whitegrid")

"""##Data Exploration"""

data.head()

data.describe()

data.info()



#Introducing Missing Timestamps in dataset and setting their pm2.5 value to NaN

data.sort_index(ascending = False, inplace = True)
data.reset_index(inplace = True)
data.set_index("date", inplace = True, drop = False)
df = pd.DataFrame(pd.date_range(start = '2018-01-01', end = '2018-04-20', freq = '1H'), columns = ["date"])
df.set_index("date", inplace = True, drop = False)
data = df.join(data, how = "left", lsuffix = "_or", rsuffix = "_dup")

data.drop(labels = ["index", "date_dup"], inplace = True, axis = 1)
data.rename(columns = {'date_or':'date'}, inplace = True)

data

data[data["pm25"] == "-"]

"""Observation:
There are 80 observations with missing "pm25" value.
"""

data[data["pm25"] == 0]

#Replacing all "-" with 0 and creatinf a new variable "pm25_with0"
data["pm25"] = data["pm25"].replace(to_replace = "-", value = np.nan)



"""The above cell replaces the "-" with NaN."""

data[data["pm25"] == "-"]

plt.figure(figsize = (25,10))
plt.plot(data["date"], data["pm25"])
plt.title("Size of PM for every hour for 4 months")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

"""Observation:


This series seems to be following a decreasing trend over 4 months.

You can see some sudden gaps between series, indicating missing NaN values. Two major gaps are between timestamp - (15/01/2018 , 01/02/2018) and before 01/04/2018.
"""

#Enlarging the gaps

data_gaps = data[(data["date"]>="2018-01-15 00:00:00") & (data["date"]<="2018-02-01 00:00:00")]

plt.figure(figsize = (25,10))
plt.plot(data_gaps["date"], data_gaps["pm25"])
plt.title("Size of PM for every hour in Jan end")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Enlarging the gaps

data_gaps = data[(data["date"]>="2018-03-25 00:00:00") & (data["date"]<="2018-04-01 00:00:00")]

plt.figure(figsize = (25,10))
plt.plot(data_gaps["date"], data_gaps["pm25"])
plt.title("Size of PM for every hour before 1st april")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Calculating the number of hourly timestamps between "2018-01-01 00:00:00" 
#and "2018-04-20 00:00:00" 

from datetime import datetime, timedelta
count = 0
def daterange(start_date, end_date):
    delta = timedelta(hours=1)
    while start_date < end_date:
        yield start_date
        start_date += delta

start_date = datetime(2018, 1, 1, 00, 00)
end_date = datetime(2018, 4, 20, 00, 00)
for single_date in daterange(start_date, end_date):
    #print(single_date.strftime("%Y-%m-%d %H:%M:%S"))
    count+=1

print("Total Hourly Time Stamps: ", count)

"""Observation:

As we can see, between 1st Jan 2018 and 20th April 2018 there are 2616 hourly timestamps. In the dataset there are 2374 hourly timestamp. Hence there are-> 2616-2374 = 242 missing timestamp from the dataset.
"""

data

#Creating a variable "timestamp_day_name" which is the day name of that particular
#timestamp.

data["timestamp_day_name"] = [i.day_name() for i in data["date"]]

data["timestamp_day_name"]

data[data["timestamp_day_name"] == "Sunday"]["pm25"]

#Seasonality for Sunday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Sunday"]["date"], 
         data[data["timestamp_day_name"] == "Sunday"]["pm25"])
plt.title("Size of PM for every Sunday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Monday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Monday"]["date"], 
         data[data["timestamp_day_name"] == "Monday"]["pm25"])
plt.title("Size of PM for every Monday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Tuesday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Tuesday"]["date"], 
         data[data["timestamp_day_name"] == "Tuesday"]["pm25"])
plt.title("Size of PM for every Tuesday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Wednesday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Wednesday"]["date"], 
         data[data["timestamp_day_name"] == "Wednesday"]["pm25"])
plt.title("Size of PM for every Wednesday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Thursday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Thursday"]["date"], 
         data[data["timestamp_day_name"] == "Thursday"]["pm25"])
plt.title("Size of PM for every Thursday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Friday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Friday"]["date"], 
         data[data["timestamp_day_name"] == "Friday"]["pm25"])
plt.title("Size of PM for every Friday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

#Seasonality for Saturday

plt.figure(figsize = (25,10))
plt.plot(data[data["timestamp_day_name"] == "Saturday"]["date"], 
         data[data["timestamp_day_name"] == "Saturday"]["pm25"])
plt.title("Size of PM for every Saturday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")

"""Observation:

Looking at the graphs for every single day over these 4 months we can see some kind of seasonality. The seasonality looks similar for all the days. Hence we can say that PM25 is showing cyclic repetition every day.
"""



#Seasonality for Friday
data_gaps_1 = data[(data["date"]>="2018-02-02 00:00:00") & (data["date"]<="2018-02-02 23:00:00")]

plt.figure(figsize = (25,10))
plt.plot(data_gaps_1["date"], 
         data_gaps_1["pm25"])
plt.title("Size of PM for every Friday")
plt.xlabel("Time Scale in Hours")
plt.ylabel("Size of Particulate Matter")



data



data["only_date"] = [i.strftime("%Y-%m-%d") for i in data["date"]]

date_list = []
date_median = []

for i in (data["only_date"].unique()):
  date_list.append(i)
  date_median.append(data.groupby(by = "only_date", axis = 0).get_group(i)["pm25"].median(axis = 0))

date_data = pd.DataFrame(date_list, columns = ["date"])
date_data["median"] = date_median

plt.figure(figsize = (25,10))
plt.scatter(date_data["date"], date_data["median"] )
plt.xticks(rotation = 90)



data.head()














"""##Interpolation"""



#Using various interpolation techniques

data["linear"] = data["pm25"].interpolate(method = "linear")
data["slinear"] = data["pm25"].interpolate(method = "slinear")
data["pm25_poly3"] = data["pm25"].interpolate(method = "polynomial", order = 3)
data["pm25_poly5"] = data["pm25"].interpolate(method = "polynomial", order = 5)
data["pm25_poly7"] = data["pm25"].interpolate(method = "polynomial", order = 7)
data["pm25_time"] = data["pm25"].interpolate(method = "time")
data["pm25_spline3"] = data["pm25"].interpolate(method = "spline", order = 3)
data["pm25_spline5"] = data["pm25"].interpolate(method = "spline", order = 4)
data["pm25_spline7"] = data["pm25"].interpolate(method = "spline", order = 5)
data["pm25_akima"] = data["pm25"].interpolate(method = "akima")

data







#Drawing interpolation graphs

columns = ["pm25",'linear', 'slinear',
       'pm25_poly3', 'pm25_poly5', 'pm25_poly7', 'pm25_time', 'pm25_spline3',
       'pm25_spline5', 'pm25_spline7', 'pm25_akima']


fig, ax = plt.subplots(11,1, figsize = (25,30), sharex = True)
i = 0
for col in columns:  
  ax[i].plot(data[col])
  ax[i].set_title(col)
  i+=1

