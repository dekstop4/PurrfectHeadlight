from sqlalchemy import Column, Integer, String, Date, DateTime, func
from app.database import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    car_model = Column(String(100), nullable=False)
    service_type = Column(String(100), nullable=False)
    appointment_date = Column(Date, nullable=False)
    status = Column(String(20), default="Новая")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())