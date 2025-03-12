import json
import csv
import httpx
from pathlib import Path
from .kff_data_sources import DATA_SOURCES


BASE_DIR = Path(__file__).parent.parent.parent


def get_json_from_html(url: str) -> dict:
    """
    This function takes in a url and returns the html, when the html is a json,
    and returns a python dictionary. This function is meant to be used with the
    KFF data contained in kff_data_sources.py.

    Parameters:
        url: The url to the website that contains the json.

    Returns:
        A dictionary with the data contained in the json.
    """
    json_html = httpx.get(url).text

    json_dict = json.loads(json_html)

    return json_dict


def write_to_csv(data: dict, fieldnames: list, output_file: str):
    """
    This function writes data to a csv given a list of dictionaries and the
    fieldnames for the name of the csv.

    Parameters:
        data: a list of dictionaries for the data to be written to csv
        fieldnames: a list of the column names in the csv
        output_file: the path and filename to where the data should be saved.
    
    Returns:
        None, the information gets written to a file.
    """
    # Write the list of dictionaries to a csv
    with open(BASE_DIR / output_file, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def extract_state_info(raw_data: list, variables: list):
    """
    This function parses a list of lists containing state data and creates a 
    list of dictionaries, which will later be written to a csv. Note that the 
    length of the variables must match the length of each list containing state
    information. This function is meant to be used with the KFF data contained 
    in kff_data_sources.py.

    Parameters:
        raw_data: a list of lists containing state data.
        variables: a list of variable names, corresponding to the number of
            fields within each row of state data.

    Returns:
        None, the information gets written to a file.
    """
    data = []

    # raw_data is a list of lists, where each list is a row of data for a state.
    # In this for loop, state_info is a list with the state name at the 0 index,
    # and other information in the subsequent indexes.
    for state_info in raw_data:
        # For each state's info, write the data for each row into a dictionary
        row = {variable: None for variable in variables}
        for i, key in enumerate(row.keys()):
            row[key] = state_info[i]

        # Add dictionary with state info into data list
        data.append(row)

    return data


def run_kff_scrapers():
    """
    This function runs the web scraping functions on the data to be scraped.

    Parameters:
        data_sources: The dictionary that contains all of the necessary
            information needed to scrape all of the data sources.
    """
    # Unpack the important information for each data source to be scraped
    for url, variables, start_index, output_file in DATA_SOURCES.values():
        info = get_json_from_html(url)
        data = extract_state_info(info["data"][start_index:], variables)
        write_to_csv(data, variables, output_file)
