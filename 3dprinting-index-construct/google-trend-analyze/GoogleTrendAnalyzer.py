# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:57:15 2017

@author: lcao
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pkg_resources import resource_filename

def main():

    gt = pd.read_csv(resource_filename('google-trend-analyze.resources', 'GoogleTrends.csv'), header = None)
    gt = gt.rename(columns={0:'Date',1:'Number'})
    
    # compute search number of each year
    gt_yearly = pd.DataFrame({'Year':np.arange(2004,2018,1),
                              'Number':[0]*len(np.arange(2004,2018,1))})
    for i in np.arange(2004,2018,1):
       idx = np.where(np.array([int(x.split('-')[0]) for x in gt['Date']])==i)[0]
       gt_yearly['Number'].iloc[(i-2004)] = np.sum(gt['Number'].iloc[idx])
       
    gt_yearly.to_csv(resource_filename('google-trend-analyze.resources', 'GoogleTrendsYearly.csv'), index = False)
    
    s = pd.Series(
        np.array(gt_yearly['Number']),
        index = list(gt_yearly['Year'])
        )

    plt.title("Google Trends by Year")
    plt.ylabel('Google Trends')
    plt.xlabel('Year')
    ax = plt.gca()
    ax.tick_params(axis='x', colors='blue')
    ax.tick_params(axis='y', colors='red')
    my_colors = 'rgbkymc'  #red, green, blue, black, etc.
    s.plot(
        kind='bar',
        color = my_colors,
        alpha = 0.5
    )
    plt.xticks(rotation = 30)
    rects = ax.patches
    labels = s.values
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center', va='bottom')
    plt.show()  
    
    
if __name__ == '__main__':
    main()