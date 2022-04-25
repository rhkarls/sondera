"""
Geographical functions for sondera
"""
# for type hints and cyclic imports of Coordinate
from __future__ import annotations
from typing import TYPE_CHECKING

import geopandas
import numpy as np
from shapely.geometry import Point

if TYPE_CHECKING:
    from sondera.datatypes import Coordinate


def find_nearby_stations():
    raise NotImplementedError


def find_stations_in_polygon():
    raise NotImplementedError

# FIXME return Coordinate object also? if so base it as a copy of coord_in
# Also coord_in already has epsg_in defined?
def transform_coordinate(coord_in: Coordinate, epsg_in: int, epsg_out: int):

    gs_in = geopandas.GeoSeries([Point(coord_in.x, coord_in.y)], crs=epsg_in)
    gs_out = gs_in.to_crs(epsg=epsg_out)

    return gs_out.iloc[0].x, gs_out.iloc[0].y


def distance_euclidean(coord1: Coordinate, coord2: Coordinate) -> float:
    """Euclidean Distance in meter between two coordinates

        Parameters
        ----------
        coord1
        coord2

        Returns
        -------
        Distance between coord1 and coord2 in meters

        """
    raise NotImplementedError

def distance_haversine(coord1: Coordinate, coord2: Coordinate) -> float:
    """Distance in meter between two spherical coordinates on Earth using
    Haversine method

    Parameters
    ----------
    coord1
    coord2

    Returns
    -------
    Distance between coord1 and coord2 in meters

    """
    r_earth = 6371  # mean Earth radius in km

    # Coordinates in radians
    lat1 = np.deg2rad(coord1.y)
    lat2 = np.deg2rad(coord2.y)
    lon1 = np.deg2rad(coord1.x)
    lon2 = np.deg2rad(coord2.x)

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = (np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2)
         * np.sin(d_lon / 2) ** 2)
    c = 2 * np.asin(np.sqrt(a))
    d = r_earth * c * 1000  # distance in meters

    return d
