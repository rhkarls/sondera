# -*- coding: utf-8 -*-
"""
Client for SMHI hydroobs open-data api
Inherits from metobs
"""
# All dates in the JSON answers are in Unix time stamp. Timezone UTC  # FIXME
# Allow for returning data in different timezone ?

import datetime as dt

import pandas as pd

from ..parameters import ParametersHydroObs as Parameters
from .metobs import MetObsClient
from ...datatypes import Coordinate, DataSeries, StationType, Station


class HydroObsClient(MetObsClient):
    _api_url = 'https://opendata-download-hydroobs.smhi.se/api/version/1.0'

    def __init__(self):
        super().__init__()
        self.Parameters = Parameters

    def _create_data_obj(self, aux_df, obs_s, parameter,
                         station_md, station_name, md_str):
        pos_coord = Coordinate(y=station_md['latitude'],
                               x=station_md['longitude'],
                               epsg_xy=4326)

        station_obj = Station(name=station_name,
                              id=int(station_md['key']),
                              agency=station_md.get('owner', 'SMHI'),
                              position=pos_coord,
                              station_type=StationType.HydroStation,
                              active_station=station_md['active'],
                              active_period=[pd.to_datetime(station_md['from'], unit='ms',
                                                            origin='unix'),
                                             pd.to_datetime(station_md['to'], unit='ms',
                                                            origin='unix')],
                              last_updated=None,
                              station_info={})

        data_obj = DataSeries(station=station_obj,
                              data=obs_s,
                              aux_data=aux_df,
                              parameter=parameter,
                              metadata=md_str,
                              start_date=obs_s.index.min(),
                              end_date=obs_s.index.max())

        return data_obj
