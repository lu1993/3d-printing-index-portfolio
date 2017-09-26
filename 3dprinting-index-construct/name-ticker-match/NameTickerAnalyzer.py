# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 15:33:40 2017

@author: LuCao
"""

from similarity import lcs
import json
import pandas as pd
import numpy as np
import re
from pkg_resources import resource_filename

with open(resource_filename('name-ticker-match.resources', 'NameMatchSuspects.json'),'r') as f:    
    suspects = json.load(f)
f.close()


def main():
    # string match similary >= 90%   
    confirm = pd.DataFrame(columns = ['Name','Match','nameStrPercent','matchStrPercent'])
    for i in range(len(suspects)):
        item = suspects.items()[i]
        if item[1][1] >= 0.9 or item[1][2] >= 0.9:
            df = pd.DataFrame({'Name':item[0], 
                               'Match':item[1][-1],
                               'nameStrPercent':item[1][2],
                               'matchStrPercent':item[1][1]},index = [0])
            confirm = confirm.append(df, ignore_index = True)
    
      
    # word match %
    confirm['nameWordPercent'] = [0] * confirm.shape[0]
    confirm['matchWordPercent'] = [0] * confirm.shape[0]
    for i in range(confirm.shape[0]):
        name = re.sub(r'[^\w]', ' ', confirm['Name'].iloc[i])
        match = re.sub(r'[^\w]', ' ', confirm['Match'].iloc[i])
        
        name_word = name.split()
        match_word = match.split()
        
        count = 0
        for word in name_word:
            if word in match_word:
                count = count + 1
        p1 = 1.0 * count/len(name_word)
        
        count = 0
        for word in match_word:
            if word in name_word:
                count = count + 1
        p2 = 1.0 * count/len(match_word)
        
        confirm['nameWordPercent'].iloc[i] = p1
        confirm['matchWordPercent'].iloc[i] = p2
      
     
    # word match similarity >= 90%
    confirm_new = pd.DataFrame(columns = ['Name','Match',
                                          'nameStrPercent','matchStrPercent',
                                          'nameWordPercent','matchWordPercent'])
    for i in range(confirm.shape[0]):
        if confirm['nameWordPercent'].iloc[i]> 0 or confirm['matchWordPercent'].iloc[i] > 0:
            confirm_new = confirm_new.append(confirm.iloc[i], ignore_index = True)
    
    
    # remove potential duplicates
    duplicates = pd.DataFrame(columns = ['Name1','Name2'])
    for i in range((confirm_new.shape[0]-1)):
        for j in np.arange((i+1),confirm_new.shape[0],1):
            name1 = confirm_new['Name'].iloc[i]
            name2 = confirm_new['Name'].iloc[j]
            l = lcs(name1,name2)
            if len(l) > 0:
                if 1.0 * len(l[0])/len(name1) >= 0.9 or 1.0 * len(l[0])/len(name2) >= 0.9:
                    df = pd.DataFrame({'Name1':name1, 'Name2':name2}, index = [0])
                    duplicates = duplicates.append(df, ignore_index = True)
    rm_name = ['PyroGenesis Canada', '3D Lab', 'Engineering', 'Dimension', 'Victrex plc']
    confirm_new = confirm_new.loc[[x not in rm_name for x in confirm_new['Name']]]
        
        
    # create a universe of stop words based on frequency
    universe = []
    for i in range(confirm_new.shape[0]):
        name = re.sub(r'[^\w]', ' ', confirm['Name'].iloc[i])
        match = re.sub(r'[^\w]', ' ', confirm['Match'].iloc[i])
        name_word = name.split()
        match_word = match.split()
        universe.extend(name_word)
        universe.extend(match_word)             
    
    frequency = pd.DataFrame({'Universe':np.unique(universe),
                              'Frequency':[0] * len(np.unique(universe))
                              })
    for i in range(frequency.shape[0]):
        frequency['Frequency'].iloc[i] = len(np.where(np.array(universe) == frequency.iloc[i]['Universe'])[0])
    frequency = frequency.sort_values(by = 'Frequency', ascending = False)
    
    stopword = np.array(frequency.loc[frequency['Frequency']>2]['Universe'])
    
    
    # compute word match % after removing stop words
    for i in range(confirm_new.shape[0]):
        name = re.sub(r'[^\w]', ' ', confirm_new['Name'].iloc[i])
        match = re.sub(r'[^\w]', ' ', confirm_new['Match'].iloc[i])
        
        name_word = name.split()
        match_word = match.split()
        
        name_word = [x for x in name_word if x not in stopword]
        match_word = [x for x in match_word if x not in stopword]
        
        if len(name_word) > 0:
            count = 0
            for word in name_word:
                if word in match_word:
                    count = count + 1
            p1 = 1.0 * count/len(name_word)
        else:
            p1 = 0
        
        if len(match_word) > 0:
            count = 0
            for word in match_word:
                if word in name_word:
                    count = count + 1
            p2 = 1.0 * count/len(match_word)
        else:
            p2 = 0
        
        confirm_new['nameWordPercent'].iloc[i] = p1
        confirm_new['matchWordPercent'].iloc[i] = p2
        
        
    confirm_final = pd.DataFrame(columns = ['Name','Match',
                                            'nameStrPercent','matchStrPercent',
                                            'nameWordPercent','matchWordPercent'])
    for i in range(confirm_new.shape[0]):
        if confirm_new['nameWordPercent'].iloc[i]> 0 or confirm_new['matchWordPercent'].iloc[i] > 0:
            confirm_final = confirm_final.append(confirm_new.iloc[i], ignore_index = True)
    
    
    # append tickers 
    stocks = pd.read_csv('stocks.csv')  
    confirm_final['Ticker'] = [np.nan] * confirm_final.shape[0]
    confirm_final['Exchange'] = [np.nan] * confirm_final.shape[0]
    for i in range(confirm_final.shape[0]):
        match = confirm_final['Match'].iloc[i]
        if isinstance(match, unicode):
            match = match.encode('utf8')
        elif not isinstance(match, basestring):
            print 'name is not string!'
            break
        confirm_final['Ticker'].iloc[i] = stocks.loc[stocks['Name'] == match]['Ticker'].values[0]
        confirm_final['Exchange'].iloc[i] = stocks.loc[stocks['Name'] == match]['Exchange'].values[0]
    
    
    confirm_final['Name'] = [x.encode('utf8') for x in confirm_final['Name']]
    confirm_final['Exchange'] = [x.encode('utf8') for x in confirm_final['Exchange']]
    confirm_final['Ticker'] = [x.encode('utf8') for x in confirm_final['Ticker']]
    confirm_final.to_csv('tickers.csv', index = False)  


if __name__ == '__main__':
    main()




