# sondera

[![pypi_shield](https://img.shields.io/pypi/v/sondera.svg)](https://pypi.org/project/sondera/)
[![pypi_license](https://badgen.net/pypi/license/sondera/)](https://pypi.org/project/sondera/)
![tests_workflow](https://github.com/rhkarls/sondera/actions/workflows/run_flake8_pytest.yml/badge.svg)

## Overview
sondera is a python package providing clients for accessing Swedish hydrology and meteorology related open data and observations.

Development Status: :bangbang: Pre-Alpha.
Consider the API unstable, it may change at short/no notice.

### Data sources and licenses
It is the end users responsibility to adhere to the license of each respective
data provider. See the links to the licenses below.

The following clients are currently implemented or under implementation:

**Observations**
- SMHI Open Data Meteorological Observations ([license](https://creativecommons.org/licenses/by/4.0/legalcode), [host link](https://opendata.smhi.se/apidocs/metobs/#license))
- SMHI Open Data Hydrological Observations ([license](https://creativecommons.org/licenses/by/4.0/legalcode), [host link](https://opendata.smhi.se/apidocs/hydroobs/#license))
- SGU Groundwater level time series ([license](https://creativecommons.org/licenses/by/4.0/legalcode), [host link](https://resource.sgu.se/oppnadata/html/grundvatten/grundvatten.html))

**Model products**
- SMHI Strång mesoscale model for solar radiation ([license](https://creativecommons.org/licenses/by/4.0/legalcode), [host link](https://opendata.smhi.se/apidocs/strang/#license))

## Requirements and installation

Requirements:

    numpy
	pandas
	geopandas
	requests
    tqdm

Install from pypi using pip

    pip install sondera

## General description and example usage

Observational data which is linked to a station is returned as a DataSeries object,
which contains metadata information in addition to the observed data series.

Modelling products are returned as the data series only, which is either a pandas
Series or DataFrame, or xarray for multi-dimensional data.


```python
# Example getting hourly air temperature for the latest months from
# SMHI station Stockholm-Observatoriekullen A  (number 98230)
from sondera.clients.smhi import MetObsClient, ParametersMetObs

client = MetObsClient()
# For the parameter we can pass either the ParametersMetObs enum
# or simply the SMHI integer id (which is 1 for hourly air temperature)
air_temp = client.get_observations(parameter=ParametersMetObs.TemperatureAirHour,
                         station= 98230,
                         period= 'latest-months')

# observations are stored under "data" attribute as a pandas.Series
air_temp.data.head(5)
timestamp
2021-12-31 01:00:00    4.9
2021-12-31 02:00:00    4.2
2021-12-31 03:00:00    3.5
2021-12-31 04:00:00    3.1
2021-12-31 05:00:00    3.0
Name: TemperatureAirHour, dtype: float64

# additional data, such as quality tags are stored under "aux_data"
air_temp.aux_data.head(5)
                    quality
timestamp                  
2021-12-31 01:00:00       G
2021-12-31 02:00:00       G
2021-12-31 03:00:00       G
2021-12-31 04:00:00       G
2021-12-31 05:00:00       G

# information on the station is also available, such as name, id, coordinates,
# and history
air_temp.station
Station(name='Stockholm-Observatoriekullen A', id=98230, agency='SMHI', 
        position=Coordinate(y=59.341681, x=18.054928, z=43.133, epsg_xy=4326, epsg_z=5613),
        station_type=<StationType.MetStation: 2>, active_station=True, 
        active_period=[Timestamp('1996-10-01 00:00:00'), Timestamp('2022-05-10 07:00:00')],
        last_updated=Timestamp('2022-05-10 07:00:00'), station_info={}, 
        position_history=[{'from': Timestamp('1996-10-01 00:00:00'), 
                           'to': Timestamp('2022-05-10 07:00:00'), 
                           'position': Coordinate(y=59.341681, x=18.054928, z=43.133,
                                                  epsg_xy=4326, epsg_z=5613)}])
```

## Feedback and issues

Please report issues here: https://github.com/rhkarls/sondera/issues

General feedback is most welcome, please post that as well under issues.

