from pydantic import BaseModel, Field
from api.core.domain.flight_summary import FlightSummary


class FlightSummaryResponse(BaseModel):
    """DTO para la respuesta del endpoint de resumen de vuelos."""
    total_flights: int = Field(..., description="Total de vuelos registrados.")
    avg_distance: float = Field(...,
                                description="Distancia promedio de los vuelos en km.")
    total_fuel_saving: float = Field(
        ..., description="Ahorro total de combustible (kg) vs. simulación.")
    total_co2_saving: float = Field(
        ..., description="Ahorro total de CO2 por pasajero (kg) vs. simulación.")

    @staticmethod
    def from_domain(summary: FlightSummary) -> "FlightSummaryResponse":
        return FlightSummaryResponse(**summary.__dict__)
