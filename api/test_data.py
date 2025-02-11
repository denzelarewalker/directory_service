import random
from sqlalchemy.ext.asyncio import AsyncSession
from .models import BuildingORM, OrganizationORM, ActivityORM, PhoneNumberORM


async def load(db: AsyncSession):
    async with db.begin():  # Начинаем транзакцию

        food = ActivityORM(name="Еда")
        sushi = ActivityORM(name="Суши", parent=food)
        meat = ActivityORM(name="Мясная продукция", parent=food)
        dairy = ActivityORM(name="Молочная продукция", parent=food)
        cars = ActivityORM(name="Автомобили")
        trucks = ActivityORM(name="Грузовые", parent=cars)
        cars_light = ActivityORM(name="Легковые", parent=cars)
        parts = ActivityORM(name="Запчасти", parent=cars_light)
        accessories = ActivityORM(name="Аксессуары", parent=cars_light)
        db.add_all([food, meat, dairy, cars, trucks, cars_light, parts, accessories])

        buildings = [
            # Санкт-Петербург
            BuildingORM(
                adress="г. Санкт-Петербург, ул. Малая Конюшенная 1",
                latitude=59.9340,
                longitude=30.3294,
            ),
            BuildingORM(
                adress="г. Санкт-Петербург, ул. Думская 1",
                latitude=59.9355,
                longitude=30.3199,
            ),
            BuildingORM(
                adress="г. Санкт-Петербург, Невский пр., 28",
                latitude=59.9343,
                longitude=30.3351,
            ),
            # Москва
            BuildingORM(
                adress="г. Москва, ул. Мясницкая 28",
                latitude=55.7635,
                longitude=37.6156,
            ),
            # Нью-Йорк
            BuildingORM(
                adress="г. Нью-Йорк, ул. Broadway 100",
                latitude=40.7590,
                longitude=-73.9845,
            ),
        ]

        db.add_all(buildings)

        await db.flush()  # Сохраняем здания, чтобы получить их id

        organizations = [
            OrganizationORM(name="Ресторан 'Вкусно и Точка'", building=buildings[0], activities=[food]),
            OrganizationORM(name="Пекарня 'Хлеб и Соль'", building=buildings[0], activities=[food]),
            OrganizationORM(name="Суши-бар 'Суши Мания'", building=buildings[0], activities=[sushi]),
            OrganizationORM(name="Сервис 'АвтоМастер'", building=buildings[1], activities=[trucks, parts]),
            OrganizationORM(name="Бистро 'Скороход'", building=buildings[1], activities=[meat, dairy]),
            OrganizationORM(name="Фастфуд 'Горячие Бургеры'", building=buildings[2], activities=[meat]),
            OrganizationORM(name="Салон 'Элегантные Авто'", building=buildings[3], activities=[cars_light]),
            OrganizationORM(name="Автосервис 'ТехноАвто'", building=buildings[3], activities=[parts]),
            OrganizationORM(name="Кафе 'Уютный Уголок'", building=buildings[4], activities=[food]),
        ]

        db.add_all(organizations)

        await db.flush()  # Сохраняем организацию, чтобы получить её id

        phone_numbers = []

        for org in organizations:
            num_phone_numbers = random.randint(0, 2)  # Случайное количество номеров от 0 до 2
            for _ in range(num_phone_numbers):
                # Генерация случайного номера телефона (пример)
                phone_number = f"{random.randint(1, 9)}-{random.randint(100, 999)}-{random.randint(100, 999)}"
                phone_numbers.append(PhoneNumberORM(number=phone_number, organization_id=org.id))

        db.add_all(phone_numbers)

        await db.commit()
