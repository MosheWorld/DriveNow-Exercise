from database import SessionLocal, engine, Base
from models import Car, CarStatus

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
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
