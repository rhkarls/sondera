"""
Test:
Getting obs based on integer parameter id and all periods
Getting obs based on parameter enum
Getting csv data correctly parsed (test all parameters)
"""
import pytest

from sondera.clients.smhi import ParametersMetObs
from sondera.clients.smhi import MetObsClient

@pytest.fixture(scope="module")
def api_client():
    return MetObsClient()

@pytest.mark.parametrize("parameter, period", [
    (2, 'latest-months'),
    (ParametersMetObs.TemperatureAirDay, 'latest-months'),
    (2, 'corrected-archive'),
    (2, 'corrected-archive-latest-months')
])
def test_get_observations(api_client, parameter, period):
    api_data = api_client.get_observations(parameter, 159880, period)
    assert len(api_data.data) > 0

# test that csv pattern parsing works on api data
@pytest.mark.parametrize("parameter, station", [
    (1, 159880),
    (2, 159880),
    (3, 159880),
    (4, 159880)
])
def test_csv_patterns(api_client, parameter, station):
    period = 'corrected-archive'
    api_data = api_client.get_observations(parameter, 159880, period)
    assert len(api_data.data) > 0
