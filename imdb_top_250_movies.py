# import the required python modules
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# access the HTML content from the webpage
# create a BeautifulSoup object
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# extract desired data table from HTML data by inspecting the DOM
movies = soup.find("tbody", class_="lister-list").find_all("tr")

# create an empty list to store parsed data
movie_list = []
# create dictionary to store parsed data onto another list
for movie in movies:
    rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]
    title = movie.find("td", class_="titleColumn").a.text
    year = movie.find("td", class_="titleColumn").span.text.strip("()")
    rating = movie.find("td", class_="ratingColumn imdbRating").strong.text
    data = {"rank": rank, "title": title, "year": year, "rating": rating}
    movie_list.append(data)

df = pd.DataFrame(movie_list)
df.index = range(1, df.shape[0] + 1)
df.set_index("rank", inplace=True)
print(df)
df.to_csv("/Users/marshall/Downloads/imdb_top_250_movies.csv")