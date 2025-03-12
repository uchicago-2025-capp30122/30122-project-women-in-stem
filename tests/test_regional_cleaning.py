import csv
from pathlib import Path
import pandas as pd
import pytest
import mortality.regional_clean


@pytest.fixture
def regional_clean_df():
    """To load the cleaned regional mortality dataset."""
    file = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
    mortality_data = pd.read_csv(file)
    return mortality_data


def test_mortality_rate_validity(regional_clean_df):
    """Test that mortality_rate is a float and between 0 and 1."""
    assert regional_clean_df["mortality_rate"].dtype in [float, "float64"]
    assert regional_clean_df["mortality_rate"].between(0, 1).all()


def test_no_invalid_characters_in_education(regional_clean_df):
    """Test that the 'education' column does not contain '?' or '.'"""
    assert not regional_clean_df["education"].astype(str).str.contains(r"[?.]").any()


def test_correct_row_count(regional_clean_df):
    """Test that the cleaned dataset contains exactly 120 rows.
    Number of rows ==  120 before cleaned, so we shouldnt lose or gain any new rows."""
    assert len(regional_clean_df) == 120, (
        f"Expected 120 rows, but got {len(regional_clean_df)}"
    )
