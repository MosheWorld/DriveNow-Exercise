from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from uuid import UUID
from db.car_model import CarStatus
from api.factories import car_service_factory
from services.interfaces.car_service_interface import ICarService
from api.schemas.car_schemas import CarCreate, CarResponse, CarUpdate
from api.common.exceptions import NotFoundException, DatabaseException, InputValidationException

router = APIRouter(prefix="/cars", tags=["cars"])

@router.post("", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate, service: ICarService = Depends(car_service_factory)):
    try:
        return service.create_car(model=car.model, year=car.year, status=car.status)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: UUID, car_update: CarUpdate, service: ICarService = Depends(car_service_factory)):
    try:
        return service.update_car(car_id=car_id, model=car_update.model, year=car_update.year, status=car_update.status)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("", response_model=List[CarResponse])
def get_cars(status: Optional[CarStatus] = None, service: ICarService = Depends(car_service_factory)):
    try:
        return service.get_all_cars(status)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
