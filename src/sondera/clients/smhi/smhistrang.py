# https://opendata.smhi.se/apidocs/strang/
# to be implemented
# model data and not observation, so will not use the station and dataclasses
# simply return the data as either pd.Series or xarray
# https://opendata.smhi.se/apidocs/strang/get_points.html <-- pandas.Series
# https://opendata.smhi.se/apidocs/strang/get_multipoint.html <-- xarray

# from ..parameters import ParametersStrang as Parameters

class StrangClient:
    _api_url = 'https://opendata-download-metanalys.smhi.se/api/category/strang1g/version/1/geotype'

    def __init__(self):
        raise NotImplementedError

    def get_data_point(self):
        pass

    def get_data_multipoint(self):
        pass

    def _create_data_obj(self):
        pass
