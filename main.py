from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import doctors, appointments


def create_app() -> FastAPI:
    app = FastAPI(title="Healthcare Appointment Booking API", version="1.0.0")

    # CORS for local frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
    app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])

    @app.get("/")
    def root():
        return {
            "message": "Healthcare Appointment Booking API",
            "version": "1.0.0",
            "docs": "/docs",
            "endpoints": {
                "doctors": "/doctors/",
                "appointments": "/appointments/",
                "openapi": "/openapi.json"
            }
        }

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app


app = create_app()


