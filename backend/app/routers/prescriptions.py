from fastapi import APIRouter, Depends

from ..crud_factory import register_crud_routes
from ..models import Prescription
from ..schemas import PrescriptionCreate, PrescriptionUpdate, PrescriptionRead

from ..auth import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"], dependencies=[Depends(get_current_user)])

register_crud_routes(router, Prescription, PrescriptionCreate, PrescriptionUpdate, PrescriptionRead, "prescription")
