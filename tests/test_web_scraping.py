import pytest
import pandas as pd
from pathlib import Path
from mortality.scrapers.kff_web_scraping import extract_state_info

TEST_DATA = [
    ["U.S.", " ", "In God We Trust"],
    ["New York", "Excelsior", "Ever Upward"],
    ["Chicago", "Urbs in Horto", "City in a Garden"],
]

VARIABLES = ["location", "motto_latin", "motto_english"]


@pytest.fixture
def abortion_df():
    file = Path(__file__).parent.parent.joinpath("data/scrape_data/abortion.csv")
    return pd.read_csv(file)


def test_abortion_data_valid(abortion_df):
    assert len(abortion_df) == 50

    state = "Kansas"
    exception = "Exceptions to Statutory Limits on Abortions"
    assert (
        abortion_df.loc[abortion_df["Location"] == state, exception].values[0]
        == "Life and physical health"
    )


def test_location_extracted():
    data = extract_state_info(TEST_DATA, VARIABLES)
    assert data[0]["location"] == "U.S."
    assert data[2]["location"] == "Chicago"


def test_motto_extracted():
    data = extract_state_info(TEST_DATA, VARIABLES)
    assert data[1]["motto_english"] == "Ever Upward"
    assert data[2]["motto_english"] == "City in a Garden"
