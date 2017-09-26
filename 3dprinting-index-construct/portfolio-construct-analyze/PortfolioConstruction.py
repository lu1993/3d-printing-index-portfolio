# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 12:53:39 2017

@author: LuCao
"""

import pandas as pd
import numpy as np
import pickle
from pkg_resources import resource_filename
 
price = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'price_data.csv'), index_col = 0)
beta = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'beta_data.csv'), index_col = 0)
marketcap = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'marketcap_data.csv'), index_col = 0)
revenue = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'revenue_data.csv'), index_col = 0)


def main():
       
    metric = ['price','equal','marketcap','beta','revenue']
    portfolio = {}
    
    for k in range(len(metric)):
        m = metric[k]

        if m == 'equal':
            weight_data = [[1.0/len(price.iloc[i].dropna()) if not np.isnan(x) else \
                            0 for x in price.iloc[i]] for \
                            i in range(price.shape[0])]
        else:
            if m == 'price':
                criteria_data = price
                
            elif m == 'marketcap':
                criteria_data = marketcap

            elif m == 'beta':
                criteria_data = beta
                
            elif m == 'revenue':
                criteria_data = revenue
            
            weight_data = [[x/np.sum(criteria_data.iloc[i].dropna()) if not np.isnan(x) else \
                            0 for x in criteria_data.iloc[i]] for \
                            i in range(criteria_data.shape[0])] 
        
        weight_data = pd.DataFrame(weight_data,
                                   columns = [x+'_Weight' for x in price.columns.values],
                                   index = price.index)
        full_data = price.join(weight_data)
        
        # performance
        full_data['Performance'] = [np.sum([x * y for x,y in zip(np.array(price.iloc[i]),
                                                                 np.array(weight_data.iloc[i])) if \
                                            not np.isnan(x)]) for i in range(price.shape[0])]
        full_data['DailyReturn'] = [1.0 * x/y for x,y in zip(np.array(full_data['Performance'].diff()),np.array(full_data['Performance']))]
        full_data['DailyReturn'].iloc[0] = 0
                
        # cummulative return
        full_data['CumulativeReturn'] = np.array(full_data['Performance'])/full_data['Performance'].iloc[0]
                        
        # remove outliers for beta
        if m == 'beta':
            for i in range(1,full_data.shape[0]):
                if full_data['DailyReturn'].iloc[i] > 1 or full_data['DailyReturn'].iloc[i] < -1:
                    full_data['DailyReturn'].iloc[i] = 0
            
            for i in range(1,full_data.shape[0]):
                if full_data['CumulativeReturn'].iloc[i] > 2.5:
                    full_data['CumulativeReturn'].iloc[i] = full_data['CumulativeReturn'].iloc[(i-1)] 
        
        # max drawdown
        dd, DD = 0,0
        for j in range(full_data.shape[0]-1):
            low = np.min(np.array(full_data['CumulativeReturn'])[(j+1):])
            dd = 1 - low/np.array(full_data['CumulativeReturn'])[j]
            if dd > DD:
                DD = dd
                
        # risk metrics
        riskmetrics = {'CumulativeReturn':full_data['CumulativeReturn'].iloc[-1],
                       'SharpeRatio':np.sqrt(252) * np.mean(np.array(full_data['DailyReturn'].dropna()))/np.std(np.array(full_data['DailyReturn'].dropna())),
                       'MaxDrawdown':DD,
                       'MaxDailyloss':np.min(np.array(full_data['DailyReturn']))}
        
        portfolio.update({m: {'portfolio':full_data,'riskmetrics':riskmetrics}})
        
        with open(resource_filename('portfolio-construct-analyze.resources', 'portfolio.pickle'), 'w') as f:
            pickle.dump(portfolio, f)
        f.close()


if __name__ == '__main__':
    main()