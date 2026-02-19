from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db, engine, Base
from db.models import CarStatus
from repositories.car_repository import CarRepository
from repositories.rental_repository import RentalRepository
from typing import List
from .car_schemas import CarCreate, CarResponse
from .rental_schemas import RentalCreate, RentalResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/cars", response_model=List[CarResponse])
def get_cars(db: Session = Depends(get_db)):
    repo = CarRepository(db)
    return repo.get_all()

@app.get("/rentals", response_model=List[RentalResponse])
def get_rentals(db: Session = Depends(get_db)):
    repo = RentalRepository(db)
    return repo.get_all()

@app.post("/cars", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    repo = CarRepository(db)
    return repo.create(model=car.model, year=car.year, status=car.status)

@app.post("/rentals", response_model=RentalResponse)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    car_repo = CarRepository(db)
    car = car_repo.get_by_id(rental.car_id)
    
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    
    if car.status != CarStatus.AVAILABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car is not available for rent")

    rental_repo = RentalRepository(db)
    new_rental = rental_repo.create(car_id=rental.car_id, customer_name=rental.customer_name)
    car.status = CarStatus.IN_USE
    db.commit()
    
    return new_rental

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
