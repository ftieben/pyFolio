# -*- coding: utf-8 -*-
import os
import pandas as pd
import yfinance as yf
import pf_influx as influx


def readPortfolio():
    porfolio_csv = os.path.join("config", "portfolio.csv")
    df = pd.read_csv(porfolio_csv)
    return df


def createSymbolList(df):
    symbollist = []
    for index, row in df.iterrows():
        symbollist.append(row["name"])
    return symbollist


def enrichData(df):
    for index, row in df.iterrows():
        extract = yf.Ticker(row["name"])
        row["price"] = extract.info["regularMarketOpen"]
        row["sum"] = row["price"] * row["amount"]
        df.loc[index, "price"] = row["price"]
        df.loc[index, "sum"] = row["sum"]
    return df


def getData(list):
    #extract = yf.Ticker(list)
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=list,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period="1d",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval="5m",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by='ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust=True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost=True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy=None
    )
    return data.info()


def main():
    influx \
        .write_to_influx(
            getData(
                createSymbolList(
                    readPortfolio()
                )
            )
        )


if __name__ == '__main__':
    main()