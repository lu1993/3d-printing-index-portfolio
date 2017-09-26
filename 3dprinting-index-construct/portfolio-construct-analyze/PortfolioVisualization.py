# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:28:30 2017

@author: LuCao
"""

import pandas as pd
import pickle
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pkg_resources import resource_filename
 
with open(resource_filename('portfolio-construct-analyze.resources', 'portfolio.pickle'), 'r') as f:
    portfolio = pickle.load(f)
f.close()
    
    
def main():
    
    date_format='%Y-%m-%d' 
        
    for i in range(len(portfolio.keys())):
        p = portfolio[portfolio.keys()[i]]
        p = p[p.keys()[0]]
        y = list(p['CummulativeReturn'])
        #x = p.index 
        x=[dt.datetime.strptime(d,date_format) for d in p.index]
        plt.plot(x,y,label = portfolio.keys()[i])
        
    plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=20)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=240))
    plt.grid()
    plt.legend(loc='upper left',prop={'size':10})
    plt.title('Cumulative Return by Index Portfolio')
    plt.show()
    
    risk_metrics = pd.DataFrame(columns = ['CumulativeReturn','SharpeRatio',
                                           'MaxDrawdown','MaxDailyloss'],
                                index = portfolio.keys())
    for i in range(len(portfolio.keys())):
        p = portfolio[portfolio.keys()[i]]
        p = p[p.keys()[1]]
        print portfolio.keys()[i]
        print p
        risk_metrics.loc[portfolio.keys()[i]] = [p['CumulativeReturn'],
                                             p['SharpeRatio'],
                                             p['MaxDrawdown'],
                                             p['MaxDailyloss']]
    risk_metrics = risk_metrics.sort_values(by = 'CumulativeReturn', ascending = False)
    risk_metrics.to_csv(resource_filename('portfolio-construct-analyze.resources', 'risk_metrics.csv'), index = True)
    
if __name__ == '__main__':
    main()
    
