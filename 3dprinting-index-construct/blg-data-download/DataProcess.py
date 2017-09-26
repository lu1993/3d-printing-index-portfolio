# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 10:41:05 2017

@author: lcao
"""
import pandas as pd
import numpy as np
import pyodbc

def fillData(array, type_):
    if type_ == 'na':
        for i in range(len(array)):
            if (array[i] == 0 or np.isnan(array[i])):
                    array[i] = np.nan
                    
    elif type_ in ['mean','median']:
        for i in range(len(array)):
            if (array[i] == 0 or np.isnan(array[i])):
                if i == 0:
                    array[i] = np.nan
                else:
                    if np.isnan(array[(i-1)]):
                        array[i] = np.nan
                    else:
                        s = array[:i]
                        if type_ == 'mean':                          
                            array[i] = np.mean([x for x in s if not np.isnan(x)])
                        else:
                            array[i] == np.median([x for x in s if not np.isnan(x)])
                            
    elif type_ == 'sma':
        for i in range(len(array)):
            if (array[i] == 0 or np.isnan(array[i])):
                if i == 0:
                    array[i] = np.nan
                else:
                    if np.isnan(array[(i-1)]):
                        array[i] = np.nan
                    else:
                        if i < 5:
                            s = array[:i]
                        else:
                            s = array[(i-5):i]
                        array[i] = np.mean([x for x in s if not np.isnan(x)])
    return array
                        
                        
def retrieveData(conStr, query):

    cnxn = pyodbc.connect(conStr)
    cursor = cnxn.cursor()

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    cnxn.close()
    for i in range(len(data)):
        data[i]=tuple(data[i])
    data = pd.DataFrame(data, columns = columns)
    
    return data                        
    
                    
countNA = lambda x:np.sum([1.0 * np.isnan(xx) for xx in x.loc[x.first_valid_index():x.last_valid_index()]])/len(x.loc[x.first_valid_index():x.last_valid_index()])
