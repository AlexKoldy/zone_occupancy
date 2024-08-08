from __future__ import annotations
from typing import List, Dict, Any, Optional
from shapely.geometry import Polygon

from src.zones.zone import Zone


class Vehicle:
    """
    Simple class to store vehicle information.

    Attributes:
        raw_polygon (Polygon): polygon object representing the raw, unbuffered
            vehicle bounds.
        polygon (Polygon): polygon object representing the buffered vehicle bounds.
        buffer_rate (float): rate at which vehicle bounds are buffered out. Default
            of 3.0. meters per second. [m/s]
        id (int): unique identifier for the vehicle object.
    """

    _id_counter = 0  # stores a count of vehicle objects

    def __init__(self, bounds: List[List[float]], buffer_rate: float = 3.0):
        """
        Initializes the Vehicle class with its bounds and buffer rate.

        Args:
            bounds (List[List[float]]): a list of (x, y) pairs describing the vertices
                of the polygon defining the vehicle bounds. [m]
            buffer_rate (float): rate at which vehicle bounds are buffered out. Default
                of 3.0. meters per second. [m/s]
        """
        # Plug bounds into a shapely Polygon object
        self.raw_polygon = Polygon(bounds)  # used for resetting the buffer
        self.polygon = Polygon(bounds)

        # Set buffer rate
        self.buffer_rate = buffer_rate

        # Set up unique ID. This might be useful for distinguising between
        # vehicles down the line
        type(self)._id_counter += 1
        self.id = type(self)._id_counter

    def buffer_bounds(self, disconnect_time: float) -> None:
        """
        Buffers the bounds of the vehicle given the time since the vehicle connection
        was lost.

        Args:
            disconnect_time (float): amount of time since the vehicle disconnected. [s]
        """
        if disconnect_time != 0.0:
            distance = disconnect_time * self.buffer_rate  # [m]
            self.polygon = self.polygon.buffer(distance)

    def reset_buffer(self) -> None:
        """
        Resets the vehicle's buffer to its original bounds.
        """
        self.polygon = self.raw_polygon

    def in_zone(self, zone: Zone) -> bool:
        """
        Checks if the vehicle is completely within a given zone.

        Args:
            zone (Zone): the zone to check containment with.

        Returns:
            (bool): whether or not this vehicle is completely within the given
                zone.
        """
        # Using Shapely, returns 'True' if the zone polygon completely contains
        # the vehicle polygon and 'False' if not
        return zone.polygon.contains(self.polygon)

    def intersects_zone(self, zone: Zone) -> bool:
        """
        Checks if the vehicle intersects a given zone.

        Args:
            zone (Zone): the zone to check intersection with.

        Returns:
            (bool): whether or not this vehicle intersects a zone.
        """
        # Using Shapely, returns 'True' if the zone polygon intersects the vehicle
        # polygon and 'False' if not
        return self.polygon.intersects(zone.polygon)

    def intersects_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Checks if the vehicle intersects another given vehicle.

        Args:
            vehicle (Vehicle): the vehicle to check intersection with.

        Returns:
            (bool): whether or not this vehicle intersects the given vehicle.
        """
        # Using Shapely, returns 'True' if the other vehicle polygon intersects this
        # vehicle's polygon and 'False' if not
        return self.polygon.intersects(vehicle.polygon)
