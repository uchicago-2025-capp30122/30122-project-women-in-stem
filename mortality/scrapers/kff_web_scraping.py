"""
This file runs web scraping functions to extract data from various urls
contained within webpages from the Kaiser Family Foundation to extract health-
related data.
"""

from web_scraping_functions import get_json_from_html, extract_state_info
from data_sources import DATA_SOURCES

def run_scrapers(data_sources: dict):
    """
    This function runs the web scraping functions on the data to be scraped.

    Parameters: 
        data_sources: The dictionary that contains all of the necessary
            information needed to scrape all of the data sources.
    """
    for (url, variables, start_index, output_file) in data_sources.values():
        info_dict = get_json_from_html(url)
        extract_state_info(info_dict['data'][start_index:], variables, output_file)

run_scrapers(DATA_SOURCES)
