# Example getting daily discharge from
# SMHI station xxx  (number xxx)

# Other data periods can be downloaded by changing `period` keyword on
# client.get_observations() call.
# latest-hour, latest-day, latest-months or corrected-archive are supported
# directly by the SMHI api. In addition, ‘corrected-archive-latest-months’
# can be passed, which is a combination of the two api calls.
# Note that all periods are not available for all stations/parameters.

from sondera.clients.smhi import HydroObsClient, ParametersHydroObs

client = HydroObsClient()
# For the parameter we can pass either the ParametersHydroObs enum
# or simply the SMHI integer id (which is 1 for daily discharge, the only
# parameter available from the HydroObs API)
air_temp = client.get_observations(parameter=ParametersHydroObs.Discharge,
                                   station=98230,
                                   period='latest-months')

# observations are stored under "data" attribute as a pandas.Series
air_temp.data.head(5)

# additional data, such as quality tags are stored under "aux_data"
air_temp.aux_data.head(5)

# information on the station is also available, such as name, id, coordinates,
# and history
air_temp.station
