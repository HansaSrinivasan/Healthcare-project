from datetime import date, time

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_add_doctor_and_list():
    # Add doctor
    resp = client.post(
        "/doctors/",
        json={"name": "Dr. Jane", "specialty": "Cardiology", "slots_per_day": 3},
    )
    assert resp.status_code == 201, resp.text
    doctor = resp.json()
    assert doctor["id"] > 0
    assert doctor["slots_per_day"] == 3

    # List doctors
    resp = client.get("/doctors/")
    assert resp.status_code == 200
    doctors = resp.json()
    assert any(d["name"] == "Dr. Jane" for d in doctors)


def test_booking_and_prevent_overbooking():
    # Add doctor with 1 slot per day
    resp = client.post(
        "/doctors/",
        json={"name": "Dr. John", "specialty": "Dermatology", "slots_per_day": 1},
    )
    assert resp.status_code == 201
    doctor_id = resp.json()["id"]

    # Book first appointment
    day = date.today().isoformat()
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Alice",
            "date": day,
            "time_slot": time(9, 0).isoformat(),
        },
    )
    assert resp.status_code == 201, resp.text

    # Try to overbook same day
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Bob",
            "date": day,
            "time_slot": time(10, 0).isoformat(),
        },
    )
    assert resp.status_code == 400


def test_invalid_time_slot():
    # Add doctor
    resp = client.post(
        "/doctors/",
        json={"name": "Dr. Eve", "specialty": "Neurology", "slots_per_day": 2},
    )
    assert resp.status_code == 201
    doctor_id = resp.json()["id"]

    # Book outside working hours
    day = date.today().isoformat()
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Zed",
            "date": day,
            "time_slot": time(8, 30).isoformat(),
        },
    )
    assert resp.status_code == 422  # Pydantic validation error


def test_cancel_appointment_increases_capacity():
    resp = client.post(
        "/doctors/",
        json={"name": "Dr. Kim", "specialty": "Pediatrics", "slots_per_day": 1},
    )
    assert resp.status_code == 201
    doctor_id = resp.json()["id"]

    day = date.today().isoformat()
    # First booking
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Ann",
            "date": day,
            "time_slot": time(9, 0).isoformat(),
        },
    )
    assert resp.status_code == 201
    appt_id = resp.json()["id"]

    # Overbooking should fail
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Ben",
            "date": day,
            "time_slot": time(10, 0).isoformat(),
        },
    )
    assert resp.status_code == 400

    # Cancel first appointment
    resp = client.delete(f"/appointments/{appt_id}")
    assert resp.status_code == 200

    # Booking should now succeed
    resp = client.post(
        f"/appointments/doctors/{doctor_id}",
        json={
            "patient_name": "Ben",
            "date": day,
            "time_slot": time(10, 0).isoformat(),
        },
    )
    assert resp.status_code == 201


