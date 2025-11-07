from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    slots_per_day = Column(Integer, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")


class AppointmentStatusEnum(str):
    ACTIVE = "active"
    CANCELED = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    patient_name = Column(String, nullable=False)
    date = Column(Date, nullable=False, index=True)
    time_slot = Column(Time, nullable=False)
    status = Column(String, nullable=False, default=AppointmentStatusEnum.ACTIVE)

    doctor = relationship("Doctor", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("doctor_id", "date", "time_slot", name="uq_doctor_date_time"),
    )


