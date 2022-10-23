import pandas as pd
import pytest

from sondera.clients.smhi import ParametersStrang
from sondera.clients.smhi import StrangClient


@pytest.fixture(scope="module")
def api_client():
    return StrangClient()

# Test valid inputs for all parameters
@pytest.mark.parametrize("parameter", [
    (116),
    (117),
    (118),
    (120),
    (122),
    (122),
])
def test_point_valid(api_client, parameter):
    longitude = 16.158
    latitude = 58.5812
    date_from = '2022-06-01 01:00'
    date_to = '2022-06-02 21:00'
    agg_interval = 'hourly'
    api_data = api_client.get_data_point(parameter=parameter,
                                         lon=longitude,
                                         lat=latitude,
                                         date_from=date_from,
                                         date_to=date_to,
                                         agg_interval=agg_interval)

    assert len(api_data) > 0


def test_point_datetime():
    pass


def test_point_pd_timestamp():
    pass


def test_point_tz():
    pass
