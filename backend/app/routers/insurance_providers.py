from fastapi import APIRouter

from ..crud_factory import register_crud_routes
from ..models import InsuranceProvider
from ..schemas import InsuranceProviderCreate, InsuranceProviderUpdate, InsuranceProviderRead

router = APIRouter(prefix="/insurance-providers", tags=["insurance_providers"])

register_crud_routes(router, InsuranceProvider, InsuranceProviderCreate, InsuranceProviderUpdate, InsuranceProviderRead, "insurance_provider")
