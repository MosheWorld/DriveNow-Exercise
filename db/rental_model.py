from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from datetime import datetime, timezone
import uuid

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    car_id = Column(UUID(as_uuid=True), ForeignKey("cars.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    car = relationship("Car", back_populates="rentals")
