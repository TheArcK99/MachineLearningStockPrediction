import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_datareader as pdr
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

yr1 = input("What is the first year you want to analyze? ")
yr2 = input("What is the next year you want to analyze? ")
yr3 = input("What is the last year you want to analyze? ")

start_date = '2000-01-01'
end_date = dt.date.today().strftime('%Y-%m-%d')

tickers = []
stockA = input("Please enter the ticker for the stock: ")
tickers.append(stockA)

each_df = {}
for ticker in tickers:
    each_df[ticker] = pdr.DataReader(ticker, 'yahoo', start_date, end_date)

stocks = pd.concat(each_df, axis=1, keys = tickers)

stocks.columns.names = ['Ticker Symbol', 'Stock Info']

closing_prices_df = stocks.xs(key='Adj Close',axis=1,level=1)

returns = pd.DataFrame()

for ticker in tickers:
    returns[ticker]=closing_prices_df[ticker].pct_change()*100

a = returns[ticker].loc[yr1+'-01-01':yr1+'-08-01'].dropna()
b = returns[ticker].loc[yr2+'-01-01':yr2+'-08-01'].dropna()
c = returns[ticker].loc[yr3+'-01-01':yr3+'-08-01'].dropna()

plt.figure(figsize =(10,7))
a.plot(kind='hist', label=yr1, bins=50, alpha=0.5)
b.plot(kind='hist', label=yr2, bins=50, alpha=0.5)
c.plot(kind='hist', label=yr3, bins=50, alpha=0.5)
plt.title('Distribution of '+ticker+ ' returns')
plt.xlabel('Daily Returns (%)')
plt.legend()
plt.show()

