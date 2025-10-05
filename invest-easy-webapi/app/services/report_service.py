from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Dict, Any, Optional
from fastapi import Depends, HTTPException
from sqlalchemy import select
import uuid
from datetime import datetime

from ..domain.users import User
from ..infrastructure.db import get_async_session


class ReportService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session

    async def get_report_by_code(self, code: str) -> Optional[str]:
        return ''

    async def generate_report(self, user: User, report_code: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError
