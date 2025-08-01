from unittest.mock import MagicMock, patch

from api.core.exceptions.flights_exceptions import FlightNotFoundError


@patch("api.adapters.routes.flight_routes.flight_service")
def test_create_flight_success(mock_flight_service, client, sample_flight):
    """Test that a new flight can be created successfully."""
    mock_flight_service.add_new_flight.return_value = sample_flight

    flight_data = sample_flight.to_dict()

    response = client.post("/flights", json=flight_data)

    assert response.status_code == 201
    assert "message" in response.json()
    assert "created successfully" in response.json()["message"]
    mock_flight_service.add_new_flight.assert_called_once()


@patch("api.adapters.routes.flight_routes.flight_service")
def test_create_flight_failure(mock_flight_service, client, sample_flight):
    """Test that a 500 error is returned if the service fails to create a flight."""
    mock_flight_service.add_new_flight.return_value = None
    flight_data = sample_flight.to_dict()

    response = client.post("/flights", json=flight_data)

    assert response.status_code == 400
    assert "Failed to create flight" in response.json()["detail"]


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_all_flights_success(mock_flight_service, client, sample_flight):
    """Test retrieving a list of all flights."""
    mock_flight_service.get_all_flights.return_value = [sample_flight]

    response = client.get("/flights")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["fr24_id"] == "A1B2C3D4"


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_flight_by_id_success(mock_flight_service, client, sample_flight):
    """Test retrieving a single flight by its ID."""
    mock_flight_service.get_flight_by_id.return_value = sample_flight

    response = client.get("/flights/1")

    assert response.status_code == 200
    assert response.json()["flight_id"] == 1
    assert response.json()["fr24_id"] == "A1B2C3D4"


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_flight_by_id_not_found(mock_flight_service, client):
    """Test that a 404 error is returned for a non-existent flight ID."""
    mock_flight_service.get_flight_by_id.side_effect = FlightNotFoundError(
        "Flight not found."
    )

    response = client.get("/flights/999")

    assert response.status_code == 404
    assert "Flight not found" in response.json()["detail"]


@patch("api.adapters.routes.flight_routes.flight_service")
@patch("api.adapters.routes.flight_routes.position_service")
def test_get_flight_positions_success(
    mock_position_service, mock_flight_service, client, sample_positions
):
    """Test retrieving all positions for a flight."""
    mock_flight_service.get_flight_by_id.return_value = MagicMock()
    mock_position_service.get_positions_for_flight.return_value = sample_positions

    response = client.get("/flights/1/positions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    assert response.json()[0]["latitude"] == 34.0522


@patch("api.adapters.routes.flight_routes.flight_service")
@patch("api.adapters.routes.flight_routes.position_service")
def test_delete_flight_positions_success(
    mock_position_service, mock_flight_service, client
):
    """Test deleting all positions for a flight."""
    mock_flight_service.get_flight_by_id.return_value = MagicMock()
    mock_position_service.delete_positions_for_flight.return_value = True

    response = client.delete("/flights/1/positions")

    assert response.status_code == 200
    assert "message" in response.json()
    assert "deleted successfully" in response.json()["message"]
