from fastapi import APIRouter

from ..crud_factory import register_crud_routes
from ..models import FAQ
from ..schemas import FAQCreate, FAQUpdate, FAQRead

router = APIRouter(prefix="/faqs", tags=["faqs"])

register_crud_routes(router, FAQ, FAQCreate, FAQUpdate, FAQRead, "faq")
