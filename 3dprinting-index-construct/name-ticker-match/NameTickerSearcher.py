# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 11:58:09 2017

@author: LuCao
"""

import pandas as pd
import numpy as np
import concurrent.futures
import json
import time
import sys
sys.path.append("C:/Users/LuCao/Documents/3DPrinting/3dprinting-index-construct/name-ticker-match")
from similarity import searchName
from pkg_resources import resource_filename

companies = pd.read_csv(resource_filename('name-ticker-match.resources', 'CompanyName.csv'))
stocks = pd.read_csv(resource_filename('name-ticker-match.resources', 'stocks.csv')) 
    

def main():  
    data = {}
    start = time.time()
    namedata = {'name':np.array(companies['CompanyName']),
                'match':stocks['Name']}
    with concurrent.futures.ProcessPoolExecutor() as  executor:
        for name, suspect in zip(np.array(companies['CompanyName']),executor.map(searchName, namedata)):
            data.update(suspect)
            print suspect
    end = time.time()
    print 'hours eclapsed: ' + str(1.0 * (end-start)/3600)
            
    with open(resource_filename('name-ticker-match.resources', 'NameMatchSuspects.json'), 'w') as fp:
        json.dump(data, fp)
    fp.close()
        
            
if __name__ == '__main__':
    main()