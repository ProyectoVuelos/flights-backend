from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Flight:
    """
    Represents a flight record.
    """

    fr24_id: str
    flight: Optional[str] = None
    callsign: Optional[str] = None
    aircraft_model: Optional[str] = None
    aircraft_reg: Optional[str] = None
    departure: Optional[str] = None
    arrival: Optional[str] = None
    distance_km: Optional[float] = None
    circle_distance: Optional[float] = None

    # Phase Durations (in seconds)
    duration_takeoff_s: Optional[int] = None
    duration_climb_s: Optional[int] = None
    duration_cruise_s: Optional[int] = None
    duration_descent_s: Optional[int] = None
    duration_landing_s: Optional[int] = None

    # Fuel Estimations (in kg)
    fuel_takeoff_kg: Optional[float] = None
    fuel_climb_kg: Optional[float] = None
    fuel_cruise_kg: Optional[float] = None
    fuel_descent_kg: Optional[float] = None
    fuel_landing_kg: Optional[float] = None

    # CO2 Estimations (in kg)
    co2_takeoff_kg: Optional[float] = None
    co2_climb_kg: Optional[float] = None
    co2_cruise_kg: Optional[float] = None
    co2_descent_kg: Optional[float] = None
    co2_landing_kg: Optional[float] = None
    co2_total_kg: Optional[float] = None
    co2_per_passenger_kg: Optional[float] = None

    # Internal Database ID
    flight_id: Optional[int] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance to a dictionary, suitable for database insertion.
        This is optimized using dataclasses.asdict().
        """
        data = asdict(self)
        if "flight_id" in data and data["flight_id"] is None:
            del data["flight_id"]

        if "created_at" in data:
            data["created_at"] = self.created_at.isoformat()

        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Flight":
        """
        Creates a Flight instance from a dictionary (e.g., from a Supabase response).
        """
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return Flight(**data)
