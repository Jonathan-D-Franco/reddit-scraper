# Write you web scraping code here.

# importing all the packages need including time which will allow me to gather more data
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# standard url along with a header for a user agent as a machine running macOs on safari, this is to prevent Reddit from thinking im a bot
url = 'https://old.reddit.com/r/leagueoflegends/'
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
response = requests.get(url, headers=headers)

# create the soup magic
soup = BeautifulSoup(response.content, 'html.parser')

# attributes so that I can find my way to the posts
attributes = {'class': 'thing', 'data-domain': 'self.leagueoflegends'}
posts = soup.find_all('div', attrs=attributes)
# empty lists to use for my csv/ data frame
title = []
timedisp = []
author = []
upvotes = []
comments = []
links = []
# useful tool to keep track of how many data points I have
row = 1
# this loops through the pages of reddit checking how many data points i have
while (row <= 99):
    for post in posts:
        # each on of these just navigates the html to find the correct item and appends it
        title.append(post.find('a', class_="title").text)
        author.append(post.find('a', class_='author').text)
        # there are special cases for these two because sometimes the html returns more than what we want
        timedisp_temp = post.find('p', class_="tagline").text
        upvotes_temp = post.find('div', attrs={'class':'score likes'}).text
        comments_temp = post.find('a', class_='comments').text.split()[0]
        links.append("https://old.reddit.com" + post.find('a', class_="title").get('href'))
        if timedisp_temp.split()[1] == 'months':
            timedisp = timedisp_temp.split()[0]*30*24
        elif timedisp_temp.split()[1] == 'days':
            timedisp = timedisp_temp.split()[0]*24
        elif timedisp_temp.split()[1] == 'hours':
            timedisp = timedisp_temp.split()[0]
        # is returned when there has been no down vote or upvote on a post
        if upvotes_temp == '•':
            upvotes_temp = 0
        # just want the number of comments 
        if comments_temp == 'comment':
            comments_temp = 0
        upvotes.append(upvotes_temp)
        comments.append(comments_temp)
        timedisp.append(timedisp)
        row += 1
    # used to pull the link to the next page on the site
    next = soup.find('span', class_='next-button')
    next_page = next.find('a').attrs['href']
    # stop reddit from thinking im a bot by instantly going to the next page
    time.sleep(2)
    # replace the old link with the next page i just went to
    response = requests.get(next_page, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    posts = soup.find_all('div', attrs=attributes)

# creating the data frame
categories = ['title', 'author', 'upvotes', 'comments', 'links', 'timedisp']
df = pd.DataFrame(columns=categories)
df = pd.DataFrame({'title':pd.Series(title), 'author':pd.Series(author), 'upvotes':pd.Series(upvotes), 'comments':pd.Series(comments), 'links':pd.Series(links), 'timedisp':pd.Series(timedisp)})
# creating the csv from the df into my data folder
df.to_csv('polyglot-BeepingJohnson\R\App\data\data.csv')
