from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class FlightPosition:
    """
    Represents a time-series GPS position for a flight.
    """

    flight_id: int
    timestamp: datetime
    latitude: float
    longitude: float
    altitude: Optional[int] = None
    ground_speed: Optional[int] = None
    vertical_rate: Optional[int] = None

    position_id: Optional[int] = None

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance to a dictionary.
        This is optimized using dataclasses.asdict().
        """
        data = asdict(self)
        if "position_id" in data and data["position_id"] is None:
            del data["position_id"]

        if "timestamp" in data:
            data["timestamp"] = self.timestamp.isoformat()

        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlightPosition":
        """
        Creates a FlightPosition instance from a dictionary (e.g., from a Supabase response).
        """
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return FlightPosition(**data)
