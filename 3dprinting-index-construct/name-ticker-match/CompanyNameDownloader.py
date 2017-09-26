# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:26:26 2017

@author: lcao
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import pyodbc as p
from datetime import datetime
import os
os.chdir('D:/Strategy/QuickCheck/SplitAnnouncement')




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# get companies from 3dprintingbusiness
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
companies = []
home_url = "https://www.3dprintingbusiness.directory/companies/"
for k in np.arange(1,186,1):
    if k == 1:
        url = home_url
    else:
        url = home_url + "page/" + str(k) + "/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    company = soup.find_all('div', class_='listing-title')
    companies.append(company)
    
def striphtml(data):
    comp = re.compile(r'<.*?>')
    return comp.sub('', data)

companies = [striphtml(str(x)) for x in company] 