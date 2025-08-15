from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class FlightQueryFilters(BaseModel):
    search: Optional[str] = Field(
        None, description="Search term for flight, fr24_id, or callsign."
    )
    airport: Optional[str] = Field(
        None, description="Filter by departure or arrival airport ICAO code."
    )
    aircraft_model: Optional[str] = Field(None, description="Filter by aircraft model.")
    flight_date: Optional[date] = Field(
        None, description="Filter by flight date (YYYY-MM-DD)."
    )
    limit: int = Field(100, ge=1, le=1000, description="Number of records to return.")
    offset: int = Field(
        0, ge=0, description="Number of records to skip for pagination."
    )
