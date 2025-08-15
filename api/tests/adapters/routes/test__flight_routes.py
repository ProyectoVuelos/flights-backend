from unittest.mock import patch

from api.core.exceptions.flights_exceptions import FlightNotFoundError


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_all_flights_success(mock_flight_service, client, sample_flight):
    """
    Test que al obtener todos los vuelos se devuelve la estructura de respuesta correcta.
    """
    mock_flight_service.get_all_flights.return_value = [sample_flight.to_dict()]

    response = client.get("/api/v1/flights")

    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert "data" in json_response
    assert isinstance(json_response["data"], list)
    assert len(json_response["data"]) == 1
    assert json_response["data"][0]["fr24_id"] == sample_flight.fr24_id


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_all_flights_with_filters(mock_flight_service, client):
    """
    Test que los filtros de la URL se pasan correctamente al servicio.
    """
    mock_flight_service.get_all_flights.return_value = []

    response = client.get("/api/v1/flights?airport=JFK&limit=50&offset=10")

    assert response.status_code == 200
    mock_flight_service.get_all_flights.assert_called_once_with(
        search=None,
        airport="JFK",
        aircraft_model=None,
        flight_date=None,
        limit=50,
        offset=10
    )


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_flight_by_id_success(mock_flight_service, client, sample_flight):
    """
    Test que al obtener un vuelo por ID se devuelve el objeto correcto en la estructura estándar.
    """
    mock_flight_service.get_flight_by_id.return_value = sample_flight.to_dict()

    response = client.get(f"/api/v1/flights/{sample_flight.flight_id}")

    assert response.status_code == 200
    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["flight_id"] == sample_flight.flight_id
    assert json_response["data"]["fr24_id"] == sample_flight.fr24_id


@patch("api.adapters.routes.flight_routes.flight_service")
def test_get_flight_by_id_not_found(mock_flight_service, client):
    """
    Test que devuelve un 404 si el servicio lanza FlightNotFoundError.
    """
    mock_flight_service.get_flight_by_id.side_effect = FlightNotFoundError(
        "Flight with id 999 not found."
    )

    response = client.get("/api/v1/flights/999")

    assert response.status_code == 404
    assert "Flight with id 999 not found" in response.json()["detail"]


@patch("api.adapters.routes.flight_routes.flight_service")
def test_create_flight_success(mock_flight_service, client, sample_flight_dict):
    """
    Test que la creación de un vuelo devuelve un 201 y la data correcta.
    """
    mock_flight_service.create_flight.return_value = sample_flight_dict
    
    request_data = {
        "fr24_id": sample_flight_dict["fr24_id"],
        "flight": sample_flight_dict["flight"],
        "departure_icao": sample_flight_dict["departure_icao"],
    }

    response = client.post("/api/v1/flights", json=request_data)

    assert response.status_code == 201
    json_response = response.json()
    assert "message" in json_response
    assert "data" in json_response
    assert json_response["data"]["fr24_id"] == sample_flight_dict["fr24_id"]
    mock_flight_service.create_flight.assert_called_once()
