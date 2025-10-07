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
from ..infrastructure.akshare_tools import (
    QueryStockFinacialReport,
    QueryStockHistoricalData,
    QueryStockNews,
    QueryStockPeerComparison,
    QueryStockSpotData,
    QueryStockValue,
)
from ..infrastructure.easy_tools import write_file, read_file
from ..config import settings


class ReportService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self.session = session
        self.model = init_chat_model(
            model="deepseek-chat",
            model_provider="deepseek",
            api_key=settings.deepseek_api_key,
            streaming=True,
        )

    async def generate_report(self, user: User, report_code: str):
        """
        生成股票分析报告，支持流式响应

        Args:
            user: 用户对象
            report_code: 股票代码

        Returns:
            生成器，逐块返回报告内容
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """你是金融专家，会使用很多金融工具：
1.QueryStockFinacialReport：查询财报
2.QueryStockHistoricalData：查询历史行情数据
3.QueryStockNews：查询股票相关新闻
4.QueryStockPeerComparison：查询和同行业比较的数据
5.QueryStockSpotData：查询当前行情
6.QueryStockValue：查询个股估值情况
请根据用户的股票代码，使用合适的工具查询最近的季度或者报告期的相关数据，结合价值投资的理念分析这家公司的四要素:
### 盈利能力
1. 净利率是否稳定，避免忽高忽低。
2. 毛利率越高说明有溢价空间，例如茅台常年90%+的毛利。
3. 净利润能否持续稳定，3~5年10%以上就是不错的

### 竞争优势
1. 营收增长率，如果跑赢行业平均，则说明在抢占市场。
2. 研发投入，尤其是科技公司，投入高则说明在提高技术壁垒。
3. 客户集中度，如果前5大客户占收入80%则说明有依赖过高的风险。

### 财务健康度
避免踩雷
1. 资产负债率，一般制造业在60%以下，金融服务业稍高但也要看结构。
2. 现金流，一般要常年为正，且和净利润成正比，避免赚钱但是没钱的现象。

### 估值
入场时机
1. 市盈率 PE，和行业平均相比是否合理。
2. 市净率 PB，适合重资产行业，例如银行，低于1时结合资产结构进行判断。

最后评估该股票是否值得关注，主要亮点和风险是什么？
                 """,
                ),
                ("human", "{input}"),
                (
                    "placeholder",
                    "{agent_scratchpad}",
                ),  # 这部分agnet提示符写法是写死的不可以修改
            ]
        )

        tools = [
            QueryStockFinacialReport,
            QueryStockHistoricalData,
            QueryStockNews,
            QueryStockPeerComparison,
            QueryStockSpotData,
            QueryStockValue,
        ]

        agent = create_tool_calling_agent(llm=self.model, tools=tools, prompt=prompt)

        executer = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return executer.invoke(
            {"input": "请分析股票" + report_code + "的四要素，并总结是否值得关注。"}
        )
