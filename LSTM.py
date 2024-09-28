import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from pandas_datareader import data
import datetime as dt
import urllib.request, json
import os
import tensorflow as tf

#t = input("Enter the ticker of the sctok you wish to analyze:")

sP = 0
t = ""
def data(x,t1):
    sP=x
    t=t1

def getSP():
    return sP

def getTick():
    return t


def loadData(t): 
        dataSource = 'kaggle' 
        if dataSource == 'alphavantage':
            apiKey = 'IO6P1R7C46AHL9O6'
            ticker = t
            urlString = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,apiKey)
            savedFile = 'stock_market_data-%s.csv'%ticker

            if not os.path.exists(savedFile):
                with urllib.request.urlopen(urlString) as url:
                    data = json.loads(url.read().decode())
                    data = data['Time Series (Daily)']
                    df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
                    for k,v in data.items():
                        date = dt.datetime.strptime(k, '%Y-%m-%d')
                        dataRow = [date.date(), float(v['3. low']), float(v['2. high']), float(v['4. close']), float(v['1. open'])]
                        df.loc[-1,:] = dataRow
                        df.index = df.index + 1
                df.to_csv(savedFile)
            else:
                df = pd.read_csv(savedFile)
        else:
            df = pd.read_csv(os.path.join('Stocks', 'hpq.us.txt'),delimiter=',',usecols=['Date','Open','High','Low','Close'])
        return df

def run(d):
    df = d
    df = df['Open'].values
    df = df.reshape(-1,1)

    dataset_train = np.array(df[:int(df.shape[0]*0.8)])
    dataset_test = np.array(df[int(df.shape[0]*0.8):])

    scaler = MinMaxScaler(feature_range=(0,1))
    dataset_train = scaler.fit_transform(dataset_train)
    dataset_test = scaler.transform(dataset_test)

    def create_datasheet(df):
        x = []
        y = []
        for i in range(50, df.shape[0]):
            x.append(df[i-50:i, 0])
            y.append(df[i, 0])
        x = np.array(x)
        y = np.array(y)
        return x,y

    x_train, y_train = create_datasheet(dataset_train)
    x_test, y_test = create_datasheet(dataset_test)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    model.compile(loss='mean_squared_error', optimizer='adam')

    model.fit(x_train, y_train, epochs=50, batch_size=32)

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    y_test_scaled = scaler.inverse_transform(y_test.reshape(-1,1))

    fig, ax = plt.subplots(figsize=(16,8))
    ax.set_facecolor('#000041')
    ax.plot(y_test_scaled, color='red', label='Original Price')
    plt.plot(predictions, color='cyan', label='Predicted Price')
    plt.legend()
    plt.show()                        

    return predictions[-1]