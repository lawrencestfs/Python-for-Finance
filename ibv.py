##!/usr/bin/python
# -*- coding: utf-8 -*-

# File Name: ibv.py
# Author: Lawrence Fernandes
# Copyright (C) 2017 Lawrence Fernandes

""" This module donwloads historical prices of stocks listed at Ibovespa from Yahoo Finance.
"""
# Import Python standard modules
import os
import pickle
import requests
import datetime as dt
# Import external modules
import bs4 as bs
import numpy as np
import pandas as pd
import pandas_datareader.data as web

def save_ibovespa_tickers():
    """ Return the tickers of the stocks that comprises the Ibovespa index"""
    tickers = []

    resp = requests.get("http://exame.abril.com.br/mercados/cotacoes-bovespa/indices/BVSP/integrantes?page=1")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class":"data-table"}) 
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        ticker += ".SA"
        tickers.append(ticker)

    resp = requests.get("http://exame.abril.com.br/mercados/cotacoes-bovespa/indices/BVSP/integrantes?page=2")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class":"data-table"}) 
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        if ".SA" not in ticker: ticker += ".SA"
        tickers.append(ticker)

    with open("ibovespa.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

def get_data_from_yahoo(reload_ibovespa=False):
    """ Get the Ibovespa stock's historical prices from Yahoo Finance"""
    if reload_ibovespa:
        tickers = save_ibovespa_tickers()
    else:
        with open("ibovespa.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("ibovespa_stocks"):
        os.makedirs("ibovespa_stocks")

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tickers:
        if not os.path.exists("ibovespa_stocks/{}.csv".format(ticker)):
            try:
                df = web.DataReader(ticker,"yahoo",start, end)
                df.to_csv("ibovespa_stocks/{}.csv".format(ticker))
                print "Success in retreiving data for: ", ticker
            except:
                print "Failed in retreiving data for: ",ticker
                continue
        else:
            print("Already have {}".format(ticker))

save_ibovespa_tickers()
get_data_from_yahoo()