# -*- coding: utf-8 -*-
import os
import pandas as pd
import coinmarketcapapi
import yfinance as yf
import pf_influx as influx
from datetime import datetime


def get_api_key():
    keyfile = os.path.join("config", "apikey.txt")
    f = open(keyfile, "r")
    apikey = f.readline()
    f.close()
    return apikey


def readPortfolio():
    porfolio_csv = os.path.join("config", "portfolio.csv")
    df = pd.read_csv(porfolio_csv)
    return df


def getData(df):
    for index, row in df.iterrows():
        if row["type"] == "crypto":
            cmc = coinmarketcapapi.CoinMarketCapAPI(get_api_key(), sandbox=False)
            extract = cmc.cryptocurrency_quotes_latest(symbol=row["name"])
            row["price"] = extract.data[row["name"]]["quote"]["USD"]["price"]
            row["sum"] = row["price"] * row["amount"]
            df.loc[index, "price"] = row["price"]
            df.loc[index, "sum"] = row["sum"]
        else:
            extract = yf.Ticker(row["name"])
            row["price"] = extract.info["regularMarketPrice"]
            row["sum"] = row["price"] * row["amount"]
            df.loc[index, "price"] = row["price"]
            df.loc[index, "sum"] = row["sum"]
    print(df)
    return df


def main():
    influx \
        .write_to_influx(
        getData(
            readPortfolio()))

if __name__ == '__main__':
    main()