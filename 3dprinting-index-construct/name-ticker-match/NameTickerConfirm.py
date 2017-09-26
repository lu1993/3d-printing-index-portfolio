# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 21:27:25 2017

@author: LuCao
"""

import pandas as pd
import numpy as np
from google import search
import time
import json
import sys
sys.path.append("C:/Users/LuCao/Documents/3DPrinting/3dprinting-index-construct/name-ticker-match")
from similarity import matchName
from pkg_resources import resource_filename

tickers = pd.read_csv(resource_filename('name-ticker-match.resources', 'tickers.csv'))


def main():
    names = np.array(tickers['Name'])
    matches = np.array(tickers['Match'])
    nametickers = [np.nan] * len(names)
    matchtickers = [np.nan] * len(matches)
    
     
    # use google search to check tickers for company names
    start = time.time()
    for i in range(len(names)):
        query = "Summary for " + names[i] + " Yahoo Finance"
        ticker = [result.replace('https://finance.yahoo.com/quote/','').replace('/','').split(',')[0] for \
                  result in search(query, tld="co.in", num=5, stop=1, pause=10) if \
                  result.startswith('https://finance.yahoo.com/quote/',0,)]
        if len(ticker)>0:
            print ticker[0]
            nametickers[i] = ticker
    end = time.time()
    print 'Hours eclapsed: ' + str(1.0 * (end - start)/3600)
      
    
    start = time.time()
    for i in range(len(matches)):
        query = "Summary for " + matches[i] + " Yahoo Finance"
        ticker = [result.replace('https://finance.yahoo.com/quote/','').replace('/','').split(',')[0] for \
                  result in search(query, tld="co.in", num=5, stop=1, pause=10) if \
                  result.startswith('https://finance.yahoo.com/quote/',0,)]
        if len(ticker)>0:
            print ticker[0]
            matchtickers[i] = ticker
    end = time.time()
    print 'Hours eclapsed: ' + str(1.0 * (end - start)/3600)
    
    
    newTickers = pd.DataFrame({'Name':names,
                               'Match':matches,
                               'YahooTicker':tickers['Ticker'],
                               'NameTicker':nametickers,
                               'MatchTicker':matchtickers})
    suspect_Tickers = newTickers.loc[[x != y for x,y in zip(newTickers['NameTicker'],newTickers['MatchTicker'])]]
    safe_Tickers = newTickers.loc[[x == y for x,y in zip(newTickers['NameTicker'],newTickers['MatchTicker'])]]
    suspect_Tickers.shape[0]
    safe_Tickers.shape[0]


    # cases where names are too general
    short_name = []
    for i in range(suspect_Tickers.shape[0]):
        if len(suspect_Tickers['Name'].iloc[i].split()) == 1:
            short_name.extend(suspect_Tickers['Name'].iloc[i].split())
    pd.DataFrame({'CompanyName':short_name}).to_csv(resource_filename('name-ticker-match.resources', 'SingleWordNames.csv'), index = False)
    

    # cases with multiple tickers
    nameData = suspect_Tickers[['NameTicker','MatchTicker']]
    suspects = {}
    for i in range(nameData.shape[0]):
        suspect = matchName(np.array(nameData.iloc[i]))
        if suspect.items()[0][1][1] >= 0.5 or suspect.items()[0][1][2] >= 0.5:
            suspects.update(suspect)
            
    with open(resource_filename('name-ticker-match.resources', 'MultiTickers.json'), 'w') as f:
        json.dump(suspects, f)
            
    
    safe_Tickers.to_csv(resource_filename('portfolio-construct-analyze.resources', 'confirmed_tickers.csv'), index = False)


if __name__ == '__main__':
    main()