import json
from typing import List

from fastapi import APIRouter, HTTPException, Response, status

from api.adapters.dtos.flight_dtos import FlightPostRequest
from api.adapters.dtos.flight_position_dtos import FlightPositionPostRequest
from api.adapters.repositories.supabase.flight_position_repository import \
    SupabaseFlightPositionRepository
from api.adapters.repositories.supabase.flight_repository import \
    SupabaseFlightRepository
from api.core.exceptions.flights_exceptions import FlightNotFoundError
from api.core.use_cases.flight_position_use_cases import FlightPositionUseCase
from api.core.use_cases.flight_use_cases import FlightUseCase

flight_repository = SupabaseFlightRepository()
flight_service = FlightUseCase(flight_port=flight_repository)

position_repository = SupabaseFlightPositionRepository()
position_service = FlightPositionUseCase(position_port=position_repository)

flights_router = APIRouter(prefix="/flights", tags=["Flights"])


@flights_router.post("", status_code=status.HTTP_201_CREATED)
def create_flight(new_flight_data: FlightPostRequest) -> Response:
    """
    Creates a new flight record.
    """
    try:
        new_flight = new_flight_data.to_domain_model()
        created_flight = flight_service.add_new_flight(new_flight)
        if not created_flight:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create flight.",
            )

        return Response(
            content=json.dumps(
                {
                    "message": f"Flight with ID {created_flight.flight_id} created successfully!"
                }
            ),
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@flights_router.get("")
def get_all_flights() -> Response:
    """
    Retrieves all flight records.
    """
    try:
        flights = flight_service.get_all_flights()
        flights_dicts = [flight.to_dict() for flight in flights]

        return Response(
            content=json.dumps(flights_dicts),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@flights_router.get("/{flight_id}")
def get_flight_by_id(flight_id: int) -> Response:
    """
    Retrieves a single flight record by its internal database ID.
    """
    try:
        flight = flight_service.get_flight_by_id(flight_id)

        return Response(
            content=json.dumps(flight.to_dict()),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except FlightNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@flights_router.get("/{fr24_id}/fr24")
def get_flight_by_fr24_id(fr24_id: str) -> Response:
    """
    Retrieves a single flight record by its FlightRadar24 ID.
    """
    try:
        flight = flight_service.get_flight_by_fr24_id(fr24_id)

        return Response(
            content=json.dumps(flight.to_dict()),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except FlightNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@flights_router.post("/{flight_id}/positions", status_code=status.HTTP_201_CREATED)
def add_flight_positions(
    flight_id: int, positions: List[FlightPositionPostRequest]
) -> Response:
    """
    Adds a list of flight position records to a specific flight.
    """
    try:
        flight_service.get_flight_by_id(flight_id)

        new_positions = [pos.to_domain_model() for pos in positions]

        success = position_service.add_positions_to_flight(flight_id, new_positions)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add flight positions.",
            )

        return Response(
            content=json.dumps({"message": "Flight positions added successfully."}),
            status_code=status.HTTP_201_CREATED,
        )
    except FlightNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@flights_router.get("/{flight_id}/positions")
def get_flight_positions(flight_id: int) -> Response:
    """
    Retrieves all position data for a specific flight.
    """
    try:
        flight_service.get_flight_by_id(flight_id)
        positions = position_service.get_positions_for_flight(flight_id)
        positions_dicts = [position.to_dict() for position in positions]

        return Response(
            content=json.dumps(positions_dicts),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except FlightNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@flights_router.delete("/{flight_id}/positions", status_code=status.HTTP_200_OK)
def delete_flight_positions(flight_id: int) -> Response:
    """
    Deletes all position data associated with a specific flight.
    """
    try:
        flight_service.get_flight_by_id(flight_id)

        success = position_service.delete_positions_for_flight(flight_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete flight positions.",
            )

        return Response(
            content=json.dumps({"message": "Flight positions deleted successfully."}),
            status_code=status.HTTP_200_OK,
        )
    except FlightNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
