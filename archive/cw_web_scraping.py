import re
import json
import csv
import pathlib
import httpx
import lxml.html
from mortality.utils import STATE_ABBREVIATIONS

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

# Maternal Mortality Data from the Commonwealth Fund
# https://www.commonwealthfund.org/publications/scorecard/2024/jul/2024-state-scorecard-womens-health-and-reproductive-care

# infogram.com embeds this URL within the page:
# https://e.infogram.com/...<ID>...?parent_url=https%3A%2F%2Fwww.commonwealthfund.org%2Fpublications%2Fscorecard%2F2024%2Fjul%2F2024-state-scorecard-womens-health-and-reproductive-care&src=embed#async_embed
# (If we need a different map, swap out the ...<ID>... portion from the divs we find on the page.)


###### ----------------> Incorrect Map

# id = 36e7002e-d5e2-45c1-9d5c-76b70a74b57a
# link = https://e.infogram.com/36e7002e-d5e2-45c1-9d5c-76b70a74b57a?parent_url=https%3A%2F%2Fwww.commonwealthfund.org%2Fpublications%2Fscorecard%2F2024%2Fjul%2F2024-state-scorecard-womens-health-and-reproductive-care&src=embed#async_embed

url = "https://e.infogram.com/36e7002e-d5e2-45c1-9d5c-76b70a74b57a?parent_url=https%3A%2F%2Fwww.commonwealthfund.org%2Fpublications%2Fscorecard%2F2024%2Fjul%2F2024-state-scorecard-womens-health-and-reproductive-care&src=embed#async_embed"
html = httpx.get(url)
html.raise_for_status()
root = lxml.html.fromstring(html.text)

rawdata_json = root.cssselect("body script")[0].text

# Need to clean json slightly because there are words/symbols at beginning and end of string that block starting { and ending }
# "window.infographicData=" at beginning of string, ";" at end of string
to_delete = r"window.infographicData="
rawdata_json_clean = re.sub(to_delete, "", rawdata_json[:len(rawdata_json)-1])

try:
    rawdata_dict = json.loads(rawdata_json_clean)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")

rawdata_list = rawdata_dict["elements"]["content"]["content"]["entities"]["55ba4d56-b27d-484a-8a48-02665e5450d34fe678da-40b9-4009-8271-f3335714f9df"]["props"]["chartData"]["data"]

state_data = []

for state_info in rawdata_list[0]:
    if state_info[0]["value"] == 'District of Columbia':
        continue
    state = state_info[0]["value"]
    deaths = state_info[2]["value"] # Deaths per 100,000 female population ages 15–44
    lower, upper = deaths.split('–')
    lat_long = state_info[3]["value"]
    lat, long = lat_long.split()

    if state in STATE_ABBREVIATIONS:
        abbrev = STATE_ABBREVIATIONS[state]

    state_data.append({'state': state, 'abbrev' : abbrev, 'deaths': deaths, 'lower': lower, 'upper': upper, 'lat_long': lat_long, 'lat': lat, 'long': long})

field_names = ['state', 'abbrev', 'deaths', 'lower', 'upper', 'lat_long', 'lat', 'long']

with open(BASE_DIR / 'data/scrape_data/cw_deaths.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = field_names) 
    writer.writeheader()
    writer.writerows(state_data)


###### ----------------> Correct Map

# id = 2b3a4805-bae1-4b51-8ccd-16f53448494d
# link = https://e.infogram.com/2b3a4805-bae1-4b51-8ccd-16f53448494d?parent_url=https%3A%2F%2Fwww.commonwealthfund.org%2Fpublications%2Fscorecard%2F2024%2Fjul%2F2024-state-scorecard-womens-health-and-reproductive-care&src=embed#async_embed

url = "https://e.infogram.com/2b3a4805-bae1-4b51-8ccd-16f53448494d?parent_url=https%3A%2F%2Fwww.commonwealthfund.org%2Fpublications%2Fscorecard%2F2024%2Fjul%2F2024-state-scorecard-womens-health-and-reproductive-care&src=embed#async_embed"
html = httpx.get(url)
html.raise_for_status()
root = lxml.html.fromstring(html.text)

rawdata_json = root.cssselect("body script")[0].text

to_delete = r"window.infographicData="
rawdata_json_clean = re.sub(to_delete, "", rawdata_json[:len(rawdata_json)-1])

try:
    rawdata_dict = json.loads(rawdata_json_clean)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")

rawdata_list = rawdata_dict["elements"]["content"]["content"]["entities"]["55ba4d56-b27d-484a-8a48-02665e5450d34fe678da-40b9-4009-8271-f3335714f9df"]["props"]["chartData"]["data"]

state_data = []

for state_info in rawdata_list[0]:
    print(state_info)
    state = state_info[0]["value"]
    print(state)
    deaths = state_info[2]["value"] # Maternal mortality rates per 100,000 live births
    print(deaths)
    if deaths == 'Data not available ':
        lower = ' '
        upper = ' '
    else:
        lower, upper = deaths.split('–')

    state_data.append({'state': state, 'deaths': deaths, 'lower': lower, 'upper': upper})

field_names = ['state', 'deaths', 'lower', 'upper']

with open(BASE_DIR / 'data/scrape_data/cw_maternal_mortality.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = field_names) 
    writer.writeheader()
    writer.writerows(state_data)
