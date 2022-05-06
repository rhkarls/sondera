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

## Feedback and issues

Please report issues here: https://github.com/rhkarls/sondera/issues

General feedback is most welcome, please post that as well under issues.

