"""Seed script for Smart Hospital Assistant backend.

Run from the `backend` directory:

    python scripts/seed_db.py

This script clears existing rows and repopulates every table with randomized
sample data that respects foreign-key relationships.
"""

import os
import random
import string
import sys
from datetime import date, datetime, time, timedelta

from sqlalchemy.exc import SQLAlchemyError

# Ensure the project root (backend/) is on sys.path so `app` package imports work.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models
from app.auth import get_password_hash
from app.database import SessionLocal

RANDOM = random.SystemRandom()

FIRST_NAMES = [
    "Aarav", "Aisha", "Rohan", "Priya", "Kabir", "Neha", "Vikram", "Sara",
    "Arjun", "Meera", "Aditya", "Ananya", "Dev", "Isha", "Karan", "Nisha",
]
LAST_NAMES = [
    "Sharma", "Patel", "Gupta", "Singh", "Iyer", "Reddy", "Mehta", "Verma",
    "Nair", "Khan", "Bose", "Malhotra", "Kapoor", "Chopra", "Das", "Saxena",
]
SPECIALIZATIONS = [
    ("Cardiology", "Heart and vascular care"),
    ("Neurology", "Brain, spine, and nerve care"),
    ("Pediatrics", "Children's health and wellness"),
    ("Orthopedics", "Bones, joints, and muscles"),
    ("Dermatology", "Skin, hair, and nail care"),
    ("Gynecology", "Women's reproductive health"),
    ("ENT", "Ear, nose, and throat care"),
    ("General Medicine", "Primary care and diagnosis"),
]
QUALIFICATIONS = [
    "MBBS, MD",
    "MBBS, DNB",
    "MBBS, MS",
    "MBBS, DM",
    "MBBS, MCh",
]
FAQ_TEMPLATES = [
    ("How do I book an appointment?", "Use the appointment section or contact the front desk.", "Appointments"),
    ("What are the clinic timings?", "The hospital is open from 8 AM to 8 PM on working days.", "General"),
    ("How can I get my lab reports?", "Your lab reports are available in the reports section after processing.", "Reports"),
    ("Do you accept insurance?", "Yes, we accept several major insurance providers.", "Billing"),
    ("Can I consult a doctor online?", "Online consultation is available for selected specializations.", "Telemedicine"),
    ("Where is the emergency department?", "The emergency department is on the ground floor near the main entrance.", "Emergency"),
]
INTENTS = [
    "book_appointment",
    "check_doctor_availability",
    "request_report",
    "ask_billing",
    "general_query",
    "insurance_query",
    "medicine_info",
    "follow_up",
]
USER_MESSAGES = [
    "I want to book a doctor visit.",
    "Can I see my latest lab report?",
    "What is the consultation fee?",
    "Is my insurance accepted here?",
    "I need help with follow-up care.",
    "Which doctor handles this problem?",
    "Please reschedule my appointment.",
    "What are the hospital timings?",
]
BOT_RESPONSES = [
    "Sure, I can help you with that.",
    "Your request has been noted.",
    "Please check the corresponding section in the app.",
    "I can connect you with the front desk.",
    "Let me guide you to the right department.",
    "The information is available in your account.",
]
INSURANCE_PROVIDERS = [
    "Star Health",
    "HDFC Ergo",
    "ICICI Lombard",
    "Bajaj Allianz",
    "Care Health",
    "Niva Bupa",
]
REPORT_NAMES = [
    "Blood Test Report",
    "X-Ray Summary",
    "MRI Scan Report",
    "ECG Report",
    "Liver Function Report",
    "Kidney Function Report",
]
PRESCRIPTION_TEXTS = [
    "Take the prescribed medicine twice daily after meals.",
    "Use the medication for 5 days and return for review.",
    "Follow a low-salt diet and take the tablets regularly.",
    "Rest well and complete the antibiotic course.",
    "Take one tablet in the morning and one at night.",
]


def random_choice(items):
    return RANDOM.choice(items)


def random_name():
    return f"{random_choice(FIRST_NAMES)} {random_choice(LAST_NAMES)}"


