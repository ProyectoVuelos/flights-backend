from abc import ABC, abstractmethod
from typing import List, Optional

from api.core.domain.flight import Flight


class FlightPort(ABC):
    """
    An abstract base class (port) that defines the contract for
    interacting with flight data. Concrete implementations (adapters)
    will fulfill this contract, such as a Supabase repository.
    """

    @abstractmethod
    def add(self, new_flight: Flight) -> Optional[Flight]:
        """
        Adds a new flight record. Returns the added flight object,
        potentially with a new database-generated ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, flight_id: int) -> Optional[Flight]:
        """
        Retrieves a single flight record by its internal database ID.
        Returns None if no flight is found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_fr24_id(self, fr24_id: str) -> Optional[Flight]:
        """
        Retrieves a single flight record by its FlightRadar24 unique ID.
        Returns None if no flight is found.
        """
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Flight]:
        """
        Retrieves a list of all flight records.
        """
        raise NotImplementedError
