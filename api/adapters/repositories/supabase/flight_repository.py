from datetime import date, datetime, timedelta
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
                return Flight.from_db_row(response.data[0])
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
                return Flight.from_db_row(response.data)
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
                return Flight.from_db_row(response.data)
            return None
        except Exception as e:
            print(f"Error retrieving flight by FR24 ID '{fr24_id}': {e}")
            return None

    def find_all(
        self,
        search: Optional[str] = None,
        airport: Optional[str] = None,
        aircraft_model: Optional[str] = None,
        flight_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Flight]:
        """
        Retrieves a filtered and paginated list of flight records by dynamically building the query.
        """
        try:
            query = self.supabase.table("flights").select("*")

            if search:
                search_term = f"%{search}%"
                or_query = f"flight.ilike.{search_term},fr24_id.ilike.{search_term},callsign.ilike.{search_term}"
                query = query.or_(or_query)

            if airport:
                airport_term = f"%{airport.upper()}%"
                or_query = f"departure_icao.ilike.{airport_term},arrival_icao.ilike.{airport_term}"
                query = query.or_(or_query)

            if aircraft_model:
                query = query.ilike("aircraft_model", f"%{aircraft_model}%")

            if flight_date:
                start_of_day = datetime.combine(flight_date, datetime.min.time())
                end_of_day = start_of_day + timedelta(days=1)
                query = query.gte("departure_time_utc", start_of_day.isoformat())
                query = query.lt("departure_time_utc", end_of_day.isoformat())

            response: PostgrestAPIResponse = query.range(
                offset, offset + limit - 1
            ).execute()

            if response.data:
                return [Flight.from_db_row(data) for data in response.data]
            return []

        except Exception as e:
            print(f"Error retrieving all flights with filters: {e}")
            return []

    def get_summary_metrics(self) -> Optional[dict]:
        """
        Llama a la función de la base de datos para obtener las métricas de resumen.
        """
        try:
            response: PostgrestAPIResponse = self.supabase.rpc(
                "get_flight_summary_metrics", {}
            ).execute()

            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error retrieving summary metrics: {e}")
            return None
