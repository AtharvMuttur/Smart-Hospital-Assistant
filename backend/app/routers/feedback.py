from fastapi import APIRouter, Depends

from ..crud_factory import register_crud_routes
from ..models import Feedback
from ..schemas import FeedbackCreate, FeedbackUpdate, FeedbackRead

from ..auth import get_current_user

router = APIRouter(prefix="/feedback", tags=["feedback"], dependencies=[Depends(get_current_user)])

register_crud_routes(router, Feedback, FeedbackCreate, FeedbackUpdate, FeedbackRead, "feedback")
