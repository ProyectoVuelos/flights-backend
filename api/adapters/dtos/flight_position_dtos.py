from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.core.domain.flight_position import FlightPosition


class FlightPositionPostRequest(BaseModel):
    """DTO for creating flight position records."""

    timestamp: datetime = Field(..., description="Timestamp of the position.")
    latitude: float = Field(..., description="Latitude coordinate.")
    longitude: float = Field(..., description="Longitude coordinate.")
    altitude: Optional[int] = Field(None, description="Altitude in meters.")
    ground_speed: Optional[int] = Field(None, description="Ground speed in km/h.")
    vertical_rate: Optional[int] = Field(None, description="Vertical rate in m/s.")

    def to_domain_model(self) -> FlightPosition:
        """Converts the DTO to a core domain model."""
        return FlightPosition(**self.model_dump())
