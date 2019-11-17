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
    df = pd.DataFrame.from_csv(porfolio_csv)
    return df


def getData(portfolio):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for item in portfolio:
        item.update({'time': current_time})
        if item["type"] == "crypto":
            cmc = coinmarketcapapi.CoinMarketCapAPI(get_api_key(), sandbox=False)
            extract = cmc.cryptocurrency_quotes_latest(symbol=item["name"])
            price = extract.data[item["name"]]["quote"]["USD"]["price"]
            summe = price * item["amount"]
            item.update({'price': price, 'sum': summe})
        else:
            extract = yf.Ticker(item["name"])
            price = extract.info["regularMarketPrice"]
            summe = price * item["amount"]
            item.update({'price': price, 'sum': summe})
    return portfolio

def main():
    influx \
        .write_to_influx(
        getData(
            readPortfolio()))

if __name__ == '__main__':
    print("hallo")
    main()