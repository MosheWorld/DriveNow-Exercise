import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from datetime import datetime, timezone
import uuid

class CarStatus(enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "under_maintenance"

class Car(Base):
    __tablename__ = "cars"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(CarStatus), default=CarStatus.AVAILABLE, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    rentals = relationship("Rental", back_populates="car")
