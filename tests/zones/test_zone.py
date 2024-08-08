import pytest
from shapely.geometry import Polygon
from src.zones.zone import Zone


@pytest.fixture(autouse=True)
def reset_zone_counters():
    for key in Zone._zone_counters.keys():
        Zone._zone_counters[key] = 0


def test_zone_initialization():
    polygon = Polygon([[0, 0], [0, 2], [2, 2], [2, 0]])
    zone = Zone(polygon, "autonomousOperatingZone")
    assert zone.polygon.equals(polygon)
    assert zone.zone_type == "autonomousOperatingZone"
    assert zone.id == 1


def test_multiple_zones_different_types():
    polygon1 = Polygon([[0, 0], [0, 2], [2, 2], [2, 0]])
    polygon2 = Polygon([[1, 1], [1, 3], [3, 3], [3, 1]])
    zone1 = Zone(polygon1, "autonomousOperatingZone")
    zone2 = Zone(polygon2, "singleTruckZone")
    assert zone1.id == 1
    assert zone2.id == 1


def test_zone_id_counter_per_type():
    polygon1 = Polygon([[0, 0], [0, 2], [2, 2], [2, 0]])
    polygon2 = Polygon([[1, 1], [1, 3], [3, 3], [3, 1]])
    zone1 = Zone(polygon1, "autonomousOperatingZone")
    zone2 = Zone(polygon2, "autonomousOperatingZone")
    assert zone1.id == 1
    assert zone2.id == 2


if __name__ == "__main__":
    pytest.main()
