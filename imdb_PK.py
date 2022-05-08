import pandas
import requests
from bs4 import BeautifulSoup
from random import randint

import time
import spacy
import streamlit as st
from collections import Counter
import seaborn

st.title('Analiza danych z IMDB - Paulina Kowalczyk')

movies = []
urls = range(1,1000,100)

for url in urls:
    url = requests.get(
        f"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start={url}&ref_=adv_nxt",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Referer": "https://www.imdb.com/search/title/",
            "Accept-Language": "en-US"
        }
    )
    soup = BeautifulSoup(url.text, 'html.parser')
    movie_data = soup.find_all('div', attrs = {'class': 'lister-item mode-advanced'})
   
    for i in movie_data:
        title = i.h3.a.text

        
        year = i.find('span', class_= 'lister-item-year text-muted unbold').text
        year = year[-5:-1]
        year = int(year)

        
        timee = i.find('span', class_= 'runtime').text
        timee = int(timee.split(" ")[0])

        
        rating = float(i.find('div', {"class": "inline-block ratings-imdb-rating"})["data-value"])

       
        stats = i.find("p", {"class": "sort-num_votes-visible"}).find_all("span")
        votes = stats[1]["data-value"]
        if len(stats)>2 and stats[3].text == "Gross:":
            gross = int(stats[4]["data-value"].replace(",", ""))
        else:
            gross = pandas.NA

      
        genre = i.find('span', class_= 'genre').text.strip().split(", ")

       
        people = i.find('p', {"class": ""}).text.strip()
        people = people.replace("\n", "")
        people = people.split("|")
        directors = people[0].split(":")[1].split(", ")
        stars = people[1].split(":")[1].split(", ")

        description = i.find_all('p', {"class": 'text-muted'})[-1].text.strip()

        movies.append(
            (title, year, timee, rating, votes, gross, genre, directors, stars, description)
        )

   
    time.sleep(randint(1, 5))

    movie_df = pandas.DataFrame(
    movies,
    columns=["Title", "Year", "Time", "Rating", "Votes", "Gross", "Genres", "Directors", "Stars", "Description"]
)

st.dataframe(movie_df)

