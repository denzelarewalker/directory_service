# Directory of organizaions (FastAPI)

## Установка

1. Клонируйте репозиторий командой:

   ```
   git clone https://github.com/denzelarewalker/directory_service
   ```

2. Запустите `docker-compose` командой:
   ```
   docker-compose up -d
   ```

## Генерация миграции с помощью Alembic

Для создания новой миграции в проекте, использующем Alembic для управления схемой базы данных, выполните следующую команду:

```
docker-compose exec app poetry run alembic revision --autogenerate -m "initial migration"
```

## API документация

После запуска сервиса можно перейти к документации API по ссылке:
[API Documentation](http://127.0.0.1:8000/docs#/)


## Use Cases


|  Endpoint                                                                       | Test items                |
|--------------|--------------------------------------------------------------------------------|
| GET Organization By Id: <br> [http://127.0.0.1:8000/organizations/id/{id}](http://127.0.0.1:8000/organizations/id/1)   | id = 1  |
| GET Organization By Name: <br> [http://127.0.0.1:8000/organizations/name/{name}]('http://127.0.0.1:8000/organizations/name/%D0%A0%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%20%27%D0%92%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D0%A2%D0%BE%D1%87%D0%BA%D0%B0%27')   | name = Ресторан 'Вкусно и Точка'  |
| GET Organizations By Building: <br> [http://127.0.0.1:8000/organizations/building/{building_id}](http://127.0.0.1:8000/organizations/building/1)   | id = 1 |
| GET Organizations By Activity: <br> [http://127.0.0.1:8000/organizations/activity/{activity_id}](http://127.0.0.1:8000/organizations/activity/1)   |  id = 1 |
| GET Search Organizations By Activity: <br> [http://127.0.0.1:8000/organizations/search_by_activity/{activity_id}](http://127.0.0.1:8000/organizations/search_by_activity/1)  | id = 1  |
| GET Organizations Nearby: <br> [http://127.0.0.1:8000/organizations/nearby/](http://127.0.0.1:8000/organizations/nearby?lat=59.9340&lon=30.3294&radius=0.01)   | latitude = 59.9340 <br> longitude = 30.3294 <br> radius = 0.01 |
| GET All Organizations: <br> [http://127.0.0.1:8000/organizations](http://127.0.0.1:8000/organizations)   | ---- |
