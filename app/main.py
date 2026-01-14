from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from datetime import date
import asyncio

from app.database import get_db, engine, Base
from app.models import ServiceRequest

app = FastAPI(title="Сервис автомобильных фар")
templates = Jinja2Templates(directory="templates")

# Список доступных услуг
SERVICE_TYPES = [
    "Полировка фар",
    "Замена стекол фар",
    "Установка Bi-LED",
    "Коррекция фар по ГОСТу",
    "Поклейка бронеплёнки",
    "Рестайлинг фар",
    "Чистка и герметизация",
    "Диагностика фар"
]


# Создаем таблицы при старте приложения
@app.on_event("startup")
async def startup_event():
    print("🚀 Запуск сервиса автомобильных фар...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы базы данных созданы")


# Главная страница - список всех заявок
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # Получаем все заявки из БД
        result = await db.execute(
            select(ServiceRequest).order_by(ServiceRequest.appointment_date)
        )
        requests = result.scalars().all()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "requests": requests,
            "service_types": SERVICE_TYPES,
            "today": date.today().isoformat()
        })
    except Exception as e:
        print(f"Ошибка: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "requests": [],
            "service_types": SERVICE_TYPES,
            "today": date.today().isoformat()
        })


# Добавление новой заявки
@app.post("/add")
async def add_request(
        client_name: str = Form(...),
        phone: str = Form(...),
        car_model: str = Form(...),
        service_type: str = Form(...),
        appointment_date: date = Form(...),
        db: AsyncSession = Depends(get_db)
):
    # Создаем новую заявку
    new_request = ServiceRequest(
        client_name=client_name,
        phone=phone,
        car_model=car_model,
        service_type=service_type,
        appointment_date=appointment_date,
        status="Новая"
    )

    db.add(new_request)
    await db.commit()

    return RedirectResponse("/", status_code=303)


# Удаление заявки
@app.post("/delete/{request_id}")
async def delete_request(
        request_id: int,
        db: AsyncSession = Depends(get_db)
):
    await db.execute(
        delete(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    await db.commit()

    return RedirectResponse("/", status_code=303)


# Перенос заявки на другую дату
@app.post("/reschedule/{request_id}")
async def reschedule_request(
        request_id: int,
        new_date: date = Form(...),
        db: AsyncSession = Depends(get_db)
):
    await db.execute(
        update(ServiceRequest)
        .where(ServiceRequest.id == request_id)
        .values(appointment_date=new_date)
    )
    await db.commit()

    return RedirectResponse("/", status_code=303)


# Проверка здоровья приложения
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Сервис работает"}


# Тестовая страница
@app.get("/test")
async def test_page():
    return HTMLResponse("""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1>✅ Тестовая страница работает!</h1>
            <p>FastAPI успешно запущен.</p>
            <p><a href="/">Перейти к основному приложению</a></p>
            <p><a href="/health">Проверить статус API</a></p>
        </body>
    </html>
    """)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)