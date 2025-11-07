# Run the API first, then generate the SDK via scripts/generate_sdk.*

from healthcare_sdk import ApiClient
from healthcare_sdk.api.doctors_api import DoctorsApi
from healthcare_sdk.api.appointments_api import AppointmentsApi
from healthcare_sdk.model.doctor_create import DoctorCreate
from healthcare_sdk.model.appointment_create import AppointmentCreate
from datetime import date, time


def main() -> None:
    client = ApiClient()
    doctors_api = DoctorsApi(client)
    appts_api = AppointmentsApi(client)

    # List doctors
    doctors = doctors_api.get_doctors()
    print(doctors)

    # Add a doctor
    new_doc = doctors_api.add_doctor(DoctorCreate(name="Dr. SDK", specialty="API", slots_per_day=2))
    print("Created:", new_doc)

    # Book appointment
    booked = appts_api.book_appointment(
        new_doc.id,
        AppointmentCreate(patient_name="SDK User", date=date.today(), time_slot=time(9, 0)),
    )
    print("Booked:", booked)

    # Cancel appointment
    msg = appts_api.cancel_appointment(booked.id)
    print("Canceled:", msg)


if __name__ == "__main__":
    main()


