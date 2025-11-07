from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, validator


class DoctorBase(BaseModel):
    name: str = Field(..., min_length=1)
    specialty: str = Field(..., min_length=1)
    slots_per_day: int = Field(..., gt=0)


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_name: str = Field(..., min_length=1)
    date: date
    time_slot: time

    @validator("time_slot")
    def validate_working_hours(cls, v: time) -> time:
        # Valid hours: 09:00 to 17:00 inclusive start, exclusive end
        if not (v.hour >= 9 and (v.hour < 17 or (v.hour == 17 and v.minute == 0 and v.second == 0))):
            raise ValueError("Appointment time must be between 09:00 and 17:00")
        return v


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    doctor_id: int
    status: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str


