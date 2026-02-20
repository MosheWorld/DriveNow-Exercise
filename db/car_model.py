from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from datetime import datetime, timezone
import uuid
from domain.entities.car import CarStatus

class Car(Base):
    __tablename__ = "cars"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(CarStatus), default=CarStatus.AVAILABLE, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    rentals = relationship("Rental", back_populates="car")
