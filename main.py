from database import SessionLocal, engine, Base
from models import Car, CarStatus, Rental
from datetime import datetime, timezone

def init_db():
    Base.metadata.create_all(bind=engine)

def main():
    init_db()
    db = SessionLocal()
    
    try:
        new_car = Car(model="Kia", year=2021, status=CarStatus.AVAILABLE)
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        print(f"Car created successfully: {new_car.model} (ID: {new_car.id})")

        new_rental = Rental(car_id=new_car.id, customer_name="Moshe Binieli")
        new_car.status = CarStatus.IN_USE
        db.add(new_rental)
        db.commit()
        db.refresh(new_rental)
        
        print(f"Rental created for customer: {new_rental.customer_name} (Rental ID: {new_rental.id})")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
