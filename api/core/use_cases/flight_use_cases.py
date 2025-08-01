from typing import List

from api.core.domain.flight import Flight
from api.core.exceptions.flights_exceptions import FlightNotFoundError
from api.core.ports.flight_port import FlightPort


class FlightUseCase:
    """
    Application logic for managing flights.
    This class orchestrates business operations using a FlightPort.
    """

    def __init__(self, flight_port: FlightPort) -> None:
        """
        Initializes the use case with a concrete implementation of the FlightPort.
        This is a form of dependency injection.
        """
        self.flight_port: FlightPort = flight_port

    def add_new_flight(self, new_flight: Flight) -> Flight:
        """
        Adds a new flight record to the system.
        Returns the Flight object, which may now contain a database-generated ID.
        """
        return self.flight_port.add(new_flight)

    def get_flight_by_id(self, flight_id: int) -> Flight:
        """
        Retrieves a flight record by its internal database ID.
        Raises FlightNotFoundError if the flight does not exist.
        """
        flight = self.flight_port.get_by_id(flight_id)
        if flight is None:
            raise FlightNotFoundError(f"Flight with id: {flight_id} not found.")
        return flight

    def get_flight_by_fr24_id(self, fr24_id: str) -> Flight:
        """
        Retrieves a flight record by its unique FlightRadar24 ID.
        Raises FlightNotFoundError if the flight does not exist.
        """
        flight = self.flight_port.get_by_fr24_id(fr24_id)
        if flight is None:
            raise FlightNotFoundError(f"Flight with FR24 ID: {fr24_id} not found.")
        return flight

    def get_all_flights(self) -> List[Flight]:
        """
        Retrieves all flight records in the system.
        """
        return self.flight_port.find_all()
