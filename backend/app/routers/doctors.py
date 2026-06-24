from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Appointment, Doctor, DoctorSchedule
from ..crud_factory import register_crud_routes
from ..schemas import DoctorCreate, DoctorUpdate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["doctors"])

register_crud_routes(router, Doctor, DoctorCreate, DoctorUpdate, DoctorRead, "doctor")


@router.get("/{doctor_id}/available-slots")
def get_available_slots(
	doctor_id: int,
	schedule_date: date = Query(..., alias="date", description="Date in YYYY-MM-DD format"),
	db: Session = Depends(get_db),
):
	doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
	if not doctor:
		return {"doctor_id": doctor_id, "date": schedule_date.isoformat(), "available_slots": []}

	schedules = (
		db.query(DoctorSchedule)
		.filter(
			DoctorSchedule.doctor_id == doctor_id,
			DoctorSchedule.schedule_date == schedule_date,
			DoctorSchedule.is_active.is_(True),
		)
		.all()
	)

	if not schedules:
		return {"doctor_id": doctor_id, "date": schedule_date.isoformat(), "available_slots": []}

	booked_times = {
		appointment.appointment_time
		for appointment in db.query(Appointment.appointment_time)
		.filter(
			Appointment.doctor_id == doctor_id,
			Appointment.appointment_date == schedule_date,
			Appointment.status != "Cancelled",
		)
		.all()
	}

	available_slots = set()
	for schedule in schedules:
		schedule_start = datetime.combine(schedule_date, schedule.start_time)
		schedule_end = datetime.combine(schedule_date, schedule.end_time)
		slot_delta = timedelta(minutes=schedule.slot_duration_minutes)

		current_slot = schedule_start
		while current_slot + slot_delta <= schedule_end:
			slot_time = current_slot.time()
			if slot_time not in booked_times:
				available_slots.add(slot_time.strftime("%H:%M"))
			current_slot += slot_delta

	return {
		"doctor_id": doctor_id,
		"date": schedule_date.isoformat(),
		"available_slots": sorted(available_slots),
	}
