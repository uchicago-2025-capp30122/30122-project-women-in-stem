import pytest
from pathlib import Path
from mortality.utils import STATE_ABBREVIATIONS
from mortality.predict_model import (
    get_data,
    user_prediction
)

@pytest.fixture
def mortality_df():
    return get_data()

def test_get_data_is_binary(mortality_df):
    unique_value = mortality_df['mortality_binary'].unique()
    assert len(mortality_df['mortality_binary'].unique()) == 2
    assert 1 in unique_value
    assert 0 in unique_value

def test_user_prediction_wihtin_bound(mortality_df):
    assert user_prediction('northeast', 'white', 'unknown', '15-24') <= 1
    assert user_prediction('northeast', 'white', 'unknown', '15-24') >= 0

    assert user_prediction('south', 'asian', '8th grade or less', '35-44') <= 1
    assert user_prediction('south', 'asian', '8th grade or less', '35-44') >= 0


