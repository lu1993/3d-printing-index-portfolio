# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:40:33 2017

@author: lcao
"""

import pandas as pd
import numpy as np
import portfolioopt as pfopt
from pkg_resources import resource_filename
 


# return
price = pd.read_csv(resource_filename('portfolio-construct-analyze.resources', 'price_data.csv'), index_col = 0)
price = price[['SSYS','HPQ','DDD']]
return_ = pd.DataFrame(columns = price.columns.values,
                       index = price.index.values)
for i in range(price.shape[1]):
    col = return_.columns.values[i]
    return_[col] = [1.0 * x/y for x,y in zip(np.array(price[col].diff()),np.array(price[col]))]
    return_[col].iloc[0] = 0




# weight
window = 21
weight = pd.DataFrame(columns = price.columns.values,
                           index = price.index.values[window:])
for i in np.arange(window, price.shape[0],1):
    returns = return_.iloc[(i-window):i]
    cov_mat = np.cov(returns.transpose())
    cov_mat = pd.DataFrame(cov_mat, columns = price.columns.values, index = price.columns.values)
    
    weights = pfopt.min_var_portfolio(cov_mat)
    weight.set_value(weight.index[(i-window)],weight.columns.values,np.array(weights))
     
    
 
    
# performance
portfolio_opt = {}

price = price.loc[weight.index]
full_data = pd.DataFrame(columns = ['Performance','DailyReturn','CumulativeReturn'], 
                         index = price.index)
full_data['Performance'] = [np.sum([x * y for x,y in zip(np.array(price.iloc[i]),
                                                         np.array(weight.iloc[i])) if \
                                    not np.isnan(x)]) for i in range(price.shape[0])]
full_data['DailyReturn'] = [1.0 * x/y for x,y in zip(np.array(full_data['Performance'].diff()),np.array(full_data['Performance']))]
full_data['DailyReturn'].iloc[0] = 0
        
# cummulative return
full_data['CumulativeReturn'] = np.array(full_data['Performance'])/full_data['Performance'].iloc[0]
 
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

portfolio_opt.update({'optimization': {'portfolio':full_data,'riskmetrics':riskmetrics}})
