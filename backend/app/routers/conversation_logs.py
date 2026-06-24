from fastapi import APIRouter, Depends

from ..crud_factory import register_crud_routes
from ..models import ConversationLog
from ..schemas import ConversationLogCreate, ConversationLogUpdate, ConversationLogRead

from ..auth import get_current_user

router = APIRouter(prefix="/conversation-logs", tags=["conversation_logs"], dependencies=[Depends(get_current_user)])

register_crud_routes(router, ConversationLog, ConversationLogCreate, ConversationLogUpdate, ConversationLogRead, "conversation_log")
