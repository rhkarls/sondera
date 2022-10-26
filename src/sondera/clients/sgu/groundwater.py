# -*- coding: utf-8 -*-
"""
Client for SGU groundwater levels api
https://www.sgu.se/produkter/geologiska-data/oppna-data/grundvatten-oppna-data/grundvattennivaer-tidsserier/

"""
from typing import Union

import pandas as pd
import requests

from ...datatypes import DataSeries, StationType, Coordinate, Station

from ..parameters import SGULanCodes
from ..parameters import ParametersGWLevels as Parameters


class GroundwaterLevelsClient:
    _api_url = 'https://resource.sgu.se/oppnadata/grundvatten/api/grundvattennivaer'
    _api_url_v1 = 'https://resource.sgu.se/oppnadata/grundvatten/grundvattennivaer'

    def __init__(self):
        self.Parameters = Parameters
        # Returns all observations for a station-id
        self._api_url_template_data = (self._api_url +
                                       '/nivaer/station'
                                       '/{station}?format=json')

        # Returns all observations for all stations in a specified län
        self._api_url_template_data_lan = (self._api_url_v1 +
                                           '/nivaer/v1/lan/{lancode}'
                                           '?format=json')

        # List of stations available for each län
        self._api_url_template_stations_lan = (self._api_url +
                                               '/stationer'
                                               '/{lancode}?format=json')

        # self.api_params_dict = self.get_api_parameters(print_params=False)

    def get_observations(self,
                         station_code: str,
                         parameter: Parameters = Parameters.LevelBelowGroundSurface) -> DataSeries:
        """ Get data for a given station / groundwater well
        Returns data for groundwater level below ground surface (parameter LevelBelowGroundSurface) 
        by default.
        
        For station codes also see functions get_all_stations_lan() and get_all_stations().
        
        Parameters
        ----------
        station_code : str
            SGU station code
        parameter : str or ParametersGWLevels Enum.
            valid Enum and string options are
            ParametersGWLevels.LevelBelowWellTop : 'grundvattenniva_cm_u._roroverkant'
            ParametersGWLevels.LevelAboveSeaLevel : 'grundvattenniva_m_o.h.'
            ParametersGWLevels.LevelBelowGroundSurface : 'grundvattenniva_m_under_markyta'

            Note that  groundwater level above sea level is returned with an unknown vertical datum,
            official documentation states "usually RH70".

        Returns
        -------
        A DataSeries object with observations and station metadata
        
        Notes
        -----
        https://www.sgu.se/produkter/geologiska-data/oppna-data/grundvatten-oppna-data/grundvattennivaer-tidsserier/

        https://resource.sgu.se/dokument/produkter/oppnadata/grundvattennivaer-tidsserier-oppnadata-beskrivning.pdf
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
        aux_df = data_df[list(set(data_df.keys()) - {swe_par_key})]

        # create metadata and station data
        # TODO
        md_str = ''  # data metadata, not station

        station_name = api_data['features'][0]['properties']['stationens_namn']
        # convert coordinates to WGS84
        station_md = {'crs': api_data['crs']['properties']['name'],
                      'coordinates': api_data['features'][0]['geometry']['coordinates'],
                      'key': api_data['features'][0]['properties']['omrade-_och_stationsnummer'],
                      'active': (pd.Timestamp.today() - obs_s.index.max()).days < 90,
                      'active_period': [obs_s.index.min(), obs_s.index.max()]}

        # TODO: can lancode be taken from kommunkod? first two characters
        # can be used to query for stations nearby

        api_data_s = api_data['features'][0]
        station_md = self._add_station_info(api_data_s, station_md)

        return self._create_data_obj(aux_df, obs_s, parameter,
                                     station_md, station_name, md_str)

    def get_observations_lan(self, lan_code: Union[SGULanCodes, str]):
        # can probably share a lot with above get_station_data
        raise NotImplementedError

    def list_sgu_lan_codes(self):
        """ Prints the SGU Län codes """
        for e in SGULanCodes: print(f"{e.name}: {e.value}")

    def get_all_stations_lan(self, lan_code: Union[SGULanCodes, str]):
        """ Get all stations and station metadata for a given län. See Enum SGULanCodes or list_sgu_lan_codes()
        for list of län codes, alternatively the official documentation of the SGU API (links below).

        Notes
        -----
        https://www.sgu.se/produkter/geologiska-data/oppna-data/grundvatten-oppna-data/grundvattennivaer-tidsserier/

        https://resource.sgu.se/dokument/produkter/oppnadata/grundvattennivaer-tidsserier-oppnadata-beskrivning.pdf
        """
        # TODO return as dataframe and/or dict of Station objects?
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
                   'code': s['properties'].get('omrade-_och_stationsnummer', None), }

            station_info = {}
            station_info = self._add_station_info(s, station_info)
            # FIXME Future. 3.9 merge dicts with |
            s_d = {**s_d, **station_info['station_info']}

            stations_df = pd.concat([stations_df, pd.Series(s_d, name=s_d['code'])], axis=1)

        return stations_df

    def get_all_stations(self):
        # get station info for all lancodes
        raise NotImplementedError

    def _add_station_info(self, api_data_s, station_md):
        """ Add 'station_info' key with additional station metadata to dict """

        # station can have key 'referensniva_for_roroverkant_m_o.h.' or
        #                      'referensniva_for_roroverkant_m.o.h.'
        # for datum level.
        # only one will be present for each station, sometimes none
        try:
            ref_datum_level_key = list({'referensniva_for_roroverkant_m_o.h.', 'referensniva_for_roroverkant_m.o.h.'}
                                       .intersection(api_data_s['properties'].keys()))[0]
        except IndexError:
            ref_datum_level_key = None

        station_md['station_info'] = {
            'start_date': api_data_s['properties'].get('startdatum_for_matning', None),
            'soil_type': api_data_s['properties'].get('jordart', None),
            'aquifer_type': api_data_s['properties'].get('akvifertyp', None),
            'topographic_position': api_data_s['properties'].get('topografiskt_lage', None),
            'reference_datum_well_top': api_data_s['properties'].get(ref_datum_level_key,
                                                                     None),
            'well_elev_above_ground': api_data_s['properties'].get('rorhojd_ovan_mark_m', None),
            'well_length': api_data_s['properties'].get('total_rorlangd_m', None),
            'municipality': api_data_s['properties'].get('kommunkod', None),
            'eucd_groundwater_resource': api_data_s['properties'].get('eucd_far_grundvattenforekomst',
                                                                      None),
            'measurement_quality': api_data_s['properties'].get('nivamatningskvalitet', None)}

        return station_md

    def _create_data_obj(self, aux_df, obs_s, parameter,
                         station_md, station_name, md_str):
        # sourcery skip: inline-immediately-returned-variable

        if isinstance(parameter, str):
            try:
                parameter = self.Parameters(parameter)
            except ValueError as error:
                raise

        # TODO Z coordinate possible to get from 'station_info' and
        # 'reference_datum_well_top' - 'well_elev_above_ground'
        # Problem is unknown vertical datum, official documentation says "usually RH70"
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
                              last_updated=obs_s.index.max(),
                              station_info=station_md.get('station_info', None))

        data_obj = DataSeries(station=station_obj,
                              data=obs_s,
                              aux_data=aux_df,
                              parameter=parameter,
                              metadata=md_str,
                              start_date=obs_s.index.min(),
                              end_date=obs_s.index.max())

        return data_obj
