from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import time

from ..crud_factory import register_crud_routes
from ..models import Appointment, DoctorSchedule, Doctor
from ..schemas import AppointmentCreate, AppointmentUpdate, AppointmentRead
from ..auth import get_current_user
from ..models import User
from ..deps import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"], dependencies=[Depends(get_current_user)])


def is_valid_twenty_minute_slot(schedule_start: time, appointment_time: time) -> bool:
    start_minutes = schedule_start.hour * 60 + schedule_start.minute
    appointment_minutes = appointment_time.hour * 60 + appointment_time.minute
    if appointment_minutes < start_minutes:
        return False
    return (appointment_minutes - start_minutes) % 20 == 0


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment_with_availability_check(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create an appointment with availability validation.
    Checks if doctor is available at the requested time.
    """
    
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Check if doctor has a schedule for the requested date
    schedule = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == appointment.doctor_id,
        DoctorSchedule.schedule_date == appointment.appointment_date,
        DoctorSchedule.is_active == True
    ).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor is not available on {appointment.appointment_date}"
        )
    
    # Check if requested time falls within doctor's working hours
    if not (schedule.start_time <= appointment.appointment_time < schedule.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested time {appointment.appointment_time} is outside doctor's working hours ({schedule.start_time} - {schedule.end_time})"
        )

    # Enforce 20-minute booking intervals from the start of the doctor's schedule
    if not is_valid_twenty_minute_slot(schedule.start_time, appointment.appointment_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments can only be booked in 20-minute intervals from the schedule start time",
        )
    
    # Check if the time slot is already booked
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.appointment_time == appointment.appointment_time,
        Appointment.status != "Cancelled"
    ).first()
    
    if existing_appointment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time slot is already booked"
        )
    
    # Create the appointment
    db_appointment = Appointment(
        user_id=appointment.user_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        status=appointment.status,
        notes=appointment.notes
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    return db_appointment


# Register remaining CRUD routes (GET list, GET detail, PUT, DELETE)
# Override POST since we have a custom implementation above
from fastapi import Request

@router.get("/", response_model=list[AppointmentRead])
async def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """List all appointments"""
    return db.query(Appointment).offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get appointment by ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update appointment"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # If updating date/time/doctor, validate availability
    if (appointment_update.appointment_date and appointment_update.appointment_date != db_appointment.appointment_date) or \
       (appointment_update.appointment_time and appointment_update.appointment_time != db_appointment.appointment_time) or \
       (appointment_update.doctor_id and appointment_update.doctor_id != db_appointment.doctor_id):
        
        new_date = appointment_update.appointment_date or db_appointment.appointment_date
        new_time = appointment_update.appointment_time or db_appointment.appointment_time
        new_doctor_id = appointment_update.doctor_id or db_appointment.doctor_id
        
        # Verify doctor exists
        doctor = db.query(Doctor).filter(Doctor.id == new_doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        
        # Check schedule availability
        schedule = db.query(DoctorSchedule).filter(
            DoctorSchedule.doctor_id == new_doctor_id,
            DoctorSchedule.schedule_date == new_date,
            DoctorSchedule.is_active == True
        ).first()
        
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Doctor is not available on {new_date}"
            )
        
        # Check time is within working hours
        if not (schedule.start_time <= new_time < schedule.end_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Requested time is outside doctor's working hours"
            )

        # Enforce 20-minute booking intervals from the start of the doctor's schedule
        if not is_valid_twenty_minute_slot(schedule.start_time, new_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointments can only be booked in 20-minute intervals from the schedule start time",
            )
        
        # Check if time slot is available (exclude current appointment)
        existing_appointment = db.query(Appointment).filter(
            Appointment.id != appointment_id,
            Appointment.doctor_id == new_doctor_id,
            Appointment.appointment_date == new_date,
            Appointment.appointment_time == new_time,
            Appointment.status != "Cancelled"
        ).first()
        
        if existing_appointment:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This time slot is already booked"
            )
    
    # Update fields
    for field, value in appointment_update.dict(exclude_unset=True).items():
        setattr(db_appointment, field, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete appointment"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.delete(db_appointment)
    db.commit()
    return None
