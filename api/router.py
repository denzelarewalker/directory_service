from .repository import ActivityRepository, OrganizationRepository
from .schemas import Organization
from fastapi import APIRouter


router = APIRouter(
    prefix="/organizations",
    tags=["Организации"],
)


@router.get("")
async def get_all_organizations() -> list[Organization]:
    return await OrganizationRepository.find_all()


@router.get("/id/{id}")
async def get_organization_by_id(id: int) -> Organization:
    return await OrganizationRepository.find_by_id(id)


@router.get("/name/{name}")
async def get_organization_by_name(name: str) -> Organization:
    return await OrganizationRepository.find_by_name(name)


@router.get("/building/{building_id}")
async def get_organizations_by_building(building_id: int) -> list[Organization]:
    return await OrganizationRepository.find_by_building_id(building_id)


@router.get("/activity/{activity_id}")
async def get_organizations_by_activity(activity_id: int) -> list[Organization]:
    return await OrganizationRepository.find_by_activity(activity_id)


# Поиск организаций по виду деятельности (включая дочерние)
@router.get("/search_by_activity/{activity_id}")
async def search_organizations_by_activity(activity_id: int) -> list[Organization]:
    activities = await ActivityRepository.get_activity_tree(activity_id)
    organizations = []
    for activity in activities:
        orgs = await OrganizationRepository.find_by_activity(activity.id)
        organizations.extend(orgs)
    return organizations



@router.get("/nearby", response_model=list[Organization])
async def get_organizations_nearby(lat: float, lon: float, radius: float):
    return await OrganizationRepository.find_nearby(lat, lon, radius)

