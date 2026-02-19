from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db, engine, Base
from db.car_model import CarStatus
from services.car_service import CarService
from services.rental_service import RentalService
from typing import List
from .car_schemas import CarCreate, CarResponse
from .rental_schemas import RentalCreate, RentalResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/cars", response_model=List[CarResponse])
def get_cars(db: Session = Depends(get_db)):
    service = CarService(db)
    return service.get_all_cars()

@app.get("/rentals", response_model=List[RentalResponse])
def get_rentals(db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.get_all_rentals()

@app.post("/cars", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.create_car(model=car.model, year=car.year, status=car.status)

@app.post("/rentals", response_model=RentalResponse)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.create_rental(car_id=rental.car_id, customer_name=rental.customer_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
