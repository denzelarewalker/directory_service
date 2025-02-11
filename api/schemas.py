from pydantic import BaseModel, ConfigDict


class Organization(BaseModel):
    name: str
    building: str
    phone_numbers: list[str]
    activities: list[str]
    model_config = ConfigDict(from_attributes=True)


class Activity(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)