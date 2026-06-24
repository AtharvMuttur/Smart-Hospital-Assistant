from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel


class ORMBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UserRead(ORMBaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str


class SpecializationBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None


class SpecializationRead(ORMBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


class DoctorBase(BaseModel):
    name: str
    specialization_id: int
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization_id: Optional[int] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class DoctorRead(ORMBaseModel):
    id: int
    name: str
    specialization_id: int
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime


class DoctorScheduleBase(BaseModel):
    doctor_id: int
    schedule_date: date
    start_time: time
    end_time: time
    slot_duration_minutes: int = 30
    max_patients_per_slot: int = 1
    is_active: bool = True


class DoctorScheduleCreate(DoctorScheduleBase):
    pass


class DoctorScheduleUpdate(BaseModel):
    doctor_id: Optional[int] = None
    schedule_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    slot_duration_minutes: Optional[int] = None
    max_patients_per_slot: Optional[int] = None
    is_active: Optional[bool] = None


class DoctorScheduleRead(ORMBaseModel):
    id: int
    doctor_id: int
    schedule_date: date
    start_time: time
    end_time: time
    slot_duration_minutes: int
    max_patients_per_slot: int
    is_active: bool


class AppointmentBase(BaseModel):
    user_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str = "Booked"
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    user_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentRead(ORMBaseModel):
    id: int
    user_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FAQBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    display_order: Optional[int] = None


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    display_order: Optional[int] = None


class FAQRead(ORMBaseModel):
    id: int
    question: str
    answer: str
    category: Optional[str] = None
    display_order: Optional[int] = None
    created_at: datetime


class ConversationLogBase(BaseModel):
    user_id: Optional[int] = None
    user_message: str
    bot_response: str
    intent: Optional[str] = None
    confidence: Optional[str] = None
    session_id: Optional[str] = None


class ConversationLogCreate(ConversationLogBase):
    pass


class ConversationLogUpdate(BaseModel):
    user_id: Optional[int] = None
    user_message: Optional[str] = None
    bot_response: Optional[str] = None
    intent: Optional[str] = None
    confidence: Optional[str] = None
    session_id: Optional[str] = None


class ConversationLogRead(ORMBaseModel):
    id: int
    user_id: Optional[int] = None
    user_message: str
    bot_response: str
    intent: Optional[str] = None
    confidence: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime


class InsuranceProviderBase(BaseModel):
    name: str
    contact_info: Optional[str] = None
    accepted: bool = True


class InsuranceProviderCreate(InsuranceProviderBase):
    pass


class InsuranceProviderUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    accepted: Optional[bool] = None


class InsuranceProviderRead(ORMBaseModel):
    id: int
    name: str
    contact_info: Optional[str] = None
    accepted: bool


class MedicalReportBase(BaseModel):
    user_id: int
    report_name: str
    report_url: str
    report_date: Optional[date] = None


class MedicalReportCreate(MedicalReportBase):
    pass


class MedicalReportUpdate(BaseModel):
    user_id: Optional[int] = None
    report_name: Optional[str] = None
    report_url: Optional[str] = None
    report_date: Optional[date] = None


class MedicalReportRead(ORMBaseModel):
    id: int
    user_id: int
    report_name: str
    report_url: str
    report_date: Optional[date] = None
    created_at: datetime


class PrescriptionBase(BaseModel):
    user_id: int
    doctor_id: int
    prescription_text: str
    prescribed_date: Optional[date] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(BaseModel):
    user_id: Optional[int] = None
    doctor_id: Optional[int] = None
    prescription_text: Optional[str] = None
    prescribed_date: Optional[date] = None


class PrescriptionRead(ORMBaseModel):
    id: int
    user_id: int
    doctor_id: int
    prescription_text: str
    prescribed_date: Optional[date] = None
    created_at: datetime


class FeedbackBase(BaseModel):
    user_id: int
    doctor_id: int
    rating: int
    comment: Optional[str] = None
    verified: bool = False


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    user_id: Optional[int] = None
    doctor_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    verified: Optional[bool] = None


class FeedbackRead(ORMBaseModel):
    id: int
    user_id: int
    doctor_id: int
    rating: int
    comment: Optional[str] = None
    verified: bool
    created_at: datetime
