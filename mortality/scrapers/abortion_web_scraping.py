import re
import json
import csv
import pathlib
import httpx
import lxml.html

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

# https://www.kff.org/womens-health-policy/state-indicator/gestational-limit-abortions/?currentTimeframe=0&selectedRows=%7B%22states%22:%7B%22all%22:%7B%7D%7D,%22wrapups%22:%7B%22united-states%22:%7B%7D%7D%7D&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D

# Data is on line 580

# div id="content" class="inner is-single-post"
# script type="text/javascript"

# 577 si where the div starts, 668 is where this div ends

# Look in gdocsObject

url = "https://www.kff.org/womens-health-policy/state-indicator/gestational-limit-abortions/?currentTimeframe=0&selectedRows=%7B%22states%22:%7B%22all%22:%7B%7D%7D,%22wrapups%22:%7B%22united-states%22:%7B%7D%7D%7D&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D"
html = httpx.get(url)
html.raise_for_status()
root = lxml.html.fromstring(html.text)

rawdata_json = root.cssselect('#content script[type="text/javascript"]')[0].text

#to_delete = r"	var appJs = appJs || {};    appJs = jQuery.extend(appJs, " #59
#rawdata_json_clean = re.sub(to_delete, "", rawdata_json[:len(rawdata_json)-3])
rawdata_json_clean =  rawdata_json[57:len(rawdata_json)-3]

rawdata_dict = json.loads(rawdata_json_clean)

rawdata_list = rawdata_dict["gdocsObject"]

state_data = []

for state_info in rawdata_list[0][1]:
    state = state_info[0]

    if len(state_info) < 2:
        limit = "NA"
        exception = "NA"
        legal = "NA"
    elif len(state_info) < 4:
        exception = "NA"
        legal = "NA"
    else:
        limit = state_info[1]
        exception = state_info[2]
        legal = state_info[3]

    state_data.append({'Location': state,
                       'Statutory Limit on Abortions': limit,
                       'Exceptions to Statutory Limits on Abortions': exception,
                       'Legal Standard for Health/Life Exception': legal})

field_names = ['Location', 'Statutory Limit on Abortions', 'Exceptions to Statutory Limits on Abortions', 'Legal Standard for Health/Life Exception']

with open(BASE_DIR / 'data/scrape_data/abortion.csv', 'w') as file: 
    writer = csv.DictWriter(file, fieldnames = field_names) 
    writer.writeheader()
    writer.writerows(state_data[3:])
