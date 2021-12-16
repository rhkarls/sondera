# -*- coding: utf-8 -*-
"""
Client for SMHI hydroobs open-data api
Inherits from metobs
"""
# All dates in the JSON answers are in Unix time stamp. Timezone UTC  # FIXME
# Allow for returning data in different timezone

import datetime as dt

from .parameters import ParametersHydroObs as Parameters
from .smhimetobs import ClientSMHIMetObs
from ..datatypes import Coordinate, SonderaData, StationType


class ClientSMHIHydroObs(ClientSMHIMetObs):
    _api_url = 'https://opendata-download-hydroobs.smhi.se/api/version/1.0'

    def __init__(self):
        super().__init__()
        self.Parameters = Parameters

    def _create_data_obj(self, aux_df, obs_s, parameter, station_md, station_name, md_str):
        """ Create SonderaData object with HydroObs data"""
        from_date = dt.datetime.utcfromtimestamp(station_md['from'] / 1000)
        to_date = dt.datetime.utcfromtimestamp(station_md['to'] / 1000)

        pos_coord = Coordinate(y=station_md.get('latitude'),
                               x=station_md.get('longitude'),
                               z=station_md.get('height', None),
                               epsg=4326)

        station_data = SonderaData(name=station_name,
                                   position=pos_coord,
                                   station_type=StationType.HydroStation,
                                   data=obs_s,
                                   aux_data=aux_df,
                                   parameter=parameter,
                                   metadata=md_str,
                                   active_station=station_md['active'],
                                   start_date=from_date,
                                   end_date=to_date)
        return station_data
