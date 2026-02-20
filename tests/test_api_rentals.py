import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime, timezone
from api.api import app
from api.factories import get_db, car_service_factory, rental_service_factory
from db.rental_model import Rental
from services.rental_service import RentalService
from services.interfaces.rental_service_interface import IRentalService
from services.interfaces.car_service_interface import ICarService

mock_car_service: Mock = Mock(spec=ICarService)
mock_rental_service: Mock = Mock(spec=IRentalService)

def override_get_db() -> None:
    """Mock the DB dependency so no connection is attempted."""
    pass

def override_rental_service_factory() -> Mock:
    """Mock the factory to return our controlled mocked service."""
    return mock_rental_service

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[rental_service_factory] = override_rental_service_factory

client: TestClient = TestClient(app)

def test_api_create_rental_success() -> None:
    """
    API Endpoint: Successfully create a rental.
    
    This acts as our end-to-end integration test. It mocks the service layer
    and ensures that the router correctly translates a well-formed JSON payload 
    into a successful 201 HTTP response with serialized data.
    """
    # Setup
    car_id = uuid4()
    rental_id = uuid4()
    mock_rental = Rental(id=rental_id, car_id=car_id, customer_name="Moshe Binieli", start_date=datetime.now(timezone.utc), created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    mock_rental_service.create_rental.return_value = mock_rental
    
    # Act
    payload = {"car_id": str(car_id), "customer_name": "Moshe Binieli"}
    response = client.post("/rentals", json=payload)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == str(rental_id)
    assert data["car_id"] == str(car_id)
    assert data["customer_name"] == "Moshe Binieli"
    mock_rental_service.create_rental.assert_called_once_with(car_id=car_id, customer_name="Moshe Binieli")

def test_api_create_rental_invalid_input() -> None:
    """
    API Endpoint: Fail to create rental on invalid input (Pydantic failure).
    
    Ensures that our Pydantic schema validation correctly intercepts bad inputs
    (like an empty customer name violating the min_length constraint) 
    and returns an HTTP 422 before ever reaching the service layer.
    """
    # Act
    payload = {"car_id": str(uuid4()), "customer_name": ""}
    response = client.post("/rentals", json=payload)
    
    # Assert
    assert response.status_code == 422
