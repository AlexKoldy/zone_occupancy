from typing import List
from shapely.geometry import Polygon


class Zone:
    """
    Simple class to store zone information.

    Attributes:
        polygon (Polygon): polygon object representing the zone bounds.
        zone_type (str): the type of zone. Either 'autonomousOperatingZone' or
            'singleTruckZone'.
        id (int): unique identifier for a zone object of a specific zone type.
    """

    _zone_counters = {}  # stores a count of zone objects per zone type

    def __init__(self, polygon: Polygon, zone_type: str):
        """
        Initializes the Zone class with its bounds and zone type.

        Args:
            polygon (Polygon): polygon object representing the zone bounds.
             zone_type (str): the type of zone. Either 'autonomousOperatingZone' or
                'singleTruckZone'.
        """
        self.polygon = polygon
        self.zone_type = zone_type

        # Set up unique ID. This might be useful for distinguising between
        # zones down the line. Since there are multiple zone types, start
        # from the beginning for each one.
        if zone_type not in type(self)._zone_counters:
            type(self)._zone_counters[zone_type] = 0
        type(self)._zone_counters[zone_type] += 1
        self.id = type(self)._zone_counters[zone_type]