def slug(value):
    return "".join(ch.lower() for ch in value if ch.isalnum())


def random_phone():
    return "+91" + "".join(RANDOM.choice(string.digits) for _ in range(10))


def random_email(name, domain="example.com"):
    base = slug(name)
    suffix = "".join(RANDOM.choice(string.digits) for _ in range(3))
    return f"{base}{suffix}@{domain}"


def random_future_date(days=30):
    return date.today() + timedelta(days=RANDOM.randint(1, days))


def random_date_span(days_back=7, days_forward=60):
    return date.today() + timedelta(days=RANDOM.randint(-days_back, days_forward))


def random_past_or_future_date(days=30):
    return date.today() + timedelta(days=RANDOM.randint(-days, days))


def random_time_slot(start_hour=8, end_hour=18):
    hour = RANDOM.randint(start_hour, end_hour - 1)
    minute = RANDOM.choice([0, 15, 30, 45])
    return time(hour=hour, minute=minute)


def random_confidence():
    return f"{RANDOM.uniform(0.72, 0.99):.2f}"


def reset_tables(db):
    # Delete children first to satisfy foreign-key constraints.
    for model in [
        models.Feedback,
        models.Prescription,
        models.MedicalReport,
        models.Appointment,
        models.DoctorSchedule,
        models.ConversationLog,
        models.FAQ,
        models.InsuranceProvider,
        models.Doctor,
        models.Specialization,
        models.User,
    ]:
        db.query(model).delete(synchronize_session=False)
    db.commit()


def seed_users(db, count=10):
    users = []
    for _ in range(count):
        name = random_name()
        user = models.User(
            name=name,
            email=random_email(name),
            phone=random_phone(),
            password=get_password_hash("Password123!"),
        )
        db.add(user)
        users.append(user)
    db.flush()
    return users


def seed_specializations(db):
    specializations = []
    for name, description in SPECIALIZATIONS:
        spec = models.Specialization(
            name=name,
            description=description,
            icon_url=f"https://example.com/icons/{slug(name)}.png",
        )
        db.add(spec)
        specializations.append(spec)
    db.flush()
    return specializations


def seed_doctors(db, specializations, doctors_per_specialization=2):
    doctors = []
    for spec in specializations:
        for _ in range(doctors_per_specialization):
            name = random_name()
            doctor = models.Doctor(
                name=name,
                specialization_id=spec.id,
                qualification=random_choice(QUALIFICATIONS),
                experience_years=RANDOM.randint(2, 25),
                consultation_fee=RANDOM.randint(300, 2000),
                email=random_email(name, domain="hospital.com"),
                phone=random_phone(),
            )
            db.add(doctor)
            doctors.append(doctor)
    db.flush()
    return doctors


def seed_schedules(db, doctors):
    schedules = []
    for doctor in doctors:
        for _ in range(3):
            schedule_date = random_date_span(days_back=0, days_forward=45)
            start_hour = RANDOM.randint(8, 15)
            start = time(hour=start_hour, minute=0)
            end = time(hour=min(start_hour + RANDOM.randint(2, 4), 20), minute=0)
            schedule = models.DoctorSchedule(
                doctor_id=doctor.id,
                schedule_date=schedule_date,
                start_time=start,
                end_time=end,
                slot_duration_minutes=RANDOM.choice([15, 20, 30]),
                max_patients_per_slot=RANDOM.choice([1, 2, 3]),
                is_active=True,
            )
            db.add(schedule)
            schedules.append(schedule)
    db.flush()
    return schedules


def seed_faqs(db, count=10):
    faqs = []
    for idx in range(count):
        question, answer, category = random_choice(FAQ_TEMPLATES)
        faq = models.FAQ(
            question=f"{question} ({idx + 1})",
            answer=answer,
            category=category,
            display_order=idx + 1,
        )
        db.add(faq)
        faqs.append(faq)
    db.flush()
    return faqs


