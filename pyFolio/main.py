# -*- coding: utf-8 -*-
import os
import pandas as pd
import yfinance as yf
import pf_influx as influx
import concurrent.futures


def readPortfolio():
    porfolio_csv = os.path.join("config", "portfolio.csv")
    df = pd.read_csv(porfolio_csv)
    return df


def getData(row):
    extract = yf.Ticker(row["name"])
    row["price"] = extract.info["regularMarketOpen"]
    row["sum"] = row["price"] * row["amount"]
    influx.write_row_to_influx(row)
    return True


def main():
    df = readPortfolio()
    threads = len(df.index)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for index, row in df.iterrows():
            executor.submit(getData, row)
    executor.shutdown(wait=True)


if __name__ == '__main__':
    main()