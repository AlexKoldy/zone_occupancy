import pytest
import os
from shapely.geometry import Polygon

from src.utils.parser import Parser


@pytest.fixture
def geojson_file():
    file_path = os.path.join(os.path.dirname(__file__), "../../data/zone.json")
    return file_path


def test_extract_zones_from_geojson(geojson_file):
    zones = Parser.extract_zones_from_geojson(geojson_file)
    assert len(zones) == 2
    assert zones[0].zone_type == "autonomousOperatingZone"
    assert zones[1].zone_type == "singleTruckZone"
    assert zones[0].polygon.equals(
        Polygon([[10.0, 10.0], [10.0, -10.0], [-10.0, -10.0], [-10.0, 10.0]])
    )
    assert zones[1].polygon.equals(
        Polygon([[7.0, 7.0], [7.0, -5.0], [-5.0, -5.0], [-5.0, 7.0]])
    )


if __name__ == "__main__":
    pytest.main()
