import asyncio
from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from ..infrastructure.users import current_active_user, User
from ..services.report_service import ReportService
from fastapi.responses import StreamingResponse
from langchain.chat_models import init_chat_model
from ..config import settings
from sse_starlette import EventSourceResponse

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    # dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


async def event_generator(sent: str):
    for char in sent:
        yield {"event": "message", "data": char}
        await asyncio.sleep(0.2)

@router.get("/chatbot/stream")
async def sse_endpoint(sent: str = "default"):
    return EventSourceResponse(event_generator(sent))

@router.get("/generate/{report_code}")
async def generate_report_endpoint(
    report_code: str,
    user: User = Depends(current_active_user),
    reportSvc: ReportService = Depends(ReportService),
):
    """
    Generate a report according to the specified report code and parameters.
    This endpoint supports streaming response for real-time report generation.
    
    Parameters:
    - report_code: The code identifying the report type to generate
    """
    # 返回流式响应，设置正确的媒体类型
    return EventSourceResponse(reportSvc.generate_report(user, report_code))
