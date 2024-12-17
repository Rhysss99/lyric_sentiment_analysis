import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

csv_file = 'king_gizzard_discography.csv'

if os.path.exists(csv_file):
    print("Loading data from existing CSV file...")
    df = pd.read_csv(csv_file, index_col=0)  
else:
    print("No CSV found. Running scraper...")
    

    url = "https://en.wikipedia.org/wiki/List_of_songs_recorded_by_King_Gizzard_%26_the_Lizard_Wizard"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        exit()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    if not table:
        print("Failed to find the table with the specified class.")
        exit()
    
    rows = table.find('tbody').find_all('tr')
    titles, years, albums, lengths = [], [], [], []

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 4:
            titles.append(cols[0].text.strip())
            years.append(cols[1].text.strip())
            albums.append(cols[2].text.strip())
            lengths.append(cols[3].text.strip())
        time.sleep(random.uniform(0.5, 1.5))

    data = {'Title': titles, 'Year': years, 'Album': albums, 'Length': lengths}
    df = pd.DataFrame(data)
    
    df.to_csv(csv_file, index=True)
    print("Data saved to king_gizzard_discography.csv")

print(df)
