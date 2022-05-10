"""
Test:
Getting obs based on integer parameter id and all periods
Getting obs based on parameter enum
Getting csv data correctly parsed (test all parameters)
"""
import pandas as pd
import pytest

from sondera.clients.smhi import ParametersHydroObs
from sondera.clients.smhi import HydroObsClient

@pytest.fixture(scope="module")
def api_client():
    return HydroObsClient()

@pytest.mark.parametrize("parameter, period", [
    (1, 'corrected-archive'),
    (ParametersHydroObs.Discharge, 'corrected-archive'),
    (1, 'latest-day'),
    (ParametersHydroObs.Discharge, 'latest-day'),
])
def test_get_observations(api_client, parameter, period):
    api_data = api_client.get_observations(parameter, 2357, period)
    assert len(api_data.data) > 0

    assert pd.api.types.is_numeric_dtype(api_data.data)
    assert pd.api.types.is_datetime64_dtype(api_data.data.index)

    assert not api_data.data.index.duplicated().any()
    assert api_data.data.index.is_monotonic_increasing

# test that csv pattern parsing works on api data
@pytest.mark.parametrize("parameter, station", [
    (1, 2357)
])
def test_csv_patterns(api_client, parameter, station):
    period = 'corrected-archive'
    api_data = api_client.get_observations(parameter, station, period)
    assert len(api_data.data) > 0

