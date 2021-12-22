"""
Author : Shivam Ojha
Version : 1
Version Date : 10th Dec 2021
Description : Python function to predict weather values using RNN
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers, losses
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.losses import SparseCategoricalCrossentropy, BinaryCrossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import models
from tensorflow.keras.callbacks import EarlyStopping
import os

class neuralnet_model():
    def __init__(self, X, Y, n_outputs, n_lag, n_ft, n_layer, batch, epochs, lr,
        Xval=None, Yval=None, mask_value=-999.0, min_delta=0.001, patience=5):
        
        lstm_input = Input(shape=(n_lag, n_ft))

        # Series signal 
        lstm_layer = LSTM(n_layer, activation='relu')(lstm_input)
        x = Dense(n_outputs)(lstm_layer)
        
        self.model = models.Model(inputs=lstm_input, outputs=x)
        self.batch = batch 
        self.epochs = epochs
        self.n_layer=n_layer
        self.lr = lr 
        self.Xval = Xval
        self.Yval = Yval
        self.X = X
        self.Y = Y
        self.mask_value = mask_value
        self.min_delta = min_delta
        self.patience = patience

    def trainCallback(self):
        return EarlyStopping(monitor='loss', patience=self.patience, min_delta=self.min_delta)

    def train(self):
        # Getting the untrained model 
        empty_model = self.model
        
        # Initiating the optimizer
        optimizer = keras.optimizers.Adam(learning_rate=self.lr)

        # Compiling the model
        empty_model.compile(loss=losses.MeanAbsoluteError(), optimizer=optimizer)

        if (self.Xval is not None) & (self.Yval is not None):
            history = empty_model.fit(self.X, self.Y, 
                epochs=self.epochs, batch_size=self.batch, 
                validation_data=(self.Xval, self.Yval), 
                shuffle=False, callbacks=[self.trainCallback()])
        else:
            history = empty_model.fit(self.X, self.Y, 
                epochs=self.epochs, batch_size=self.batch,
                shuffle=False, callbacks=[self.trainCallback()])
        # Saving to original model attribute in the class
        self.model = empty_model
        # Returning the training history
        return history
    
    def predict(self, X):
        return self.model.predict(X)


def get_df_from_db(database_url, sql_statement):
    """
    Function to get dataframe from a table

    Args:
        database_url ([type]): [description]

    Returns:
        df_ (dataframe): dataframe returned from the sql query
    """
    df_ = pd.read_sql_query(sql_statement, database_url)
    return df_


def create_X_Y(timeseries, lag, n_ahead, target_index=0):
    """
    A method to create X and Y matrix from a time series array for the training of 
    deep learning models 
    """
    # Extracting the number of features that are passed from the array 
    n_features = timeseries.shape[1]
    # Creating placeholder lists
    X, Y = [], []
    if len(timeseries) - lag <= 0:
        X.append(timeseries)
    else:
        for i in range(len(timeseries) - lag - n_ahead):
            Y.append(timeseries[(i + lag):(i + lag + n_ahead), target_index])
            X.append(timeseries[i:(i + lag)])
    X, Y = np.array(X), np.array(Y)
    # Reshaping the X array to an RNN input shape 
    X = np.reshape(X, (X.shape[0], lag, n_features))
    return X, Y


def main():
    """
    Main function
    """
    database_url = os.getenv('database_url')
    weather_schema_name = 'weather'
    weather_table_processed = 'weather_data_processed'
    sql_statement = '''select * from {}.{}'''.format(weather_schema_name, weather_table_processed)
    weather_df = get_df_from_db(database_url, sql_statement)

    weather_df.sort_values('Date', inplace=True)

    # Extracting the hour of day
    weather_df["hour1"] = [x.hour for x in weather_df["Datetime"]]

    # Creating the cyclical daily feature 
    weather_df["day_cos"] = [np.cos(x * (2 * np.pi / 24)) for x in weather_df["hour1"]]
    weather_df["day_sin"] = [np.sin(x * (2 * np.pi / 24)) for x in weather_df["hour1"]]

    # Extracting the timestamp from the datetime object 
    weather_df["timestamp"] = [x.timestamp() for x in weather_df["Datetime"]]

    # Seconds in day 
    s = 24 * 60 * 60

    # Seconds in year 
    year = (365.25) * s
    weather_df["month_cos"] = [np.cos((x) * (2 * np.pi / year)) for x in weather_df["timestamp"]]
    weather_df["month_sin"] = [np.sin((x) * (2 * np.pi / year)) for x in weather_df["timestamp"]]

    del weather_df["Precip Rate"]
    del weather_df["Wind Gust"]

    timeseries = weather_df[['Temp', 'day_cos', 'day_sin', 'month_sin', 'month_cos']].values
    X, Y = create_X_Y(timeseries, lag=3, n_ahead=1)

    lag = 48 # Number of lags (hours back) to use for models
    n_ahead = 1 # Steps ahead to forecast
    test_div = 0.1 # Share of obs in testing
    epochs = 20 # Epochs for training
    batch_size = 512 # Batch size
    lr = 0.001 # Learning rate
    n_layer = 10 # Number of neurons in LSTM layer

    # Features used in the modeling
    features_final = ['Temp', 'day_cos', 'day_sin', 'month_sin', 'month_cos']

    # Subseting only the needed columns 
    ts = weather_df[features_final]
    nrows = ts.shape[0]

    # Spliting into train and test sets
    train = ts[0:int(nrows * (1 - test_div))]
    test = ts[int(nrows * (1 - test_div)):]

    # Scaling data 
    train_mean = train.mean()
    train_std = train.std()
    train = (train - train_mean) / train_std
    test = (test - train_mean) / train_std

    # final scaled dataframe 
    ts_s = pd.concat([train, test])

    # X and Y for training
    X, Y = create_X_Y(ts_s.values, lag=lag, n_ahead=n_ahead)
    n_ft = X.shape[2]

    # Spliting into train and test sets 
    Xtrain, Ytrain = X[0:int(X.shape[0] * (1 - test_div))], Y[0:int(X.shape[0] * (1 - test_div))]
    Xval, Yval = X[int(X.shape[0] * (1 - test_div)):], Y[int(X.shape[0] * (1 - test_div)):]

    #Shape of training data: (87717, 48, 5)
    #Shape of the target data: (87717, 1)
    #Shape of validation data: (9747, 48, 5)
    #Shape of the validation target data: (9747, 1)

    # Model
    model = neuralnet_model(X=Xtrain, Y=Ytrain, n_outputs=n_ahead, n_lag=lag,
                            n_ft=n_ft, n_layer=n_layer, batch=batch_size, epochs=epochs,
                            lr=lr, Xval=Xval, Yval=Yval,)
    # Train the model 
    history = model.train()

    # Compare the forecasts with the actual values
    yhat = [x[0] for x in model.predict(Xval)]
    y = [y[0] for y in Yval]

    # dataframe to store both predictions
    days = weather_df["Datetime"].values[-len(y):]
    frame = pd.concat([
    pd.DataFrame({'day': days, 'Temp': y, 'type': 'original'}),
    pd.DataFrame({'day': days, 'Temp': yhat, 'type': 'forecast'})
    ])

    # Creating the unscaled values column
    frame['temp_absolute'] = [(x * train_std['Temp']) + train_mean['Temp'] for x in frame['Temp']]

    pivoted = frame.pivot_table(index='day', columns='type')
    pivoted.columns = ['_'.join(x).strip() for x in pivoted.columns.values]
    pivoted['res'] = pivoted['temp_absolute_original'] - pivoted['temp_absolute_forecast']
    pivoted['res_abs'] = [abs(x) for x in pivoted['res']]

    # Visualise results
    plt.figure(figsize=(12, 12))
    plt.plot(pivoted.index, pivoted.temp_absolute_original, color='blue', label='original')
    plt.plot(pivoted.index, pivoted.temp_absolute_forecast, color='red', label='forecast', alpha=0.6)
    plt.title('Temperature forecasts — absolute data')
    plt.legend()
    plt.savefig('Forecast_actual_temp',dpi=300)
    plt.show()

if __name__ == '__main__':
    main()
