import pytest
from shapely.geometry import Polygon

from src.vehicles.vehicle import Vehicle
from src.zones.zone import Zone


@pytest.fixture(autouse=True)
def reset_id_counters():
    Vehicle._id_counter = 0
    for key in Zone._zone_counters.keys():
        Zone._zone_counters[key] = 0


def test_vehicle_init():
    vehicle = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    assert vehicle.raw_polygon.equals(Polygon([[0, 0], [0, 2], [2, 2], [2, 0]]))
    assert vehicle.polygon.equals(Polygon([[0, 0], [0, 2], [2, 2], [2, 0]]))
    assert vehicle.buffer_rate == 3.0
    assert vehicle.id == 1


def test_buffer_bounds():
    vehicle = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    vehicle.buffer_bounds(2)
    assert vehicle.polygon.equals(vehicle.raw_polygon.buffer(6.0))


def test_reset_buffer():
    vehicle = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    vehicle.buffer_bounds(2)
    vehicle.reset_buffer()
    assert vehicle.polygon.equals(vehicle.raw_polygon)


def test_in_zone():
    vehicle_bounds = [[0, 0], [0, 2], [2, 2], [2, 0]]
    zone_bounds = Polygon([[-1, -1], [-1, 3], [3, 3], [3, -1]])
    vehicle = Vehicle(vehicle_bounds)
    zone = Zone(zone_bounds, "autonomousOperatingZone")
    assert vehicle.in_zone(zone) == True


def test_intersects_zone():
    vehicle = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    zone = Zone(Polygon([[1, 1], [1, 3], [3, 3], [3, 1]]), "singleTruckZone")
    assert vehicle.intersects_zone(zone) == True


def test_intersects_vehicle():
    vehicle1 = Vehicle([[0, 0], [0, 2], [2, 2], [2, 0]])
    vehicle2 = Vehicle([[1, 1], [1, 3], [3, 3], [3, 1]])
    assert vehicle1.intersects_vehicle(vehicle2) == True


if __name__ == "__main__":
    pytest.main()
