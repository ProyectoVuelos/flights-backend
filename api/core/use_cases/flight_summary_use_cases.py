from typing import Optional
from api.core.domain.flight_summary import FlightSummary
from api.core.ports.flight_port import FlightPort


class GetFlightSummaryUseCase:
    def __init__(self, flight_port: FlightPort):
        self.flight_port = flight_port

    def execute(self) -> Optional[FlightSummary]:
        summary_data = self.flight_port.get_summary_metrics()

        if not summary_data:
            return None

        return FlightSummary(
            total_flights=int(summary_data.get('total_flights', 0)),
            avg_distance=float(summary_data.get('avg_distance', 0.0)),
            total_fuel_saving=float(
                summary_data.get('total_fuel_saving', 0.0)),
            total_co2_saving=float(summary_data.get('total_co2_saving', 0.0))
        )
