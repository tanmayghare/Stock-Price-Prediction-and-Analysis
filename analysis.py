import requests
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import statsmodels.formula.api as smf

class StockPriceAnalysis:
    def __init__(self):
        self.url = r"https://www.sec.gov/Archives/edgar/full-index/2021/QTR1/master.idx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept-Encoding': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.sec.gov'
        }
        self.tickersDict = {
            'MNG.L': 'M&G INVESTMENT MANAGEMENT LTD', 'GBX': 'GREENBRIER COMPANIES INC', 'BION.SW': 'BB BIOTECH AG',
            'MLR': 'MILLER INDUSTRIES INC', 'SWN': 'SOUTHWESTERN ELECTRIC POWER CO', 'HDSN': 'HUDSON TECHNOLOGIES INC',
            'TESS': 'TESSCO TECHNOLOGIES INC', 'JPM': 'JPMORGAN CHASE & CO', 'OCC': 'OPTICAL CABLE CORP', 'GEOS': 'GEOSPACE TECHNOLOGIES CORP',
            'EL': 'ESTEE LAUDER COMPANIES INC', 'CCBG': 'CAPITAL CITY BANK GROUP INC', 'MGTI': 'MGT CAPITAL INVESTMENTS, INC.',
            'WFC': 'WELLS FARGO & COMPANY', 'ASTC': 'ASTROTECH Corp', 'HBIA': 'HILLS BANCORPORATION', 'NTAP': 'NetApp, Inc.', 'BMRA': 'BIOMERICA INC',
            'WSTL': 'WESTELL TECHNOLOGIES INC', 'TCI': 'TRANSCONTINENTAL REALTY INVESTORS INC', 'OTEX': 'OPEN TEXT CORP', 'MSM': 'MSC INDUSTRIAL DIRECT CO INC',
            'MEOH': 'METHANEX CORP', 'TWIN': 'TWIN DISC INC', 'SM': 'SM Energy Co', 'BRN': 'BARNWELL INDUSTRIES INC',
            'LJPC': 'LA JOLLA PHARMACEUTICAL CO', 'TSN': 'TYSON FOODS, INC.', 'IMAX': 'IMAX CORP', 'SSRM': 'SSR MINING INC'
        }
        self.tickersLst = list(self.tickersDict.keys())

    def download_filing_data(self):
        """
        Downloads the SEC EDGAR filing data and saves it to a text file.
        """
        request_content = requests.get(self.url, headers=self.headers).content
        result = request_content.decode("utf-8", "ignore")
        with open('master_index_2021QTR1.txt', 'w') as f:
            f.write(result)

    def process_filing_data(self):
        """
        Processes the downloaded filing data, filters it based on significant corporate events,
        and saves the filtered data to a CSV file.
        """
        with open('master_index_2021QTR1.txt', 'r') as f:
            lines = f.readlines()

        columns = tuple(lines[9].split('|'))
        records = [tuple(line.split('|')) for line in lines[11:]]

        data = pd.DataFrame(records, columns=columns)
        data['date_filed'] = pd.to_datetime(data['Date Filed'])
        subdata = pd.DataFrame()

        for ticker, cname in self.tickersDict.items():
            mask = (data['Company Name'].str.upper().str.contains(cname) == True)
            temp_data = data[mask]
            temp_data['ticker'] = np.where(temp_data['Company Name'].str.upper().str.contains(cname) == True, ticker, np.nan)
            subdata = subdata.append(temp_data)

        subdata.to_csv(r'filing_data.csv')
        return subdata

    def download_stock_data(self):
        """
        Downloads historic stock data from Yahoo Finance API and saves it to a CSV file.
        """
        df = pd.DataFrame()
        for ticker in self.tickersLst:
            temp_df = pdr.DataReader(ticker, 'yahoo', '2021-01-01', '2021-03-31')
            temp_df['ticker'] = ticker
            temp_df['date'] = temp_df.index
            df = df.append(temp_df)

        df.to_csv(r'stock_data.csv')
        return df

    def merge_data(self, stock_data, filing_data):
        """
        Merges the stock data and filing data, creates an event dummy variable,
        and saves the merged data to a CSV file.
        """
        merge_data = pd.merge(stock_data, filing_data, left_on=['ticker', 'date'], right_on=['ticker', 'date_filed'], how='left')
        merge_data['event_dummy'] = np.where(merge_data['date_filed'].isnull(), 0, 1)
        merge_data.to_csv(r'merged_data.csv')
        return merge_data

    def produce_summary_statistics(self, merged_data):
        """
        Produces summary statistics of the stock indicators during event and non-event dates.
        """
        formula = 'Volume ~ C(event_dummy)'
        est_model = smf.ols(formula, merged_data).fit()
        print(est_model.summary())

    def run_analysis(self):
        """
        Runs the entire analysis pipeline for conducting an econometric procedure.
        """
        self.download_filing_data()
        filing_data = self.process_filing_data()
        stock_data = self.download_stock_data()
        merged_data = self.merge_data(stock_data, filing_data)
        self.produce_summary_statistics(merged_data)
        print(stock_data.describe())

if __name__ == "__main__":
    analysis = StockPriceAnalysis()
    analysis.run_analysis()
