import pytest
import pandas as pd
from sondera.clients.sgu import GroundwaterLevelsClient
from sondera.clients.sgu import ParametersGWLevels
import sondera


@pytest.fixture(scope="module")
def api_client():
    return GroundwaterLevelsClient()


def test_get_all_stations_lan(api_client):
    api_data = api_client.get_all_stations_lan('03')

    assert isinstance(api_data, pd.DataFrame)
    assert api_data.size > 0


def test_get_observations(api_client):
    api_data = api_client.get_observations('101_1')

    assert isinstance(api_data, sondera.datatypes.DataSeries)
    assert len(api_data.data) > 0


@pytest.mark.parametrize("parameter", [
    ParametersGWLevels.LevelBelowGroundSurface,
    'grundvattenniva_m_under_markyta',
    ParametersGWLevels.LevelBelowWellTop,])
def test_get_observations_parameter(api_client, parameter):
    api_data = api_client.get_observations('101_1', parameter)

    assert isinstance(api_data, sondera.datatypes.DataSeries)
    assert len(api_data.data) > 0
