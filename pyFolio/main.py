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
        influx.write_row_to_influx(row)
    return df


def main():
   getData(readPortfolio())


if __name__ == '__main__':
    main()