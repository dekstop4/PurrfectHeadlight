import pytest
from httpx import AsyncClient
from datetime import date, timedelta
from app.main import app

pytestmark = pytest.mark.asyncio


class TestServiceRequests:
    async def test_create_request(self, async_client: AsyncClient):
        """Тест создания заявки"""
        request_data = {
            "client_name": "Иван Иванов",
            "phone": "+79161234567",
            "car_model": "Toyota Camry",
            "service_type": "Полировка фар",
            "appointment_date": str(date.today() + timedelta(days=1))
        }

        response = await async_client.post("/api/requests", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["client_name"] == request_data["client_name"]
        assert data["car_model"] == request_data["car_model"]
        assert data["status"] == "Новая"

    async def test_get_requests(self, async_client: AsyncClient):
        """Тест получения списка заявок"""
        response = await async_client.get("/api/requests")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_update_request(self, async_client: AsyncClient):
        """Тест обновления заявки"""
        # Сначала создаем заявку
        create_data = {
            "client_name": "Петр Петров",
            "phone": "+79161234568",
            "car_model": "Honda Accord",
            "service_type": "Замена стекол фар",
            "appointment_date": str(date.today() + timedelta(days=2))
        }

        create_response = await async_client.post("/api/requests", json=create_data)
        request_id = create_response.json()["id"]

        # Обновляем заявку
        update_data = {
            "appointment_date": str(date.today() + timedelta(days=3)),
            "status": "В работе"
        }

        response = await async_client.put(f"/api/requests/{request_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["appointment_date"] == update_data["appointment_date"]
        assert data["status"] == update_data["status"]

    async def test_web_interface(self, async_client: AsyncClient):
        """Тест веб-интерфейса"""
        response = await async_client.get("/requests")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Сервис автомобильных фар" in response.text


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client