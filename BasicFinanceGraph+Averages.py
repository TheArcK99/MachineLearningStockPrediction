from calendar import month
from pickle import TRUE
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf

yr = input("From what year do you want to start the analysis (Ex. 2022): ")
mon = input("From what month do you want to start the analysis (Ex. 8 or 12):  ")
day = input("From what day do you want to start the analysis (Ex. 8 or 12): ")

yr = int(yr)
mon = int(mon)
day = int(day)

yf.pdr_override()
stockA = input("Please enter the ticker for the stock you wish to graph: ")
st = {}
st = pdr.get_data_yahoo(stockA,
                           start = datetime.datetime(yr,mon,day),
                           end = datetime.date.today().strftime('%Y-%m-%d'))


print("Here is a graph of the stock price:")
st['Close'].plot(grid=True)
plt.show()

daily_close = st[['Adj Close']]
daily_pct_c = daily_close.pct_change()
daily_pct_c.fillna(0,inplace=True)

print("Here is a list of the daily and total returns for your stock:")
print(daily_pct_c)
daily_log_returns = np.log(daily_close.pct_change()+1)
print(daily_log_returns)


print("Here is te data over the monthly and quarterly change in the stock:")
monthly = st.resample('BM').apply(lambda x: x[-1])
print(monthly.pct_change())
quarter = st.resample('4M').mean()
print(quarter.pct_change())
print("")

print("Here is the adjusted daily returns of the stock p:")
daily_pct_c = daily_close / daily_close.shift(1)-1
print(daily_pct_c)

print("Here is a histogram of the average daily return:")
daily_pct_c.hist(bins=50)
plt.show()
print(daily_pct_c.describe())
print()

print("Here is a graph of the cumulative return as well as some data about it: ")

cum_daily_return = (1+daily_pct_c).cumprod()
print(cum_daily_return)

cum_daily_return.plot(figsize=(15,8))
plt.show()

cum_monthly_return = cum_daily_return.resample("M").mean()
print(cum_monthly_return)

adj_close_px = st['Adj Close']
moving_avg = adj_close_px.rolling(window=40).mean()
moving_avg[-10:]

print("Here is a graph of the stock and the calculated moving averages:")
st['42'] = adj_close_px.rolling(window=40).mean()
st['252'] = adj_close_px.rolling(window=252).mean()
st[['Adj Close','42','252']].plot()
plt.show()

short_window = 40
long_window = 100
