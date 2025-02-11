from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from .models import ActivityORM, OrganizationORM
from .schemas import Activity, Organization
from .database import new_session


class OrganizationRepository:

    @classmethod
    async def find_all(cls) -> list[Organization]:
        async with new_session() as session:
            query = select(OrganizationORM).options(
                selectinload(OrganizationORM.phone_numbers),
                selectinload(OrganizationORM.building),
                selectinload(OrganizationORM.activities),
            )
            result = await session.execute(query)
            organizations_models = result.scalars().all()

            organizations_schemas = [
                Organization(
                    name=org.name,
                    building=org.building.adress,
                    phone_numbers=[phone.number for phone in org.phone_numbers],
                    activities=[activity.name for activity in org.activities],
                )
                for org in organizations_models
            ]
            return organizations_schemas

    @classmethod
    async def find_by_building_id(cls, building_id: int) -> list[Organization]:
        async with new_session() as session:
            query = (
                select(OrganizationORM)
                .options(
                    selectinload(OrganizationORM.phone_numbers),
                    selectinload(OrganizationORM.building),
                    selectinload(OrganizationORM.activities),
                )
                .where(OrganizationORM.building_id == building_id)
            )
            result = await session.execute(query)
            organizations_models = result.scalars().all()
            organizations_schemas = [
                Organization(
                    name=org.name,
                    building=(org.building.adress),
                    phone_numbers=[phone.number for phone in org.phone_numbers],
                    activities=[activity.name for activity in org.activities],
                )
                for org in organizations_models
            ]
            return organizations_schemas

    @classmethod
    async def find_by_id(cls, id: int) -> Organization:
        async with new_session() as session:
            query = select(OrganizationORM).where(OrganizationORM.id == id)
            result = await session.execute(query)
            organization_model = result.scalars().first()
            organization_schema = Organization(
                name=organization_model.name,
                building=organization_model.building.adress,
                phone_numbers=[
                    phone.number for phone in organization_model.phone_numbers
                ],
                activities=[
                    activity.name for activity in organization_model.activities
                ],
            )
            return organization_schema

    @classmethod
    async def find_by_name(cls, name: str) -> Organization:
        async with new_session() as session:
            query = (
                select(OrganizationORM)
                .options(
                    selectinload(OrganizationORM.phone_numbers),
                    selectinload(OrganizationORM.building),
                    selectinload(OrganizationORM.activities),
                )
                .where(
                    func.lower(OrganizationORM.name) == func.lower(name)
                )  # Нечувствительный к регистру поиск
            )
            result = await session.execute(query)
            organization_model = result.scalars().first()

            if not organization_model:
                raise HTTPException(status_code=404, detail="Organization not found")

            organization_schema = Organization(
                name=organization_model.name,
                building=organization_model.building.adress,
                phone_numbers=[
                    phone.number for phone in organization_model.phone_numbers
                ],
                activities=[
                    activity.name for activity in organization_model.activities
                ],
            )

            return organization_schema

    @classmethod
    async def find_nearby(
        cls, latitude: float, longitude: float, radius: float
    ) -> list[Organization]:
        async with new_session() as session:
            query = (
                select(OrganizationORM)
                .options(
                    selectinload(OrganizationORM.phone_numbers),
                    selectinload(OrganizationORM.building),
                    selectinload(OrganizationORM.activities),
                )
            )
            result = await session.execute(query)

            organizations_models = result.scalars().all()

            if not organizations_models:
                raise HTTPException(status_code=404, detail="Organization not found")

            organizations_schemas = [
                Organization(
                    name=org.name,
                    building=org.building.adress,
                    phone_numbers=[phone.number for phone in org.phone_numbers],
                    activities=[activity.name for activity in org.activities],
                )
                for org in organizations_models
                if (org.building.latitude - latitude) ** 2
                + (org.building.longitude - longitude) ** 2
                <= radius**2
            ]
            return organizations_schemas

    @classmethod
    async def find_by_activity(cls, activity_id: int) -> list[Organization]:
        async with new_session() as session:
            # Получаем все организации, связанные с указанной деятельностью
            query = (
                select(OrganizationORM)
                .options(selectinload(OrganizationORM.activities))
                .join(OrganizationORM.activities)
                .where(ActivityORM.id == activity_id)
            )
            result = await session.execute(query)
            organizations_models = result.scalars().all()
            return [
                Organization(
                    name=org.name,
                    building=org.building.adress,
                    phone_numbers=[phone.number for phone in org.phone_numbers],
                    activities=[activity.name for activity in org.activities],
                )
                for org in organizations_models
            ]


class ActivityRepository:

    @classmethod
    async def get_activity_tree(cls, activity_id: int) -> list[Activity]:
        async with new_session() as session:
            # Загружаем активность вместе с дочерними элементами рекурсивно
            query = (
                select(ActivityORM)
                .options(selectinload(ActivityORM.children))
                .where(ActivityORM.id == activity_id)
            )
            result = await session.execute(query)
            activity = result.scalars().first()
            
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            
            # Рекурсивно собираем все дочерние активности
            all_activities = [activity] + await cls._get_all_children(session, activity) 
            return [Activity.from_orm(a) for a in all_activities]

    @classmethod
    async def _get_all_children(cls, session: AsyncSession, activity: ActivityORM) -> list[ActivityORM]:
        children = activity.children.copy()
        for child in activity.children:
            # Явно загружаем дочерние элементы каждого ребенка
            await session.refresh(child, attribute_names=["children"])
            children += await cls._get_all_children(session, child)
        return children