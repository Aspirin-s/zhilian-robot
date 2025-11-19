"""
数据模型定义
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class EntityModel(BaseModel):
    """实体模型"""
    text: str = Field(..., description="实体文本")
    label: str = Field(..., description="实体类型")
    score: float = Field(default=0.0, description="置信度")


class RelationModel(BaseModel):
    """关系模型"""
    subject: str = Field(..., description="主体实体")
    relation: str = Field(..., description="关系类型")
    object: str = Field(..., description="客体实体")
    confidence: float = Field(default=0.0, description="置信度")


class TextAnalysisRequest(BaseModel):
    """文本分析请求"""
    text: str = Field(..., description="待分析文本")
    extract_entities: bool = Field(default=True, description="是否提取实体")
    extract_relations: bool = Field(default=True, description="是否提取关系")


class TextAnalysisResponse(BaseModel):
    """文本分析响应"""
    entities: Dict[str, List[str]] = Field(default_factory=dict)
    relations: List[RelationModel] = Field(default_factory=list)
    summary: str = Field(default="", description="分析摘要")


class GraphNode(BaseModel):
    """图谱节点"""
    id: str
    name: str
    type: str
    properties: Dict = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """图谱边"""
    source: str
    target: str
    relation: str
    properties: Dict = Field(default_factory=dict)


class GraphData(BaseModel):
    """图谱数据"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class CompanyInfo(BaseModel):
    """企业信息"""
    name: str
    industry: Optional[str] = None
    products: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class IndustryChainQuery(BaseModel):
    """产业链查询请求"""
    company_name: str = Field(..., description="企业名称")
    depth: int = Field(default=2, description="查询深度")
    relation_types: Optional[List[str]] = Field(default=None, description="关系类型过滤")
