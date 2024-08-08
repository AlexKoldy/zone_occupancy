from typing import List, Optional
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from src.vehicles.vehicle import Vehicle
from src.zones.zone import Zone


class Plotter:
    """
    Utility class containing methods to plot vehicles and zones for debugging.
    """

    @staticmethod
    def plot_vehicles_and_zones(
        vehicles: Optional[List[Vehicle]] = None,
        zones: Optional[List[Zone]] = None,
        target_vehicle: Optional[Vehicle] = None,
    ) -> None:
        """
        Plots all provided vehicles and zones on the same figure. A target vehicle
        can be specified for more specific debugging.

        This is a static method and does not depend on any instance or class state.

        Args:
            vehicles (Optional[List[Vehicle]]): list of vehicle objects to plot. Optional.
            zones (Optional[List[Zone]]): list of zone objects to plot. Optional.
            target_vehicle (Optional[Vehicle]): a specified target vehicle to highlight. Optional.
        """
        # Set up figure for plotting
        _, ax = plt.subplots(figsize=(10, 10))

        # If a list of vehicles exists, plot their raw and buffered bounds
        if vehicles:
            # Ensure that larger polygons are plotted first as to not cover
            # any smaller ones
            vehicles = sorted(
                vehicles, key=lambda vehicle: vehicle.polygon.area, reverse=True
            )

            for vehicle in vehicles:
                # Extract raw and buffered vehicle polygons
                polygon = gpd.GeoSeries(vehicle.polygon)
                raw_polygon = gpd.GeoSeries(vehicle.raw_polygon)

                # Plot buffered bounds and annotate the unique ID
                polygon.plot(ax=ax, color="red", edgecolor="black", zorder=2)
                ax.annotate(
                    text=vehicle.id,
                    xy=[polygon.centroid[0].x - 0.2, polygon.centroid[0].y - 0.2],
                    zorder=4,
                )

                # Plot raw (unbuffered) bounds if there is a buffer
                if not polygon.all() == raw_polygon.all():
                    raw_polygon.plot(ax=ax, color="darkred", zorder=3)

        # If a list of zones exists, plot each of them
        if zones:
            # Ensure that larger polygons are plotted first as to not cover
            # any smaller ones
            zones = sorted(zones, key=lambda zone: zone.polygon.area, reverse=True)
            for zone in zones:
                # Extract zone polygon
                polygon = gpd.GeoSeries(zone.polygon)

                # Set color for plotting based on zone type
                color = (
                    "blue" if zone.zone_type == "autonomousOperatingZone" else "purple"
                )

                # Plot zone
                polygon.plot(ax=ax, color=color, edgecolor="black", zorder=1)

        # If a target vehicle specifically exists, plot it
        if target_vehicle:
            # Extract raw and buffered vehicle polygons
            polygon = gpd.GeoSeries(target_vehicle.polygon)
            raw_polygon = gpd.GeoSeries(target_vehicle.raw_polygon)

            # Plot buffered bounds and annotate the unique ID
            polygon.plot(ax=ax, color="green", edgecolor="black", zorder=5)
            ax.annotate(
                text=target_vehicle.id,
                xy=[polygon.centroid[0].x - 0.2, polygon.centroid[0].y - 0.2],
                zorder=7,
            )

            # Plot raw (unbuffered) bounds if there is a buffer
            if not polygon.all() == raw_polygon.all():
                raw_polygon.plot(ax=ax, color="darkgreen", zorder=6)

        # Set the x and y labels
        ax.set_xlabel(r"$x [m]$")
        ax.set_ylabel(r"$y [m]$")

        plt.legend(
            handles=[
                Patch(facecolor="red", label="vehicle"),
                Patch(facecolor="darkred", label="unbuffered vehicle"),
                Patch(facecolor="green", label="target vehicle"),
                Patch(facecolor="darkgreen", label="unbuffered target vehicle"),
                Patch(facecolor="blue", label="autonomous operating zone"),
                Patch(facecolor="purple", label="single truck zone"),
            ],
            loc="upper center",
            bbox_to_anchor=(0.5, 1.05),
            ncol=3,
            fancybox=True,
            shadow=True,
        )
        plt.show()
