import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Dict, Any, Optional
from fastapi import Depends, HTTPException
from sqlalchemy import select
import uuid, os
from datetime import datetime
from ..domain.users import User
from ..infrastructure.db import get_async_session
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from ..infrastructure.akshare_tools import QueryStockValue,QueryUSStockFinacialReport
from ..config import settings

class ReportService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session
        self.model = init_chat_model(
            model="deepseek-chat",
            model_provider="deepseek",
            api_key=settings.deepseek_api_key,
        )

    async def get_report_by_code(self, code: str) -> Optional[str]:
        return ""

    async def generate_report(self, user: User, report_code: str) -> Dict[str, Any]:
        # 1. Call akshare to get news
        # 2. Call akshare to get zygc
        # 3. Call akshare to get growth comparision
        # 4. history price
        # 5. balance
        # 6. profit
        # 7. 根据6块内容，按照价值投资的方法，分析四要素：盈利能力、竞争优势、财务健康、进场时机。
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "你是金融专家，请根据用户的股票代码，查询美股财务报表数据"),
                ("human", "{input}"),
                (
                    "placeholder",
                    "{agent_scratchpad}",
                ),  # 这部分agnet提示符写法是写死的不可以修改
            ]
        )

        tools = [QueryStockValue, QueryUSStockFinacialReport]

        agent = create_tool_calling_agent(
            llm=self.model, tools=tools, prompt=prompt
        )

        executer = AgentExecutor(agent=agent,tools=tools,verbose=True)

        response = executer.invoke({"input": "请查询" + report_code + "的年度现金流量表"})
        logging.info(response)
        return {"status":"ok"}
