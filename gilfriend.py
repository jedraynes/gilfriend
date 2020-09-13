#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:31:24 2020

@author: jedraynes
"""
# sources

# IMDb
## https://www.imdb.com/title/tt0238784/episodes?season=1

# IMDb scraping code
## https://towardsdatascience.com/scraping-tv-show-epsiode-imdb-ratings-using-python-beautifulsoup-7a9e09c4fbe5


# import packages and set up imdb access
import pandas as pd
from bs4 import BeautifulSoup
from  requests import get
import sys

# source code per link above as edited for this use case
def main():
    gg_episodes = []
    
    for season in range(1, 8):
        response = get('https://www.imdb.com/title/tt0238784/episodes?season=' + str(season))
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        episode_containers = soup.find_all('div', class_ = 'info')
        for episode in episode_containers:
            
            season_number = season
            episode_number = episode.meta['content']
            title = episode.a['title']
            airdate = episode.find('div', class_='airdate').text.strip()
            rating = episode.find('span', class_ = 'ipl-rating-star__rating').text
            
            episode_data = [season_number, episode_number, title, airdate, rating]
            
            gg_episodes.append(episode_data)
        
    # making the dataframe
    gg_episodes = pd.DataFrame(gg_episodes, columns = ['season_number', 'episode_number', 'title', 'airdate', 'rating'])
    
    # data wrangling
    gg_episodes['rating'] = gg_episodes.rating.astype('float')
    gg_episodes['airdate'] = pd.to_datetime(gg_episodes.airdate)
    
    # save as csv
    path = '/Users/jedraynes/Documents/Python/Gilfriend/'
    confirm = input('Confirm? y/n: ')
    if confirm == 'y':
        print('Saving as csv...')
        gg_episodes.to_csv(path + 'gilmore_girls.csv', index = False)
        print('...done!')
    else:
        print('Script canceled. Exiting...')
        sys.exit()
    return

# run script
if __name__ == '__main__':
    main()