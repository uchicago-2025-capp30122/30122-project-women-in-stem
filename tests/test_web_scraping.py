import pytest
import pandas as pd
from pathlib import Path
from mortality.scrapers.kff_web_scraping import extract_state_info

TEST_DATA = [["U.S.", " ", "In God We Trust"],
             ["New York", "Excelsior", "Ever Upward"],
             ["Chicago", "Urbs in Horto", "City in a Garden"]]

VARIABLES = ["location", "motto_latin", "motto_english"]

@pytest.fixture
def test_location_extracted(TEST_DATA):
    data = extract_state_info(TEST_DATA, VARIABLES)
    assert data[0]["location"] == "U.S."
    assert data[2]["location"] == "Chicago"

def test_motto_extracted(TEST_DATA):
    data = extract_state_info(TEST_DATA, VARIABLES)
    assert data[1]["motto_english"] == "Ever Upward"
    assert data[2]["motto_english"] == "City in a Garden"

def abortion_df():
    file = Path(__file__).parent.parent.joinpath("data/scrape_data/abortion.csv")
    return pd.read_csv(file)

def test_abortion_data_valid(abortion_df):
    assert len(abortion_df) == 51

    for row in abortion_df.iterrows():
        assert len(row) == 4
