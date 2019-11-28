# -*- coding: utf-8 -*-
import os
import pandas as pd
import yfinance as yf
import pf_influx as influx


def readPortfolio():
    porfolio_csv = os.path.join("config", "portfolio.csv")
    df = pd.read_csv(porfolio_csv)
    return df


def getData(df):
    for index, row in df.iterrows():
        extract = yf.Ticker(row["name"])
        row["price"] = extract.info["regularMarketOpen"]
        row["sum"] = row["price"] * row["amount"]
        df.loc[index, "price"] = row["price"]
        df.loc[index, "sum"] = row["sum"]
    return df


def main():
    influx \
        .write_to_influx(
        getData(
            readPortfolio()))

if __name__ == '__main__':
    main()