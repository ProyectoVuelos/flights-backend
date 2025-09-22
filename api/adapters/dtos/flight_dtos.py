from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.core.domain.flight import (
    DetailedCalculation,
    EmissionComparison,
    Flight,
    PhaseDurations,
    StatisticalSimulation,
)


class PhaseDurationsDTO(BaseModel):
    """DTO para el objeto 'phase_durations_s'."""
    takeoff: Optional[int] = Field(
        0, description="Takeoff duration in seconds.")
    climb: Optional[int] = Field(0, description="Climb duration in seconds.")
    cruise: Optional[int] = Field(0, description="Cruise duration in seconds.")
    descent: Optional[int] = Field(
        0, description="Descent duration in seconds.")
    landing: Optional[int] = Field(
        0, description="Landing duration in seconds.")


class DetailedCalculationDTO(BaseModel):
    """DTO para el objeto 'detailed_calculation'."""
    total_fuel_kg: Optional[float] = Field(None)
    co2_total_kg: Optional[float] = Field(None)
    co2_per_passenger_kg: Optional[float] = Field(None)
    total_climate_impact_co2e_per_pax_kg: Optional[float] = Field(None)
    efficiency_kg_pax_km: Optional[float] = Field(None)


class StatisticalSimulationDTO(BaseModel):
    """DTO para el objeto 'statistical_simulation'."""
    total_fuel_kg: Optional[float] = Field(None)
    co2_per_passenger_kg: Optional[float] = Field(None)
    total_climate_impact_co2e_per_pax_kg: Optional[float] = Field(None)
    efficiency_kg_pax_km: Optional[float] = Field(None)


class EmissionComparisonDTO(BaseModel):
    """DTO para el objeto principal 'emission_comparison'."""
    detailed_calculation: DetailedCalculationDTO
    statistical_simulation: StatisticalSimulationDTO


class FlightPostRequest(BaseModel):
    """DTO for creating or updating a flight record via API."""

    fr24_id: str = Field(...,
                         description="The unique ID from the FlightRadar24 API.")
    flight: Optional[str] = Field(
        None, description="Flight number, e.g., 'UAL173'.")
    callsign: Optional[str] = Field(
        None, description="Flight callsign, e.g., 'SWA2914'.")
    aircraft_model: Optional[str] = Field(None, description="Aircraft model.")
    aircraft_reg: Optional[str] = Field(
        None, description="Aircraft registration.")
    departure_icao: Optional[str] = Field(
        None, description="4-letter ICAO airport code for departure.")
    arrival_icao: Optional[str] = Field(
        None, description="4-letter ICAO airport code for arrival.")
    distance_calculated_km: Optional[float] = Field(
        None, description="Calculated flight distance in kilometers.")
    great_circle_distance_km: Optional[float] = Field(
        None, description="Geodesic distance in kilometers.")
    departure_time_utc: Optional[datetime] = Field(
        None, description="Actual departure time in UTC.")
    arrival_time_utc: Optional[datetime] = Field(
        None, description="Actual arrival time in UTC.")
    flight_duration_s: Optional[int] = Field(
        None, description="Total flight duration in seconds.")

    phase_durations_s: Optional[PhaseDurationsDTO] = Field(None)
    emission_comparison: Optional[EmissionComparisonDTO] = Field(None)

    def to_domain_model(self) -> Flight:
        """
        Converts the DTO with its nested models to the core Flight domain model with its nested dataclasses.
        """
        main_data = self.model_dump(
            exclude={'phase_durations_s', 'emission_comparison'})

        phase_durations_obj = None
        if self.phase_durations_s:
            phase_durations_obj = PhaseDurations(
                **self.phase_durations_s.model_dump())

        emission_comparison_obj = None
        if self.emission_comparison:
            detailed_obj = DetailedCalculation(
                **self.emission_comparison.detailed_calculation.model_dump())
            stats_obj = StatisticalSimulation(
                **self.emission_comparison.statistical_simulation.model_dump())
            emission_comparison_obj = EmissionComparison(
                detailed_calculation=detailed_obj,
                statistical_simulation=stats_obj
            )

        return Flight(
            **main_data,
            phase_durations_s=phase_durations_obj,
            emission_comparison=emission_comparison_obj
        )
