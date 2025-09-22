from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class BaseSchema:
    """Clase base para facilitar la conversión a diccionario."""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PhaseDurations(BaseSchema):
    """Representa el objeto anidado 'phase_durations_s'."""
    takeoff: Optional[int] = 0
    climb: Optional[int] = 0
    cruise: Optional[int] = 0
    descent: Optional[int] = 0
    landing: Optional[int] = 0


@dataclass
class DetailedCalculation(BaseSchema):
    """Representa el objeto 'detailed_calculation'."""
    total_fuel_kg: Optional[float] = None
    co2_total_kg: Optional[float] = None
    co2_per_passenger_kg: Optional[float] = None
    total_climate_impact_co2e_per_pax_kg: Optional[float] = None
    efficiency_kg_pax_km: Optional[float] = None


@dataclass
class StatisticalSimulation(BaseSchema):
    """Representa el objeto 'statistical_simulation'."""
    total_fuel_kg: Optional[float] = None
    co2_per_passenger_kg: Optional[float] = None
    total_climate_impact_co2e_per_pax_kg: Optional[float] = None
    efficiency_kg_pax_km: Optional[float] = None


@dataclass
class EmissionComparison(BaseSchema):
    """Representa el objeto principal 'emission_comparison'."""
    detailed_calculation: Optional[DetailedCalculation] = None
    statistical_simulation: Optional[StatisticalSimulation] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EmissionComparison":
        """Crea una instancia anidada a partir de un diccionario."""
        detailed_data = data.get('detailed_calculation')
        stats_data = data.get('statistical_simulation')

        return EmissionComparison(
            detailed_calculation=DetailedCalculation(
                **detailed_data) if detailed_data else None,
            statistical_simulation=StatisticalSimulation(
                **stats_data) if stats_data else None
        )


@dataclass
class Flight:
    """
    Representa un registro de vuelo, alineado con la nueva estructura de la base de datos.
    """
    fr24_id: str
    flight: Optional[str] = None
    callsign: Optional[str] = None
    aircraft_model: Optional[str] = None
    aircraft_reg: Optional[str] = None
    departure_icao: Optional[str] = None
    arrival_icao: Optional[str] = None
    distance_calculated_km: Optional[float] = None
    great_circle_distance_km: Optional[float] = None
    departure_time_utc: Optional[datetime] = None
    arrival_time_utc: Optional[datetime] = None
    flight_duration_s: Optional[int] = None

    phase_durations_s: Optional[PhaseDurations] = None
    emission_comparison: Optional[EmissionComparison] = None

    flight_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convierte la instancia completa a un diccionario, manejando objetos anidados y fechas."""
        data = asdict(self)
        if "flight_id" in data and data["flight_id"] is None:
            del data["flight_id"]

        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @staticmethod
    def from_db_row(data: Dict[str, Any]) -> "Flight":
        """
        Crea una instancia de Flight desde una fila de la base de datos,
        convirtiendo los JSONB en objetos dataclass.
        """
        for key in ["created_at", "last_updated", "departure_time_utc", "arrival_time_utc"]:
            if key in data and data[key] and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key])

        if 'phase_durations_s' in data and data['phase_durations_s']:
            data['phase_durations_s'] = PhaseDurations(
                **data['phase_durations_s'])

        if 'emission_comparison' in data and data['emission_comparison']:
            data['emission_comparison'] = EmissionComparison.from_dict(
                data['emission_comparison'])

        return Flight(**data)
