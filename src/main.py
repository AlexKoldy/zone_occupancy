import os

from src.vehicles.vehicle import Vehicle
from src.utils.parser import Parser
from src.utils.plotter import Plotter
from src.utils.utils import vehicle_intersects_zone_with_others, any_vehicles_intersect

if __name__ == "__main__":
    show_plot = True  # flag for plotting
    geojson_name = "zone"  # name of .json file containing zone information

    # Set up vehicles
    vehicle1 = Vehicle(bounds=[[1, 4], [3, 6], [5, 4], [3, 2]])
    vehicle2 = Vehicle(bounds=[[-2, -2], [-6, -2], [-6, -4], [-2, -4]])
    vehicle3 = Vehicle(bounds=[[-3, 9], [-3, 11], [-5, 11], [-5, 9]])
    vehicles = [vehicle1, vehicle2, vehicle3]

    # Set up zones
    file_path = os.path.join(os.path.dirname(__file__), f"../data/{geojson_name}.json")
    zones = Parser.extract_zones_from_geojson(file_path)
    single_truck_zone = next(
        zone for zone in zones if zone.zone_type == "singleTruckZone"
    )
    autonomous_operating_zone = next(
        zone for zone in zones if zone.zone_type == "autonomousOperatingZone"
    )

    # Questions
    print("######################### QUESTION 1 #########################")
    print("For each vehicle, submit answers to the following:")
    for i, vehicle in enumerate(vehicles):
        print(f"------------------------Vehicle {i + 1}------------------------")
        print("(1) Is the vehicle contained in the autonomous operating zone?")
        (print("Yes.") if vehicle.in_zone(autonomous_operating_zone) else print("No."))
        print("(2) Is any part of the vehicle intersecting the single truck zone?")
        (print("Yes.") if vehicle.intersects_zone(single_truck_zone) else print("No."))
        print(
            "(3) Is any part of the vehicle intersecting the single truck zone that is"
            + " already occupied by another vehicle?"
        )
        (
            print("Yes.")
            if vehicle_intersects_zone_with_others(
                zone=single_truck_zone,
                vehicles=vehicles[:i] + vehicles[i + 1 :],
                target_vehicle=vehicle,
            )
            else print("No.")
        )
        if show_plot:
            Plotter.plot_vehicles_and_zones(
                zones=zones,
                vehicles=vehicles[:i] + vehicles[i + 1 :],
                target_vehicle=vehicle,
            )

    print("######################### QUESTION 2 #########################")
    print(
        "In the event of a comms loss, the vehicle bounds are buffered out in"
        + " every direction from its last known position at a rate of 3 m/s. If vehicle 2"
        + " has been missing for 5 seconds, are any vehicle buffers intersecting?"
    )
    vehicles[1].buffer_bounds(5.0) # buffer vehicle 2
    print("Yes.") if any_vehicles_intersect(vehicles) else print("No.")
    if show_plot:
        Plotter.plot_vehicles_and_zones(
            zones=zones,
            vehicles=vehicles,
        )
