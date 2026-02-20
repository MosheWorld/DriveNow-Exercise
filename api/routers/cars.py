from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from uuid import UUID
from db.car_model import CarStatus
from api.factories import car_service_factory
from services.interfaces.car_service_interface import ICarService
from api.schemas.car_schemas import CarCreate, CarResponse, CarUpdate
from common.exceptions import NotFoundException, DatabaseException, InputValidationException
from common.logger import Logger

router = APIRouter(prefix="/cars", tags=["cars"])
logger = Logger()

@router.post("", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate, service: ICarService = Depends(car_service_factory)):
    """
    Register a new car in the fleet registry.

    This endpoint adds a new vehicle. Validates that the model name is provided 
    and the production year is after 1950.
    """
    try:
        return service.create_car(model=car.model, year=car.year, status=car.status)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        logger.error(f"Database error creating car: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        logger.critical(f"Unexpected error creating car: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: UUID, car_update: CarUpdate, service: ICarService = Depends(car_service_factory)):
    """
    Update details of an existing vehicle.

    Allows modifying the model, year, or current operational status of a car. 
    Verifies that the car exists before applying changes.
    """
    try:
        return service.update_car(car_id=car_id, model=car_update.model, year=car_update.year, status=car_update.status)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseException as e:
        logger.error(f"Database error updating car {car_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        logger.critical(f"Unexpected error updating car {car_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("", response_model=List[CarResponse])
def get_cars(status: Optional[CarStatus] = None, service: ICarService = Depends(car_service_factory)):
    """
    List all vehicles with optional status filtering.

    Retrieves the complete fleet or a subset of vehicles filtered by their 
    current status (available, in_use, or under_maintenance).
    """
    try:
        return service.get_all_cars(status)
    except DatabaseException as e:
        logger.error(f"Database error retrieving cars: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        logger.critical(f"Unexpected error retrieving cars: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
