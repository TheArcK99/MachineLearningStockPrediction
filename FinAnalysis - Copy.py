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

closing_prices_df = stocks.xs(key='Adj Close',axis=1,level=1)

returns = pd.DataFrame()

for ticker in tickers:
    returns[ticker]=closing_prices_df[ticker].pct_change()*100

print()
print("Here are the returns for each stock from the past 5 days")
print(returns.tail())

print()
print("Here is the average daily return for each stock")
print(returns.mean())

worst = returns.idxmin()
best = returns.idxmax()

best_and_worst_returns = pd.DataFrame({"Worst":worst, "Best":best})
best_and_worst_returns.columns.names = ['Single Day Returns']
best_and_worst_returns.index.names = ['Ticker']

print()
print("Here are the days with the best and worst returns for each stock")
print(best_and_worst_returns)

print()
print("Here is the standard deviation for each stock")
print(returns.std())

std_2020 = returns.loc['2020-01-01':'2020-08-01'].std()
std_2021 = returns.loc['2021-01-01':'2021-08-01'].std()
std_2022 = returns.loc['2022-01-01':'2022-08-01'].std()

std_comparison_df = pd.DataFrame({"2020":std_2020, "2021":std_2021, "2022":std_2022})
std_comparison_df.columns.names = ['STD Over Years Comparison']
std_comparison_df.index.names = ['Ticker']

print()
print("Here is the standard deviation for each stock based on the year")
print(std_comparison_df)

print()
print("Here is a plot that shows the risk vs. return for your chosen stocks")

fig = px.scatter(returns, x=returns.mean(), y=returns.std(), text=returns.columns, size_max=60, labels={
    "x": 'Daily Expected Returns (%)',
    "y": "Risk",
    },
    title="Stock Risk Vs Returns")
fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')#, range=[-0.005, 0.01])
fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')#, range=[-0.01, 0.01])
fig.update_traces(textposition='top center')
fig.show()









