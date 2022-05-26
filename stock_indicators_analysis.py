# ICM 142 - Programming for Finance

# ==========================================================
# 1) Downloading the Data of Type of Filings from SEC EDGAR:
# ==========================================================

import requests
url = r"https://www.sec.gov/Archives/edgar/full-index/2021/QTR1/master.idx"
heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         'Accept-Encoding': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'Host': 'www.sec.gov'}

request_content = requests.get(url, headers=heads).content
result = request_content.decode("utf-8", "ignore")
with open('master_index_2021QTR1.txt','w') as f:
    f.write(result)

import pandas as pd
import numpy as np

with open('master_index_2021QTR1.txt','r') as f:
    lines = f.readlines()

columns = tuple(lines[9].split('|'))
records = [tuple(line.split('|')) for line in lines[11:]]

data = pd.DataFrame(records, columns=columns)
data['date_filed'] = pd.to_datetime(data['Date Filed'])
sample = data.sample(10)
data['Form Type'].unique()

# Filtering the dataset based on significant corporate events/filing types and selecting 30 companies:
tickersDict = {'MNG.L': 'M&G INVESTMENT MANAGEMENT LTD', 'GBX': 'GREENBRIER COMPANIES INC', 'BION.SW': 'BB BIOTECH AG',
            'MLR': 'MILLER INDUSTRIES INC', 'SWN': 'SOUTHWESTERN ELECTRIC POWER CO', 'HDSN': 'HUDSON TECHNOLOGIES INC',
            'TESS': 'TESSCO TECHNOLOGIES INC', 'JPM': 'JPMORGAN CHASE & CO', 'OCC': 'OPTICAL CABLE CORP', 'GEOS': 'GEOSPACE TECHNOLOGIES CORP',
            'EL': 'ESTEE LAUDER COMPANIES INC', 'CCBG': 'CAPITAL CITY BANK GROUP INC', 'MGTI': 'MGT CAPITAL INVESTMENTS, INC.',
            'WFC': 'WELLS FARGO & COMPANY', 'ASTC': 'ASTROTECH Corp', 'HBIA': 'HILLS BANCORPORATION', 'NTAP': 'NetApp, Inc.', 'BMRA': 'BIOMERICA INC',
            'WSTL': 'WESTELL TECHNOLOGIES INC', 'TCI': 'TRANSCONTINENTAL REALTY INVESTORS INC', 'OTEX': 'OPEN TEXT CORP', 'MSM': 'MSC INDUSTRIAL DIRECT CO INC',
            'MEOH': 'METHANEX CORP', 'TWIN': 'TWIN DISC INC', 'SM': 'SM Energy Co', 'BRN': 'BARNWELL INDUSTRIES INC',
            'LJPC': 'LA JOLLA PHARMACEUTICAL CO', 'TSN': 'TYSON FOODS, INC.', 'IMAX': 'IMAX CORP', 'SSRM': 'SSR MINING INC'}

subdata = pd.DataFrame()

for ticker, cname in tickersDict.items():
    mask = (data['Company Name'].str.upper().str.contains(cname)==True)
    temp_data = data[mask]
    temp_data['ticker']= np.where(temp_data['Company Name'].str.upper().str.contains(cname)==True, ticker, np.nan)
    subdata = subdata.append(temp_data)

subdata.to_csv(r'filing_data.csv') # Saving the filing data for reference

# ==============================================================
# 2) Downloading the historic stock data from Yahoo Finance API:
# ==============================================================

tickersLst = ['MNG.L', 'GBX', 'BION.SW', 'MLR', 'SWN', 'HDSN', 'TESS', 'JPM', 'OCC', 'GEOS', 'EL', 'CCBG', 'MGTI', 'WFC', 'ASTC', 'HBIA', 'NTAP', 'BMRA',
             'WSTL', 'TCI', 'OTEX', 'MSM', 'MEOH', 'TWIN', 'SM', 'BRN', 'LJPC', 'TSN', 'IMAX', 'SSRM']

import pandas_datareader as pdr

df = pd.DataFrame()

for ticker in tickersLst:
    temp_df = pdr.DataReader(ticker,'yahoo','2021-01-01','2021-03-31')
    temp_df['ticker'] = ticker
    temp_df['date'] = temp_df.index
    df = df.append(temp_df)

df.to_csv(r'stock_data.csv') # Saving the stock data for reference

# =========================================================
# 3) Merging the filing data and historic stock price data:
# =========================================================

merge_data = pd.merge(df, subdata, left_on=['ticker', 'date'], right_on=['ticker', 'date_filed'], how='left')
merge_data['event_dummy'] = np.where(merge_data['date_filed'].isnull(), 0, 1)

merge_data.to_csv(r'merged_data.csv') # Saving the merged data for reference

# =========================================================================================
# 4) Producing summary statistics of the stock indicators during event and non-event dates:
# =========================================================================================

import statsmodels.formula.api as smf

formula = 'Volume ~ C(event_dummy)'
est_model = smf.ols(formula, merge_data).fit()

print(est_model.summary())

# =========================================================================================
# 5) Conducting an Econometric Procedure :
# =========================================================================================

print(df.describe())