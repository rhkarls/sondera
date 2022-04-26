# -*- coding: utf-8 -*-
"""
Client for SGU groundwater levels api
https://www.sgu.se/produkter/geologiska-data/oppna-data/grundvatten-oppna-data/grundvattennivaer-tidsserier/

"""

import collections
from enum import Enum
from io import StringIO
import datetime as dt
from typing import Union

import pandas as pd
import requests

from ...datatypes import DataSeries, StationType, Coordinate

from ..parameters import parameter_patterns, SGULanCodes
from ..parameters import ParametersGWLevels as Parameters


class GroundwaterLevels:
    _api_url = 'https://resource.sgu.se/oppnadata/grundvatten/api/grundvattennivaer'

    def __init__(self):

        #self.Parameters = Parameters

        self._api_url_template_data = (self._api_url +
                                       '/nivaer/station'
                                       '/{station}?format=json')

        self._api_url_template_data_lan = (self._api_url +
                                           '/nivaer/lan'
                                           '/{lancode}?format=json')

        self._api_url_template_stations_lan = (self._api_url +
                                               '/stationer'
                                               '/{lancode}?format=json')

        # self.api_params_dict = self.get_api_parameters(print_params=False)

    def get_station_data(self,
                         station_code: str,
                         parameter: Parameters = Parameters.LevelBelowGroundSurface):
        """ Get data for a given station / groundwater well
        Returns data for LevelBelowGroundSurface if not provided
        """

        api_vars = {'station': station_code}

        api_url_data = self._api_url_template_data.format(api_vars)
        api_get_data = requests.get(api_url_data)
        api_data = api_get_data.json()
        data_json = api_data['features'][0]['properties']['Mätningar']

        data_df = pd.DataFrame(data_json)

        data_df['timestamp'] = pd.to_datetime(data_df['datum_for_matning'])
        data_df = data_df.drop('datum_for_matning', axis=1)
        data_df = data_df.set_index('timestamp')

        swe_par_key = parameter.value
        obs_s = data_df[swe_par_key].copy()
        obs_s.name = parameter.name
        aux_df = data_df[set(data_df.keys()) - {swe_par_key}]

        # create metadata

        # convert coordinates to WGS84



    def get_all_data_lan(self, lan_code: Union[SGULanCodes, str]):
        # can probably share a lot with above get_station_data
        pass

    def get_station_info_lan(self, lan_code: Union[SGULanCodes, str]):
        """ Get all stations and station metadata for a given län"""

        if isinstance(lan_code, str):
            lan_code = SGULanCodes(lan_code)

        api_vars = {'lancode': lan_code.value}

        api_url_stations = self._api_url_template_stations_lan.format(api_vars)
        api_get_stations = requests.get(api_url_stations)
        stations = api_get_stations.json()

        stations_df = pd.DataFrame()
        for s in stations['features']:
            try:
                s_x = s.get('geometry', {}).get('coordinates', [None, None])[1]
                s_y = s.get('geometry', {}).get('coordinates', [None, None])[0]
            except AttributeError:
                s_x = None
                s_y = None

            s_d = {'X': s_x,
                   'Y': s_y,
                   'code': s['properties'].get('omrade-_och_stationsnummer', None),
                   'name': s['properties'].get('stationens_namn', None),
                   'start_date': s['properties'].get('startdatum_for_matning', None),
                   'aquifer_type': s['properties'].get('akvifertyp', None),
                   'topographic_position': s['properties'].get('topografiskt_lage', None),
                   'reference_datum_well_top': s['properties'].get('referensniva_for_roroverkant_m.o.h.', None),
                   'well_elev_above_ground': s['properties'].get('rorhojd_ovan_mark_m', None),
                   'well_length': s['properties'].get('total_rorlangd_m', None),
                   'municipality': s['properties'].get('kommunkod', None),
                   'eucd_groundwater_resource': s['properties'].get('eucd_far_grundvattenforekomst', None),
                   'measurement_quality': s['properties'].get('nivamatningskvalitet', None)
                   }
            stations_df = stations_df.append(pd.Series(s_d, name=s_d['code']))

        return stations_df
