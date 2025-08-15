from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Flight:
    """
    Representa un registro de vuelo, alineado con la tabla final de la base de datos.
    """

    # --- Campos Actualizados ---
    fr24_id: str
    flight: Optional[str] = None
    callsign: Optional[str] = None
    aircraft_model: Optional[str] = None
    aircraft_reg: Optional[str] = None
    departure_icao: Optional[str] = None
    arrival_icao: Optional[str] = None
    distance_calculated_km: Optional[float] = None
    great_circle_distance_km: Optional[float] = None

    # Tiempos de Vuelo (Añadidos)
    departure_time_utc: Optional[datetime] = None
    arrival_time_utc: Optional[datetime] = None
    flight_duration_s: Optional[int] = None

    # Duraciones de Fase (sin cambios)
    duration_takeoff_s: Optional[int] = None
    duration_climb_s: Optional[int] = None
    duration_cruise_s: Optional[int] = None
    duration_descent_s: Optional[int] = None
    duration_landing_s: Optional[int] = None

    # Estimaciones de Combustible (sin cambios)
    fuel_takeoff_kg: Optional[float] = None
    fuel_climb_kg: Optional[float] = None
    fuel_cruise_kg: Optional[float] = None
    fuel_descent_kg: Optional[float] = None
    fuel_landing_kg: Optional[float] = None

    # Estimaciones de CO2 (sin cambios)
    co2_takeoff_kg: Optional[float] = None
    co2_climb_kg: Optional[float] = None
    co2_cruise_kg: Optional[float] = None
    co2_descent_kg: Optional[float] = None
    co2_landing_kg: Optional[float] = None
    co2_total_kg: Optional[float] = None
    co2_per_passenger_kg: Optional[float] = None

    # Metadatos de la Base de Datos
    flight_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """
        Convierte la instancia a un diccionario, formateando las fechas como texto ISO 8601.
        """
        data = asdict(self)
        if "flight_id" in data and data["flight_id"] is None:
            del data["flight_id"]

        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Flight":
        """
        Crea una instancia de Flight desde un diccionario (ej. de la base de datos).
        """
        for key in [
            "created_at",
            "last_updated",
            "departure_time_utc",
            "arrival_time_utc",
        ]:
            if key in data and data[key] and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key])
        return Flight(**data)
