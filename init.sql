-- Создание таблиц уже будет через SQLAlchemy
-- Но можно добавить начальные данные

INSERT INTO service_requests (client_name, phone, car_model, service_type, appointment_date, status)
VALUES
    ('Алексей Смирнов', '+79161234567', 'BMW X5', 'Полировка фар', CURRENT_DATE + 1, 'Новая'),
    ('Мария Петрова', '+79162345678', 'Mercedes C-Class', 'Замена стекол фар', CURRENT_DATE + 2, 'В работе'),
    ('Сергей Иванов', '+79163456789', 'Audi A6', 'Установка Bi-LED', CURRENT_DATE + 3, 'Завершена');