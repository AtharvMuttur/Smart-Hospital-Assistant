from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import (
    Appointment,
    ConversationLog,
    Doctor,
    DoctorSchedule,
    FAQ,
    Feedback,
    InsuranceProvider,
    MedicalReport,
    Prescription,
    Specialization,
    User,
)
from .schemas import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
    ConversationLogCreate,
    ConversationLogRead,
    ConversationLogUpdate,
    DoctorCreate,
    DoctorRead,
    DoctorScheduleCreate,
    DoctorScheduleRead,
    DoctorScheduleUpdate,
    DoctorUpdate,
    FAQCreate,
    FAQRead,
    FAQUpdate,
    FeedbackCreate,
    FeedbackRead,
    FeedbackUpdate,
    InsuranceProviderCreate,
    InsuranceProviderRead,
    InsuranceProviderUpdate,
    MedicalReportCreate,
    MedicalReportRead,
    MedicalReportUpdate,
    PrescriptionCreate,
    PrescriptionRead,
    PrescriptionUpdate,
    SpecializationCreate,
    SpecializationRead,
    SpecializationUpdate,
    UserCreate,
    UserLogin,
    UserRead,
    UserUpdate,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

# include routers
from .routers import (
    users,
    specializations,
    doctors,
    doctor_schedules,
    appointments,
    faqs,
    conversation_logs,
    insurance_providers,
    medical_reports,
    prescriptions,
    feedback,
)

app.include_router(users.router)
app.include_router(specializations.router)
app.include_router(doctors.router)
app.include_router(doctor_schedules.router)
app.include_router(appointments.router)
app.include_router(faqs.router)
app.include_router(conversation_logs.router)
app.include_router(insurance_providers.router)
app.include_router(medical_reports.router)
app.include_router(prescriptions.router)
app.include_router(feedback.router)
