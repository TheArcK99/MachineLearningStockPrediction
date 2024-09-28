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
plt.rcParams['figure.figsize'] = (20,10)


#yr = input("Please enter the start year: ")
#mon = input("Please enter the start month: ")
#day = input("Please enter the start day: ")

#start_date = yr+"-"+mon+"-"+day

start_date = "2019-01-01"
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

def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma

stock_df['sma_20'] = sma(stock_df['Close'],20)
print(stock_df.tail())

def bolband(data, sma, window):
    std = data.rolling(window=window).std()
    upper_bb = sma + std *2
    lower_bb = sma - std *2
    return upper_bb, lower_bb

stock_df['upper_bb'], stock_df['lower_bb'] =bolband(stock_df['Close'],stock_df['sma_20'],20)
print(stock_df.tail())

stock_df['Close'].plot(label = 'Close Prices', color = 'skyblue')
stock_df['upper_bb'].plot(label = 'Upper BB 20', linestyle = '--', linewidth = 1, color = 'black')
stock_df['lower_bb'].plot(label = 'Lower BB 20', linestyle = '--', linewidth = 1, color = 'black')
stock_df['sma_20'].plot(label = 'Middle BB 20', linestyle = '--', linewidth = 1.2, color = 'grey')
plt.legend(loc = 'upper left')
plt.title(stockA+' Bollinger Bands')
plt.show()

def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0

    for i in range(len(data)):
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, sell_price, bb_signal

buy_price, sell_price, bb_signal = implement_bb_strategy(stock_df['Close'], stock_df['lower_bb'],stock_df['upper_bb'] )

stock_df['Close'].plot(label = 'Close Prices', alpha = 0.3)
stock_df['upper_bb'].plot(label = 'Upper BB', linestyle = '--', linewidth = 1, color = 'black')
stock_df['lower_bb'].plot(label = 'Lower BB', linestyle = '--', linewidth = 1, color = 'black')
stock_df['sma_20'].plot(label = 'Middle BB', linestyle = '--', linewidth = 1.2, color = 'grey')
plt.scatter(stock_df.index, buy_price, marker = '^', s =200, color = 'green', label = 'BUY')
plt.scatter(stock_df.index, sell_price, marker = 'v', s =200, color = 'red', label = 'SELL')
plt.legend(loc = 'upper left')
plt.title(stockA+' BB STRATEGY TRADING SIGNALS')
plt.show()

position = []
for i in range(len(bb_signal)):
    if bb_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len(stock_df['Close'])):
    if bb_signal[i] == 1:
        position[i] = 1
    elif bb_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]

upper_bb = stock_df['upper_bb']
lower_bb = stock_df['lower_bb']
close_price = stock_df['Close']
bb_signal = pd.DataFrame(bb_signal).rename(columns={0:'bb_signal'}).set_index(stock_df.index)
position = pd.DataFrame(position).rename(columns={0:'bb_position'}).set_index(stock_df.index)

frames = [close_price, upper_bb, lower_bb, bb_signal, position]
strategy = pd.concat(frames,join = 'inner', axis = 1)
strategy = strategy.reset_index().drop('Date', axis = 1)

stock_ret = pd.DataFrame(np.diff(stock_df['Close'])).rename(columns = {0:'returns'})
bb_strategy_ret = []

for i in range(len(stock_ret)):
    try:
        returns = stock_ret['returns'][i]*strategy['bb_position'][i]
        bb_strategy_ret.append(returns)
    except:
        pass


bb_strategy_ret_df = pd.DataFrame(bb_strategy_ret).rename(columns = {0:'bb_returns'})

money = input("Please enter the backtest amount: ")
investment_value = float(money)

number_stocks = math.floor(investment_value/stock_df['Close'][-1])
bb_investment_ret = []

for i in range(len(bb_strategy_ret_df['bb_returns'])):
    returns = number_stocks*bb_strategy_ret_df['bb_returns'][i]
    bb_investment_ret.append(returns)


bb_strategy_ret_df = pd.DataFrame(bb_investment_ret).rename(columns={0:'Investment_returns'})
total_investment_ret = round(sum(bb_strategy_ret_df['Investment_returns']), 2)
profit_percentage = math.floor(total_investment_ret/investment_value*100)
print(cl("Profit gained from the startegy by investing $"+money+" in "+stockA+": ${} in 1 Year".format(total_investment_ret),attrs=['bold']))
print(cl('Profit percentage of the BB strategy : {}%' .format(profit_percentage), attrs=['bold']))

def get_benchmark(stock_prices, start_date, investment_value):
    end_date = dt.date.today().strftime('%Y-%m-%d')
    try:
        stock = []
        stock = yf.download('SPY',start=start_date, end=end_date, progress=False)
    
        if len(stock) == 0:
            None
        else:
            stock['Name']='SPY'
            stock_df_spy = stock_df.append(stock,sort=False)
    except Exception:
        None
    
    spy = stock_df_spy
    #spy = spy.set_index('Date')
    spy = spy[spy.index >= start_date]['Close']
    benchmark = pd.DataFrame(np.diff(spy)).rename(columns = {0:'benchmark_returns'})
    
    investment_value = investment_value
    number_of_stocks = math.floor(investment_value/stock_prices[-1])
    benchmark_investment_ret = []
    
    for i in range(len(benchmark['benchmark_returns'])):
        returns = number_of_stocks*benchmark['benchmark_returns'][i]
        benchmark_investment_ret.append(returns)

    benchmark_investment_ret_df = pd.DataFrame(benchmark_investment_ret).rename(columns = {0:'investment_returns'})
    return benchmark_investment_ret_df

benchmark = get_benchmark(stock_df['Close'], '2020-01-01', 100000)

investment_value = 100000
total_benchmark_investment_ret = round(sum(benchmark['investment_returns']), 2)
benchmark_profit_percentage = math.floor((total_benchmark_investment_ret/investment_value)*100)
print(cl('Benchmark profit by investing $100k : {}'.format(total_benchmark_investment_ret), attrs = ['bold']))
print(cl('Benchmark Profit percentage : {}%'.format(benchmark_profit_percentage), attrs = ['bold']))
print(cl('BB Strategy profit is {}% higher than the Benchmark Profit'.format(profit_percentage - benchmark_profit_percentage), attrs = ['bold']))
