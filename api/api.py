from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db, engine, Base
from db.car_model import CarStatus
from services.car_service import CarService
from services.rental_service import RentalService
from typing import List, Optional
from uuid import UUID
from .car_schemas import CarCreate, CarResponse, CarUpdate
from .rental_schemas import RentalCreate, RentalResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/cars", response_model=List[CarResponse])
def get_cars(status: Optional[CarStatus] = None, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.get_all_cars(status)

@app.get("/rentals", response_model=List[RentalResponse])
def get_rentals(db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.get_all_rentals()

@app.post("/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.create_car(model=car.model, year=car.year, status=car.status)

@app.put("/cars/{car_id}", response_model=CarResponse)
def update_car(car_id: UUID, car_update: CarUpdate, db: Session = Depends(get_db)):
    service = CarService(db)

    updated_car = service.update_car( car_id=car_id, model=car_update.model, year=car_update.year, status=car_update.status)
    if not updated_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return updated_car

@app.post("/rentals", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.create_rental(car_id=rental.car_id, customer_name=rental.customer_name)

@app.post("/rentals/{rental_id}/end", response_model=RentalResponse)
def end_rental(rental_id: UUID, db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.end_rental(rental_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
