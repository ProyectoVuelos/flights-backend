from abc import ABC, abstractmethod
from typing import List, Optional

from api.core.domain.flight_position import FlightPosition


class FlightPositionPort(ABC):
    """
    An abstract base class (port) that defines the contract for
    storing and retrieving flight position data.
    """

    @abstractmethod
    def add_positions(self, flight_id: int, positions: List[FlightPosition]) -> bool:
        """
        Adds a list of flight positions associated with a given flight ID.
        Returns True on success, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_positions_by_flight_id(self, flight_id: int) -> List[FlightPosition]:
        """
        Retrieves all flight positions for a specific flight ID.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_positions_by_flight_id(self, flight_id: int) -> bool:
        """
        Deletes all flight positions for a specific flight ID.
        Returns True on success, False otherwise.
        """
        raise NotImplementedError
