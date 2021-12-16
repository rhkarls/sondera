"""sondera data types"""
import datetime
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np
import pandas as pd


class StationType(Enum):
    HydroStation = auto()
    MetStation = auto()
    GWStation = auto()


@dataclass
class Coordinate:
    y: float  # Northing or latitude
    x: float  # Easting or longitude
    z: float = None
    epsg: int = None  # EPSG code for CRS

    def distance_to(self, other):
        """
        Haversine distance in meter to other coordinate point for WGS84
        Euclidean distance in CRS units for other epsg codes
        """
        if self.epsg == 4326: # FIXME list of wgs84 codes?
            pass
        else:
            return np.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # def to_wgs84(self):
    #     if self.epsg == 4326:
    #         return self
    #     else:
    #         pass
    #         # convert to lat lon and return new Coordinate


@dataclass
class SonderaData:
    """ General class for data"""
    # station has coordinate, name, description, data source, agency
    # data (dataframe)
    # some can have additional info, like catchment polygon, catchment size
    # SGU wells carry a lot of fields that are quite relevant
    name: str
    position: Coordinate
    station_type: StationType
    data: pd.Series
    parameter: Enum
    metadata: str
    active_station: bool
    start_date: datetime.datetime
    end_date: datetime.datetime
    position_history: list = None
    aux_data: pd.DataFrame = None



