from datetime import date as date_type
from datetime import time as time_type
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from . import models, schemas


def create_doctor(db: Session, doctor_in: schemas.DoctorCreate) -> models.Doctor:
    doctor = models.Doctor(
        name=doctor_in.name,
        specialty=doctor_in.specialty,
        slots_per_day=doctor_in.slots_per_day,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def list_doctors(db: Session) -> List[models.Doctor]:
    return db.query(models.Doctor).all()


def get_doctor(db: Session, doctor_id: int) -> Optional[models.Doctor]:
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def count_active_appointments_for_day(db: Session, doctor_id: int, day: date_type) -> int:
    return (
        db.query(func.count(models.Appointment.id))
        .filter(
            models.Appointment.doctor_id == doctor_id,
            models.Appointment.date == day,
            models.Appointment.status == models.AppointmentStatusEnum.ACTIVE,
        )
        .scalar()
        or 0
    )


def is_time_slot_taken(db: Session, doctor_id: int, day: date_type, slot: time_type) -> bool:
    exists = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor_id,
            models.Appointment.date == day,
            models.Appointment.time_slot == slot,
            models.Appointment.status == models.AppointmentStatusEnum.ACTIVE,
        )
        .first()
    )
    return exists is not None


def create_appointment(
    db: Session, doctor: models.Doctor, appointment_in: schemas.AppointmentCreate
) -> models.Appointment:
    appointment = models.Appointment(
        doctor_id=doctor.id,
        patient_name=appointment_in.patient_name,
        date=appointment_in.date,
        time_slot=appointment_in.time_slot,
        status=models.AppointmentStatusEnum.ACTIVE,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def cancel_appointment(db: Session, appointment: models.Appointment) -> models.Appointment:
    appointment.status = models.AppointmentStatusEnum.CANCELED
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


