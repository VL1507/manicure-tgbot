import datetime
from typing import List

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Appointments(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime.date] = mapped_column(Date)
    time_start: Mapped[str] = mapped_column(String)
    time_end: Mapped[str] = mapped_column(String)

    service_to_appointments: Mapped[List["ServiceToAppointments"]] = relationship(
        "ServiceToAppointments", back_populates="appointment"
    )


class Services(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    duration_minutes: Mapped[int] = mapped_column(Integer)

    service_to_appointments: Mapped[List["ServiceToAppointments"]] = relationship(
        "ServiceToAppointments", back_populates="service"
    )


class ServiceToAppointments(Base):
    __tablename__ = "service_to_appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"))

    appointment: Mapped["Appointments"] = relationship(
        "Appointments", back_populates="service_to_appointments"
    )
    service: Mapped["Services"] = relationship(
        "Services", back_populates="service_to_appointments"
    )
