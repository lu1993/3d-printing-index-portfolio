# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 11:58:09 2017

@author: LuCao
"""

'''
compute the similarity between two strings
'''
def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = []
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c >= longest:
                    lcs_set = []
                    longest = c
                    lcs_set.append(S[i-c+1:i+1])
    return lcs_set


def matchName(namedata):
    
    if len(namedata) == 2:
        name = namedata[0]
        check = namedata[1]
        suspects = {name:[0,0,0,check]}
        if isinstance(check, basestring):
            if len(lcs(name,check)) > 0:
                if len(lcs(name,check)[0]) > 0:
                    suspects.update({name:[len(lcs(name,check)[0]),\
                                           1.0 * len(lcs(name,check)[0])/len(check),\
                                           1.0 * len(lcs(name,check)[0])/len(name),\
                                           check]})
    else:
        print 'Input should contain two names!'
        suspects = []
        
    return suspects


def searchName(namedata):
    
    if isinstance(namedata, dict):
        name = namedata[namedata.keys()[0]]
        match = namedata[namedata.keys()[0]]
        suspects = {name:[0,0,0,'n']}
        for check in match:
            if isinstance(check, basestring):
                if len(lcs(name,check)) > 0:
                    if len(lcs(name,check)[0]) > 0:
                        if len(lcs(name,check)[0]) > suspects[name][0]:
                            suspects.update({name:[len(lcs(name,check)[0]),\
                                                   1.0 * len(lcs(name,check)[0])/len(check),\
                                                   1.0 * len(lcs(name,check)[0])/len(name),\
                                                   check]})
    else:
        print 'Input should be a dictionary!'
        suspects = []
        
    return suspects