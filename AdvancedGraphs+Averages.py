from calendar import month
from pickle import TRUE
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance

yr = input("From what year do you want to start the analysis (Ex. 2022): ")
mon = input("From what month do you want to start the analysis (Ex. 8 or 12):  ")
day = input("From what day do you want to start the analysis (Ex. 8 or 12): ")

yr = int(yr)
mon = int(mon)
day = int(day)

def get(tickers, startdate, enddate):
    def data(ticker):
        return(pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

num = input("How many stocks do you want to analyze? ")
tickers = []
num = int(num)

for x in range(0,num):
  stockA = input("Please enter the ticker for the stock: ")
  tickers.append(stockA)

all_data = get(tickers, datetime.datetime(yr,mon,day), datetime.date.today().strftime('%Y-%m-%d'))
print(all_data.head())

daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date','Ticker','Adj Close')
daily_pct_change = daily_close_px.pct_change()
daily_pct_change.hist(bins=50,sharex=True,figsize=(15,8))
print("Here are a few histograms to show the frequency of returns for all your stocks:")
plt.show()

print("Here is a scatter matrix with the daily change data for your stocks: ")
pd.plotting.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1, figsize=(13,13))
plt.show()

min_periods = 75

print("And here is a simple volatlity calculation for all the stocks across time: ")
vol = daily_pct_change.rolling(min_periods).std()*np.sqrt(min_periods)
vol.plot(figsize=(10,8))
plt.show()