def seed_insurance_providers(db):
    providers = []
    for name in INSURANCE_PROVIDERS:
        provider = models.InsuranceProvider(
            name=name,
            contact_info=f"support@{slug(name)}.com | +91{''.join(RANDOM.choice(string.digits) for _ in range(10))}",
            accepted=RANDOM.choice([True, True, True, False]),
        )
        db.add(provider)
        providers.append(provider)
    db.flush()
    return providers


def seed_appointments(db, users, doctors, count=20):
    appointments = []
    statuses = ["Booked", "Confirmed", "Completed", "Cancelled"]
    for _ in range(count):
        appointment = models.Appointment(
            user_id=random_choice(users).id,
            doctor_id=random_choice(doctors).id,
            appointment_date=random_future_date(60),
            appointment_time=random_time_slot(9, 18),
            status=random_choice(statuses),
            notes=random_choice([
                "Patient requested a morning slot.",
                "Follow-up consultation.",
                "Initial assessment.",
                "Needs review of test results.",
                None,
            ]),
        )
        db.add(appointment)
        appointments.append(appointment)
    db.flush()
    return appointments


def seed_medical_reports(db, users, count=12):
    reports = []
    for idx in range(count):
        user = random_choice(users)
        report_name = random_choice(REPORT_NAMES)
        report = models.MedicalReport(
            user_id=user.id,
            report_name=f"{report_name} #{idx + 1}",
            report_url=f"https://example.com/reports/{user.id}/{idx + 1}.pdf",
            report_date=random_past_or_future_date(45),
        )
        db.add(report)
        reports.append(report)
    db.flush()
    return reports


def seed_prescriptions(db, users, doctors, count=15):
    prescriptions = []
    for idx in range(count):
        prescription = models.Prescription(
            user_id=random_choice(users).id,
            doctor_id=random_choice(doctors).id,
            prescription_text=f"{random_choice(PRESCRIPTION_TEXTS)} Reference ID {idx + 1000}.",
            prescribed_date=random_past_or_future_date(20),
        )
        db.add(prescription)
        prescriptions.append(prescription)
    db.flush()
    return prescriptions


def seed_feedback(db, users, doctors, count=15):
    feedback_entries = []
    for _ in range(count):
        feedback = models.Feedback(
            user_id=random_choice(users).id,
            doctor_id=random_choice(doctors).id,
            rating=RANDOM.randint(1, 5),
            comment=random_choice([
                "Great experience and helpful doctor.",
                "Waiting time was acceptable.",
                "Doctor explained everything clearly.",
                "The consultation was very satisfying.",
                None,
            ]),
            verified=RANDOM.choice([True, False, True]),
        )
        db.add(feedback)
        feedback_entries.append(feedback)
    db.flush()
    return feedback_entries


def seed_conversation_logs(db, users, count=20):
    logs = []
    for _ in range(count):
        linked_user = random_choice(users + [None])
        log = models.ConversationLog(
            user_id=linked_user.id if linked_user else None,
            user_message=random_choice(USER_MESSAGES),
            bot_response=random_choice(BOT_RESPONSES),
            intent=random_choice(INTENTS),
            confidence=random_confidence(),
            session_id="sess-" + "".join(RANDOM.choice(string.ascii_lowercase + string.digits) for _ in range(10)),
        )
        db.add(log)
        logs.append(log)
    db.flush()
    return logs


def seed():
    db = SessionLocal()
    try:
        reset_tables(db)

        users = seed_users(db, count=10)
        specializations = seed_specializations(db)
        doctors = seed_doctors(db, specializations, doctors_per_specialization=2)
        seed_schedules(db, doctors)
        seed_faqs(db, count=10)
        seed_insurance_providers(db)
        seed_appointments(db, users, doctors, count=20)
        seed_medical_reports(db, users, count=12)
        seed_prescriptions(db, users, doctors, count=15)
        seed_feedback(db, users, doctors, count=15)
        seed_conversation_logs(db, users, count=20)

        db.commit()
        print("Database seeding completed successfully with randomized values.")
    except SQLAlchemyError as e:
        db.rollback()
        print("Error while seeding database:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
