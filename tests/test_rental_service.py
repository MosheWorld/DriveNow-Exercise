import pytest
from unittest.mock import Mock
from uuid import uuid4
from db.car_model import Car, CarStatus
from db.rental_model import Rental
from common.exceptions import NotFoundException, CarStatusUnavailableException, InputValidationException, RentalAlreadyEndedException
from services.rental_service import RentalService
from repositories.interfaces.car_repository_interface import ICarRepository
from repositories.interfaces.rental_repository_interface import IRentalRepository
from services.interfaces.metrics_service_interface import IMetricsService
from common.interfaces.logger_interface import ILogger

@pytest.fixture
def mock_logger() -> Mock:
    """Fixture for mocking the Logger interface."""
    return Mock(spec=ILogger)

@pytest.fixture
def mock_metrics() -> Mock:
    """Fixture for mocking the Metrics Service interface."""
    return Mock(spec=IMetricsService)

@pytest.fixture
def mock_car_repo() -> Mock:
    """Fixture for mocking the Car Repository interface."""
    return Mock(spec=ICarRepository)

@pytest.fixture
def mock_rental_repo() -> Mock:
    """Fixture for mocking the Rental Repository interface."""
    return Mock(spec=IRentalRepository)

@pytest.fixture
def rental_service(mock_logger: Mock, mock_metrics: Mock, mock_rental_repo: Mock, mock_car_repo: Mock) -> RentalService:
    """Fixture that provides a RentalService instance injected with mocked dependencies."""
    return RentalService(
        logger=mock_logger,
        metrics=mock_metrics,
        rental_repository=mock_rental_repo,
        car_repository=mock_car_repo
    )

def test_create_rental_success(rental_service: RentalService, mock_car_repo: Mock, mock_rental_repo: Mock, mock_metrics: Mock) -> None:
    """
    Successfully create a new rental.
    
    Verifies that providing valid inputs for an available car will properly
    create the rental, change the car status to IN_USE, and update metrics.
    """
    # Setup
    car_id = uuid4()
    mock_car = Car(id=car_id, model="Kia", status=CarStatus.AVAILABLE)
    mock_car_repo.get_by_id.return_value = mock_car
    
    expected_rental = Rental(id=uuid4(), car_id=car_id, customer_name="Moshe Binieli")
    mock_rental_repo.create.return_value = expected_rental

    # Act
    rental = rental_service.create_rental(car_id=car_id, customer_name="Moshe Binieli")

    # Assert
    assert rental == expected_rental
    assert mock_car.status == CarStatus.IN_USE
    mock_car_repo.get_by_id.assert_called_once_with(car_id)
    mock_car_repo.update.assert_called_once_with(mock_car)
    mock_rental_repo.create.assert_called_once_with(car_id=car_id, customer_name="Moshe Binieli")
    mock_metrics.decrement_active_cars.assert_called_once()
    mock_metrics.increment_ongoing_rentals.assert_called_once()

def test_create_rental_empty_customer_name(rental_service: RentalService) -> None:
    """
    Fail to create a rental with an empty customer name.
    
    Verifies that our domain logic rejects empty customer names with an
    InputValidationException before hitting repositories.
    """
    # Setup / Act / Assert
    with pytest.raises(InputValidationException) as exc_info:
        rental_service.create_rental(car_id=uuid4(), customer_name="   ")
    assert "Customer name cannot be empty" in str(exc_info.value)

def test_create_rental_car_not_found(rental_service: RentalService, mock_car_repo: Mock) -> None:
    """
    Fail to create a rental when the target car does not exist.
    
    Verifies that a NotFoundException is raised if the car repository returns None.
    """
    # Setup
    car_id = uuid4()
    mock_car_repo.get_by_id.return_value = None

    # Act / Assert
    with pytest.raises(NotFoundException) as exc_info:
        rental_service.create_rental(car_id=car_id, customer_name="Moshe Binieli")
    assert f"Car {car_id} not found" in str(exc_info.value)

def test_create_rental_car_not_available(rental_service: RentalService, mock_car_repo: Mock) -> None:
    """
    Fail to create a rental when the target car is already in use.
    
    Verifies that a CarStatusUnavailableException is raised if the car is currently
    not in the AVAILABLE status.
    """
    # Setup
    car_id = uuid4()
    mock_car_repo.get_by_id.return_value = Car(id=car_id, model="Kia", status=CarStatus.IN_USE)

    # Act / Assert
    with pytest.raises(CarStatusUnavailableException) as exc_info:
        rental_service.create_rental(car_id=car_id, customer_name="Moshe Binieli")
    assert "Car is not available for rent" in str(exc_info.value)

