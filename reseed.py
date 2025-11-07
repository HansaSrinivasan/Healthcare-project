import os
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal, init_db, engine
from backend.app import crud, schemas, models

def main() -> None:
    print("Reseeding: Clearing existing doctors...")
    init_db()
    db: Session = SessionLocal()
    try:
        # Delete all existing doctors (this will cascade to appointments)
        db.query(models.Doctor).delete()
        db.query(models.Appointment).delete()
        db.commit()
        print("Reseeding: Existing data cleared.")
        
        print("Reseeding: Creating Indian doctors...")
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Rajesh Kumar", specialty="Cardiology", slots_per_day=5))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Priya Sharma", specialty="Pediatrics", slots_per_day=4))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Amit Patel", specialty="Orthopedics", slots_per_day=6))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Anjali Desai", specialty="Dermatology", slots_per_day=4))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Vikram Singh", specialty="General Medicine", slots_per_day=5))
        crud.create_doctor(db, schemas.DoctorCreate(name="Dr. Meera Reddy", specialty="Gynecology", slots_per_day=4))
        print("Reseeding: Done! 6 Indian doctors created.")
    finally:
        db.close()


if __name__ == "__main__":
    main()


