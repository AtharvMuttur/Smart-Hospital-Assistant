from fastapi import APIRouter, Depends

from ..crud_factory import register_crud_routes
from ..models import MedicalReport
from ..schemas import MedicalReportCreate, MedicalReportUpdate, MedicalReportRead

from ..auth import get_current_user

router = APIRouter(prefix="/medical-reports", tags=["medical_reports"], dependencies=[Depends(get_current_user)])

register_crud_routes(router, MedicalReport, MedicalReportCreate, MedicalReportUpdate, MedicalReportRead, "medical_report")
