from typing import List

from api.core.domain.flight_position import FlightPosition
from api.core.ports.flight_position_port import FlightPositionPort


class FlightPositionUseCase:
    """
    Application logic for managing flight position data.
    """

    def __init__(self, position_port: FlightPositionPort) -> None:
        """
        Initializes the use case with a concrete implementation of the FlightPositionPort.
        """
        self.position_port: FlightPositionPort = position_port

    def add_positions_to_flight(
        self, flight_id: int, positions: List[FlightPosition]
    ) -> bool:
        """
        Adds a batch of position data to a specific flight.
        Returns True on success, False on failure.
        """
        return self.position_port.add_positions(flight_id, positions)

    def get_positions_for_flight(self, flight_id: int) -> List[FlightPosition]:
        """
        Retrieves all position data for a specific flight.
        """
        return self.position_port.get_positions_by_flight_id(flight_id)

    def delete_positions_for_flight(self, flight_id: int) -> bool:
        """
        Deletes all position data associated with a specific flight.
        Returns True on success, False on failure.
        """
        return self.position_port.delete_positions_by_flight_id(flight_id)
