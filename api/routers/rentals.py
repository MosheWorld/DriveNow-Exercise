from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from api.factories import rental_service_factory
from services.interfaces.rental_service_interface import IRentalService
from api.schemas.rental_schemas import RentalCreate, RentalResponse

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(rental: RentalCreate, service: IRentalService = Depends(rental_service_factory)):
    return service.create_rental(car_id=rental.car_id, customer_name=rental.customer_name)

@router.patch("/{rental_id}/end-rental", response_model=RentalResponse)
def end_rental(rental_id: UUID, service: IRentalService = Depends(rental_service_factory)):
    return service.end_rental(rental_id)
