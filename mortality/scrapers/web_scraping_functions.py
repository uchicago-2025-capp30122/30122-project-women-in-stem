import json
import csv
import httpx
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

def get_json_from_html(url: str) -> dict:
    """
    This function takes in a url and returns the html, when the html is a json, 
    and returns a python dictionary.

    Parameters:
        url: The url to the website that contains the json.
    
    Returns:
        A dictionary with the data contained in the json.
    """
    json_html = httpx.get(url).text

    json_dict = json.loads(json_html)

    return json_dict


def extract_state_info(raw_data: list, variables: list, output_file: str):
    """
    This function parses a list of lists containing state data and writes the
    important information to a csv. Note that the length of the variables must
    match the length of each list containing state information.

    Parameters: 
        raw_data: a list of lists containing state data.
        variables: a list of variable names, corresponding to the number of 
            fields within each row of state data.
        output_file: the path and filename to where the data should be saved.
    
    Returns:
        None, the information gets written to a file.
    """
    data = []

    for state_info in raw_data:
        row = {variable: None for variable in variables}
        for i, key in enumerate(row.keys()):
            row[key] = state_info[i]

        data.append(row)

    with open(BASE_DIR / output_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames = variables)
        writer.writeheader()
        writer.writerows(data)
