from dataclasses import dataclass, asdict


@dataclass
class FlightSummary:
    """Modelo de dominio para el resumen de métricas de vuelos."""
    total_flights: int
    avg_distance: float
    total_fuel_saving: float
    total_co2_saving: float

    def to_dict(self) -> dict:
        """Convierte la instancia de la dataclass a un diccionario."""
        return asdict(self)
