
from unittest import skip
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_datareader as pdr
import plotly.express as px
import plotly.graph_objects as go


yr = input("From what year do you want to start the analysis (Ex. 2022): ")
mon = input("From what month do you want to start the analysis (Ex. 08 or 12):  ")
day = input("From what day do you want to start the analysis (Ex. 08 or 12): ")

start_date = yr+"-"+mon+"-"+day
end_date = dt.date.today().strftime('%Y-%m-%d')

num = input("How many stocks do you want to graph? ")
tickers = []
num = int(num)

for x in range(0,num):
  stockA = input("Please enter the ticker for the stock: ")
  tickers.append(stockA)



each_df = {}
for ticker in tickers:
    each_df[ticker] = pdr.DataReader(ticker, 'yahoo', start_date, end_date)


stocks = pd.concat(each_df, axis=1, keys = tickers)

stocks.columns.names = ['Ticker Symbol', 'Stock Info']

stocks.head().round(2)
stocks.tail()

stocks.shape

closing_prices_df = stocks.xs(key='Adj Close',axis=1,level=1)

fig = px.line(closing_prices_df, x=closing_prices_df.index, y=closing_prices_df.columns, title="Adjusted Closing Prices")
fig.update_layout(hovermode='x',yaxis_title="Price")
fig.show()

