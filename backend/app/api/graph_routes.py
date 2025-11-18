"""
API路由 - 图谱查询接口
"""
from fastapi import APIRouter, HTTPException, Query, Body
from app.models.schemas import GraphData, IndustryChainQuery
from app.services.graph_service import graph_service
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/graph", tags=["Graph"])


@router.post("/build")
async def build_graph(text: str, use_llm: bool = False):
    """
    从文本构建产业链图谱(会重新进行文本分析)
    """
    try:
        result = graph_service.build_graph_from_text(text, use_llm)
        return result
    except Exception as e:
        logger.error(f"图谱构建失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_to_graph(
    entities: Dict = Body(...),
    relations: List[Dict] = Body(...)
):
    """
    保存已分析的实体和关系到图谱(不重新分析)
    """
    try:
        result = graph_service.save_analyzed_data(entities, relations)
        return result
    except Exception as e:
        logger.error(f"保存到图谱失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=GraphData)
async def query_industry_chain(query: IndustryChainQuery):
    """
    查询企业产业链关系
    """
    try:
        result = graph_service.query_industry_chain(
            query.company_name,
            query.depth
        )
        return result
    except Exception as e:
        logger.error(f"图谱查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{company_name}")
async def get_company_relations(
    company_name: str,
    depth: int = Query(default=2, ge=1, le=5)
):
    """
    获取企业的产业链关系
    """
    try:
        result = graph_service.query_industry_chain(company_name, depth)
        return result
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_graph_statistics():
    """
    获取图谱统计信息
    """
    try:
        stats = graph_service.get_graph_statistics()
        return stats
    except Exception as e:
        logger.error(f"统计查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_graph():
    """
    清空图谱数据(谨慎使用)
    """
    try:
        query = "MATCH (n) DETACH DELETE n"
        graph_service.neo4j.execute_write(query)
        return {"message": "图谱已清空"}
    except Exception as e:
        logger.error(f"清空失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
