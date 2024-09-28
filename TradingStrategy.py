from calendar import month
from pickle import TRUE
from turtle import color
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

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Price in $')
st['Close'].plot(ax=ax1, color='r', lw=2.)

signals[['short_mavg','long_mavg']].plot(ax=ax1, lw=2.)
ax1.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='k')

print("Here is a graph that models an ideal trading strategy and using moving averages to calculate when you should buy and sell. The buy siganls are in purple and the sell ones in black: ")
plt.show()