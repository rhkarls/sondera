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

from ...datatypes import DataSeries, StationType, Coordinate, Station

from ..parameters import parameter_patterns, SGULanCodes
from ..parameters import ParametersGWLevels as Parameters


class GroundwaterLevels:
    _api_url = 'https://resource.sgu.se/oppnadata/grundvatten/api/grundvattennivaer'

    def __init__(self):

        # self.Parameters = Parameters

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

        api_url_data = self._api_url_template_data.format(**api_vars)
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

        # create metadata and station data
        # TODO
        md_str = ''  # data metadata, not station

        station_name = api_data['features'][0]['properties']['stationens_namn']
        # convert coordinates to WGS84
        station_md = {}
        station_md['crs'] = api_data['crs']['properties']['name']
        station_md['coordinates'] = api_data['features'][0]['geometry']['coordinates']
        station_md['key'] = api_data['features'][0]['properties']['omrade-_och_stationsnummer']

        # station labeled active if last data is less than 30 days old
        station_md['active'] = (pd.Timestamp.today() - obs_s.index.max()).days < 30
        station_md['active_period'] = [obs_s.index.min(), obs_s.index.max()]

        # FIXME station can have key 'referensniva_for_roroverkant_m_o.h.' or
        #                            'referensniva_for_roroverkant_m.o.h.'
        # only one will be present for each station
        # Also fix below
        # TODO: can lancode be taken from kommunkod? first two characters
        # can be used to query for stations around

        ref_datum_level_key = list(
            set(['referensniva_for_roroverkant_m_o.h.', 'referensniva_for_roroverkant_m.o.h.']).intersection(
                api_data['features'][0]['properties'].keys()))[0]

        # FIXME DRY: code block repeated
        station_md['station_info'] = {
            'start_date': api_data['features'][0]['properties'].get('startdatum_for_matning', None),
            'aquifer_type': api_data['features'][0]['properties'].get('akvifertyp', None),
            'topographic_position': api_data['features'][0]['properties'].get('topografiskt_lage', None),
            'reference_datum_well_top': api_data['features'][0]['properties'].get(ref_datum_level_key,
                                                                                  None),
            'well_elev_above_ground': api_data['features'][0]['properties'].get('rorhojd_ovan_mark_m', None),
            'well_length': api_data['features'][0]['properties'].get('total_rorlangd_m', None),
            'municipality': api_data['features'][0]['properties'].get('kommunkod', None),
            'eucd_groundwater_resource': api_data['features'][0]['properties'].get('eucd_far_grundvattenforekomst',
                                                                                   None),
            'measurement_quality': api_data['features'][0]['properties'].get('nivamatningskvalitet', None)}

        station_data = self._create_data_obj(aux_df, obs_s, parameter, station_md, station_name, md_str)

        return station_data

    def get_all_data_lan(self, lan_code: Union[SGULanCodes, str]):
        # can probably share a lot with above get_station_data
        pass

    def get_station_info_lan(self, lan_code: Union[SGULanCodes, str]):
        """ Get all stations and station metadata for a given län"""

        if isinstance(lan_code, str):
            lan_code = SGULanCodes(lan_code)

        api_vars = {'lancode': lan_code.value}

        api_url_stations = self._api_url_template_stations_lan.format(**api_vars)
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

    def get_all_stations(self):
        # get station info for all lancodes
        raise NotImplementedError

    def _create_data_obj(self, aux_df, obs_s, parameter,
                         station_md, station_name, md_str):

        pos_coord = Coordinate(x=station_md['coordinates'][0],
                               y=station_md['coordinates'][1],
                               epsg_xy=station_md['crs'])
        pos_coord = pos_coord.to_wgs84()

        station_obj = Station(name=station_name,
                              id=int(station_md['key']),
                              agency='SGU',
                              position=pos_coord,
                              station_type=StationType.GWStation,
                              active_station=station_md['active'],
                              active_period=station_md['active_period'],
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
