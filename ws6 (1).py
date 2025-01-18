#%% Outline

# Schedule

# WORKSHOPS
# 1) Web scraping and API
# 2) Visualization with dash and plotly
# 3) Linear regression and K-means clustering
# 4) Decision trees and random forest

# Final project; alone or in groups of 3

# Canvas page

# Questions

#%% Inspecting HTML

# API (Application Programming Interface). API's works like a bridge between
# different platforms e.g. Facebook and Instagram. API's containts different methods,
# where the most common ones are GET (accessing a page on FB) and POST (Create a
# twitter post)
# Then we also have web scraping, which is accessing/extracting data from a webpage.
# The main diff between API vs scrape is that with web scrapeing we can only extract
# data and not change it. With API's we can sometimes change data and extract.

# Also, API's typically format the data in a certain way, while webscraping typically
# is more "raw"

# Also, webscraping is typically static

# All websites doesn't have API's, and therefore we need to learn how to extract
# data on our own, i.e. web scrapeing.


# When we do webscraping we typically use API's to gather the data, but the main
# diff is if we gather the "raw" data or if the data is formatted nicely

#%%
# "https://en.wikipedia.org/wiki/Warren_Buffett"

# API who we can use to send a get-request to get the data on a webpage.
import requests as rq

#%%
# Notice the output "Response [200]". 200 Indicates a succesful requests. 401, 404, 204 indicates
# some kind of error e.g. server not found or bad request etc.
rq.get("https://en.wikipedia.org/wiki/Warren_Buffett")
#%%
# This returns a request object
r1 = rq.get("https://en.wikipedia.org/wiki/Warren_Buffett")
#%%
# This formats into a string, i.e. all the html code as a string
print(r1.text)


#%% HyperText Markup Language
# Websites are usualyy written in HTML code, and HTML - Describes all elements 
# on a webpage. Within HTML we have different tags that encapsulates the different
# content on the webpage. For example we have a tag called <head> <\head> which
# contains the head of the webpage, within that we have another tag called title.
# We also have tags like body, which contains the main block of the data on the webpage.
# Within the body we can have loads of other tags, so there is a hierarchy within
# the html code suggesting what piece of content that belongs to what, i.e. subgroups.
# For example if we have a table, that is on element marked with tags, and within the
# table there are the data in the table which have tags such as th, td, tr

# The data within the tags is the data which we can/want to extract from the website


# BeautifulSoup turns messy html into a beautiful soup
from bs4 import BeautifulSoup as bs
# Why timeout? How long time we should wait for the server to give a response
r2 = rq.get("https://linclund.com", timeout=0.1)

# This will parse the content in a html format, just like we saw it when inspecting
# the webpage
# Parsing is in general a description of how we should translate and divide a piece
# of content. 
# Parsing: the process of analyzing a sequence of symbols to understand its structure and meaning. 
# Ex) I am great : English parser Pronoun, verb, adjective. Swedish parser: i is 
# preposition, different things so we need to tell bs which parser to use (html)
soup = bs(r2.content, 'html.parser')
print(soup)

#%%
# This formats the content in a html-maner i.e. indents and hierarchies more visible
print(soup.prettify())

#%%
print(soup.title)

#%%
# This returns all the text on the page
print(soup.get_text())

#%% 
# Href: Hyperlinks, i.e. clickable links in the webpage. They typically have the tag
# <a> </a>
# find_all searches through the html content or the soup to find all elements that 
# correspond the input of the functions. It has a few different parameters as input
# and the first input is the HTML-tag that we want to search for.
hyperlinks = soup.find_all('a')
print(len(hyperlinks))

#%%
# Financial Times Stock Exchange 100 Index, "Footsie", share index of the 100 companies 
# listed on the London Stock Exchange with the highest market capitalisation
r3 = rq.get("https://www.ig.com/en/indices/markets-indices/ftse-100")
soup = bs(r3.content, 'html.parser')
# Previously when using find_all we only used the tag as parameter, but typically
# the different elements has a class and a name aswell. So we are going to use
# this to find a specific element within all div tags.
mydivs = soup.find_all('div', {'class' : 'price-ticket__fluctuations'})
print(mydivs)
#%%
# This output is a bit messy, so we need to clean it up, i.e. remove the new lines
print(mydivs[0].text)
#%%
quote = ' '.join(mydivs[0].text.split())
print(quote)

#%% More data at once i.e. table
# Want to extract the tickers for SP500, In BPW we used request and pandas to do this,
# but in this case we will do it on our own
r4 = rq.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
soup = bs(r4.content, 'html.parser')
table = soup.find('table', {'class' : 'wikitable sortable'})
#%%
# tr:= table row, th:= table head, td:= table data




#%%
def save_sp500_tickers():
   # Request the page and create a BeautifulSoup object
   r4 = rq.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
   soup = bs(r4.content, 'html.parser')

   # Find the specific table (assuming there's only one such table, otherwise adjust)
   table = soup.find('table', {'class': 'wikitable sortable'})

   # Initialize a list to store tickers
   tickers = []

   # Iterate over each row in the table, skipping the header row
   for row in table.find_all('tr')[1:]:
       cells = row.find_all('td')
       if len(cells) > 4:  # Check that there are enough cells to avoid index errors
           ticker1 = cells[1].text.strip()  # Third column for the first company's ticker
           ticker2 = cells[3].text.strip()  # Fifth column for the second company's ticker
           if ticker1:  # Check if ticker1 is not empty
               tickers.append(ticker1)
           if ticker2:  # Check if ticker2 is not empty
               tickers.append(ticker2)

   return tickers

tickers = save_sp500_tickers()
print(tickers)

tickers = save_sp500_tickers()
#%%
import pandas as pd
import pandas_datareader as dr
import random

my_tickers = random.sample(tickers, 15)

stocks = dr.stooq.StooqDailyReader(my_tickers, '2010-01-01', '2023-05-03')
stocks = pd.DataFrame(stocks.read())['Close']
