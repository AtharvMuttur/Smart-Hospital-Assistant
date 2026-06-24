from fastapi import APIRouter

from ..crud_factory import register_crud_routes
from ..models import DoctorSchedule
from ..schemas import DoctorScheduleCreate, DoctorScheduleUpdate, DoctorScheduleRead

router = APIRouter(prefix="/doctor-schedules", tags=["doctor_schedules"])

register_crud_routes(router, DoctorSchedule, DoctorScheduleCreate, DoctorScheduleUpdate, DoctorScheduleRead, "doctor_schedule")
