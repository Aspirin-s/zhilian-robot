"""
API路由 - 文本分析接口
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import TextAnalysisRequest, TextAnalysisResponse
from app.nlp import ner_processor, re_processor, llm_processor
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/nlp", tags=["NLP"])


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    分析文本,提取实体和关系
    """
    try:
        result = {
            "entities": {},
            "relations": [],
            "summary": ""
        }
        
        if request.extract_entities:
            # 提取实体
            result["entities"] = ner_processor.extract_industry_entities(request.text)
        
        if request.extract_relations and request.extract_entities:
            # 提取关系
            entity_list = []
            for category, items in result["entities"].items():
                for item in items:
                    entity_list.append({"text": item, "label": category})
            
            relations = re_processor.extract_relations(request.text, entity_list)
            result["relations"] = relations
        
        # 生成摘要
        entity_count = sum(len(v) for v in result["entities"].values())
        relation_count = len(result["relations"])
        result["summary"] = f"识别到{entity_count}个实体,{relation_count}个关系"
        
        return result
    except Exception as e:
        logger.error(f"文本分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-llm", response_model=TextAnalysisResponse)
async def analyze_text_with_llm(request: TextAnalysisRequest):
    """
    使用大语言模型分析文本
    """
    try:
        result = llm_processor.analyze_industry_chain(request.text)
        return result
    except Exception as e:
        logger.error(f"LLM分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entities/categories")
async def get_entity_categories():
    """
    获取支持的实体类别
    """
    return {
        "categories": [
            {"key": "companies", "label": "企业"},
            {"key": "products", "label": "产品"},
            {"key": "technologies", "label": "技术"},
            {"key": "persons", "label": "人物"},
            {"key": "locations", "label": "地点"},
            {"key": "organizations", "label": "组织"}
        ]
    }


@router.get("/relations/types")
async def get_relation_types():
    """
    获取支持的关系类型
    """
    return {
        "types": [
            "供应商",
            "客户",
            "合作伙伴",
            "竞争对手",
            "投资方",
            "子公司",
            "母公司",
            "技术提供方",
            "产品使用方"
        ]
    }
