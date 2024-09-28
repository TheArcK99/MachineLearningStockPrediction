import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

ticker = input("Input the stock ticker: ")
data = pd.DataFrame()
data[ticker] = wb.DataReader(ticker, data_source='yahoo', start='2010-1-1')['Adj Close']
data.head()

log_returns = np.log(1+data.pct_change())
log_returns.head()

sns.displot(log_returns.iloc[1:])
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.show()

data.plot(figsize=(15,6))

log_returns.plot(figsize=(15,6))

u = log_returns.mean()
var = log_returns.var()

drift = u - (0.5*var)
drift


stddev = log_returns.std()
x = np.random.rand(10,2)
x
norm.ppf(x)
Z = norm.ppf(np.random.rand(50,10000))
Z
t_intervals = 1000
iterations = 10

daily_returns = np.exp(drift.values + stddev.values * norm.ppf(np.random.rand(50,1000)))
daily_returns
S0 = data.iloc[-1]
S0

price_list = np.zeros_like(daily_returns)
price_list.shape
price_list[0] = S0
price_list
for t in range(1,50):
    price_list[t] = price_list[t-1]*daily_returns[t]
price_list.shape
plt.figure(figsize=(15,6))
plt.plot(pd.DataFrame(price_list).iloc[:,0:10])
sns.displot(pd.DataFrame(price_list).iloc[-1])
plt.xlabel("Price after 50 days")
plt.show()

df = pd.DataFrame(price_list)
df.head()