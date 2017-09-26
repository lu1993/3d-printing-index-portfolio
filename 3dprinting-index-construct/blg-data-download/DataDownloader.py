# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 12:05:20 2017

@author: lcao
"""

import pandas as pd
import numpy as np
import sys
sys.path.append("C:/Users/LuCao/Documents/3DPrinting/3dprinting-index-construct/blg-data-download")
from DataProcess import retrieveData, fillData, countNA
from pkg_resources import resource_filename
confirmed_tickers = pd.read_csv(resource_filename('blg-data-download.resources', 'confirmed_tickers.csv'))


def main():
    
    # select us equities
    tickers = []
    for i in range(confirmed_tickers.shape[0]):
        t = confirmed_tickers['NameTicker'].iloc[i]
        if len(t.split('.')) == 1:
            tickers.extend([t])

    # set time frame
    start = '2011-01-01'
    end = '2017-09-22'
    data = retrieveData(
            conStr = ('DRIVER={SQL Server Native Client 11.0};\
                      SERVER=p7sql1;DATABASE=Trade;uid=quant;pwd=quant'),
            query = "select * from dbo.tblStockPrice \
            where symbol = 'SPY' and PriceDate >= '" + start +"' and PriceDate <= '" + end + "'")
    data = data.sort_values('PriceDate', ascending = True)
    
    price = pd.DataFrame(columns = tickers, index = data['PriceDate'])
    beta = pd.DataFrame(columns = tickers, index = data['PriceDate'])
    marketcap = pd.DataFrame(columns = tickers, index = data['PriceDate'])

    # download and clean data
    miss_ticker = []
    na_ticker = []
    for i in range(len(tickers)):
        data = retrieveData(
                conStr = ('DRIVER={SQL Server Native Client 11.0};\
                          SERVER=p7sql1;DATABASE=Trade;uid=quant;pwd=quant'),
                query = "select * from dbo.tblStockPrice \
                where symbol = '"+tickers[i]+"' and PriceDate >= '" + start +"' and PriceDate <= '" + end +"'")
        data = data.sort_values('PriceDate', ascending = True)
        data = data[['PriceDate','symbol','ClosePrice','Volume','Beta','MarketCap']]
        if data.shape[0] == 0:
            print 'There is no data for ' + tickers[i]
            miss_ticker.extend([tickers[i]])
        else:
            for k in ['ClosePrice','Volume','Beta','MarketCap']:
                data[k] = fillData(np.array(data[k]),'na')
                        
            na_idx = np.where(np.array(data[['ClosePrice','Beta','MarketCap']].apply(countNA, axis = 0))>0.01)[0]
            na_volume_idx = np.where(np.array(data[['Volume']].apply(countNA, axis = 0))!=0)[0]
            
            if len(na_idx) != 0 or len(na_volume_idx) != 0:
                na_ticker.extend([tickers[i]])
            else:
                for k in ['ClosePrice','Beta','MarketCap']:
                    data[k] = fillData(np.array(data[k]),'sma')
                
                price[tickers[i]].loc[data['PriceDate']] = np.array(data['ClosePrice'])
                #volume[tickers[i]].loc[[x in volume.index for x in data['PriceDate']]] = np.array(data['Volume'])
                beta[tickers[i]].loc[data['PriceDate']] = np.array(data['Beta'])
                marketcap[tickers[i]].loc[data['PriceDate']] = np.array(data['MarketCap'])
        
    rm_ticker = list(set(np.append(np.array(miss_ticker),np.array(na_ticker))))
    keep_ticker = [x for x in tickers if x not in rm_ticker]
    
    price = price[keep_ticker]
    beta = beta[keep_ticker]
    marketcap = marketcap[keep_ticker]

    price.to_csv(resource_filename('portfolio-construct-analyze.resources', 'price_data.csv'), index = True)
    beta.to_csv(resource_filename('portfolio-construct-analyze.resources', 'beta_data.csv'), index = True)
    marketcap.to_csv(resource_filename('portfolio-construct-analyze.resources', 'marketcap_data.csv'), index = True)
    final_tickers = pd.DataFrame({'NameTicker':keep_ticker})
    final_tickers.to_csv(resource_filename('portfolio-construct-analyze.resources', 'final_tickers.csv'), index = False)
    
    
if __name__ == '__main__':
    main()
