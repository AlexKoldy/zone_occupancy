from typing import List
import itertools

from src.vehicles.vehicle import Vehicle
from src.zones.zone import Zone


def vehicle_intersects_zone_with_others(
    zone: Zone, vehicles: List[Vehicle], target_vehicle: Vehicle
) -> bool:
    """
    Checks if the target vehicle is intersecting the zone and if another vehicle is
    also intersecting the zone.

    Args:
        zone (Zone): the zone to check intersections with.
        vehicles (List[Vehicle]): list of vehicle objects to check.
        target_vehicle (Vehicle): the specific vehicle to check for intersection.

    Returns:
        (bool): whether or not the zone intersects with both the target vehicle and
            a vehicle within the given list.
    """
    # Check if the target vehicle intersects the zone
    if not target_vehicle.intersects_zone(zone):
        return False

    # Check if any other vehicle also intersects the zone
    for vehicle in vehicles:
        if vehicle != target_vehicle and vehicle.intersects_zone(zone):
            return True

    return False


def any_vehicles_intersect(vehicles: List[Vehicle]) -> bool:
    """
    Checks if any vehicles within the given list have intersecting boundaries.

    Args:
        vehicles (List[Vehicle]): list of vehicle objects to check.

    Returns:
        (bool): whether or not any two vehicles in the list have intersecting
            boundaries.
    """
    for vehicle1, vehicle2 in itertools.combinations(vehicles, 2):
        if vehicle1.intersects_vehicle(vehicle2):
            return True

    return False
