# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 15:14:24 2017

@author: lcao
"""

import sqlUpdateLib3 as sq
import blbReferenceData as blpR
import pandas as pd
import numpy as np
import datetime as dt
import os
from pkg_resources import resource_filename
import sys
sys.path.append("C:/Users/LuCao/Documents/3DPrinting/3dprinting-index-construct/blg-data-download")
from DataProcess import retrieveData


def main():
    
    date_format = '%Y-%m-%d'
    direct = r'Z:\lcao'
    tickers = pd.read_csv('Z:\lcao\final_tickers.csv')
    symbolSet = list(tickers['NameTicker'])
    
    equity = blpR.makeBBSymbol(symbolSet)
    
    startDate = '20110101'
    strData = ['sales_rev_turn']    
    endDate = '20170922'
    
    price = blpR.getHistfromBB(equity, strData,startDate,endDate) 
    price = blpR.blb2sqlRecord(price)
    param = ['[Symbol]','[PriceDate]']+strData

    print ("back up to local disk...")
    filename = sq.record2file(param, os.path.join(direct,'Revenue'), price)
    print filename
    
    # change the structure of revenue data
    revenue_quarterly = pd.read_csv(resource_filename('blg-data-download.resources', 'revenue_quarterly.csv'), index_col = 0)
    revenue_quarterly = revenue_quarterly.rename(columns = {'[PriceDate]':'PriceDate','sales_rev_turn':'Revenue'})
    revenue_quarterly['PriceDate'] = np.array([dt.datetime.strptime(x, date_format).date() for x in revenue_quarterly['PriceDate']])
    final_tickers = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'final_tickers.csv'))
    final_tickers = list(final_tickers['NameTicker'])
    
    # set time frame
    start = '2011-01-01'
    end = '2017-09-22'
    data = retrieveData(
            conStr = ('DRIVER={SQL Server Native Client 11.0};\
                      SERVER=p7sql1;DATABASE=Trade;uid=quant;pwd=quant'),
            query = "select * from dbo.tblStockPrice \
            where symbol = 'SPY' and PriceDate >= '" + start +"' and PriceDate <= '" + end + "'")
    data = data.sort_values('PriceDate', ascending = True)
    revenue = pd.DataFrame(columns = final_tickers, index = data['PriceDate'])
    
    # put revenue into new data frame
    for i in range(len(final_tickers)):
        subdata = revenue_quarterly.loc[revenue_quarterly.index == final_tickers[i]]
        for k in range(revenue.shape[0]):
            idx = np.where(np.array(subdata['PriceDate'])<=revenue.index[k])[0]
            if len(idx) != 0:
                idx = idx[-1]
                revenue[final_tickers[i]].iloc[k] = subdata['Revenue'].iloc[idx]
            else:
                revenue[final_tickers[i]].iloc[k] = 0
      
    revenue.to_csv(resource_filename('portfolio-construct-analyze.resources', 'revenue_data.csv'), index = True)
    

if __name__ == '__main__':
    main()