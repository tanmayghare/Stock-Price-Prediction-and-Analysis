import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

class StockPricePrediction:
    def __init__(self, company, start_date, end_date):
        # Initialize the class with company ticker, start date, and end date
        self.company = company
        self.start = dt.datetime(*map(int, start_date.split('.')))
        self.end = dt.datetime(*map(int, end_date.split('.')))
        self.data = web.DataReader(company, 'yahoo', self.start, self.end)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.prediction_days = 60
        self.model = self._build_model()

    def _build_model(self):
        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.prediction_days, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def prepare_data(self):
        # Prepare the data for training
        scaled_data = self.scaler.fit_transform(self.data['Close'].values.reshape(-1, 1))
        x_train, y_train = [], []
        for x in range(self.prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x - self.prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        return x_train, y_train

    def train_model(self, x_train, y_train):
        # Train the LSTM model
        self.model.fit(x_train, y_train, epochs=25, batch_size=32)

    def test_model(self):
        # Test the model on historical data
        test_start = dt.datetime(2020, 1, 1)
        test_end = dt.datetime.now()
        test_data = web.DataReader(self.company, 'yahoo', test_start, test_end)
        actual_prices = test_data['Close'].values
        total_dataset = pd.concat((self.data['Close'], test_data['Close']), axis=0)
        model_inputs = total_dataset[len(total_dataset) - len(test_data) - self.prediction_days:].values
        model_inputs = model_inputs.reshape(-1, 1)
        model_inputs = self.scaler.transform(model_inputs)
        x_test = []
        for x in range(self.prediction_days, len(model_inputs)):
            x_test.append(model_inputs[x - self.prediction_days:x, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predicted_prices = self.model.predict(x_test)
        predicted_prices = self.scaler.inverse_transform(predicted_prices)
        self._plot_predictions(actual_prices, predicted_prices)

    def _plot_predictions(self, actual_prices, predicted_prices):
        # Plot the actual vs predicted prices
        plt.plot(actual_prices, color='black', label=f"Actual {self.company} Price")
        plt.plot(predicted_prices, color='green', label=f"Predicted {self.company} Price")
        plt.title(f"{self.company} Share Price")
        plt.xlabel('Time')
        plt.ylabel(f"{self.company} Share Price")
        plt.legend()
        plt.show()

    def predict_next_day(self):
        # Predict the next day's closing price
        model_inputs = self.scaler.transform(self.data['Close'].values.reshape(-1, 1))
        real_data = [model_inputs[len(model_inputs) + 1 - self.prediction_days:len(model_inputs + 1), 0]]
        real_data = np.array(real_data)
        real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
        prediction = self.model.predict(real_data)
        prediction = self.scaler.inverse_transform(prediction)
        print(f"Predicted price of {self.company} next day: {prediction}")

if __name__ == "__main__":
    company = input("Enter the ticker symbol of the company: ")
    start_date = input("Enter the start date for generating dataset (In YYYY.MM.DD format): ")
    end_date = input("Enter the end date for generating dataset (In YYYY.MM.DD format): ")
    stock_predictor = StockPricePrediction(company, start_date, end_date)
    x_train, y_train = stock_predictor.prepare_data()
    stock_predictor.train_model(x_train, y_train)
    stock_predictor.test_model()
    stock_predictor.predict_next_day()
