from fastapi import FastAPI
from db.database import engine, Base
from api.routers import cars, rentals
from api.middleware.logging_middleware import log_requests

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DriveNow API")

app.middleware("http")(log_requests)

app.include_router(cars.router)
app.include_router(rentals.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
