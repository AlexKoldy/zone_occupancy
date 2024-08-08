import pytest
from shapely.geometry import Polygon

from src.utils.utils import vehicle_intersects_zone_with_others, any_vehicles_intersect
from src.vehicles.vehicle import Vehicle
from src.zones.zone import Zone


@pytest.fixture(autouse=True)
def reset_id_counters():
    Vehicle._id_counter = 0
    for key in Zone._zone_counters.keys():
        Zone._zone_counters[key] = 0


def test_vehicle_intersects_zone_with_others():
    vehicle1 = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    vehicle2 = Vehicle([[1, 1], [1, 3], [3, 3], [3, 1]])
    vehicle3 = Vehicle([[3, 3], [3, 5], [5, 5], [5, 3]])

    zone = Zone(
        Polygon([[-1, 0], [-1, 2.5], [2.5, 2.5], [2.5, -1]]), "autonomousOperatingZone"
    )

    # Case (1): Target vehicle intersects the zone and another vehicle
    # intersects the zone
    result = vehicle_intersects_zone_with_others(zone, [vehicle2, vehicle3], vehicle1)
    assert result == True

    # Case (2): Target vehicle intersects the zone, but no other vehicle
    # intersects the zone
    result = vehicle_intersects_zone_with_others(zone, [vehicle3], vehicle1)
    assert result == False

    # Case (3): Target vehicle does not intersect the zone
    result = vehicle_intersects_zone_with_others(zone, [vehicle1, vehicle2], vehicle3)
    assert result == False


def test_any_vehicles_intersect():
    vehicle1 = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    vehicle2 = Vehicle([[1, 1], [1, 3], [3, 3], [3, 1]])
    vehicle3 = Vehicle([[3, 3], [3, 5], [5, 5], [5, 3]])

    # Case (1): Two vehicle intersect
    result = any_vehicles_intersect([vehicle1, vehicle2, vehicle3])
    assert result == True

    # Case (2): No vehicles intersect
    result = any_vehicles_intersect([vehicle1, vehicle3])
    assert result == False


if __name__ == "__main__":
    pytest.main()
