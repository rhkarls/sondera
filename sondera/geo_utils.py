"""
Geographical functions for sondera
"""
# for type hints and cyclic imports of Coordinate
from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

import geopandas
import numpy as np

if TYPE_CHECKING:
    from sondera.datatypes import Coordinate


def find_nearby_stations():
    raise NotImplementedError


def find_stations_in_polygon():
    raise NotImplementedError


def transform_coordinate(coord_in: Coordinate, epsg_out: int):
    """ Transform a Coordinate object's 2D coordinates with epsg code

    Parameters
    ----------
    coord_in
    epsg_out

    Returns
    -------

    """
    if coord_in.epsg_xy is None:
        raise ValueError('coord_in Coordinate object does not have epsg_xy set')

    gs_in = geopandas.GeoSeries(geopandas.points_from_xy(x=[coord_in.x],
                                                         y=[coord_in.y],
                                                         crs=coord_in.epsg_xy))
    gs_out = gs_in.to_crs(epsg=epsg_out)

    coord_out = deepcopy(coord_in)
    coord_out.x = gs_out.iloc[0].x
    coord_out.y = gs_out.iloc[0].y
    coord_out.epsg_xy = epsg_out

    return coord_out


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
    return np.sqrt((coord2.x - coord1.x) ** 2 + (coord2.y - coord1.y) ** 2)


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
