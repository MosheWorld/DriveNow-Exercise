from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID
from api.factories import rental_service_factory
from services.interfaces.rental_service_interface import IRentalService
from api.schemas.rental_schemas import RentalCreate, RentalResponse
from common.exceptions import NotFoundException, CarStatusUnavailableException, RentalAlreadyEndedException, DatabaseException, InputValidationException

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(rental: RentalCreate, service: IRentalService = Depends(rental_service_factory)):
    try:
        return service.create_rental(car_id=rental.car_id, customer_name=rental.customer_name)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (CarStatusUnavailableException, RentalAlreadyEndedException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.patch("/{car_id}/end-rental", response_model=RentalResponse)
def end_rental_by_car_id(car_id: UUID, service: IRentalService = Depends(rental_service_factory)):
    try:
        return service.end_rental_by_car_id(car_id)
    except InputValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RentalAlreadyEndedException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
