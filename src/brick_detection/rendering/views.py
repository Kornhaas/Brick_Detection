"""View sets shared by rendering scripts and regular Python tests."""

from __future__ import annotations


def view_definitions(view_set: str) -> list[dict[str, float | str]]:
    """Return deterministic camera poses for a named synthetic reference view set."""
    if view_set == "single":
        return [{"name": "view_00", "azimuth": -45.0, "elevation": 28.0}]
    if view_set == "poc-28":
        orbit_views: list[dict[str, float | str]] = [
            {
                "name": f"orbit_{azimuth:03d}_{elevation:02d}",
                "azimuth": float(azimuth),
                "elevation": float(elevation),
            }
            for azimuth in range(0, 360, 45)
            for elevation in (20, 45, 70)
        ]
        return orbit_views + [
            {"name": "top", "azimuth": 0.0, "elevation": 88.0},
            {"name": "bottom", "azimuth": 0.0, "elevation": -70.0},
            {"name": "front", "azimuth": 0.0, "elevation": 0.0},
            {"name": "back", "azimuth": 180.0, "elevation": 0.0},
        ]
    if view_set == "poc-60":
        upper_views: list[dict[str, float | str]] = [
            {
                "name": f"upper_{azimuth:03d}_{elevation:02d}",
                "azimuth": float(azimuth),
                "elevation": float(elevation),
            }
            for azimuth in range(0, 360, 30)
            for elevation in (20, 45, 70, 85)
        ]
        lower_views: list[dict[str, float | str]] = [
            {
                "name": f"lower_{azimuth:03d}",
                "azimuth": float(azimuth),
                "elevation": -70.0,
            }
            for azimuth in range(0, 360, 60)
        ]
        side_views: list[dict[str, float | str]] = [
            {
                "name": f"side_{azimuth:03d}",
                "azimuth": float(azimuth),
                "elevation": 0.0,
            }
            for azimuth in range(0, 360, 60)
        ]
        return upper_views + lower_views + side_views
    raise ValueError(f"Unknown view set: {view_set}.")
