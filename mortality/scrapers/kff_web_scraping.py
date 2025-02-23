import sys
import re
import json
import csv
import pathlib
import httpx
import lxml.html

BASE_DIR = pathlib.Path(__file__).parent.parent

# Data Source #2: Women's Demographics
# https://www.kff.org/interactive/womens-health-profiles/alabama/demographics/

# for this, we had to go into the network tab and search through the requests made in order to find the data of interest


### Demographics

# race distribution
# https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Race%20Distribution

# age distribution
# https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Age%20distribution

# fpl distribution
# https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=FPL%20distribution

# median weekly earnings
# https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Median%20Weekly%20Earnings

def get_json_from_html(url: str) -> dict:
    json_html = httpx.get(url).text

    json_dict = json.loads(json_html)

    return json_dict

race_dict = get_json_from_html("https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Race%20Distribution")

age_dict = get_json_from_html("https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Age%20distribution")

fpl_dict = get_json_from_html("https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=FPL%20distribution")

earnings_dict = get_json_from_html("https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Median%20Weekly%20Earnings")

##### RACE
race_data = []

for state_info in race_dict['data'][2:]:
    state, total, white, black, hispanic, asian, nhopi, aian, other = state_info

    race_data.append({'state': state, 'total': total, 'white': white, 'black': black, 'hispanic': hispanic, 'asian': asian, 'nhopi': nhopi, 'aian': aian, 'other': other})

race_field_names = ['state', 'total', 'white', 'black', 'hispanic', 'asian', 'nhopi', 'aian', 'other']

with open(BASE_DIR / '../data/scrape_data/race.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = race_field_names) 
    writer.writeheader()
    writer.writerows(race_data)

##### AGE
age_data = []

for state_info in age_dict['data'][2:]:
    state, total, age19_25, age26_34, age35_54, age55_64 = state_info

    age_data.append({'state': state, 'total': total, 'age19_25': age19_25, 'age26_34': age26_34, 'age35_54': age35_54, 'age55_64': age55_64})

age_field_names = ['state', 'total', 'age19_25', 'age26_34', 'age35_54', 'age55_64']

with open(BASE_DIR / '../data/scrape_data/age.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = age_field_names) 
    writer.writeheader()
    writer.writerows(age_data)

##### FPL
fpl_data = []

for state_info in fpl_dict['data'][2:]:
    state, total, fplless_100, fpl100_199, fpl200_399, fplmore_400 = state_info

    fpl_data.append({'state': state, 'total': total, 'fplless_100': fplless_100, 'fpl100_199': fpl100_199, 'fpl200_399': fpl200_399, 'fplmore_400': fplmore_400})

poverty_field_names = ['state', 'total', 'fplless_100', 'fpl100_199', 'fpl200_399', 'fplmore_400']

with open(BASE_DIR / '../data/scrape_data/poverty.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = poverty_field_names) 
    writer.writeheader()
    writer.writerows(fpl_data)

##### Median Weekly Earnings
earnings_data = []

for state_info in earnings_dict['data'][2:]:
    state, women_weekly, men_weekly, ratio = state_info

    earnings_data.append({'state': state, 'women_weekly': women_weekly, 'men_weekly': men_weekly, 'ratio': ratio})

earnings_field_names = ['state', 'women_weekly', 'men_weekly', 'ratio']

with open(BASE_DIR / '../data/scrape_data/earnings.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = earnings_field_names) 
    writer.writeheader()
    writer.writerows(earnings_data)
