import pandas as pd
import numpy as np
import itertools

VolumeDF = pd.read_csv('merged_data.csv', usecols=[5], index_col=False)
OpenCloseDF = pd.read_csv('merged_data.csv', usecols=[3,4], index_col=False)
EventDummyDF = pd.read_csv('merged_data.csv', usecols=[15], index_col=False)
tickerDF = pd.read_csv('merged_data.csv', usecols=[7], index_col=False)

nedates = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edates = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

nedatesMean = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesMean = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}             

nedatesStdDev = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesStdDev = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

nedatesVar = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesVar = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}        

nedatesVar = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesVar = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}                    

nedatesReturns = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesReturns = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []} 

nedatesAvgEventDates = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}

edatesAvgEventDates = {'MNG.L': [], 'GBX': [], 'BION.SW': [], 'MLR': [], 'SWN': [], 'HDSN': [], 'TESS': [], 'JPM': [], 'OCC': [], 'GEOS': [], 'EL': [], 'CCBG': [], 'MGTI': [], 'WFC': [], 'ASTC': [], 'HBIA': [], 'NTAP': [], 'BMRA': [],
             'WSTL': [], 'TCI': [], 'OTEX': [], 'MSM': [], 'MEOH': [], 'TWIN': [], 'SM': [], 'BRN': [], 'LJPC': [], 'TSN': [], 'IMAX': [], 'SSRM': []}             

# Volume
for (volume, ticker, event_dummy) in zip(VolumeDF['Volume'], tickerDF['ticker'], EventDummyDF['event_dummy']):

    if event_dummy == 1:
        edates[(ticker)].append(int(volume))
    else:
        nedates[(ticker)].append(int(volume))

# Mean
for ticker, value in edates.items():
        meanEventDates = edates.get((ticker))
        edatesMean[(ticker)] = np.average(meanEventDates)

print("\nMean of the Volume of Stocks on Event Dates:\n", edatesMean)

for ticker, value in nedates.items():
        meanEventDates = nedates.get((ticker))
        nedatesMean[(ticker)] = np.average(meanEventDates)

print("\nMean of the Volume of Stocks on Non-Event Dates:\n", nedatesMean)

# Standard Deviation
for ticker, value in edates.items():
        meanEventDates = edates.get((ticker))
        edatesStdDev[(ticker)] = np.std(meanEventDates)

print("\nStandard Deviation (Volatility) of the Volume of Stocks on Event Dates:\n", edatesStdDev)

for ticker, value in nedates.items():
        meanEventDates = nedates.get((ticker))
        nedatesStdDev[(ticker)] = np.std(meanEventDates)

print("\nStandard Deviation (Volatility) of the Volume of Stocks on Non-Event Dates:\n", nedatesStdDev)

# Variance
for ticker, value in edates.items():
        meanEventDates = edates.get((ticker))
        edatesVar[(ticker)] = np.var(meanEventDates)

print("\nVariance of the Volume of Stocks on Event Dates:\n", edatesVar)

for ticker, value in nedates.items():
        meanEventDates = nedates.get((ticker))
        nedatesVar[(ticker)] = np.var(meanEventDates)

print("\nVariance of the Volume of Stocks on Non-Event Dates:\n", nedatesVar)

# Average Returns
for (open, close, ticker, event_dummy) in zip(OpenCloseDF['Open'], OpenCloseDF['Close'], tickerDF['ticker'], EventDummyDF['event_dummy']):
    if event_dummy == 1:
        edatesReturns[(ticker)].append(((close - open)/open) * 100)   
    else:
        nedatesReturns[(ticker)].append(((close - open)/open) * 100)

for ticker, value in edatesReturns.items():
        ReturnEventDates = edatesReturns.get((ticker))
        edatesAvgEventDates[(ticker)] = round(np.average(ReturnEventDates), 2)

print("\nAverage Returns of the Stocks on Event Dates (in %):\n", edatesAvgEventDates)

for ticker, value in nedatesReturns.items():
        ReturnNonEventDates = nedatesReturns.get((ticker))
        nedatesAvgEventDates[(ticker)] = round(np.average(ReturnNonEventDates), 2)      

print("\nAverage Returns of the Stocks on Non-Event Dates (in %):\n", nedatesAvgEventDates)