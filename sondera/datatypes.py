"""sondera data types"""
import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Any, Optional

import numpy as np
import pandas as pd

from sondera.geo_utils import distance_haversine, transform_coordinate


class StationType(Enum):
    HydroStation = auto()
    MetStation = auto()
    GWStation = auto()


@dataclass
class Coordinate:
    y: float  # Northing or latitude
    x: float  # Easting or longitude
    z: float = None
    epsg_xy: int = None  # EPSG code for CRS for x,y coordinates
    epsg_z: int = None  # EPSG code for vertical (z) datum

    def distance_to(self, other):
        """
        Haversine distance in meter to other coordinate point for WGS84
        Euclidean distance in CRS units for other epsg codes
        """
        if self.epsg_xy == 4326:  # FIXME list of wgs84 codes?
            return haversine(self, other)
        else:
            return np.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    def to_wgs84(self):
        if self.epsg_xy != 4326:
            self.x, self.y = transform_coordinate([self.x, self.y],
                                 epsg_in=self.epsg_xy,
                                 epsg_out=4326)

            self.epsg_xy = 4326


@dataclass
class Station:

    name: str
    id: int
    agency: str
    location: Coordinate
    station_type: StationType
    active_station: bool
    active_period: List[datetime.datetime]
    last_updated: datetime.datetime


@dataclass
class SonderaData:
    """ General class for data"""
    # station has coordinate, name, description, data source, agency
    # data (dataframe)
    # some can have additional info, like catchment polygon, catchment size
    # SGU wells carry a lot of fields that are quite relevant
    station: Station
    data: pd.Series
    parameter: Enum
    metadata: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    position_history: Optional[List] = None
    aux_data: Optional[pd.DataFrame] = None
