from typing import List
import geopandas as gpd

from src.zones.zone import Zone


class Parser:
    """
    Utlility class containing methods related to retriving zone information
    from a GeoJSON file.
    """

    @staticmethod
    def extract_zones_from_geojson(geojson_file: str) -> List[Zone]:
        """
        Parses a GeoJSON file and returns a list of zones defined in the file.

        This is a static method and does not depend on any instance or class state.

        Args:
            geojson_file (str): the path to the geojson_file.

        Returns:
            (List[Zone]): list of zones.
        """
        # Read the file to a GeoDataFrame object
        gdf = gpd.read_file(geojson_file)

        # Set up a list of Zone objects and parse the zone type and polygon
        # information for each zone.
        zones = []
        for _, row in gdf.iterrows():
            zone_type = row["zoneType"]
            polygon = row["geometry"]
            zones.append(Zone(polygon=polygon, zone_type=zone_type))

        return zones
