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

a = input("Please type in the stock you wish to analyze: ")

tickers = []
tickers.append(a)

each_df = {}
for ticker in tickers:
    each_df[ticker] = pdr.DataReader(ticker, 'yahoo', start_date, end_date)

fig = go.Figure(data=[go.Candlestick(x=each_df[ticker].index,
                open=each_df[ticker]['Open'],
                high=each_df[ticker]['High'],
                low=each_df[ticker]['Low'],
                close=each_df[ticker]['Close'])])

fig.update_layout(
    title='Candlestick Chart for ' + ticker,
    yaxis_title='Price',
    xaxis_title='Date',
    hovermode='x'
)
fig.show()
                


