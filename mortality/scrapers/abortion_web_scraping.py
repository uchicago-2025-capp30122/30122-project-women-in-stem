import json
import csv
import pathlib
import httpx
import lxml.html
from mortality.utils import STATE_ABBREVIATIONS

BASE_DIR = pathlib.Path(__file__).parent.parent.parent


def run_abortion_policy_scraper():
    """
    This function runs web scraping for an abortion policy webpage.
    """
    url = "https://www.kff.org/womens-health-policy/state-indicator/gestational-limit-abortions/?currentTimeframe=0&selectedRows=%7B%22states%22:%7B%22all%22:%7B%7D%7D,%22wrapups%22:%7B%22united-states%22:%7B%7D%7D%7D&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D"
    html = httpx.get(url)
    html.raise_for_status()
    root = lxml.html.fromstring(html.text)

    # Extract where the data is from the json text
    rawdata = root.cssselect('#content script[type="text/javascript"]')[0].text

    # Delete unnecessary characters so that the json can be loaded into a dict
    rawdata_clean = rawdata[57 : len(rawdata) - 3]
    rawdata_dict = json.loads(rawdata_clean)
    # Extract the data, which is a list of lists 
    rawdata_list = rawdata_dict["gdocsObject"]

    state_data = []

    # In this for loop, state_info is a list with the state name at the 0 index,
    # and other information in the subsequent indexes.
    for state_info in rawdata_list[0][1]:
        if (
            state_info[0] == "District of Columbia"
            or state_info[0] == "United States"
            or state_info[0] == ""
        ):
            continue

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

        if state in STATE_ABBREVIATIONS:
            abbrev = STATE_ABBREVIATIONS[state]

        state_data.append(
            {
                "Location": state,
                "Abbreviation": abbrev,
                "Statutory Limit on Abortions": limit,
                "Exceptions to Statutory Limits on Abortions": exception,
                "Legal Standard for Health/Life Exception": legal,
            }
        )

    field_names = [
        "Location",
        "Abbreviation",
        "Statutory Limit on Abortions",
        "Exceptions to Statutory Limits on Abortions",
        "Legal Standard for Health/Life Exception",
    ]

    # Write the list of dictionaries to a csv
    with open(BASE_DIR / "data/scrape_data/abortion.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(state_data[:])


run_abortion_policy_scraper()
