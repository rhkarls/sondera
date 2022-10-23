"""
Client for SMHI Strång API
https://opendata.smhi.se/apidocs/strang/

model data and not observation, so will not use the station and dataclasses
simply return the data as either pd.Series or xarray
https://opendata.smhi.se/apidocs/strang/get_points.html <-- pandas.Series
https://opendata.smhi.se/apidocs/strang/get_multipoint.html <-- xarray (api returns the full field)

Todo:
Multipoint

"""
from typing import Union
import datetime
import pandas as pd

from ..parameters import ParametersStrang as Parameters

from .common import _make_request


class StrangClient:
    # Fixed to version 1
    _api_url = 'https://opendata-download-metanalys.smhi.se/api/category/strang1g/version/1/geotype'

    def __init__(self):
        self.Parameters = Parameters
        self._api_url_template_point = (self._api_url +
                                        '/point/lon/{longitude}'
                                        '/lat/{latitude}'
                                        '/parameter/{parameter}'
                                        '/data.json?'
                                        '?from={from}'
                                        '&to={to}'
                                        '&interval={interval}')

    def get_data_point(self,
                       parameter: Union[Parameters, int],
                       lon: float,
                       lat: float,
                       date_from: Union[pd.Timestamp, datetime.datetime, str],
                       date_to: Union[pd.Timestamp, datetime.datetime, str],
                       agg_interval: str,  # Valid values are hourly, daily and monthly.
                       ) -> pd.Series:

        if isinstance(parameter, int):
            try:
                parameter = self.Parameters(parameter)
            except ValueError as error:
                raise

        # format date string if passed time is not string
        # "UTC. For example 2020-01-02T10:00:00Z"
        # TODO support timezone, strftime now doesnt do this correctly if datetime is localized?
        # datetimeobject.isoformat() ?
        if isinstance(date_from, str):
            date_from_f = date_from
        else:
            date_from_f = date_from.strftime('%Y-%m-%dT%H:%M:%SZ')

        if isinstance(date_to, str):
            date_to_f = date_to
        else:
            date_to_f = date_to.strftime('%Y-%m-%dT%H:%M:%SZ')

        api_vars = {'parameter': parameter.value,
                    'longitude': lon,
                    'latitude': lat,
                    'from': date_from_f,
                    'to': date_to_f,
                    'interval': agg_interval}

        # Get data
        api_url = self._api_url_template_point.format(**api_vars)
        api_get_result = _make_request(api_url)

        api_df = pd.DataFrame(api_get_result.json())
        api_df['datetime'] = pd.to_datetime(api_df['date_time'])
        data_series = api_df.set_index('datetime')['value']
        data_series.name = parameter.name

        return data_series


    def get_data_multipoint(self):
        raise NotImplementedError # requires xarray heavy dependence

