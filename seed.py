import os
from datetime import date

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal, init_db
from backend.app import crud, schemas


def main() -> None:
    init_db()
    db: Session = SessionLocal()
    try:
        doctors = crud.list_doctors(db)
        if doctors:
            print("Seed: doctors already exist, skipping.")
            return
        print("Seed: creating Indian doctors...")
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Rajesh Kumar", specialty="Cardiology", slots_per_day=5))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Priya Sharma", specialty="Pediatrics", slots_per_day=4))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Amit Patel", specialty="Orthopedics", slots_per_day=6))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Anjali Desai", specialty="Dermatology", slots_per_day=4))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Vikram Singh", specialty="General Medicine", slots_per_day=5))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Meera Reddy", specialty="Gynecology", slots_per_day=4))
        print("Seed: done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()


