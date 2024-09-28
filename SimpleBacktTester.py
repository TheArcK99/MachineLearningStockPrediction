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

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
         portfolio.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
         portfolio.total[signals.positions == -1.0],
         'v', markersize=10, color='k')
print("Here is the simlation of your portoflio value with $100,000 to invest along with the trade signals: ")
plt.show()