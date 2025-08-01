from typing import List

from supabase import Client, PostgrestAPIResponse, create_client

from api.core.domain.flight_position import FlightPosition
from api.core.ports.flight_position_port import FlightPositionPort
from api.utils.env_manager import settings


class SupabaseFlightPositionRepository(FlightPositionPort):
    """
    Supabase adapter for the FlightPositionPort interface.
    This class handles database interactions for the 'flight_positions' table.
    """

    def __init__(self):
        """
        Initializes the Supabase client using environment variables.
        """
        self.supabase: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )

    def add_positions(self, flight_id: int, positions: List[FlightPosition]) -> bool:
        """
        Adds a list of flight positions associated with a given flight ID.
        """
        try:
            data_to_insert = [
                {**pos.to_dict(), "flight_id": flight_id} for pos in positions
            ]

            response: PostgrestAPIResponse = (
                self.supabase.table("flight_positions").insert(data_to_insert).execute()
            )

            return bool(response.data)
        except Exception as e:
            print(f"Error adding flight positions for flight ID '{flight_id}': {e}")
            return False

    def get_positions_by_flight_id(self, flight_id: int) -> List[FlightPosition]:
        """
        Retrieves all flight positions for a specific flight ID.
        """
        try:
            response: PostgrestAPIResponse = (
                self.supabase.table("flight_positions")
                .select("*")
                .eq("flight_id", flight_id)
                .execute()
            )

            if response.data:
                return [FlightPosition.from_dict(data) for data in response.data]
            return []
        except Exception as e:
            print(f"Error retrieving flight positions for flight ID '{flight_id}': {e}")
            return []

    def delete_positions_by_flight_id(self, flight_id: int) -> bool:
        """
        Deletes all flight positions for a specific flight ID.
        """
        try:
            self.supabase.table("flight_positions").delete().eq(
                "flight_id", flight_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting flight positions for flight ID '{flight_id}': {e}")
            return False
