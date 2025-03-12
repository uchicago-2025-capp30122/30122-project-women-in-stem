import pytest
import pandas as pd
from pathlib import Path
from mortality.utils import STATE_ABBREVIATIONS
import mortality.kff_merger


@pytest.fixture
def merged_kff_df():
    """Fixture for loading the merged data frame."""
    file = Path(__file__).parent.parent.joinpath("data/merged_kff.csv")
    merged_kff = pd.read_csv(file)
    return merged_kff


def test_data_loading():
    """Test if scraped data files are loading correctly, and not empty."""
    maternal_mortality = pd.read_csv(mortality.kff_merger.maternal_mortality_path)
    coverage = pd.read_csv(mortality.kff_merger.coverage_path)
    earnings = pd.read_csv(mortality.kff_merger.earnings_path)
    cesarean = pd.read_csv(mortality.kff_merger.cesarean_path)

    assert not maternal_mortality.empty
    assert not coverage.empty
    assert not earnings.empty
    assert not cesarean.empty


def test_data_merging(merged_kff_df):
    """Test that the data was merged correctly, and there aren't any missing
    columns missing."""
    assert "state" in merged_kff_df.columns
    assert "mortality" in merged_kff_df.columns
    assert "uninsured" in merged_kff_df.columns
    assert "women_earnings" in merged_kff_df.columns
    assert "ratio_earnings" in merged_kff_df.columns
    assert "cesarean" in merged_kff_df.columns
    assert "abbrev" in merged_kff_df.columns
