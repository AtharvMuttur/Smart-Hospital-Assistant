from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..crud_factory import register_crud_routes
from ..models import Specialization, Doctor
from ..schemas import SpecializationCreate, SpecializationUpdate, SpecializationRead
from ..schemas import DoctorRead

router = APIRouter(prefix="/specializations", tags=["specializations"])

register_crud_routes(router, Specialization, SpecializationCreate, SpecializationUpdate, SpecializationRead, "specialization")


@router.get("/{specialization_id}/doctors", response_model=list[DoctorRead])
def get_doctors_by_specialization(
	specialization_id: int,
	db: Session = Depends(get_db),
):
	specialization = db.query(Specialization).filter(Specialization.id == specialization_id).first()
	if not specialization:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specialization not found")

	return (
		db.query(Doctor)
		.filter(Doctor.specialization_id == specialization_id)
		.order_by(Doctor.name)
		.all()
	)
