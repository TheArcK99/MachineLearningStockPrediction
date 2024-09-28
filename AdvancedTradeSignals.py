from calendar import month
from pickle import TRUE
from signal import signal
from turtle import color, position
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


stockA = input("Please enter the ticker for the stock you wish to graph: ")

st = pdr.get_data_yahoo(stockA,
                           start = datetime.datetime(yr,mon,day),
                           end = datetime.date.today().strftime('%Y-%m-%d'))

short_window = 40
long_window = 100
signals = pd.DataFrame(index=st.index)
signals['signal'] = 0.0
signals['short_mavg'] = st['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
signals['long_mavg'] = st['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                            > signals['long_mavg'][short_window:], 1.0, 0.0)
signals['positions'] = signals['signal'].diff()

initial_capital= float(100000.0)

intial_capital = float(100000.0)

positions = pd.DataFrame(index=signals.index).fillna(0.0)
positions['st'] = 100*signals['signal']

portfolio = positions.multiply(st['Adj Close'], axis=0)
pos_diff = positions.diff()

portfolio['holdings'] = (positions.multiply(st['Adj Close'], axis=0)).sum(axis=1)
portfolio['cash'] = intial_capital - (pos_diff.multiply(st['Adj Close'], axis=0)).sum(axis=1).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']
portfolio['returns'] = portfolio['total'].pct_change()

returns = portfolio['returns']
sharpe_ratio = np.sqrt(252)* (returns.mean() / returns.std())
print("Here is the sharpe ratio: ")
print(sharpe_ratio)

window = 252
rolling_max = st['Adj Close'].rolling(window, min_periods=1).min()
daily_drawdown = st['Adj Close']/rolling_max - 1.0

max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()
daily_drawdown.plot()
max_daily_drawdown.plot()
print("Here is the max daily drawdowm: ")
plt.show()

days = (st.index[-1] - st.index[0]).days 
cagr = ((((st['Adj Close'][-1]) / st['Adj Close'][1])) ** (365.0/days)) - 1
print("Here is the compounded annual growth rate: ")
print(cagr)

