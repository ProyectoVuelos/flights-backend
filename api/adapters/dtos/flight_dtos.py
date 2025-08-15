from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.core.domain.flight import Flight


class FlightPostRequest(BaseModel):
    """DTO for creating a new flight record via API."""

    fr24_id: str = Field(..., description="The unique ID from the FlightRadar24 API.")
    flight: Optional[str] = Field(None, description="Flight number, e.g., 'UAL173'.")
    callsign: Optional[str] = Field(
        None, description="Flight callsign, e.g., 'SWA2914'."
    )
    aircraft_model: Optional[str] = Field(None, description="Aircraft model.")
    aircraft_reg: Optional[str] = Field(
        None, description="Aircraft registration, e.g., 'N123UA'."
    )

    departure_icao: Optional[str] = Field(
        None, description="4-letter ICAO airport code for departure."
    )
    arrival_icao: Optional[str] = Field(
        None, description="4-letter ICAO airport code for arrival."
    )
    distance_calculated_km: Optional[float] = Field(
        None, description="Calculated flight distance in kilometers."
    )
    great_circle_distance_km: Optional[float] = Field(
        None, description="Geodesic distance in kilometers."
    )
    departure_time_utc: Optional[datetime] = Field(
        None, description="Actual departure time in UTC."
    )
    arrival_time_utc: Optional[datetime] = Field(
        None, description="Actual arrival time in UTC."
    )
    flight_duration_s: Optional[int] = Field(
        None, description="Total flight duration in seconds."
    )

    duration_takeoff_s: Optional[int] = Field(
        None, description="Duration of takeoff phase in seconds."
    )
    duration_climb_s: Optional[int] = Field(
        None, description="Duration of climb phase in seconds."
    )
    duration_cruise_s: Optional[int] = Field(
        None, description="Duration of cruise phase in seconds."
    )
    duration_descent_s: Optional[int] = Field(
        None, description="Duration of descent phase in seconds."
    )
    duration_landing_s: Optional[int] = Field(
        None, description="Duration of landing phase in seconds."
    )

    fuel_takeoff_kg: Optional[float] = Field(
        None, description="Fuel consumption during takeoff in kg."
    )
    fuel_climb_kg: Optional[float] = Field(
        None, description="Fuel consumption during climb in kg."
    )
    fuel_cruise_kg: Optional[float] = Field(
        None, description="Fuel consumption during cruise in kg."
    )
    fuel_descent_kg: Optional[float] = Field(
        None, description="Fuel consumption during descent in kg."
    )
    fuel_landing_kg: Optional[float] = Field(
        None, description="Fuel consumption during landing in kg."
    )

    co2_takeoff_kg: Optional[float] = Field(
        None, description="CO2 emissions during takeoff in kg."
    )
    co2_climb_kg: Optional[float] = Field(
        None, description="CO2 emissions during climb in kg."
    )
    co2_cruise_kg: Optional[float] = Field(
        None, description="CO2 emissions during cruise in kg."
    )
    co2_descent_kg: Optional[float] = Field(
        None, description="CO2 emissions during descent in kg."
    )
    co2_landing_kg: Optional[float] = Field(
        None, description="CO2 emissions during landing in kg."
    )
    co2_total_kg: Optional[float] = Field(
        None, description="Total CO2 emissions in kg."
    )
    co2_per_passenger_kg: Optional[float] = Field(
        None, description="CO2 per passenger in kg."
    )

    def to_domain_model(self) -> Flight:
        """Converts the DTO to a core domain model."""
        return Flight(**self.model_dump())
