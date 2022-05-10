"""sondera data types"""
import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Any, Optional, Union

import pandas as pd

from .geo_utils import distance_haversine, transform_coordinate


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

    def distance_to(self, other) -> float:
        """ Distance to other Coordinate in meters

        Distance is calculated by converting booth coordinates to
        WGS84 (epsg:4326) and then calculating Haversine distance.

        Both the instance and other need epsg_xy attribute set
        """
        coord_a = self.to_wgs84()
        coord_b = other.to_wgs84()

        return distance_haversine(coord_a, coord_b)

    def to_wgs84(self):
        """ Convert the 2D coordinates (x, y) to WGS84 epsg:4326 """
        # HINT: transform_coordinate raises ValueError if epsg_xy is None
        if self.epsg_xy != 4326:
            coord_wgs84 = transform_coordinate(self,
                                               epsg_out=4326)

            return coord_wgs84


@dataclass
class Station:
    """ Class for measurement station"""
    name: str
    id: int
    agency: str
    position: Coordinate
    station_type: StationType
    active_station: bool
    active_period: List[datetime.datetime]
    last_updated: datetime.datetime
    station_info: dict[str, Any]
    position_history: Optional[List] = None


@dataclass
class DataSeries:
    """ General class for observed data series"""
    # some can have additional info, like catchment polygon, catchment size
    # SGU wells carry a lot of fields that are quite relevant
    station: Station
    data: "pd.Series[Union[int, float]]"
    parameter: Enum
    metadata: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    aux_data: Optional[pd.DataFrame] = None
