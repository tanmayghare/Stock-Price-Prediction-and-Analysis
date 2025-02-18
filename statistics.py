import pandas as pd
import numpy as np

class StockStatistics:
    def __init__(self, data_file):
        # Initialize dataframes and dictionaries for storing statistics
        self.VolumeDF = pd.read_csv(data_file, usecols=[5], index_col=False)
        self.OpenCloseDF = pd.read_csv(data_file, usecols=[3, 4], index_col=False)
        self.EventDummyDF = pd.read_csv(data_file, usecols=[15], index_col=False)
        self.tickerDF = pd.read_csv(data_file, usecols=[7], index_col=False)
        self.nedates = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edates = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.nedatesMean = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edatesMean = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.nedatesStdDev = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edatesStdDev = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.nedatesVar = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edatesVar = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.nedatesReturns = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edatesReturns = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.nedatesAvgEventDates = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}
        self.edatesAvgEventDates = {ticker: [] for ticker in self.tickerDF['ticker'].unique()}

    def calculate_statistics(self):
        # Calculate all statistics
        self._calculate_volume()
        self._calculate_mean()
        self._calculate_std_dev()
        self._calculate_variance()
        self._calculate_average_returns()

    def _calculate_volume(self):
        # Calculate volume for event and non-event dates
        for volume, ticker, event_dummy in zip(self.VolumeDF['Volume'], self.tickerDF['ticker'], self.EventDummyDF['event_dummy']):
            if event_dummy == 1:
                self.edates[ticker].append(int(volume))
            else:
                self.nedates[ticker].append(int(volume))

    def _calculate_mean(self):
        # Calculate mean volume for event and non-event dates
        for ticker in self.edates:
            self.edatesMean[ticker] = np.average(self.edates[ticker])
        print("\nMean of the Volume of Stocks on Event Dates:\n", self.edatesMean)

        for ticker in self.nedates:
            self.nedatesMean[ticker] = np.average(self.nedates[ticker])
        print("\nMean of the Volume of Stocks on Non-Event Dates:\n", self.nedatesMean)

    def _calculate_std_dev(self):
        # Calculate standard deviation of volume for event and non-event dates
        for ticker in self.edates:
            self.edatesStdDev[ticker] = np.std(self.edates[ticker])
        print("\nStandard Deviation (Volatility) of the Volume of Stocks on Event Dates:\n", self.edatesStdDev)

        for ticker in self.nedates:
            self.nedatesStdDev[ticker] = np.std(self.nedates[ticker])
        print("\nStandard Deviation (Volatility) of the Volume of Stocks on Non-Event Dates:\n", self.nedatesStdDev)

    def _calculate_variance(self):
        # Calculate variance of volume for event and non-event dates
        for ticker in self.edates:
            self.edatesVar[ticker] = np.var(self.edates[ticker])
        print("\nVariance of the Volume of Stocks on Event Dates:\n", self.edatesVar)

        for ticker in self.nedates:
            self.nedatesVar[ticker] = np.var(self.nedates[ticker])
        print("\nVariance of the Volume of Stocks on Non-Event Dates:\n", self.nedatesVar)

    def _calculate_average_returns(self):
        # Calculate average returns for event and non-event dates
        for open_price, close_price, ticker, event_dummy in zip(self.OpenCloseDF['Open'], self.OpenCloseDF['Close'], self.tickerDF['ticker'], self.EventDummyDF['event_dummy']):
            if event_dummy == 1:
                self.edatesReturns[ticker].append(((close_price - open_price) / open_price) * 100)
            else:
                self.nedatesReturns[ticker].append(((close_price - open_price) / open_price) * 100)

        for ticker in self.edatesReturns:
            self.edatesAvgEventDates[ticker] = round(np.average(self.edatesReturns[ticker]), 2)
        print("\nAverage Returns of the Stocks on Event Dates (in %):\n", self.edatesAvgEventDates)

        for ticker in self.nedatesReturns:
            self.nedatesAvgEventDates[ticker] = round(np.average(self.nedatesReturns[ticker]), 2)
        print("\nAverage Returns of the Stocks on Non-Event Dates (in %):\n", self.nedatesAvgEventDates)

if __name__ == "__main__":
    stock_stats = StockStatistics('merged_data.csv')
    stock_stats.calculate_statistics()
