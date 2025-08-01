from typing import List, Optional

from supabase import Client, PostgrestAPIResponse, create_client

from api.core.domain.flight import Flight
from api.core.ports.flight_port import FlightPort
from api.utils.env_manager import settings


class SupabaseFlightRepository(FlightPort):
    """
    Supabase adapter for the FlightPort interface.
    This class is responsible for all low-level Supabase interactions related to the 'flights' table.
    """

    def __init__(self):
        """
        Initializes the Supabase client using environment variables.
        """
        self.supabase: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )

    def add(self, new_flight: Flight) -> Optional[Flight]:
        """
        Adds a new flight record to the 'flights' table.
        Returns the created Flight object with its new database ID, or None on failure.
        """
        try:
            response: PostgrestAPIResponse = (
                self.supabase.table("flights").insert(new_flight.to_dict()).execute()
            )

            if response.data:
                return Flight.from_dict(response.data[0])
            return None

        except Exception as e:
            print(f"Error adding flight to Supabase: {e}")
            return None

    def get_by_id(self, flight_id: int) -> Optional[Flight]:
        """
        Retrieves a single flight by its internal database ID.
        """
        try:
            response: PostgrestAPIResponse = (
                self.supabase.table("flights")
                .select("*")
                .eq("flight_id", flight_id)
                .single()
                .execute()
            )

            if response.data:
                return Flight.from_dict(response.data)
            return None
        except Exception as e:
            print(f"Error retrieving flight by ID '{flight_id}': {e}")
            return None

    def get_by_fr24_id(self, fr24_id: str) -> Optional[Flight]:
        """
        Retrieves a single flight record by its FlightRadar24 unique ID.
        """
        try:
            response: PostgrestAPIResponse = (
                self.supabase.table("flights")
                .select("*")
                .eq("fr24_id", fr24_id)
                .single()
                .execute()
            )

            if response.data:
                return Flight.from_dict(response.data)
            return None
        except Exception as e:
            print(f"Error retrieving flight by FR24 ID '{fr24_id}': {e}")
            return None

    def find_all(self) -> List[Flight]:
        """
        Retrieves a list of all flight records.
        """
        try:
            response: PostgrestAPIResponse = (
                self.supabase.table("flights").select("*").execute()
            )

            if response.data:
                return [Flight.from_dict(data) for data in response.data]
            return []
        except Exception as e:
            print(f"Error retrieving all flights: {e}")
            return []
