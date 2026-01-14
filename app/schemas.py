from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional
from enum import Enum


class ServiceType(str, Enum):
    POLISHING = "Полировка фар"
    GLASS_REPLACEMENT = "Замена стекол фар"
    BI_LED_INSTALLATION = "Установка Bi-LED"
    HEADLIGHT_ADJUSTMENT = "Коррекция фар по ГОСТу"
    ARMOR_FILM = "Поклейка бронеплёнки"
    RESTYLING = "Рестайлинг фар"
    CLEANING_SEALING = "Чистка и герметизация"
    DIAGNOSTICS = "Диагностика"


class ServiceRequestBase(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    car_model: str = Field(..., min_length=1, max_length=100)
    service_type: ServiceType
    appointment_date: date


class ServiceRequestCreate(ServiceRequestBase):
    pass


class ServiceRequestUpdate(BaseModel):
    appointment_date: Optional[date] = None
    status: Optional[str] = None

    @validator('appointment_date')
    def validate_future_date(cls, v):
        if v and v < date.today():
            raise ValueError('Дата не может быть в прошлом')
        return v


class ServiceRequestResponse(ServiceRequestBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True