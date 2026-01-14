from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from datetime import date
from models import ServiceRequest
from schemas import ServiceRequestCreate, ServiceRequestUpdate
import logging

logger = logging.getLogger(__name__)


class ServiceRequestCRUD:
    @staticmethod
    async def get_all_requests(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(ServiceRequest)
            .order_by(ServiceRequest.appointment_date.asc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_request_by_id(db: AsyncSession, request_id: int):
        result = await db.execute(
            select(ServiceRequest).where(ServiceRequest.id == request_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_request(db: AsyncSession, request: ServiceRequestCreate):
        db_request = ServiceRequest(
            client_name=request.client_name,
            phone=request.phone,
            car_model=request.car_model,
            service_type=request.service_type.value,
            appointment_date=request.appointment_date
        )
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)
        logger.info(f"Создана новая заявка ID: {db_request.id}")
        return db_request

    @staticmethod
    async def update_request(
            db: AsyncSession,
            request_id: int,
            request_update: ServiceRequestUpdate
    ):
        update_data = request_update.dict(exclude_unset=True)

        if update_data:
            stmt = (
                update(ServiceRequest)
                .where(ServiceRequest.id == request_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(stmt)
            await db.commit()

            updated_request = await ServiceRequestCRUD.get_request_by_id(db, request_id)
            logger.info(f"Обновлена заявка ID: {request_id}")
            return updated_request
        return None

    @staticmethod
    async def delete_request(db: AsyncSession, request_id: int):
        request = await ServiceRequestCRUD.get_request_by_id(db, request_id)
        if request:
            await db.delete(request)
            await db.commit()
            logger.info(f"Удалена заявка ID: {request_id}")
            return True
        return False

    @staticmethod
    async def get_requests_by_date(db: AsyncSession, target_date: date):
        result = await db.execute(
            select(ServiceRequest)
            .where(ServiceRequest.appointment_date == target_date)
            .order_by(ServiceRequest.created_at.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def reschedule_request(
            db: AsyncSession,
            request_id: int,
            new_date: date
    ):
        return await ServiceRequestCRUD.update_request(
            db,
            request_id,
            ServiceRequestUpdate(appointment_date=new_date)
        )