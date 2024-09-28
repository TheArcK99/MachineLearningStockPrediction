import pandas as pd 
import matplotlib.pyplot as plt
import requests
import math 
from termcolor import colored as cl
import numpy as np
import yfinance as yf
import datetime as dt
import pandas_datareader as pdr

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15,8)

yr = input("Please enter the start year: ")
mon = input("Please enter the start month: ")
day = input("Please enter the start day: ")

start_date = yr+"-"+mon+"-"+day
end_date = dt.date.today().strftime('%Y-%m-%d')

tickers = []
stockA = input("Please enter the ticker for the stock: ")
tickers.append(stockA)

# create empty dataframe
stock_df = pd.DataFrame()
for i in tickers:  
    
    print( str(tickers.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)  
    
    try:
        stock = []
        stock = yf.download(i,start=start_date, end=end_date, progress=False)
    
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_df = stock_df.append(stock,sort=False)
    except Exception:
        None

#print(stock_df.head())

def sma(data, n):
    sma = data.rolling(window = n).mean()
    return pd.DataFrame(sma)

n = [20, 50]
for i in n:
    stock_df[f'sma_{i}'] = sma(stock_df['Close'], i)

#print(stock_df.tail())

plt.plot(stock_df['Close'], label = stockA, linewidth = 5, alpha = 0.3)
plt.plot(stock_df['sma_20'], label = 'SMA 20')
plt.plot(stock_df['sma_50'], label = 'SMA 50')
plt.title(stockA+' Simple Moving Averages (20,50)')
plt.legend(loc = 'upper left')
plt.show()

def implement_sma_strategy(data, short_window, long_window):
    sma1= short_window
    sma2= long_window
    buy_price = []
    sell_price = []
    sma_signal = []
    signal = 0

    for i in range(len(data)):
        if sma1[i] > sma2[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                sma_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        elif sma2[i] > sma1[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                sma_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            sma_signal.append(0)

    return buy_price, sell_price, sma_signal

sma_20 = stock_df['sma_20']
sma_50 = stock_df['sma_50']

buy_price, sell_price, signal = implement_sma_strategy(stock_df['Close'], sma_20, sma_50)
plt.plot(stock_df['Close'], alpha = 0.3, label = stockA)
plt.plot(sma_20, alpha = 0.6, label = 'SMA 20')
plt.plot(sma_50, alpha = 0.6, label = 'SMA50')
plt.scatter(stock_df.index, buy_price, marker = '^', s =200, color = 'darkblue', label = 'BUY SIGNAL')
plt.scatter(stock_df.index, sell_price, marker = 'v', s =200, color = 'crimson', label = 'SELL SIGNAL')
plt.legend(loc = 'upper left')
plt.title(stockA+' SMA CROSSOVER TRADING SIGALS')
plt.show()

position = []
for i in range(len(signal)):
    if signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len(stock_df['Close'])):
    if signal[i] == 1:
        position[i] = 1
    elif signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]

sma_20 = pd.DataFrame(sma_20).rename(columns={0:'Sma_20'})
sma_50 = pd.DataFrame(sma_50).rename(columns={0:'Sma_50'})
signal = pd.DataFrame(signal).rename(columns={0:'Sma_signal'}).set_index(stock_df.index)
position = pd.DataFrame(position).rename(columns={0:'Sma_position'}).set_index(stock_df.index)

frames = [sma_20, sma_50, signal, position]
strategy = pd.concat(frames,join = 'inner', axis = 1)
strategy = strategy.reset_index().drop('Date', axis = 1)

stock_ret = pd.DataFrame(np.diff(stock_df['Close'])).rename(columns = {0:'Returns'})
#print(stock_ret.head())
sma_strategy_ret = []

for i in range(len(stock_ret)):
    try:
        returns = stock_ret['Returns'][i]*strategy['Sma_position'][i]
        sma_strategy_ret.append(returns)
    except:
        pass


sma_strategy_ret_df = pd.DataFrame(sma_strategy_ret).rename(columns = {0:'Sma_Returns'})

money = input("Please enter the backtest amount: ")
investment_value = float(money)

number_stocks = math.floor(investment_value/stock_df['Close'][1])
sma_investment_ret = []

for i in range(len(sma_strategy_ret_df['Sma_Returns'])):
    returns = number_stocks*sma_strategy_ret_df['Sma_Returns'][i]
    sma_investment_ret.append(returns)


sma_strategy_ret_df = pd.DataFrame(sma_investment_ret).rename(columns={0:'Investment_returns'})
total_investment_ret = round(sum(sma_strategy_ret_df['Investment_returns']), 2)
profit_percentage = math.floor(total_investment_ret/investment_value*100)
print(cl("Profit gained from the startegy by investing $"+money+" in "+stockA+": ${} in 1 Year".format(total_investment_ret),attrs=['bold']))
print(cl('Profit percentage of the BB strategy : {}%' .format(profit_percentage), attrs=['bold']))
