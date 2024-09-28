import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import pandas_datareader as pdr
import matplotlib.pyplot as plt

yr = input("From what year do you want to start the analysis (Ex. 2022): ")
mon = input("From what month do you want to start the analysis (Ex. 08 or 12):  ")
day = input("From what day do you want to start the analysis (Ex. 08 or 12): ")

start_date = yr+"-"+mon+"-"+day
end_date = dt.date.today().strftime('%Y-%m-%d')

t = input("Which stock do you want to analyze and predict? ")

each_df = pdr.DataReader(t, 'yahoo', start_date, end_date)['Close']


each_df.plot(figsize = (15,8))
plt.grid()
plt.ylabel("Price in Dollars")
plt.show()

#each_df['20_SMA'] = each_df.rolling(window = 20, min_periods = 1).mean()
#each_df['50_SMA'] = each_df.rolling(window = 50, min_periods = 1).mean()

print(each_df.head())

# create 20 days simple moving average column
each_df['20_SMA'] = each_df['Close Price'].rolling(window = 20, min_periods = 1).mean()
# create 50 days simple moving average column
each_df['50_SMA'] = each_df['Close Price'].rolling(window = 50, min_periods = 1).mean()

