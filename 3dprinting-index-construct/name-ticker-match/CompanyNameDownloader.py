# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:26:26 2017

@author: lcao
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd
from pkg_resources import resource_filename


def striphtml(data):
    comp = re.compile(r'<.*?>')
    return comp.sub('', data)
    

def main():
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
    
    companies = [striphtml(str(x)) for x in company] 
    pd.DataFrame({'Name':companies}).to_csv(resource_filename('name-ticker-match.resources', 'CompanyName.csv'), index = False)
    
  
if __name__ == '__main__':
    main()