def test_get_all_rentals(rental_service: RentalService, mock_rental_repo: Mock) -> None:
    """
    Successfully retrieve a list of all rentals.
    
    Verifies that the service simply delegates to the repository correctly.
    """
    # Setup
    mock_rentals = [Rental(id=uuid4(), car_id=uuid4(), customer_name="Moshe"), Rental(id=uuid4(), car_id=uuid4(), customer_name="Binieli")]
    mock_rental_repo.get_all.return_value = mock_rentals
    
    # Act
    rentals = rental_service.get_all_rentals()
    
    # Assert
    assert rentals == mock_rentals
    mock_rental_repo.get_all.assert_called_once()

def test_end_rental_success(rental_service: RentalService, mock_car_repo: Mock, mock_rental_repo: Mock, mock_metrics: Mock) -> None:
    """
    Successfully ends an ongoing rental.
    
    Verifies that the service retrieves the car and rental, marks the car as
    AVAILABLE, ends the rental in the DB, and flips the metrics appropriately.
    """
    # Setup
    car_id = uuid4()
    mock_car = Car(id=car_id, model="Kia", status=CarStatus.IN_USE)
    mock_car_repo.get_by_id.return_value = mock_car
    
    mock_active_rental = Rental(id=uuid4(), car_id=car_id, customer_name="Moshe Binieli")
    mock_rental_repo.get_active_rental_by_car_id.return_value = mock_active_rental
    
    # Act
    ended_rental = rental_service.end_rental_by_car_id(car_id)
    
    # Assert
    assert ended_rental == mock_active_rental
    assert mock_car.status == CarStatus.AVAILABLE
    mock_car_repo.get_by_id.assert_called_once_with(car_id)
    mock_rental_repo.get_active_rental_by_car_id.assert_called_once_with(car_id)
    mock_rental_repo.end_rental.assert_called_once_with(mock_active_rental)
    mock_car_repo.update.assert_called_once_with(mock_car)
    mock_metrics.increment_active_cars.assert_called_once()
    mock_metrics.decrement_ongoing_rentals.assert_called_once()

def test_end_rental_car_not_found(rental_service: RentalService, mock_car_repo: Mock) -> None:
    """
    Fail to end a rental if the target car doesn't exist.
    """
    # Setup
    car_id = uuid4()
    mock_car_repo.get_by_id.return_value = None
    
    # Act / Assert
    with pytest.raises(NotFoundException) as exc_info:
        rental_service.end_rental_by_car_id(car_id)
    assert f"Car {car_id} not found" in str(exc_info.value)

def test_end_rental_active_rental_not_found(rental_service: RentalService, mock_car_repo: Mock, mock_rental_repo: Mock) -> None:
    """
    Fail to end a rental if the car exists but has no ongoing rental associated.
    """
    # Setup
    car_id = uuid4()
    mock_car_repo.get_by_id.return_value = Car(id=car_id, model="Kia", status=CarStatus.IN_USE)
    mock_rental_repo.get_active_rental_by_car_id.return_value = None
    
    # Act / Assert
    with pytest.raises(NotFoundException) as exc_info:
        rental_service.end_rental_by_car_id(car_id)
    assert f"No active rental found for car {car_id}" in str(exc_info.value)

def test_end_rental_already_ended(rental_service: RentalService, mock_car_repo: Mock, mock_rental_repo: Mock) -> None:
    """
    Fail to end a rental if the active rental retrieved strangely has an end_date.
    
    This guards against data inconsistency states.
    """
    from datetime import datetime
    
    # Setup
    car_id = uuid4()
    mock_car_repo.get_by_id.return_value = Car(id=car_id, model="Kia", status=CarStatus.IN_USE)
    
    ended_rental = Rental(id=uuid4(), car_id=car_id, customer_name="Moshe Binieli", end_date=datetime.now())
    mock_rental_repo.get_active_rental_by_car_id.return_value = ended_rental
    
    # Act / Assert
    with pytest.raises(RentalAlreadyEndedException) as exc_info:
        rental_service.end_rental_by_car_id(car_id)
    assert "Rental already ended" in str(exc_info.value)
