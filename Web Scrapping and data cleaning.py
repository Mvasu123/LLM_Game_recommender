# -*- coding: utf-8 -*-
from google_play_scraper import search
import json
import re
import csv
import os

def clean_description(text):

    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)

    text = re.sub(r'\\u[\dA-Fa-f]{4}', '', text)


    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)


    text = re.sub(r'\s+', ' ', text).strip()

    return text

count = 0
result = search(
    "favourite game",
    lang="en",
    country="us",
    n_hits=100
)


extracted_results = []


for item in result:
    title = item.get('title')
    icon = item.get('icon')
    rating = item.get('score')
    genre = item.get('genre')
    free = item.get('free')
    description = item.get('description')
    if description:
        description = clean_description(description)
    installs = item.get('installs')


    nresult = {
        'Title': title,
        'Genre': genre,
        'Free': free,
        'Rating': rating,
        'Icon': icon,
        'Description': description,
        'Installs': installs
    }


    extracted_results.append(nresult)

csv_file_name = "arcade_games.csv"


fieldnames = ['Title', 'Genre', 'Free','Rating', 'Icon', 'Description', 'Installs']


file_exists = os.path.isfile(csv_file_name)


with open(csv_file_name, mode='a', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)


    if not file_exists:
        writer.writeheader()


    for data in extracted_results:
        writer.writerow(data)

print(f"Data successfully appended to {csv_file_name}")

import pandas as pd


csv_file_name = "arcade_games.csv"


df = pd.read_csv(csv_file_name)

df_cleaned = df.drop_duplicates(subset='Title')

df_cleaned.to_csv(csv_file_name, index=False)

print(f"Duplicates removed and data cleaned in {csv_file_name}")

