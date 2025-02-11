from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


# Таблица для связи многие-ко-многим между Организациями и Деятельностями
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id")),
)


class BuildingORM(Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    adress: Mapped[str] = mapped_column(nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    organizations: Mapped[list["OrganizationORM"]] = relationship(
        "OrganizationORM", back_populates="building"
    )


class OrganizationORM(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    phone_numbers: Mapped[list["PhoneNumberORM"]] = relationship(
        "PhoneNumberORM", back_populates="organization", lazy="selectin"
    )
    building: Mapped["BuildingORM"] = relationship(
        "BuildingORM", back_populates="organizations", lazy="selectin"
    )
    activities: Mapped[list["ActivityORM"]] = relationship(
        "ActivityORM",
        secondary=organization_activity,
        back_populates="organizations",
        lazy="selectin",
    )


class PhoneNumberORM(Base):
    __tablename__ = "phone_numbers"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["OrganizationORM"] = relationship(
        "OrganizationORM", back_populates="phone_numbers"
    )


class ActivityORM(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"))
    parent = relationship("ActivityORM", remote_side=[id], back_populates="children")
    children = relationship("ActivityORM", back_populates="parent", lazy="selectin")
    organizations = relationship(
        "OrganizationORM", secondary=organization_activity, back_populates="activities"
    )

