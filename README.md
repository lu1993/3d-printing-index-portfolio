# 3d-printing-index-portfolio

### objective: construct a tradable index portfolio to track the peformance of 3d printing related companies

Structure of code folder (3dprinting-index-construct) is as follows:

- blg-data-download
	- DataDownloader.py: download data from bloomberg 
    - DataProcess.py: process data
    - RevenueDownloader.py: download and process revenue data from bloomberg 
    - BlbReferenceData.pyc: dependency 
    - SqlUpdateLib3.pyc: dependency

- google-trend-analyze
	- GoogleTrendAnalyzer.py: process and analyze google trends

- name-ticker-match
	- NameTickerSearcher.py: use string match to match name and ticker 
    - NameTickerAnalyzer.py: use word match to match name and ticker 
    - NameTickerConfirm.py: use google search to verify the name and ticker match
    - similarity.py: functions for similarity computation

- portfolio-construct-analyze
	- PortfolioConstruction.py: construct portfolio
    - PortfolioVisualization.py: visualize result

- yahoo-finance-downlaod: download data from Yahoo Finance

- portfolio-optimization: a demo code for further portfolio optimization
