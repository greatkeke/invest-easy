from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from ..infrastructure.users import current_active_user, User
from ..services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate/{report_code}")
async def generate_report_endpoint(
    report_code: str,
    user: User = Depends(current_active_user),
    reportSvc: ReportService = Depends(ReportService),
):
    """
    Generate a report according to the specified report code and parameters.
    
    Parameters:
    - report_code: The code identifying the report type to generate
    """
    result = await reportSvc.generate_report(user, report_code)
    return result

