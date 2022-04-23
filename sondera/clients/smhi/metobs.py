# -*- coding: utf-8 -*-
"""
Client for SMHI metobs open-data api
"""

import collections
from io import StringIO
# from string import Template
import datetime as dt
from typing import Union

import pandas as pd
import requests

from ...exceptions import APIError, SonderaError
from ...datatypes import SonderaData, StationType, Coordinate

from ..parameters import parameter_patterns
from ..parameters import ParametersMetObs as Parameters


class MetObsClient:
    _api_url = 'https://opendata-download-metobs.smhi.se/api/version/1.0'

    def __init__(self):

        self.Parameters = Parameters

        # self._api_url_template_data_x = Template(self._api_url +
        #                                        '/parameter/$parameter'
        #                                        '/station/$station'
        #                                        '/period/$period'
        #                                        '/data.$extension')

        self._api_url_template_data = (self._api_url +
                                       '/parameter/{parameter}'
                                       '/station/{station}'
                                       '/period/{period}'
                                       '/data.{extension}')

        # self._api_url_template_station_x = Template(self._api_url +
        #                                           '/parameter/$parameter'
        #                                           '/station/$station')

        self._api_url_template_station = (self._api_url +
                                                  '/parameter/{parameter}'
                                                  '/station/{station}')

        self.api_params_dict = self.get_api_parameters(print_params=False)

        self.get_all_stations_called=False

    def get_observations(self,
                         parameter: Union[Parameters, int],
                         station: int,
                         period: str,
                         return_tz=None) -> SonderaData:
        """
        Get observations for a given parameter, station and period
        ----------
        parameter : Enum or int
        station : int
        period : str
            latest-hour, latest-day, latest-months or corrected-archive as
            supported directly by the SMHI api.
            In addition, 'corrected-archive-latest-months' can be passed, which is
            a combination of the two api calls.
            Note that all periods are not available for all stations/parameters.

        return_tz : Not implemented

        Returns
        -------
        SonderaData object
        """

        # 'corrected-archive-latest-months', need to move the client call away
        # from the api call itself
        if period.lower() == 'corrected-archive-latest-months':
            station_data_ca = self._api_call_observations(parameter,
                                                          station,
                                                          'corrected-archive')

            station_data_lm = self._api_call_observations(parameter,
                                                          station,
                                                          'latest-months')
            # combine the two data sets, base of data_lm and extend the data series

            station_data = station_data_lm  # TODO copy?
            new_obs_s = station_data_ca.data.combine_first(station_data_lm.data)
            new_aux_s = station_data_ca.aux_data.combine_first(station_data_lm.aux_data)
            station_data.data = new_obs_s
            station_data.aux_data = new_aux_s

            return station_data
        else:
            return self._api_call_observations(parameter, station, period)

    def _api_call_observations(self,
                               parameter: Union[Parameters, int],
                               station: int,
                               period: str) -> SonderaData:
        # extension for data
        if period.lower() == 'corrected-archive':
            api_ext = 'csv'
        else:
            api_ext = 'json'

        if isinstance(parameter, int):
            try:
                parameter = self.Parameters(parameter)
            except ValueError as error:
                raise

        api_vars = {'parameter': parameter.value,
                    'station': station,
                    'period': period,
                    'extension': api_ext}

        # Get station metadata
        api_url_station = self._api_url_template_station.format(**api_vars) + '.json'
        api_get_station = self._make_request(api_url_station)
        station_md = api_get_station.json()

        # Get data
        api_url = self._api_url_template_data.format(**api_vars)
        api_get_result = self._make_request(api_url)

        if api_ext == 'json':
            api_result_json = api_get_result.json()

            obs_s, aux_df, station_name, md_str = self._json_to_dataframe(api_result_json, parameter)
            # # below here to other function
            # df_values = pd.DataFrame(api_result_json['value'])
            #
            # if parameter_patterns[parameter]['timestamp_type'] in ['date', 'date_time']:
            #     df_values['timestamp'] = pd.to_datetime(df_values['date'], unit='ms',
            #                                             origin='unix')  # TODO set timezone
            #     df_values = df_values.drop('date', axis=1)
            # elif parameter_patterns[parameter]['timestamp_type'] == 'ref':
            #     df_values['timestamp'] = pd.to_datetime(df_values['ref'])  # TODO set timezone
            #     df_values = df_values.drop('ref', axis=1)
            #
            # df_values = df_values.set_index('timestamp')
            # obs_s = df_values['value'].copy()
            # aux_df = df_values[set(df_values.keys()) - {'value'}]
            #
            # station_name = api_result_json['station']['name']
            #
            # md_str = str(api_result_json['parameter'])
        else:
            api_content_decoded = api_get_result.content.decode(encoding='utf-8-sig')

            obs_s, aux_df, station_name, md_str = self._csv_to_dataframe(api_content_decoded, parameter)
            # # find csv data line
            # csv_data_line = self._find_csv_data_line(api_content_decoded,
            #                                          parameter_patterns[parameter]['str_pattern'])
            #
            # # parse data
            # csv_df = pd.read_csv(StringIO(api_content_decoded),
            #                      sep=';',
            #                      header=0,
            #                      skiprows=csv_data_line,
            #                      usecols=parameter_patterns[parameter]['use_cols'],
            #                      index_col=False)
            #
            # # handle the various formats date and time is provided in
            # # TODO might be able to avoid 'timestamp_type' if there is a clear system
            # # i.e. if first key is 'Datum', 'Datum (svensk sommartid)', or 'Representativt dygn'
            # if parameter_patterns[parameter]['timestamp_type'] in ['date_time']:
            #     csv_df['timestamp'] = pd.to_datetime(csv_df['Datum'] + ' '
            #                                          + csv_df['Tid (UTC)'])
            #     csv_df = csv_df.drop(['Datum', 'Tid (UTC)'], axis=1)
            # elif parameter_patterns[parameter]['timestamp_type'] in ['date']:
            #     csv_df['timestamp'] = pd.to_datetime(csv_df['Datum (svensk sommartid)'])
            #     csv_df = csv_df.drop(['Datum (svensk sommartid)'], axis=1)
            # elif parameter_patterns[parameter]['timestamp_type'] in ['ref']:
            #     csv_df['timestamp'] = pd.to_datetime(csv_df['Representativt dygn'])
            #     csv_df = csv_df.drop(['Representativt dygn'], axis=1)
            #
            # csv_df = csv_df.set_index('timestamp')
            # swe_par_name = self.api_params_dict[parameter.value]['title']
            # obs_s = csv_df[swe_par_name]
            #
            # aux_df = csv_df[set(csv_df.keys()) - {swe_par_name}]
            # # Rename 'Kvalitet' to 'quality' in aux data as in other json data
            # aux_df = aux_df.rename({'Kvalitet': 'quality'}, axis=1)
            #
            # md_buffer = StringIO(api_content_decoded)
            # md_str = ''
            # for _ in range(csv_data_line):
            #     md_str = md_str + md_buffer.readline()
            #
            # # Read station info, first two lines of csv file
            # csv_sn = pd.read_csv(StringIO(api_content_decoded),
            #                      sep=';',
            #                      nrows=1,
            #                      header=0)
            #
            # # Station name is not accessible from station .json from met obs api
            # station_name = csv_sn.loc[0]['Stationsnamn']

        obs_s.name = parameter.name

        # create data object (separate function to easily set station type
        # with inheritance
        # TODO the station_md differs for MetObs and HydroObs
        # so this (creating the SonderaData object) has to be a method that can be replaced in HydroObs
        # hydroobs does not have history, the dict is flat as it looks

        station_data = self._create_data_obj(aux_df,
                                             obs_s,
                                             parameter,
                                             station_md,
                                             station_name,
                                             md_str)

        return station_data

    def _json_to_dataframe(self, api_result_json, parameter):
        # below here to other function
        df_values = pd.DataFrame(api_result_json['value'])

        if parameter_patterns[parameter]['timestamp_type'] in ['date', 'date_time']:
            df_values['timestamp'] = pd.to_datetime(df_values['date'], unit='ms',
                                                    origin='unix')  # TODO set timezone
            df_values = df_values.drop('date', axis=1)
        elif parameter_patterns[parameter]['timestamp_type'] == 'ref':
            df_values['timestamp'] = pd.to_datetime(df_values['ref'])  # TODO set timezone
            df_values = df_values.drop('ref', axis=1)

        df_values = df_values.set_index('timestamp')
        obs_s = df_values['value'].copy()
        aux_df = df_values[set(df_values.keys()) - {'value'}]

        station_name = api_result_json['station']['name']

        md_str = str(api_result_json['parameter'])

        return obs_s, aux_df, station_name, md_str

    def _csv_to_dataframe(self, api_content_decoded, parameter):
        # find csv data line
        csv_data_line = self._find_csv_data_line(api_content_decoded,
                                                 parameter_patterns[parameter]['str_pattern'])

        if csv_data_line is None:
            raise SonderaError(message='String pattern for parsing csv not matched',
                               report_issue=True, issue_messages=[parameter])

        # parse data
        csv_df = pd.read_csv(StringIO(api_content_decoded),
                             sep=';',
                             header=0,
                             skiprows=csv_data_line,
                             usecols=parameter_patterns[parameter]['use_cols'],
                             index_col=False)

        # handle the various formats date and time is provided in
        # TODO might be able to avoid 'timestamp_type' if there is a clear system
        # i.e. if first key is 'Datum', 'Datum (svensk sommartid)', or 'Representativt dygn'
        if parameter_patterns[parameter]['timestamp_type'] in ['date_time']:
            csv_df['timestamp'] = pd.to_datetime(csv_df['Datum'] + ' '
                                                 + csv_df['Tid (UTC)'])
            csv_df = csv_df.drop(['Datum', 'Tid (UTC)'], axis=1)
        elif parameter_patterns[parameter]['timestamp_type'] in ['date']:
            csv_df['timestamp'] = pd.to_datetime(csv_df['Datum (svensk sommartid)'])
            csv_df = csv_df.drop(['Datum (svensk sommartid)'], axis=1)
        elif parameter_patterns[parameter]['timestamp_type'] in ['ref']:
            csv_df['timestamp'] = pd.to_datetime(csv_df['Representativt dygn'])
            csv_df = csv_df.drop(['Representativt dygn'], axis=1)

        csv_df = csv_df.set_index('timestamp')
        swe_par_name = self.api_params_dict[parameter.value]['title']
        obs_s = csv_df[swe_par_name]

        aux_df = csv_df[set(csv_df.keys()) - {swe_par_name}]
        # Rename 'Kvalitet' to 'quality' in aux data as in other json data
        aux_df = aux_df.rename({'Kvalitet': 'quality'}, axis=1)

        md_buffer = StringIO(api_content_decoded)
        md_str = ''
        for _ in range(csv_data_line):
            md_str = md_str + md_buffer.readline()

        # Read station info, first two lines of csv file
        csv_sn = pd.read_csv(StringIO(api_content_decoded),
                             sep=';',
                             nrows=1,
                             header=0)

        # Station name is not accessible from station .json from met obs api
        station_name = csv_sn.loc[0]['Stationsnamn']

        return obs_s, aux_df, station_name, md_str

    def _create_data_obj(self, aux_df, obs_s, parameter,
                         station_md, station_name, md_str):
        # Get positions, can be several if station moved
        position_history = []
        from_dates = []
        to_dates = []
        for pos in station_md['position']:
            pos_coord = Coordinate(y=pos.get('latitude'),
                                   x=pos.get('longitude'),
                                   z=pos.get('height', None),
                                   epsg=4326)

            pos_i = {'from': dt.datetime.utcfromtimestamp(pos['from'] / 1000),
                     'to': dt.datetime.utcfromtimestamp(pos['to'] / 1000),
                     'position': pos_coord}

            position_history.append(pos_i)
            from_dates.append(pos_i['from'])
            to_dates.append(pos_i['to'])
        pos_coord_last = position_history[-1]['position']
        station_data = SonderaData(name=station_name,
                                   position=pos_coord_last,
                                   position_history=position_history,
                                   station_type=StationType.MetStation,
                                   data=obs_s,
                                   aux_data=aux_df,
                                   parameter=parameter,
                                   metadata=md_str,
                                   active_station=station_md['active'],
                                   start_date=min(from_dates),
                                   end_date=max(to_dates))
        return station_data

    def get_parameters_station(self, station):
        # get available parameters for station
        pass
        # Requires many requests to API, not available. call get_all_stations
        # and get pars where station is listed


    def get_all_stations(self):
        pass
        # Requires many requests to API, not available
        # Need to loop over parameters
        if not self.get_all_stations_called:
            self.all_stations_dict = {}
            # call get_stations_parameter
            self.get_all_stations_called = True

        return self.all_stations_dict


    def get_stations_parameter(self, parameter):
        # Get stations where parameter is available
        # https://opendata.smhi.se/apidocs/metobs/parameter.html
        pass

    def get_periods(self):
        # get available periods for parameter and station
        pass

    def print_parameters(self):
        pass

    @staticmethod
    def _find_csv_data_line(api_content_decoded, str_pattern):
        """ Find first line of data (i.e. the data header) for .csv type returns
        Line is matched with str_pattern, which varies across parameters
        Note that line numbers varies for the same parameters as well """

        line_data_start = 0
        try:
            with StringIO(api_content_decoded) as csv_data:
                for line in csv_data:
                    if line.startswith(str_pattern):
                        return line_data_start
                    line_data_start += 1
                # if loop finishes without returning, str was not found
                return None
        except TypeError as e:
            print(e)
            raise


    def _make_request(self, api_url):
        """ All API requests are passed through this method """
        api_get_result = requests.get(api_url)

        # Check result for error
        if api_get_result.status_code != 200:
            raise APIError(api_get_result.status_code,
                           api_get_result.reason)
        else:
            return api_get_result

    def get_api_parameters(self, print_params=True):
        """ Return parameter information from API """
        api_url_version = self._api_url + '.json'
        api_get_version = requests.get(api_url_version)

        v_resource = api_get_version.json()['resource']
        v_params = {}

        for vr in v_resource:
            v_params[int(vr['key'])] = {'title': vr['title'],
                                        'summary': vr['summary']}

        v_params = collections.OrderedDict(sorted(v_params.items()))  # noqa

        if print_params:
            for vpk, vpi in v_params.items():
                print(f"{vpk}: {vpi['title']}, {vpi['summary']}")

        return v_params
